from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry_name>", views.entry, name="entry"),
    path("wiki/<str:entry_name>/edit", views.edit, name="edit"),
    path("new_page", views.new_page, name="new_page"),
    path("search", views.search, name="search"),
    path("search/<str:query>", views.search, name="search")
]
