from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.utils import timezone
# Create your views here.
from django.http import HttpResponse
from django.template import loader
from django.views.generic import ListView,DetailView,CreateView,FormView
from base.models import OmoideTran,MenMaster,GirlMaster,TextTran,CoupleMaster
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

class OmoideFormView(FormView):
    template_name = 'create_omoide.html'
    form_class = OmoideCreateForm
    success_url = reverse_lazy('base:omoidelist')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)