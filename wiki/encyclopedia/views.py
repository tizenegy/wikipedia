from django.shortcuts import render
from . import util
from django import forms
import random

class SearchForm(forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder':'Search Encyclopedia'}))

class NewEntryForm(forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder':'Enter title'}))
    md_text = forms.CharField(label="", widget=forms.Textarea(
        attrs={'placeholder':'Enter text in Markdown, for example:\n\n# This is a header\n1. First ordered list item\n2. Another item\n⋅⋅* Unordered sub-list.\n\nFor more go to:\nhttps://github.com/adam-p/markdown-here'}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": SearchForm()
    })

def new_entry(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data["md_text"]
            title = form.cleaned_data["title"]
            entry = util.get_entry(title)
            if entry is None:
                util.save_entry(title, text)
                return render(request, "encyclopedia/entry.html", {
                    "entry": util.get_entry(title),
                    "title": title.capitalize(),
                    "form": SearchForm()
                })
            else:
                return render(request, "encyclopedia/new_entry.html", {
                    "form": SearchForm(),
                    "entry_form": NewEntryForm(),
                    "message": "Article already exists."
                })

    return render(request, "encyclopedia/new_entry.html", {
        "form": SearchForm(),
        "entry_form": NewEntryForm()
    })

def entry(request, title):
    entry = util.get_entry(title)
    if entry == None:
        entry = "The requested page was not found."
    return render(request, "encyclopedia/entry.html", {
        "entry": entry,
        "title": title,
        "form": SearchForm()
    })

def edit(request, title):
    entry = util.get_entry(title)
    if entry == None:
        entry = "The requested page was not found."
    return render(request, "encyclopedia/edit.html", {
        "entry": entry,
        "title": title,
        "form": SearchForm()
    })

def get_random(request):
    title = random.choice(util.list_entries())
    entry = util.get_entry(title)
    return render(request, "encyclopedia/entry.html", {
        "entry": entry,
        "title": title,
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

