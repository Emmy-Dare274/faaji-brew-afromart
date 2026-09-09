from django import forms
from django.forms import inlineformset_factory
from .models import Category, Product, ProductImage, ProductVariant, Review


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


def _bootstrap_widgets(fields):

    """ Shared styling logic for the staff forms below: checkboxes
    get form-check-input, dropdowns get form-select, everything else
    gets form-control, so each form's __init__ is a one-liner. """

    for field in fields.values():
        if isinstance(field.widget, forms.CheckboxInput):
            field.widget.attrs["class"] = "form-check-input"
        elif isinstance(field.widget, forms.Select):
            field.widget.attrs["class"] = "form-select"
        else:
            field.widget.attrs["class"] = "form-control"


class ProductForm(forms.ModelForm):

    """ Slug and SKU are deliberately left out — Product.save()
    already generates both automatically when blank, so staff never
    have to type one by hand or risk a uniqueness clash. """

    class Meta:
        model = Product
        fields = ["category", "name", "description", "price", "stock_quantity", "is_featured", "is_active"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _bootstrap_widgets(self.fields)


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ["name", "description", "image", "is_active", "show_in_main_nav"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _bootstrap_widgets(self.fields)


class ProductImageForm(forms.ModelForm):

    class Meta:
        model = ProductImage
        fields = ["image", "alt_text", "is_primary"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _bootstrap_widgets(self.fields)


class ProductVariantForm(forms.ModelForm):

    class Meta:
        model = ProductVariant
        fields = ["variant_type", "value", "stock_quantity", "price_adjustment"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _bootstrap_widgets(self.fields)


ProductImageFormSet = inlineformset_factory(
    Product, ProductImage, form=ProductImageForm,
    fields=["image", "alt_text", "is_primary"],
    extra=1, can_delete=True,
)

ProductVariantFormSet = inlineformset_factory(
    Product, ProductVariant, form=ProductVariantForm,
    fields=["variant_type", "value", "stock_quantity", "price_adjustment"],
    extra=1, can_delete=True,
)