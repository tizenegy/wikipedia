from django.shortcuts import render
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    entry = util.get_entry(title)
    if entry == None:
        entry = "The requested page was not found."
    return render(request, "encyclopedia/entry.html", {
        "entry": entry,
        "title": title.capitalize()
    })

