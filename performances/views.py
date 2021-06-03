from pprint import pprint

import pdfkit
from django.utils import timezone
from weasyprint import HTML, CSS

from django_pdfkit import PDFView

import tempfile

from rest_framework import generics
from rest_framework.permissions import (
    SAFE_METHODS,
    DjangoModelPermissions,
    BasePermission,
    IsAuthenticated)

from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse, FileResponse
from django.template.loader import render_to_string, get_template

from .models import Institution
from .models import Event
from .models import Class
from .performance_scheduling import schedule_performances_for_each_theater, generate_time_table
from .serializers import InstitutionSerializer


class IsOwnerOrReadOnly(BasePermission):
    """Custom permission"""
    message = 'Updating of institution details and deregistration' \
              ' restricted to Head of Institution Only'

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.head_of_institution == request.user


class RegisterInstitutions(generics.RetrieveUpdateAPIView):
    """
    Update institution details once  heads of institutions are registered into the system
    """
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    lookup_field = 'id'
    lookup_url_kwarg = 'institution_pk'


def test_schedule_performances(request, event):
    list(messages.get_messages(request))  # Clear messages.

    try:
        performances_for_each_theater: dict = schedule_performances_for_each_theater(
            event=Event.objects.get(venue=event),
            all_classes=Class.objects.all())
        time_table = generate_time_table(performances_for_each_theater)

        ctx = {
            'time_table': time_table
        }

        return render(request, 'time_table.html', ctx)

    except ZeroDivisionError:
        messages.add_message(request, messages.ERROR, 'No theaters registered to the event!')
        return render(request, 'time_table.html')


WKHTMLTOPDF_PATH: str = '/usr/local/bin/wkhtmltopdf'


def schedule_performances(request, event):
    list(messages.get_messages(request))  # Clear messages.

    try:
        event = Event.objects.get(venue=event)
        performances_for_each_theater: dict = schedule_performances_for_each_theater(
            event=event,
            all_classes=Class.objects.all())
        time_table: dict = generate_time_table(performances_for_each_theater)

        event_level: str = event.event_level.lower()
        ctx = {
            'time_table': time_table,
            'event': event,
            'event_level': event_level
        }

        # Getting template, and rendering data
        template = get_template('time_table.html')
        html = template.render(ctx)

        # Function for creating file name
        # Inner function
        def create_file_name():
            file_name = 'time_table_%s.pdf' % event
            return file_name.strip()

        filename = create_file_name()

        config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_PATH)

        options = {
            'page-size': 'A4',
            'margin-top': '0.25in',
            'margin-right': '0.3in',
            'margin-bottom': '0.25in',
            'margin-left': '0.3in',
            'encoding': 'UTF-8',
            'custom-header': [
                ('Accept-Encoding', 'gzip')
            ],
            'no-outline': None,
            'enable-local-file-access': None,
            'enable-javascript': None,
        }

        with tempfile.NamedTemporaryFile(prefix=filename, suffix=".pdf") as f:
            pdfkit.from_string(html, f.name, configuration=config, options=options)
            return FileResponse(open(f.name, 'rb'), content_type='application/pdf')

    except ZeroDivisionError:
        messages.add_message(request, messages.ERROR, 'No theaters registered to the event!')
        return render(request, 'time_table.html')
