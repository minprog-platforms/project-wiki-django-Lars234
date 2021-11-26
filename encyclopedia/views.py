from django.shortcuts import render

from . import util
import markdown2
import random


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "random": random.choice(util.list_entries())   
    })

def entry(request, entry_name):
    return render(request, "encyclopedia/entry.html", {
        "name": entry_name,
        "content": markdown2.markdown(util.get_entry(entry_name)),
        "entries": util.list_entries(),
        "random": random.choice(util.list_entries())   
    })

def new_page(request):
    if request.method == "POST":
        new_title = request.POST.get('title')
        new_content = request.POST.get('content')

        # make a new md file
        new = open(f"entries/{new_title}.md", "w")
        new.write(new_content)

        ## werkt nog niet ##
        return entry(request, new_title)

    return render(request, "encyclopedia/new_page.html", {
        "entries": util.list_entries(),
        "random": random.choice(util.list_entries())
    })
