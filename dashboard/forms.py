from django import forms

from .models import ContactMessage


class ContactMessageForm(forms.ModelForm):
    name = forms.CharField(max_length=100, required=True, strip=True)
    email = forms.EmailField(max_length=254, required=True)
    message = forms.CharField(widget=forms.Textarea, required=True, strip=True)

    class Meta:
        model = ContactMessage
        fields = ('name', 'email', 'message')