from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from accounts.forms import CreateUser
from django.contrib.auth.decorators import login_required
import secrets
from django.core.mail import send_mail
from accounts.models import PasswordResetCode
from django.conf import settings
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

# Create your views here.

def login_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            data = request.POST
            username = data['username']
            password = data['password']

            try:
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                try:
                    user = User.objects.get(username=username)
                except User.DoesNotExist:
                    messages.add_message(request, messages.ERROR, 'Login failed please check your username or email and password and try again')
                    return redirect('/accounts/login')
                
            if user.check_password(password):
                user_login = authenticate(request, username=user.username, password=password)
                if user_login is not None:
                    login(request, user_login)
                    messages.add_message(request, messages.SUCCESS, f'You logged in successfully welcome {user_login.username}')
                    return redirect('/')
                else:
                    messages.add_message(request, messages.ERROR, 'This user does not exist')
                    return redirect('/accounts/signup')
            else:
                messages.add_message(request, messages.ERROR, 'Login failed please check your username and password and try again')
                return redirect('/accounts/login')
            
        form = AuthenticationForm()
        return render(request, 'accounts/login.html', {'form': form})
    
    else:
        messages.add_message(request, messages.INFO, 'You are already logged in')
        return redirect('/')

def signup_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = CreateUser(request.POST)
            if form.is_valid():
                messages.add_message(request, messages.SUCCESS, 'Successfully created the user')
                form.save()
                return redirect('/accounts/login')
            else:
                messages.add_message(request, messages.ERROR, 'Sign up failed. Please try again')
                return redirect('/accounts/signup')
            
        form = CreateUser()
        return render(request, 'accounts/signup.html', {'form': form})
    else:
        messages.add_message(request, messages.INFO, 'You are already logged in')
        return redirect('/')

@login_required(login_url='/accounts/login')
def logout_view(request):
    logout(request)
    messages.add_message(request, messages.INFO, 'You logged out')
    return redirect('/')

def forgot_password(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            email = request.POST.get('email')

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                messages.add_message(request, messages.ERROR, 'User with this email does not exist')
                return redirect('/accounts/forgot-password')
            
            code = str(secrets.randbelow(900000) + 100000)

            reset_obj, created = PasswordResetCode.objects.get_or_create(user=user)

            reset_obj.code = code
            reset_obj.save()

            send_mail(
                'Password Reset Verification Code',
                f'''Hello,

            We received a request to reset the password for your account.

            Your verification code is:

            {code}

            This code will expire in 15 minutes.

            If you did not request a password reset, you can safely ignore this email. Your password will remain unchanged.

            For security reasons, please do not share this code with anyone.

            Thank you,
            Arsha Site Team''',
                settings.EMAIL_HOST_USER,
                [user.email],
            )

            request.session['reset_user_id'] = user.id
            request.session['reset_pending'] = True

            return redirect('/accounts/verify-code')
        
        return render(request, 'accounts/forgot-password.html')
    
    else:
        messages.add_message(request, messages.INFO, 'You are already logged in')
        return redirect('/')

def verify_code(request):
    if not request.session.get('reset_pending'):
        messages.add_message(request, messages.ERROR, 'Invalid password reset session')
        return redirect('/')
    
    if request.method == 'POST':
        entered_code = request.POST.get('code')
        user_id = request.session.get('reset_user_id')

        try:
            reset_obj = PasswordResetCode.objects.get(user_id=user_id)
            
            if reset_obj.code == entered_code:
                messages.add_message(request, messages.SUCCESS, 'The entered code was correct continue the progress')
                request.session['reset_verified'] = True
                return redirect('/accounts/reset-password')
            else:
                messages.add_message(request, messages.ERROR, 'Invalid code')
                return redirect('/accounts/verify-code')
            
        except PasswordResetCode.DoesNotExist:
            messages.add_message(request, messages.ERROR, 'Invalid code')
            return redirect('/accounts/verify-code')
        
    return render(request, 'accounts/verify-code.html')

def reset_password(request):
    if not request.session.get('reset_verified'):
        messages.add_message(request, messages.ERROR, 'Invalid password reset session')
        return redirect('/')
    
    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        user = User.objects.get(id=request.session.get('reset_user_id'))

        if password1 == password2:
            try:
                validate_password(password1)
                user.set_password(password1)
                user.save()

                request.session.pop('reset_pending', None)
                request.session.pop('reset_verified', None)
                request.session.pop('reset_user_id', None)

                PasswordResetCode.objects.filter(user=user).delete()

                messages.add_message(request, messages.SUCCESS, 'Password change was successful. Do not forget it this time!')
                return redirect('/accounts/login')
            
            except ValidationError as e:
                for error in e.messages:
                    messages.add_message(request, messages.ERROR, error)

        else:
            messages.add_message(request, messages.ERROR, 'The two password are not same. Try again')
            return redirect('/accounts/reset-password')
    
    return render(request, 'accounts/reset-password.html')