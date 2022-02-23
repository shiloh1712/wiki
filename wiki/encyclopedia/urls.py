from django.urls import path

from . import views

app_name = "wiki"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.get_page, name="entries"),
    path("search", views.get_page, name="search"),
    path("create", views.new_page, name="create"),
    path("edit/<str:title>", views.edit_entry, name="edit"),
    path("random", views.random_page, name="random")
]
