from django.contrib.auth.models import (Group, Permission,
                                        ContentType)
from performances.models import Institution, Performance


def heads_of_institutions_group() -> object:
    """
    Define Head of Institution group permissions
    """
    head_of_institution_group, created = Group.objects. \
        get_or_create(name='Head of Institution Permissions')
    institution_ct = ContentType.objects.get_for_model(Institution)
    institution_permissions = Permission.objects.filter(
        content_type=institution_ct)
    head_of_institution_group.permissions.set(
        [p.id for p in institution_permissions]
    )
    return head_of_institution_group


def teachers_group() -> object:
    """
    Define teacher group permissions
    """
    teacher_group, created = Group.objects.get_or_create(name='Teacher Permissions')
    performance_ct = ContentType.objects.get_for_model(Performance)
    performance_permissions = Permission.objects.filter(content_type=performance_ct)
    teacher_group.permissions.set(
        [p.id for p in performance_permissions]
    )
    return teacher_group




