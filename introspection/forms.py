from django import forms
from django.utils.translation import ugettext_lazy as _

# iterable
GEEKS_CHOICES = (
    ("1", "FKSOLUTIONS")
)


class DatabaseChoice(forms.Form):
    database = forms.ChoiceField(label=_("Database"), choices=GEEKS_CHOICES)
