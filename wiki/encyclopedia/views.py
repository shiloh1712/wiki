from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
import markdown2
import random

from . import util

class SearchForm(forms.Form):
    key = forms.CharField(label="Search Encyclopedia")

class NewPageForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea(attrs={"row":5, "cols":10}))

class EditForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea(attrs={"row":5, "cols":10}))
     
def title_existed(title):
    return title.upper() in map(lambda x: x.upper(), util.list_entries())

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(), 
        "search_form": SearchForm(),
        "heading": "All Pages"
    })

def get_page(request, title = None):
    search_form = SearchForm()
    #When using search form
    if request.method == "POST":
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            #get search key term
            title = search_form.cleaned_data["key"]
            #if exact title not found then output a search results page
            #otherwise render the page if search term matches correct title
            if not title_existed(title):
                search_results = list(filter(lambda x: title.upper() in x.upper(), util.list_entries()))
                return render(request, "encyclopedia/index.html", {
                        "entries": search_results, 
                        "search_form": search_form,
                        "heading": f"Search Results: {title}"
    })

    #if input url is an invalid title
    if not title_existed(title):
        return render(request, "encyclopedia/not_found.html", {
            "title": title, "search_form": search_form
        })
    #when using direct url or searched title is available
    content = markdown2.markdown(util.get_entry(title))
    return render(request, "encyclopedia/entry.html", {
        "title": title, "content": content, "search_form": search_form
    })


def new_page(request):
    error_msg = None
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            if not title_existed(title):
                util.save_entry(title, form.cleaned_data["content"])
                return get_page(request, title)
            #if entry already existed
            else:
                error_msg = "This entry is already in the encyclopedia"
    else:
        form = NewPageForm()
    return render(request, "encyclopedia/create.html", {
            "title": "New entry", "new_page_form": form, "error_msg": error_msg, "search_form": SearchForm()
    })
    
def edit_entry(request, title):
    
    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            new_content = form.cleaned_data["content"]
            util.save_entry(title, new_content)
            return get_page(request, title)
    #initialize entry data
    form = EditForm()
    form.fields["title"].initial = title
    form.fields["content"].initial = util.get_entry(title)
    
    return render(request, "encyclopedia/edit.html", {
        "title": title, "form": form, "search_form": SearchForm()
    })

def random_page(request):
    return get_page(request, title = random.choice(util.list_entries()))