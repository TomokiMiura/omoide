from django.urls import path
from . import views

name = 'base'

urlpatterns = [

    path('',views.top,name='base'),
    path('login',views.login,name='login'),
    path('signup',views.signup,name='signup'),
    #path('home',views.home,name='home'),
    path('home', views.OmoideListView.as_view(), name='omoidelist'),
    path('post/<int:pk>/',views.PostDetailView.as_view(),name='post'),
    path('create_omoide/', views.omoide_create, name='create_omoide'),

]