from django.shortcuts import render, redirect
from userauths.forms import UserRegisterForm, ProfileForm, OTPVerifyForm  
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.conf import settings
from userauths.models import User, Profile, OTPVerification  
from django.contrib.auth.decorators import login_required
from django.utils import timezone  


def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  
            user.save()
            
            otp_record = OTPVerification.create_for_user(user)
            
            request.session['signup_user_id'] = user.id
            
            messages.success(request, "Account created! Verify with OTP.")
            return redirect("userauths:verify-otp")
    else:
        form = UserRegisterForm()
         
    context = {
        'form': form,
    }
    return render(request, "userauths/sign-up.html", context)

def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in.")
        return redirect("core:index")
   
    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")

        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect("core:index")
        else:
            if User.objects.filter(email__iexact=email).exists():
                messages.error(request, "Email exists, but password is incorrect.")
            else:
                messages.error(request, "No account found with this email/username.")
   
    return render(request, "userauths/sign-in.html")

def logout_view(request):
    logout(request)
    messages.success(request, "You logged out.")
    return redirect("userauths:sign-in")

@login_required
def profile_update(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.save()
            messages.success(request, "Profile Updated Successfully.")
            return redirect("core:dashboard")
    else:
        form = ProfileForm(instance=profile)
    context = {
        "form": form,
        "profile": profile,
    }
    return render(request, "userauths/profile-edit.html", context)

def verify_otp_view(request):
    user_id = request.session.get('signup_user_id')
    if not user_id:
        messages.warning(request, "Invalid registration session. Please sign up again.")
        return redirect("userauths:sign-up")
    
    try:
        user = User.objects.get(id=user_id, is_active=False)
    except User.DoesNotExist:
        messages.error(request, "User not found. Please sign up again.")
        del request.session['signup_user_id']
        return redirect("userauths:sign-up")
    
    otp_record = OTPVerification.objects.filter(
        user=user,
        purpose='registration',
        is_used=False
    ).order_by('-created_at').first()
    
    if not otp_record:
        messages.error(request, "No active OTP found. Resend or sign up again.")
        return redirect("userauths:sign-up")
    
    if request.method == "POST":
        form = OTPVerifyForm(request.POST)
        if form.is_valid():
            entered_otp = form.cleaned_data['otp']
            if otp_record.is_valid(entered_otp):
                user.is_active = True
                user.save()
                profile = Profile.objects.get(user=user)
                profile.verified = True  
                profile.save()
                otp_record.mark_as_used()
                
                del request.session['signup_user_id']
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                messages.success(request, f"Welcome {user.username}! Account verified.")
                return redirect("core:index")
            else:
                messages.error(request, "Invalid or expired OTP.")
    else:
        form = OTPVerifyForm()
    
    remaining_seconds = max(0, (otp_record.expires_at - timezone.now()).total_seconds())
    
    context = {
        'form': form,
        'email': user.email,
        'remaining_seconds': int(remaining_seconds),
        'otp_for_dev': otp_record.otp_code if settings.DEBUG else None,
    }
    return render(request, "userauths/verify-otp.html", context)

def resend_otp_view(request):
    user_id = request.session.get('signup_user_id')
    if not user_id:
        return redirect("userauths:sign-up")
    
    try:
        user = User.objects.get(id=user_id, is_active=False)
    except User.DoesNotExist:
        return redirect("userauths:sign-up")
    
    current_otp = OTPVerification.objects.filter(user=user, purpose='registration', is_used=False).first()
    if current_otp and not current_otp.is_expired:
        messages.warning(request, "Current OTP is still valid. Wait for it to expire.")
        return redirect("userauths:verify-otp")
    
    new_otp_record = OTPVerification.create_for_user(user)
    
    messages.success(request, "New OTP generated (check page in dev mode).")
    return redirect("userauths:verify-otp")


def forgot_password_simple(request):
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in.")
        return redirect("core:index")

    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()

        if not email:
            messages.warning(request, "Please enter your email.")
            return redirect("userauths:forgot-password-simple")

        user = User.objects.filter(email__iexact=email).first()

        if not user:
            messages.error(request, "No account found with this email.")
            return redirect("userauths:forgot-password-simple")

        request.session['reset_email'] = email
        messages.info(request, f"Proceeding to reset password for {email}")
        return redirect("userauths:reset-password-simple")

    return render(request, "userauths/forgot-password-simple.html")


def reset_password_simple(request):
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in.")
        return redirect("core:index")

    email = request.session.get('reset_email')

    if not email:
        messages.error(request, "Session expired. Please start over from Forgot Password.")
        return redirect("userauths:forgot-password-simple")

    user = User.objects.filter(email__iexact=email).first()
    if not user:
        del request.session['reset_email']
        messages.error(request, "Account not found. Please try again.")
        return redirect("userauths:forgot-password-simple")

    if request.method == "POST":
        password1 = request.POST.get("password1", "")
        password2 = request.POST.get("password2", "")

        if not password1 or not password2:
            messages.warning(request, "Both password fields are required.")
        elif password1 != password2:
            messages.error(request, "Passwords do not match.")
        elif len(password1) < 6:
            messages.error(request, "Password must be at least 6 characters.")
        else:
            user.set_password(password1)
            user.is_active = True  # Activate user during password reset
            user.save()
            del request.session['reset_email']
            messages.success(request, "Password changed successfully! You can now log in.")
            return redirect("userauths:sign-in")
    return render(request, "userauths/reset-password-simple.html", {"email": email})