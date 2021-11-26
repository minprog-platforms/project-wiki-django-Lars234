from django.core import validators
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.core.validators import RegexValidator
from django import forms

from . import util
import markdown2
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
            "content": markdown2.markdown(util.get_entry(entry_name)),
            "entries": util.list_entries(),
            "random": random.choice(util.list_entries())  
        })
    else:
        return render(request, "encyclopedia/error.html", {
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