from logging import exception
from django.core import validators
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.core.validators import RegexValidator
from django import forms

from . import util
import random
import re


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "random": random.choice(util.list_entries())   
    })

def entry(request, entry_name):
    # if valid, go to the requested page
    if entry_name in util.list_entries():
        return render(request, "encyclopedia/entry.html", {
            "name": entry_name,
            "content": md_to_html(entry_name),
            "entries": util.list_entries(),
            "random": random.choice(util.list_entries())  
        })
    else:
        return render(request, "encyclopedia/error.html", {
        "entries": util.list_entries(),
        "random": random.choice(util.list_entries())   
    })

def edit(request, entry_name):
    # when posted update the page and go there
    if request.method == "POST":
        new_content = request.POST.get('content')

        # overwrite a md file
        file = open(f"entries/{entry_name}.md", "w")
        file.write(new_content)

        return HttpResponseRedirect(f"/wiki/{entry_name}")

    return render(request, "encyclopedia/edit.html", {
        "name": entry_name,
        "content": md_to_html(entry_name),
        "random": random.choice(util.list_entries())
        })

def search(request, query=""):
    # searching is possible via: 
    # http//.../search/query
    # search bar

    # if posted, update the query with the form
    if request.method == "POST":
        query = request.POST.get("q")

    # if the query matches a page, go there:
    if query in util.list_entries():
        return HttpResponseRedirect(f"/wiki/{query}")

    # if it does not match, show a possible list
    else:
        return render(request, "encyclopedia/search.html", {
            "query": query,
            "entries": util.list_entries(),
            "random": random.choice(util.list_entries())
        })

def new_page(request):
    if request.method == "POST":
        new_title_form = NewPageForm(request.POST)
        unique_title = RegexValidator("".join(util.list_entries()), "The title must be unique", inverse_match=False)
        print("".join(util.list_entries()))
        if new_title_form.is_valid():
            new_title = new_title_form.cleaned_data["name"]
        else:
            # if client side validation failed, go to error page
            return HttpResponseRedirect("/error")

        new_content = request.POST.get('content')

        # make a new md file
        new = open(f"entries/{new_title}.md", "w")
        new.write(new_content)

        return HttpResponseRedirect(f"/wiki/{new_title}")

    return render(request, "encyclopedia/new_page.html", {
        "entries": util.list_entries(),
        "random": random.choice(util.list_entries()),
        "form": NewPageForm()
    })

unique_title = RegexValidator("".join(util.list_entries()), "The title must be unique", inverse_match=False)



class NewPageForm(forms.Form):
    #not_allowed = "".join(util.list_entries())
    #name = forms.RegexField(not_allowed, validators=[unique_title], required=True)
    name = forms.CharField(required=True, validators=[unique_title])

def md_to_html(file):
    with open(f"entries/{file}.md", "r") as md_file:
        html = ""
        for line in md_file.readlines():
            # check for special chars and count them:
            header = line.count("#")
            line = line.replace("#", "")

            new_line = ""

            # add a header at the front
            if header > 0:
                new_line += f"<h{header}>"
            
            # search for links
            try:
                link_text = re.search(r".*?\[(.*)].*", line).group(1)
                link_path = re.search(r"(.*?)", line).group(1)
                print(link_path)
                print(link_text)
            except Exception:
                pass

            for link in re.findall(r'(?<=\[).*?(?=\])', line):
                print(link)
            
            
            new_line += line

            # add a header at the back
            if header > 0:
                new_line += f"</h{header}>"
            
            html += new_line + "\n"
        
    return html


                


print(md_to_html("Python"))