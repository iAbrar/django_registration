from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.urls import reverse
from newsapi import NewsApiClient
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Article

def LikeView(request, pk):
    post = get_object_or_404(Article, id = request.POST.get('post_id'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True

    return HttpResponseRedirect(reverse('article-detail', args=[str(pk)]))

def index (request):

    articles = Article.objects.all().prefetch_related('likes')
    likes_list=[]
    for a in articles:
        a.is_liked = (request.user in a.likes.all())
        if a.is_liked:
            likes_list.append(a.title)


    if articles.count() < 5:
        articles = get_articles()

    return render(request, 'news/index.html',context={"articles":articles, "fav":likes_list})

class ArticleListView(ListView):
    model = Article
    template_name = 'news/index.html'
    context_object_name = ['articles','fav']
    ordering = ['-date_posted']

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'news/article_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ArticleDetailView, self).get_context_data()

        stuff= get_object_or_404(Article, id=self.kwargs['pk'])
        liked = False
        articles = Article.objects.all().prefetch_related('likes')
        likes_list=[]
        for a in articles:
            a.is_liked = (self.request.user in a.likes.all())
            if a.is_liked:
                likes_list.append(a.title)
        print(likes_list)
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked= True

        context['fav'] = likes_list
        context['liked'] = liked
        return context


def get_articles():
    newsapi = NewsApiClient(api_key='6abcd3110cc743ebb5b4bf5329c179a2')

    # /v2/top-headlines
    top_headlines = newsapi.get_top_headlines(sources='bbc-news')

    articles = top_headlines['articles']

    for i in articles:
        articel_data = Article(
            title = i['title'],
            description = i['description'],
            date_posted = i['publishedAt'],
            author = i['author'],
            image_url = i['urlToImage'],
            )
        articel_data.save()
        all_articles = Article.objects.all().order_by('-id')

    return all_articles
