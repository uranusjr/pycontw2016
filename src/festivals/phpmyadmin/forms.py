from django import forms

from festivals.models import LogInAttempt


class PHPMyAdminLogInForm(forms.Form):

    pma_username = forms.CharField(max_length=255)
    pma_password = forms.CharField(max_length=255)

    def save(self):
        data = self.cleaned_data
        instance = LogInAttempt(
            username=data['pma_username'],
            password=data['pma_password'],
        )
        instance.save()
        return instance
