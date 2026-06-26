from django.urls import path
from accounts.views import *

app_name = 'accounts'

urlpatterns = [
    path('login', login_view, name='login'),
    path('signup', signup_view, name='signup'),
    path('logout', logout_view, name='logout'),
    path('forgot-password', forgot_password, name='forgot-password'),
    path('verify-code', verify_code, name='verify-code'),
    path('reset-password', reset_password, name='reset-password')
]