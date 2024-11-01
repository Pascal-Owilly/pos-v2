from django.urls import path
from .views import login_view, register_employee, register_success
from authentication import views as list_views
from django.contrib.auth.views import (
    LogoutView,
    PasswordResetView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)

app_name = "authentication"

urlpatterns = [
    path('accounts/login/', login_view, name="login"),
    path('accounts/register-employee/', register_employee, name="register_employee"),
    path('list/employees/', list_views.employee_list, name="employee_list"),

    path('accounts/register_success/', register_success, name="register_success"),
    path('accounts/reset_password/', PasswordResetView.as_view(), name='password_reset'),  # Password reset view
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path("accounts/logout/", LogoutView.as_view(), name="logout")
]
