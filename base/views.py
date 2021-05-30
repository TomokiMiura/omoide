from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.utils import timezone
# Create your views here.
from django.http import HttpResponse
from django.template import loader
from django.views.generic import ListView,DetailView
from base.models import OmoideTran,MenMaster,GirlMaster,TextTran,CoupleMaster
from . forms import OmoideCreateForm,OmoideForm


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
    template_name = 'create_omoide.html'
    ctx = {}
    if request.method == 'GET':
        form = OmoideForm()
        ctx['form'] = form
        return render(request, template_name, ctx)
    
    if request.method == 'POST':
        omoide_form = OmoideForm(request.POST)
        if omoide_form.is_valid():
            # topic_form.save()
            omoide = OmoideTran()
            cleaned_data = omoide_form.cleaned_data
            omoide.title = cleaned_data['title']
            omoide.couple_id = cleaned_data['couple_id']
            omoide.posttime = cleaned_data['posttime']
            omoide.save()            
            return redirect(reverse_lazy('base:omoidelist'))
        else:
            ctx['form'] = omoide_form
            return render(request, template_name, ctx)




'''def omoide_create(request):
    template_name = 'create_omoide.html'
    ctx = {}
    if request.method == 'GET':
        ctx['form'] = OmoideCreateForm()
        return render(request, template_name, ctx)
    
    if request.method == 'POST':
        omoide_form = OmoideCreateForm(request.POST)
        if omoide_form.is_valid():
            omoide_form.save()
            return redirect(reverse_lazy('base:omoidelist'))
        else:
            ctx['form'] = omoide_form
            return render(request, template_name, ctx)'''
