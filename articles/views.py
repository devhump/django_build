from django.shortcuts import render
from articles.forms import ArticleForm

# Create your views here.
def index(request):

    return render(request, "articles/index.html")

def create(request):

    article_form = ArticleForm()

    context = {
        'article_form':article_form,
    }

    return render(request, "articles/create.html", context)