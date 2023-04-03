from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.validators import RegexValidator
from random import choice
from . import util


class NewArticleForm(forms.Form):
    title = forms.CharField(
        label="",
        max_length=15,
        validators=[RegexValidator(r"^[a-zA-Z0-9]+$")],
        widget=forms.TextInput(attrs={"class": "form-title", "placeholder": "Title"}),
    )
    article = forms.CharField(
        label="",
        max_length=20000,
        widget=forms.Textarea(
            attrs={"class": "form-article", "placeholder": "Write your article..."},
        ),
    )


def index(request):
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})


def article(request, title):
    content = util.get_entry(title)
    if not content:
        return render(
            request, "encyclopedia/article.html", {"content": content, "title": "404"}
        )
    content = util.to_markdown(content)
    return render(
        request, "encyclopedia/article.html", {"content": content, "title": title}
    )


def search(request):
    articles = util.list_entries()
    query = request.GET.get("q")
    if not query:
        return render(
            request, "encyclopedia/index.html", {"entries": articles, "search": True}
        )
    result = []
    for article in articles:
        if query.lower() == article.lower():
            return HttpResponseRedirect(reverse("article", args=[article]))
        result.append(article) if query.lower() in article.lower() else None
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


def edit(request, title):
    articles = util.list_entries()
    if request.method == "POST":
        edit_article = request.POST.copy()
        edit_article["title"] = title
        form = NewArticleForm(edit_article)
        if form.is_valid():
            if title.lower() in [a.lower() for a in articles]:
                util.save_entry(title, edit_article.get("article"))
                return HttpResponseRedirect(reverse("article", args=[title]))
        form.fields["title"].disabled = True
        return render(
            request,
            "encyclopedia/edit.html",
            {"form": form, "error": "Form is not valid."},
        )
    if title in articles:
        form = NewArticleForm(
            initial={"title": title, "article": util.get_entry(title)}
        )
        form.fields["title"].disabled = True
        return render(request, "encyclopedia/edit.html", {"form": form})
    return render(request, "encyclopedia/edit.html", {"not_found": True})
