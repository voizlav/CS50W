from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from . import util


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
        return render(request, "encyclopedia/index.html", {"entries": articles})
    if query in articles:
        return HttpResponseRedirect(reverse("article", args=[query]))
    result = []
    for article in articles:
        result.append(article) if query in article else None
    return render(request, "encyclopedia/index.html", {"entries": result})
