from django import forms


class ContactForm(forms.Form):
    """Simple contact form"""
    name = forms.CharField(max_length=100, label="Name")
    email = forms.EmailField(label="Email")
    message = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 4}), 
        label="Message")
    