from django.shortcuts import render
from django.db.models import Q
from django.views.generic import ListView
from functools import reduce
from operator import and_
from base.models import OmoideTran,TextTran,CoupleMaster
from django.contrib.auth.mixins import LoginRequiredMixin

class SearchResultView(LoginRequiredMixin,ListView):
    template_name = 'results.html'
    context_object_name = 'result_list'

    def get_queryset(self):
        # 検索キーワードに合致するomoideのタイトルがあった場合
        if self.request.GET.get('q', ''):
            # paramsには検索ワードが格納
            params = self.parse_search_params(self.request.GET['q'])
            query = reduce(
                # 検索ワードとomoideのタイトルで合致したものがあれば表示させる
                # スペースを空けて複数のキーワードで検索したら
                # 検索ワードと一つでも合致するタイトルであれば検索結果として表示する
                # lambda x,y:x | yで設定
                lambda x,y:x | y,
                list(map(lambda z: Q(title__icontains=z), params))
            )
            return OmoideTran.objects.filter(query)
        else:
            return None
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['query'] = self.request.GET.get('q', '')
        current_user = self.request.user
        couple_instance = CoupleMaster.objects.get(
            Q(men_id=current_user) | Q(girl_id=current_user)
        )
        if couple_instance.men_id == current_user:
            pair_user = couple_instance.girl_id
        else:
            pair_user = couple_instance.men_id
        ctx['current_username'] = current_user.username
        ctx['pair_username'] = pair_user.username
        return ctx
        
    def parse_search_params(self, words: str):
        # 引数wordsはキー(q)
        # 引数strはバリュー(検索ワード)
        # 全角スペースがあった場合は半角スペースに変換
        # スペースで区切られた検索ワードそれぞれで検索を行うためsplitメソッドを使用
        search_words = words.replace('　', ' ').split()
        return search_words
