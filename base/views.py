from django.shortcuts import render,redirect
from datetime import date, datetime
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.urls import reverse_lazy
from django.utils import timezone
# Create your views here.
from django.http import HttpResponse
from django.template import loader
from django.views.generic import ListView,DetailView,CreateView,FormView,UpdateView
from base.models import OmoideTran,MenMaster,GirlMaster,TextTran,CoupleMaster
from . forms import OmoideCreateForm,TextModelForm


def top(request):
    return render(request,'top.html')

def login(request):
    return render(request,'login.html')

def signup(request):
    return render(request,'signup.html')

class OmoideListView(ListView):
    template_name = 'home.html'
    queryset = OmoideTran.objects.order_by('-posttime')
    context_object_name = 'omoide_list'
    paginate_by = 9

    def get_context_data(self, **kwargs):
        ctx= super().get_context_data(**kwargs)
        #変更する必要あり
        men = MenMaster.objects.all()
        girl = GirlMaster.objects.all()
        ctx['men_nickname_ctx'] = men[0].men_nickname
        ctx['girl_nickname_ctx'] = girl[0].girl_nickname
        #ここまで
        return ctx

class PostDetailView(DetailView):
    template_name = 'post.html'
    model = OmoideTran
    context_object_name = 'omoidetran'

    def get_context_data(self, **kwargs):
        ctx= super().get_context_data(**kwargs)
        men = MenMaster.objects.all()
        girl = GirlMaster.objects.all()
        post_list = TextTran.objects.filter(omoide_id=self.kwargs['pk'])
        ctx['men_nickname_ctx'] = men[0].men_nickname
        ctx['girl_nickname_ctx'] = girl[0].girl_nickname
        ctx['post_list'] = post_list
        #ここまで
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
            # DBに保存しつつ、インスタンスにも格納する
            saved_form = form.save()
            # pkと保存されたデータをOmoideConfirmViewに渡す
            return redirect('base:confirm_omoide',pk=saved_form.pk)
        elif self.request.POST.get('next', '') == 'back':
            return render(self.request, 'create_omoide.html', ctx)
        else:
            # 正常動作ではここは通らない。エラーページへの遷移でも良い
            return redirect(reverse_lazy('base:top'))

class OmoideConfirmView(UpdateView):
    template_name = 'confirm_omoide.html'
    model = OmoideTran
    fields = ['title', 'posttime', 'thumbnail']
    success_url = reverse_lazy('base:omoidelist')

class OmoideCommentView(FormView):
    template_name = 'detail_omoide.html'
    form_class = TextModelForm

    def form_valid(self, form):
        # forms.pyのコメントを保存するメソッドsave_commentを実行する
        # OmoideTranにおける特定のpkのオブジェクトの情報が辞書型データ
        # としてsave_commentに渡される
        form.save_comment(self.kwargs.get('pk'))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('base:post', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self):
        ctx = super().get_context_data()
        ctx['omoide'] = OmoideTran.objects.get(id=self.kwargs['pk'])
        ctx['comment_list'] = TextTran.objects.filter(omoide_id_id=self.kwargs['pk']).order_by('posttime')
        return ctx
