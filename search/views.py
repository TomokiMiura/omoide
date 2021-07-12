from django.shortcuts import render
from django.db.models import Q
from django.views.generic import ListView
from functools import reduce
from operator import and_
from base.models import OmoideTran,TextTran

class SearchResultView(ListView):
    template_name = 'results.html'
    context_object_name = 'result_list'

    def get_queryset(self):
        # 検索キーワードに合致するomoideのタイトルがあった場合
        if self.request.GET.get('q', ''):
            # paramsには検索ワードが格納
            params = self.parse_search_params(self.request.GET['q'])
            query = reduce(
                # 検索ワードとomoideのタイトルで合致したものがあればヒットさせる
                # スペースを空けて複数のキーワードで検索したら
                # 検索ワードと一つでも合致するタイトルであれば検索結果に表示する
                # lambda x,y:x | yで設定
                lambda x,y:x | y,
                list(map(lambda z: Q(title__icontains=z), params))
            )
            # 下記でもOK
            # query = reduce(and_, [Q(title__icontains=p) | Q(message__icontains=p) for p in params])
            return OmoideTran.objects.filter(query)
        else:
            return None
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['query'] = self.request.GET.get('q', '')
        return ctx
        
    def parse_search_params(self, words: str):
        # 引数wordsはキー(q)
        # 引数strはバリュー(検索ワード)
        # もし全角スペースがあった場合は半角スペースに変換し
        # スペースで区切られた検索ワードでそれぞれ検索を行うためsplitメソッドを活用
        search_words = words.replace('　', ' ').split()
        return search_words
