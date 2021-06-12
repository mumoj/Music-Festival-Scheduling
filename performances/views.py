import tempfile

import pdfkit

from django.contrib import messages

from django.http import FileResponse
from django.shortcuts import render
from django.template.loader import get_template

from rest_framework import generics
from rest_framework.permissions import (
    SAFE_METHODS,
    BasePermission,
    IsAuthenticated)

from .models import Event
from .models import Institution
from .performance_scheduling import get_event, schedule_performances_for_each_theater, generate_time_table
from .serializers import InstitutionSerializer

WKHTMLTOPDF_PATH: str = '/usr/local/bin/wkhtmltopdf'


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


def schedule_performances(request, festival_event):
    list(messages.get_messages(request))  # Clear messages.
    event = Event.objects.get(pk=festival_event)

    try:
        get_event(event=event)
        performances_for_each_theater: dict = schedule_performances_for_each_theater()
        time_table = generate_time_table(performances_for_each_theater)

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
