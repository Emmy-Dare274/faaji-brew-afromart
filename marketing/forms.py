from django import forms
from .models import NewsletterSubscriber


class NewsletterSignupForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscriber
        fields = ["email"]
        widgets = {
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "you@example.com",
            })
        }