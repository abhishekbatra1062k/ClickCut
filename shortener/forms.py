from django import forms

class URLForm(forms.Form):
    long_url = forms.URLField(
        label="Enter URL",
        widget=forms.URLInput(attrs={"class": "form-control", "placeholder": "Enter your long URL here"}),
    )