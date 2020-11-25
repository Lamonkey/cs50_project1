from django.shortcuts import render
from django.http import HttpResponse
from markdown2 import Markdown
from django import forms
from . import util

class NewWikiPage(forms.Form):
      title = forms.CharField(label="title")
      content = forms.CharField(widget=forms.Textarea)
      
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entryPage(request,entry):
    markdowner = Markdown()
    if entry in util.list_entries():
        return(HttpResponse(markdowner.convert(util.get_entry(entry))))
    else:
        return (HttpResponse("page doesn't exist"))

def newPage(request):
    return HttpResponse("create a new page")

def search(request):
    markdowner = Markdown()
    entry = request.POST.get("entry", "")
    search_result = []
    if entry in util.list_entries():
        return(HttpResponse(markdowner.convert(util.get_entry(entry))))
    else:
        for iterator in util.list_entries():
            if(entry.lower() in iterator.lower()):
                search_result.append(iterator)
        return render(request,"encyclopedia/searchResult.html",{
            "entries":search_result
        })

# def add(request):
#     return render(request,"encyclopedia/addPage.html",{"form":NewWikiPage()
#     })

def add(request):
    if request.method == "POST":
       form = NewWikiPage(request.POST)
       if form.is_valid():
           title = form.cleaned_data["title"]
           content = form.cleaned_data["content"]
        #check if title duplicated
           if title in util.list_entries():
               return HttpResponse("The title duplicated with an existing wiki page")
           else:
                util.save_entry(title,content)
                return entryPage(request,title)
    return render(request,"encyclopedia/addPage.html",{"form":NewWikiPage()})
           #save the wikipage

def edit(request,entry):
    field = {"title":entry,"content":util.get_entry(entry)}
    form = NewWikiPage(field)
    
    if request.method == "POST":
        form = NewWikiPage(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            title = form.cleaned_data["title"]
            util.save_entry(title=title,content=content)
            return entryPage(request,entry)
    return render(request,"encyclopedia/editPage.html",{"form":form, "entry":entry})
    #return render(request,"encyclopedia/editPage.html")
    #return HttpResponse(entry)
            
def random(request):
    import random
    randomNum = random.randint(0, len(util.list_entries())-1)
    #randomNum = random.randint(0,2)
    #random.seed()
    #randomNum = random.randRange(start=0,stop=len(util.list_entries))
    return entryPage(request,util.list_entries()[randomNum])