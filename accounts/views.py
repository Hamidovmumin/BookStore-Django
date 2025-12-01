from django.shortcuts import render , reverse, redirect
from accounts.forms import RegisterForm,ForgotPassword
from .models import Account
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required

# VERIFICATION email

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model, update_session_auth_hash


# Create your views here.
def registration(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            username = email.split('@')[0]
            password = form.cleaned_data['password']
            phone_number = form.cleaned_data['phone_number']

            user = Account.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
                username=username,
                phone_number=phone_number,
            )
            user.save()

            # User activation
            current_site = get_current_site(request)
            mail_subject = 'Hesabınızı aktivləşdirin!'
            message = render_to_string('account/account_verification_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            login_url = reverse('login')
            return redirect(f'{login_url}?command=verification&email={email}')
    else:
        form = RegisterForm()

    context = {
        'form': form,
    }
    return render(request, 'account/registration.html',context)

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request,'Hesabınız aktivləşdirildi!')
        return redirect('login')
    else:
        messages.error(request,'Aktivasiya linki etibarsızdır!')
        return redirect('registration')


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request,"Ugurla daxil oldunuz!")
            return redirect('index')
        else:
            messages.error(request,"İstifadəçi adı və ya şifrə səhvdir!")
            return redirect('login')

    return render(request, 'account/login.html')


@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('index')


def forgotPassword(request):
    form = ForgotPassword(request.POST)
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            # Reset password email
            current_site = get_current_site(request)
            mail_subject = 'Parolun dəyişdirilməsi'
            message = render_to_string('account/reset_password_email.html',
                                       {
                                           'user': user,
                                           'domain': current_site.domain,
                                           'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                           'token': default_token_generator.make_token(user),
                                       })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            messages.success(request, 'Password reset email has been sent to your email address')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist')
            return redirect('forgotpassword')
    context = {
        'form': form,
    }
    return render(request, 'account/forgotPassword.html', context)

def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid) # Account.objects.get(pk=uid) kodu ile eynidir.
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid']=uid
        print('Parolu deyisin')
        return redirect('resetPassword')
    else:
        print('Aktivasiya linki etibarsızdır!')
        return redirect('login')

def resetPassword(request):
    if request.method == 'POST':
        newPassword = request.POST['newPassword']
        confirmPassword = request.POST['confirmPassword']

        if newPassword == confirmPassword:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(newPassword)
            user.save()
            print( 'Parol ugurla deyisdirildi.')
            return redirect('login')
        else:
            print('Parolu deyisme alinmadi')
            return redirect('login')
    else:
        return render(request, 'account/resetPassword.html')