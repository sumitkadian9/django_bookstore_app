from django.http import HttpResponse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import RegistrationForm, UserEditForm
from .token import account_activation_token
from .models import UserAcc

@login_required
def dashboard(request):
    return render(request, 'account/user/dashboard.html')


@login_required
def delete_user(request):
    user = UserAcc.objects.get(user_name = request.user)
    user.is_active = False
    user.save()
    logout(request)
    return redirect('account:delete_confirmation')
    

@login_required
def edit_details(request):

    if request.method == 'POST':
        userForm = UserEditForm(instance=request.user, data=request.POST)
        if userForm.is_valid():
            userForm.save()
    else:
        userForm = UserEditForm(instance=request.user)
    return render(request, 'account/user/edit_details.html',{'userForm':userForm})


def account_register(request):

    registerForm = RegistrationForm()
    if request.method == 'POST':
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data['password1'])
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Account Activation'
            message = render_to_string('account/registration/activation_mail.html', {
                'user':user,
                'domain':current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            user.email_user(subject=subject, message=message)
            return render(request, 'account/registration/mailsent.html',{'form':registerForm})
    else:
        registerForm = RegistrationForm()
    return render(request, 'account/registration/register.html', {'form':registerForm})


def account_activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserAcc.objects.get(pk=uid)
    except:
        pass
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('account:dashboard')
    else:
        return render(request, 'account/registration/activation_invalid.html')
