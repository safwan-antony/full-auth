from django.shortcuts import render , redirect 
from django.http import HttpResponse
from django.contrib.auth import get_user_model
#login 
from django.contrib.auth import authenticate, login, logout , get_user_model
from django.contrib.auth.decorators import login_required
#message send info
from django.contrib import messages
#forms and models
from .forms import *
from .models import *
#create password
from django.contrib.auth.hashers import make_password
#reset_password
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
#change password
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
#email activateà
from allauth.account.utils import send_email_confirmation 
from django.contrib.sites.shortcuts import get_current_site  
from .tokens import account_activation_token
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
 
from django.contrib.auth.models import User  
from django.core.mail import EmailMessage  

####

# Create your views here.
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request,'Login Successfully')
            return redirect('index')
        else:
            messages.warning(request,'email or password is incorrect')
    return render(request,'account/login.html')

@login_required
def logoutPage(request):
    logout(request)
    return redirect('index')

""" def signupPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            email=form.cleaned_data['email']
            if User.objects.filter(username=username).exists():
                messages.warning(request,'Username already exists')
            elif User.objects.filter(email=email).exists():
                messages.warning(request,'Email already exists')
            elif form.cleaned_data['password'] != form.cleaned_data['confirm_password']:
                messages.warning(request,'Password does not match')
            else:
                username=form.cleaned_data['username']
                email=form.cleaned_data['email']
                password = make_password(form.cleaned_data['password'])
                data = User(username=username,email=email,password=password)
                data.save()
                messages.success(request,'Account created successfully')
                return redirect('account_login')
    context = {'form':form}
    return render(request,'account/signup.html',context) """

def signupPage(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        confirm_password=request.POST.get('confirm_password')
        User = get_user_model()
        if User.objects.filter(username=username).exists():
            messages.warning(request,'Username already exists')
        elif User.objects.filter(email=email).exists():
            messages.warning(request,'Email already exists')
        elif password != confirm_password: 
            messages.warning(request,'Passwords do not match')
        else:
           # password = make_password(password)
            user = User.objects.create_user(username=username,email=email,password=password)
            
            user.save()
            send_email_confirmation(request, user)
            messages.success(request,'Account created successfully you need to activate your email to login')
            return redirect('account_login')
            # to get the domain of the current site  
       
    return render(request, 'account/signup.html')  

@login_required
def profilePage(request,pk):
    User = get_user_model()
    user = User.objects.get(id=pk)
    context={'user':user}
    return render(request,'account/my_profile.html',context)

@login_required
def editProfile(request,pk):
    User = get_user_model()
    user = User.objects.get(id=pk)
    form = ProfileForm(instance=user)
    if request.method == 'POST':
        form = ProfileForm(request.POST,request.FILES,instance=user)
        if form.is_valid():
            form.save()
            return redirect('account_profile',pk=user.id)
    context = {'form':form,'user':user}
    return render(request,'account/edit_profile.html',context)

@login_required
def profileSettings(request):
    if request.method== 'POST':
        if 'send' in request.POST:
            send_email_confirmation(request,request.user)
            messages.success(request,'Email sent successfully')
            return redirect('account_profile_settings')
      
    return render(request,'account/profile_settings.html')

@login_required
def profile_emailchange(request):
    
    if request.htmx:
        form = EmailChangeForm(instance=request.user)
        return render(request, 'account/email_form.html', {'form':form})
    
    if request.method == 'POST':
        form = EmailChangeForm(request.POST, instance=request.user)

        if form.is_valid():
            
            # Check if the email already exists
            email = form.cleaned_data['email']
            User= get_user_model()
            if User.objects.filter(email=email).exclude(id=request.user.id).exists():
                messages.warning(request, f'{email} is already in use.')
                return redirect('account_profile_settings')
            
            form.save() 
            
            # Then Signal updates emailaddress and set verified to False
            
            # Then send confirmation email 
            send_email_confirmation(request, request.user)
            
            return redirect('account_profile_settings')
        else:
            messages.warning(request, 'Form not valid')
            return redirect('account_profile_settings')
        
    return redirect('home')

@login_required
def deleteProfile(request,pk):
    User=get_user_model()
    user = User.objects.get(id=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('index')
    context = {'user':user}
    return render(request, 'account/delete_profile.html',context)

""" def changePassword(request): #is not working
    form = ChangePasswordForm(request.user)
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!   
            messages.success(request, 'Your password was successfully updated!')
            return redirect('index')
        else:
            messages.error(request, 'Please correct the error below.') 
    return render(request, 'account/change_password.html',{'form':form})"""
""" 
class ChangePasswordView(PasswordChangeView): #is not working 
    form_class = PasswordChangeForm
    success_url = reverse_lazy('index')
    template_name = 'account/change_password.html'
    context_object_name = 'form' 
    def form_valid(self, form):
        user = form.save()
        update_session_auth_hash(self.request, user)  # Important!
        return super().form_valid(form) """
    
""" def change_password(request):
    form = PasswordChangeForm()
    if request.method == 'POST':
        form = PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            update_session_auth_hash(request, form.user)
            form.save()
            messages.success(request, 'Your password was successfully updated!')
    context = {'form':form}
    return render(request, 'account/password_change.html', context) """

@login_required
def Change_Password(request):
    form = PasswordChangeForm(user =request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(user =request.user, data = request.POST)
        if form.is_valid():
            update_session_auth_hash(request, form.user)
            form.save()
            
            messages.success(request, 'Your password was successfully updated!')
            return redirect('index')
        
    return render(request, 'account/change_password.html', {'form':form})

""" def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, "Thank you for your email confirmation. Now you can login your account.")
        return redirect('login')
    else:
        messages.error(request, "Activation link is invalid!")

    return redirect('homepage') """
class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'account/password_reset.html'
    email_template_name = 'account/password_reset_email.html'
    subject_template_name = 'account/password_reset_subject.html'
    email_confirm_template_name='account/password_reset_confirm.html'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('index')
