from django import forms

def should_be_empty(value):
    if value:
        raise forms.ValidationError('Field is not empty')

class ContactForm(forms.Form):
    Topic = forms.CharField(max_length=100, label="Topic")
    Message = forms.CharField(widget=forms.Textarea, label="Message")
    Contact_Email = forms.EmailField(label="Contact")
    forcefield = forms.CharField(required=False, widget=forms.HiddenInput, label="Leave empty", validators=[should_be_empty])
