from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})


def article(request, title):
    return render(
        request, "encyclopedia/article.html", {"content": util.get_entry(title)}
    )
