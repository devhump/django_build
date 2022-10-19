from django.shortcuts import redirect, render
from articles.forms import ArticleForm
from .models import Article
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):

    articles = Article.objects.order_by("-pk")

    context = {
        "articles": articles,
    }

    return render(request, "articles/index.html", context)


@login_required
def create(request):

    if request.method == "POST":
        article_form = ArticleForm(request.POST)
        if article_form.is_valid():
            article_form.save()
            return redirect(request.GET.get("next") or "articles:index")
    else:
        article_form = ArticleForm()
    context = {
        "article_form": article_form,
    }

    return render(request, "articles/form.html", context)


def detail(request, article_pk):

    article = Article.objects.get(pk=article_pk)

    context = {
        "article": article,
    }

    return render(request, "articles/detail.html", context)


@login_required
def update(request, article_pk):

    article = Article.objects.get(pk=article_pk)

    if request.method == "POST":
        article_form = ArticleForm(request.POST, instance=article)
        if article_form.is_valid():  # 유효성 검사
            article_form.save()  # DB 저장 로직
            return redirect("articles:detail", article.pk)
    else:
        article_form = ArticleForm(instance=article)
    context = {
        "article_form": article_form,
    }

    return render(request, "articles/form.html", context)


@login_required
def delete(request, article_pk):

    article = Article.objects.get(pk=article_pk)

    article.delete()

    return redirect("articles:index")
