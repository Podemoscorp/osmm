from django.urls import path
from core import views

urlpatterns = [
    path("", views.index, name="index"),
    path("sobre-nos/", views.realizacao, name="sobre-nos"),
    path("patrocinadores/", views.patrocinadores, name="patrocinadores"),
    path("edicoes-passadas/", views.edicoes_passadas, name="edicoes-passadas"),
    path("noticias/", views.noticias, name="noticias"),
    path("noticia/<int:id>/", views.noticia, name="noticia"),
]