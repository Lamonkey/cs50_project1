from django.urls import path

from . import views

app_name="Wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.entryPage, name="entryPage"),
    path("search/", views.search, name="search"),
    path("add/", views.add, name="add"),
    path("edit/<str:entry>",views.edit, name="edit"),
    path("feelLucky/", views.random, name="random")
    
]
