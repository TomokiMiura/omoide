from django.shortcuts import render,redirect,get_object_or_404
from django.utils import timezone
# Create your views here.
from django.http import HttpResponse
from django.template import loader
from django.views.generic import ListView,DetailView
from base.models import OmoideTran,MenMaster,GirlMaster,TextTran
from . forms import OmoideCreateForm


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

def omoide_create(request):
    form = OmoideCreateForm(request.POST or None)
    if form.is_valid():
        omoide = OmoideTran()
        omoide.couple_id = 1
        #テスト用のため、1に設定
        omoide.title = form.cleaned_data['title']
        omoide.posttime = form.cleaned_data['posttime']

        OmoideTran.objects.create(
            couple_id=omoide.couple_id,
            title=omoide.title,
            posttime=omoide.posttime,
        )
        return redirect('omoidelist')
    return render(request, 'create_omoide.html', {'form': form})
