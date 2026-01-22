from django import forms
from core.models import ProductReview,Vendor

class ProductReviewForm(forms.ModelForm):
    review = forms.CharField(widget=forms.Textarea(attrs={'placeholder': "write review"}))

    class Meta:
        model = ProductReview
        fields = ['review', 'rating']


class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                "class": "form-control"
            })    

            




