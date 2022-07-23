
from django import template

from processerror.models import ProcessError

register = template.Library()


@register.simple_tag()
def error_count_simple_tag():
    return ProcessError.objects.count()
