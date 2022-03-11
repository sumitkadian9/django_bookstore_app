from django import forms
from .models import UserAcc
from django.core.exceptions import ValidationError

class RegistrationForm(forms.ModelForm):

    user_name = forms.CharField(label='Username', min_length=5, max_length=50, help_text='Required')
    email = forms.EmailField(max_length=100, help_text='Required', error_messages={'Required':'E-mail address is mandatory'})
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = UserAcc
        fields = ('user_name','email')
    
    def clean_username(self):
        user_name = self.cleaned_data['user_name'].lower()
        r = UserAcc.objects.filter(user_name=user_name)
        if r.count():    
            raise ValidationError('Username already exists!')
        return user_name
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if UserAcc.objects.filter(email=email).exists():
            raise ValidationError('E-mail address already exists!')
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            'class':'form-control mb-3', 'placeholder':'Email Address'
        })
        self.fields['user_name'].widget.attrs.update({
            'class':'form-control mb-3', 'placeholder':'Username'
        })
        self.fields['password1'].widget.attrs.update({
            'class':'form-control mb-3', 'placeholder':'Password'
        })
        self.fields['password2'].widget.attrs.update({
            'class':'form-control mb-3', 'placeholder':'Confirm Password'
        })
