from django.urls import path, include
from django.contrib.auth import views as av
from . import views
from .forms import (
    CustomAuthenticationForm, CustomPasswordChangeForm
)

app_name = 'accounts'

urlpatterns = [
    # 男性ユーザーのサインアップURL
    path('signup_men/', views.MenUserCreateView.as_view(), name="create_men_user"),
    # 女性ユーザーのサインアップURL
    path('signup_girl/', views.GirlUserCreateView.as_view(), name="create_girl_user"),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('password_change/', views.CustomPasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', views.CustomPasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('change/', views.EmailChangeView.as_view(), name="change"),
    

]
