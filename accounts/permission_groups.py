from django.contrib.auth.models import (Group, Permission,
                                        ContentType)
from performances.models import Institution


def set_heads_of_institutions_group():
    """
    Define Head of Institution group permissions
    """
    heads_of_institutions_group, created = Group.objects. \
        get_or_create(name='Head of Institution Permissions')
    institution_ct = ContentType.objects.get_for_model(Institution)
    institution_permissions = Permission.objects.filter(
        content_type=institution_ct)
    heads_of_institutions_group.permissions.set(
        [p.id for p in institution_permissions]
    )
    return heads_of_institutions_group
