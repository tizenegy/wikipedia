from django.shortcuts import render
from . import util
from django import forms

class SearchForm(forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder':'Search Encyclopedia'}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": SearchForm()
    })

def entry(request, title):
    entry = util.get_entry(title)
    if entry == None:
        entry = "The requested page was not found."
    return render(request, "encyclopedia/entry.html", {
        "entry": entry,
        "title": title.capitalize(),
        "form": SearchForm()
    })

def search(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            entry = util.get_entry(title)
            if entry == None:
                entries = util.list_entries()
                similar_entries = filter(lambda x: title.upper() in x.upper(), entries)
                return render(request, "encyclopedia/search.html", {
                "entries": similar_entries,
                "form": SearchForm()
            })
            else:
                return render(request, "encyclopedia/entry.html", {
                    "entry": entry,
                    "title": title.capitalize(),
                    "form": SearchForm()
                })
    else:
        return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": SearchForm()
    })

