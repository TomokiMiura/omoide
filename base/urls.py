from django.urls import path
from . import views
import search

app_name = 'base'

urlpatterns = [

    # サイトトップページのビュー
    path('',views.TopView.as_view(),name='base'),
    # ログイン後のトップページ(omoide一覧できる)のビュー
    path('home', views.OmoideListView.as_view(), name='omoidelist'),
    # omoideに紐づくコメントを一覧できるページのビュー
    path('post/<int:pk>',views.OmoideCommentView.as_view(),name='post'),
    # omoideを作成する入力フォームのページのビュー
    path('create_omoide/', views.OmoideCreateView.as_view(), name='create_omoide'),
    # 作成されたomoideの確認画面を表示するためのビュー
    path('confirm_omoide/<int:pk>', views.OmoideConfirmView.as_view(), name='confirm_omoide'),

]