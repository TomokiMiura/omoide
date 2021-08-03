from django.shortcuts import render,redirect
from datetime import date, datetime
from accounts.models import User
from django.db.models import Q
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.urls import reverse_lazy
from django.utils import timezone
# Create your views here.
from django.http import HttpResponse
from django.template import loader
from django.views.generic import TemplateView,ListView,DetailView,CreateView,FormView,UpdateView
from base.models import OmoideTran,TextTran,CoupleMaster
from . forms import OmoideCreateForm,TextModelForm

class TopView(TemplateView):
    template_name = 'top.html'

class OmoideListView(ListView):
    template_name = 'home.html'
    queryset = OmoideTran.objects.order_by('-posttime')
    context_object_name = 'omoide_list'
    paginate_by = 6

    def get_queryset(self):
        # ログインユーザーに合わせて表示するomoideを動的に変える
        current_user = self.request.user
        couple_instance = CoupleMaster.objects.get(
            Q(men_id=current_user) | Q(girl_id=current_user)
        )
        return OmoideTran.objects.filter(couple_id=couple_instance)
    
    def get_context_data(self):
        ctx = super().get_context_data()

        # current_user：現在のユーザーのインスタンス
        current_user = self.request.user
        # インスタンスcouple_instanceとして保存
        couple_instance = CoupleMaster.objects.get(
            Q(men_id=current_user) | Q(girl_id=current_user)
        )
        # 現在ユーザーが男性なら
        if couple_instance.men_id == current_user:
            # 女性ユーザーのインスタンスpair_userを作成
            pair_user = couple_instance.girl_id
        else:
            # 男性ユーザーのインスタンスpair_userを作成
            pair_user = couple_instance.men_id
        ctx['current_username'] = current_user.username
        ctx['pair_username'] = pair_user.username
        return ctx

class OmoideCreateView(FormView):
    template_name = 'create_omoide.html'
    form_class = OmoideCreateForm
    model = OmoideTran
    success_url = reverse_lazy('base:omoidelist')

    def form_valid(self, form):
        ctx = {'form': form}
        if self.request.POST.get('next', '') == 'confirm':
            # 確認ボタンを押下したら、一度入力内容をDBに保存する
            # DBに保存しつつ、そのインスタンスsaved_formを生成
            saved_form = form.save(self.request.user)
            # 投稿確認viewへリダイレクト
            return redirect('base:confirm_omoide',pk=saved_form.pk)
        elif self.request.POST.get('next', '') == 'back':
            return render(self.request, 'create_omoide.html', ctx)
        else:
            # 正常動作ではここは通らない。エラーページへの遷移でも良い
            return redirect(reverse_lazy('base:omoidelist'))

    def get_context_data(self):
        ctx = super().get_context_data()
        # current_user：現在のユーザーのインスタンス
        current_user = self.request.user
        # インスタンスcouple_instanceとして保存
        couple_instance = CoupleMaster.objects.get(
            Q(men_id=current_user) | Q(girl_id=current_user)
        )
        # 現在ユーザーが男性なら
        if couple_instance.men_id == current_user:
            # 女性ユーザーのインスタンスpair_userを作成
            pair_user = couple_instance.girl_id
        else:
            # 男性ユーザーのインスタンスpair_userを作成
            pair_user = couple_instance.men_id
        ctx['current_username'] = current_user.username
        ctx['pair_username'] = pair_user.username
        return ctx
 
class OmoideConfirmView(UpdateView):
    template_name = 'confirm_omoide.html'
    model = OmoideTran
    fields = ['title', 'posttime', 'thumbnail']
    success_url = reverse_lazy('base:omoidelist')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # current_user：現在のユーザーのインスタンス
        current_user = self.request.user
        # インスタンスcouple_instanceとして保存
        couple_instance = CoupleMaster.objects.get(
            Q(men_id=current_user) | Q(girl_id=current_user)
        )
        # 現在ユーザーが男性なら
        if couple_instance.men_id == current_user:
            # 女性ユーザーのインスタンスpair_userを作成
            pair_user = couple_instance.girl_id
        else:
            # 男性ユーザーのインスタンスpair_userを作成
            pair_user = couple_instance.men_id
        ctx['current_username'] = current_user.username
        ctx['pair_username'] = pair_user.username
        return ctx

class OmoideCommentView(FormView):
    template_name = 'detail_omoide.html'
    form_class = TextModelForm

    def form_valid(self, form):
        kwargs = {}
        kwargs['user'] = self.request.user
        # forms.pyのコメントを保存するメソッドsave_commentを実行する
        # OmoideTranにおける特定のpkのオブジェクトの情報が辞書型データ
        # としてsave_commentに渡される
        form.save_comment(self.kwargs.get('pk'), **kwargs)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('base:post', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self):
        ctx = super().get_context_data()
        ctx['omoide'] = OmoideTran.objects.get(id=self.kwargs['pk'])
        ctx['comment_list'] = TextTran.objects.filter(omoide_id_id=self.kwargs['pk']).order_by('posttime')
        # current_user：現在のユーザーのインスタンス
        current_user = self.request.user
        # インスタンスcouple_instanceとして保存
        couple_instance = CoupleMaster.objects.get(
            Q(men_id=current_user) | Q(girl_id=current_user)
        )
        # 現在ユーザーが男性なら
        if couple_instance.men_id == current_user:
            # 女性ユーザーのインスタンスpair_userを作成
            pair_user = couple_instance.girl_id
        else:
            # 男性ユーザーのインスタンスpair_userを作成
            pair_user = couple_instance.men_id
        ctx['current_username'] = current_user.username
        ctx['pair_username'] = pair_user.username
        return ctx