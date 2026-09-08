from django import forms
from .models import UserProfile


class ProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = [
            "default_full_name", "default_phone_number",
            "default_address_line1", "default_address_line2",
            "default_town_or_city", "default_postcode", "default_country",
        ]
        labels = {
            "default_full_name": "Full name",
            "default_phone_number": "Phone number",
            "default_address_line1": "Address line 1",
            "default_address_line2": "Address line 2",
            "default_town_or_city": "Town or city",
            "default_postcode": "Postcode",
            "default_country": "Country",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs["class"] = "form-select" if name == "default_country" else "form-control"
            field.required = False