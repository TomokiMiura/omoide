from django.shortcuts import render, redirect
from django.views.generic import TemplateView, FormView, UpdateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView,
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
)
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate

from .models import User
from .forms import (
    UserInfoChangeForm,
    CustomAuthenticationForm, CustomPasswordChangeForm,
    CustomPasswordResetForm, CustomSetPasswordForm,
    CustomUserChangeForm, CustomUserCreationForm, EmailChangeForm
)

from base.models import OmoideTran,TextTran,CoupleMaster

# Create your views here.
# 男性ユーザーを登録するためのビュー
class MenUserCreateView(FormView):
    # form_class = UserCreationForm
    form_class = CustomUserCreationForm
    template_name = 'create_men_user.html'
    # ビューの処理が完了したら、女性ユーザーの登録ビューへリダイレクト
    success_url = reverse_lazy('accounts:create_girl_user')
    def form_valid(self, form):
        print(self.request.POST['next'])
        # 戻るボタンが押下されたら、入力内容はそのままフォームを再表示
        if self.request.POST['next'] == 'back':
            return render(self.request, 'create_men_user.html', {'form': form})
        # 確認ボタンが押下されたら、入力内容を表示
        elif self.request.POST['next'] == 'confirm':
            return render(self.request, 'confirm_men_user.html', {'form': form})
        # 登録ボタンが押下されたら入力内容をフォームに保存
        elif self.request.POST['next'] == 'regist':
            set_form = form.save()
            response = redirect(reverse_lazy('accounts:create_girl_user'))
            # Cookieを使ってユーザー1のpkを保存
            response.set_cookie('men_id', set_form.pk)
            return response
        else:
            # 通常このルートは通らない
            return redirect(reverse_lazy('base:top'))

# 女性ユーザーを登録するためのビュー
class GirlUserCreateView(FormView):
    # form_class = UserCreationForm
    form_class = CustomUserCreationForm
    template_name = 'create_girl_user.html'
    # ビューの処理が完了したら、ログインビューへリダイレクト
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        print(self.request.POST['next'])
        # 戻るボタンが押下されたら、入力内容はそのままフォームを再表示
        if self.request.POST['next'] == 'back':
            return render(self.request, 'create_girl_user.html', {'form': form})
        # 確認ボタンが押下されたら、入力内容を表示
        elif self.request.POST['next'] == 'confirm':
            return render(self.request, 'confirm_girl_user.html', {'form': form})
        # 登録ボタンが押下されたら入力内容をフォームに保存
        elif self.request.POST['next'] == 'regist':
            set_form = form.save()
            response = redirect(reverse_lazy('accounts:confirm'))
            men_id = self.request.COOKIES['men_id']
            # Cookieを使ってユーザー1のpkを保存
            # response.set_cookie('girl_id', set_form.pk)
            # CoupleMasterに男性ユーザー、女性ユーザーのpkを追加する
            CoupleMaster.objects.create(men_id='men_id',girl_id = 'set_form.pk')
            return response
        else:
            # 通常このルートは通らない
            return redirect(reverse_lazy('base:top'))

class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'user_profile.html'
    def get_queryset(self):
        return User.objects.get(id=self.request.user.id)

class EmailChangeView(LoginRequiredMixin, FormView):
    template_name = 'email_change.html'
    form_class = EmailChangeForm
    success_url = reverse_lazy('accounts:profile')
    
    def form_valid(self, form):
        #formのupdateメソッドにログインユーザーを渡して更新
        form.update(user=self.request.user)
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # 更新前のユーザー情報をkwargsとして渡す
        kwargs.update({
            'email' : self.request.user.email,
        })
        return kwargs

class UserChangeView(LoginRequiredMixin, FormView):
    '''
    Django組込みのUserを利用する場合のユーザー情報変更ビュー
    カスタムユーザーでは使用しない
    '''
    template_name = 'registration/change.html'
    form_class = UserInfoChangeForm
    success_url = reverse_lazy('accounts:profile')
    
    def form_valid(self, form):
        #formのupdateメソッドにログインユーザーを渡して更新
        form.update(user=self.request.user)
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # 更新前のユーザー情報をkwargsとして渡す
        kwargs.update({
            'email' : self.request.user.email,
            'first_name' : self.request.user.first_name,
            'last_name' : self.request.user.last_name,
        })
        return kwargs

class CustomLoginView(LoginView):
    template_name = 'login.html'
    form_class = CustomAuthenticationForm

class CustomLogoutView(LogoutView):
    template_name = 'logout.html'
    next_page = '/'

class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'registration/password_change_form.html'
    success_url = reverse_lazy('accounts:password_change_done')

class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'registration/password_change_done.html'

class CustomPasswordResetView(PasswordResetView):
    email_template_name = 'registration/password_reset_email.html'
    form_class = CustomPasswordResetForm
    from_email = 'info@example.com'
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = reverse_lazy('accounts:password_reset_done')
    template_name = 'registration/password_reset_form.html'

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomSetPasswordForm
    # post_reset_loginがFalseの時、新しいパスワードが登録された時、そのままログインする
    post_reset_login = False
    post_reset_login_backend = None
    success_url = reverse_lazy('accounts:password_reset_complete')
    template_name = 'registration/password_reset_confirm.html'

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'

