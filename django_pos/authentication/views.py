from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, EmployeeRegisterForm
from .models import CustomUser
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse
from .models import Employee
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect

def register_success(request):
    """View to redirect to registration success page."""
    return render(request, 'auth/register_success.html')

def send_password_reset_email(uidb64, token, email):
    # Encode the user ID to bytes
    uid = force_bytes(uidb64)

    # Construct the reset password URL
    reset_url = f"{settings.BASE_URL}/reset/{uidb64}/{token}/"

    # Construct the email message
    subject = 'Set Your Password'
    message = f'Please click the following link to set your password: {reset_url}'
    sender_email = settings.DEFAULT_FROM_EMAIL

    # Send the email
    send_mail(subject, message, sender_email, [email])

def register_employee(request):
    if request.method == 'POST':
        form = EmployeeRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = CustomUser.EMPLOYEE
            user.save()

            # Generate uidb64 and token for password reset email
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            # Send password reset email
            send_password_reset_email(uidb64, token, user.email)

            # Create an Employee object and associate it with the user
            employee = Employee.objects.create(employee=user)

            return redirect('employee_list')
    else:
        form = EmployeeRegisterForm()
    return render(request, 'employee_register.html', {'form': form})

def register_seller(request):
    if request.method == 'POST':
        form = SellerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = CustomUser.ADMIN
            user.save()

            # Generate uidb64 and token for password reset email
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            # Send password reset email
            send_password_reset_email(uidb64, token, user.email)

            # Create a new Seller instance and associate the user with it
            seller = Seller.objects.create(seller=user)  # Assign the user to the seller_id field
            return redirect('employee_list')
    else:
        form = SellerRegistrationForm()
    return render(request, 'auth/seller_registration.html', {'form': form})

def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                msg = 'Invalid username or password!'
        else:
            msg = 'An error ocurred!.'

    return render(request, "accounts/login.html", {"form": form})

# Password reset view
password_reset_view = PasswordResetView.as_view(
    template_name='password_reset_form.html',  # Template for rendering the password reset form
    email_template_name='password_reset_email.html',  # Template for the password reset email
    subject_template_name='password_reset_subject.txt',  # Template for the email subject
    success_url=reverse_lazy('password_reset_done'),  # URL to redirect to after submitting the password reset form
)


@login_required(login_url="/accounts/login/")
def employee_list(request):
    user = request.user

    if user.role == CustomUser.ADMIN:
        # Admin sees only their employees
        employees = Employee.objects.filter(admin=user)
    elif user.role == CustomUser.EMPLOYEE:
        # Employee sees only their own profile
        employees = Employee.objects.filter(user=user)
    else:
        employees = Employee.objects.none()  # No access if neither admin nor employee

    return render(request, 'accounts/employees.html', {'employees': employees})
