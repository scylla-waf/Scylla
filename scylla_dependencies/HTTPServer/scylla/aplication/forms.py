from django import forms
from django.contrib.auth.forms import UserCreationForm


class UserCreateForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

class ScyllaForm(forms.Form):
    proxyhost = forms.CharField(label='Proxy Host', max_length=100)
    proxyport = forms.CharField(label='Proxy Port', max_length=100)
    server_addr = forms.CharField(label='Server Address', max_length=100)
    server_port = forms.CharField(label='Server Port', max_length=100)
    djangoport = forms.CharField(label='Django Port', max_length=100)
    secret_key = forms.CharField(label='Django Secret Key', max_length=100)
    CHOICES = [("deffense","deffense"),("analysis","analysis")]
    mode = forms.ChoiceField(label='Mode', required=True, choices=CHOICES,)
