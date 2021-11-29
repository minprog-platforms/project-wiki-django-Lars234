from django.core.exceptions import ValidationError
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django import forms

from . import util
import random


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
    
    file = open(f"entries/{entry_name}.md").read()

    return render(request, "encyclopedia/edit.html", {
        "name": entry_name,
        "content": file,
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

        try:
            new_content = request.POST.get('content')
            new_title = request.POST.get("name")
        except Exception:
            new_content =  ""
            new_title = ""
 
        # check if the title is unique and not ""
        if new_title in util.list_entries() and new_title:
            return render(request, "encyclopedia/new_page.html", {
                "entries": util.list_entries(),
                "random": random.choice(util.list_entries()),
                "form": NewPageForm(),
                "content": new_content,
                "error": True
            })   

        # make a new md file
        new = open(f"entries/{new_title}.md", "w")
        new.write(new_content)

        return HttpResponseRedirect(f"/wiki/{new_title}")

    # is run if method is get
    return render(request, "encyclopedia/new_page.html", {
        "entries": util.list_entries(),
        "random": random.choice(util.list_entries()),
        "form": NewPageForm(),
        "content": "",
        "error": False
    })

def is_unique_title(name):
    if name in "".join(util.list_entries()):
        raise ValidationError(
            ('%(new_title)s is not an even number'),
            params={'name': name},
        )

def md_to_html(file):
    with open(f"entries/{file}.md", "r") as md_file:
        html = []
        sentences = md_file.read().split("\n")
        print(sentences)
        
        for line in sentences:
            # first check for an empty line
            if not line:
                continue

            # check for special chars and count them:
            header = line.count("#")
            line = line.replace("#", "")
            is_list = False

            new_line = ""

            # add a header at the front
            if header > 0:
                new_line += f"<h{header}>"
            # if it is a list
            elif "* " in line[0:1]:
                is_list = True
                new_line += "<li>"
                line = line.replace("* ", "")
            else:
                new_line += "<p>"
            
            # search for links
            while "[" in line and "]" in line and "(" in line and ")" in line:
                link_name = line.split("[", 1)[1].split("]", 1)[0]
                link_path = line.split("(", 1)[1].split(")", 1)[0]
                
                # add this link
                line = line.split("[", 1)
                line[1] = line[1].split(")", 1)[1]
                line = f"<a href={link_path}>{link_name}</a>".join(line) 

            # get boldfaces
            while "**" in line:
                try:
                    bold_line = line.split("**", 2)
                    line = f"{bold_line[0]}<b>{bold_line[1]}</b>{bold_line[2]}" 
                except Exception:
                    break           
            
            new_line += line

            # add a header at the back
            if header > 0:
                new_line += f"</h{header}>"
            elif is_list:
                new_line += "</li>"
            else:
                new_line += f"</p>"
            
            html.append(new_line)
    
    output = "".join(html)

    # if there are list items, put <ul> around it
    if "<li>" in output:
        start = output.split("<li>", 1)[0]
        middle = output.split("<li>", 1)[1].rsplit("</li>", 1)[0]
        end = output.split("<li>", 1)[1].rsplit("</li>", 1)[1]

        output = f"{start}<ul><li>{middle}</li></ul>{end}"    

    return output

class NewPageForm(forms.Form):
    name = forms.CharField()
