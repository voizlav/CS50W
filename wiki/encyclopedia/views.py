from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from random import choice
from . import util


class NewArticleForm(forms.Form):
    title = forms.CharField(
        label="",
        max_length=15,
        widget=forms.TextInput(attrs={"class": "form-title", "placeholder": "Title"}),
    )
    article = forms.CharField(
        label="",
        max_length=500,
        widget=forms.Textarea(
            attrs={"class": "form-article", "placeholder": "Write your article..."},
        ),
    )


def index(request):
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})


def article(request, title):
    return render(
        request, "encyclopedia/article.html", {"content": util.get_entry(title)}
    )


def search(request):
    articles = util.list_entries()
    query = request.GET.get("q")
    if not query:
        return render(
            request, "encyclopedia/index.html", {"entries": articles, "search": True}
        )
    if query in articles:
        return HttpResponseRedirect(reverse("article", args=[query]))
    result = []
    for article in articles:
        result.append(article) if query in article else None
    return render(
        request, "encyclopedia/index.html", {"entries": result, "search": True}
    )


def random(request):
    articles = util.list_entries()
    random_choice = choice(articles)
    return HttpResponseRedirect(reverse("article", args=[random_choice]))


def new(request):
    if request.method == "POST":
        form = NewArticleForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            article = form.cleaned_data["article"]
            articles = util.list_entries()
            if title.lower() in [a.lower() for a in articles]:
                return render(
                    request,
                    "encyclopedia/new.html",
                    {"form": form, "error": "Title already exists"},
                )
            util.save_entry(title, article)
            return HttpResponseRedirect(reverse("article", args=[title]))
        return render(request, "encyclopedia/new.html", {"form": form})
    return render(request, "encyclopedia/new.html", {"form": NewArticleForm()})
