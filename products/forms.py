from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):

    """ Used for both writing a new review and editing an existing
    one — the view decides which by passing instance= or not. """

    class Meta:
        model = Review
        fields = ["rating", "title", "body"]
        widgets = {
            "rating": forms.Select(
                choices=[(i, f"{i} star{'s' if i != 1 else ''}") for i in range(5, 0, -1)],
                attrs={"class": "form-select mb-2", "style": "max-width: 200px;"},
            ),
            "title": forms.TextInput(attrs={
                "class": "form-control mb-2",
                "placeholder": "Sum up your experience",
            }),
            "body": forms.Textarea(attrs={
                "class": "form-control mb-2",
                "rows": 4,
                "placeholder": "What did you think of this product?",
            }),
        }
