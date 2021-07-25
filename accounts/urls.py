from django.urls import path
from django.contrib.auth import views as auth_views   # for resetting password
from . import views

urlpatterns = [
    path('login/',views.login,name='login'),
    path('logout/',views.logout),
    path('register/',views.register,name="register"),

    # resetting password urls
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name="password_reset_form.html"),name="reset_password"),
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"),name="password_reset_done"),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"),name="password_reset_confirm"),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"),name="password_reset_complete")
]


# password reset documentation
# https://docs.djangoproject.com/en/3.0/topics/auth/default/#all-authentication-views

# 1 - submit email form
# 2 - email sent success message
# 3 - link to password reset form in email
# 4 - password successfully change message