from django.shortcuts import render, redirect, get_object_or_404
from core.models import Contribute, Sponsor, New
from django.core.paginator import Paginator
from django.contrib import auth, messages

# Create your views here.
def index(request):

    return render(
        request,
        "pages/index.html",
    )


def edicoes_passadas(request):
    return render(request, "pages/passadas.html")


def realizacao(request):
    contributes = Contribute.objects.all().order_by("id")
    return render(request, "pages/realicacao.html", {"contributes": contributes})


def patrocinadores(request):
    patrocinadores = Sponsor.objects.all()
    return render(
        request, "pages/patrocinadores.html", {"patrocinadores": patrocinadores}
    )


def noticias(request):
    if request.is_ajax():
        ...
    else:
        ultimas = New.objects.all().order_by("-posted_in")[:6]

        noticias = New.objects.all().order_by("id")

        if "order" in request.GET:
            ...
        else:
            noticias.order_by("-posted_in")

        paginator = Paginator(noticias, 30)
        page_number = 1
        if "page" in request.GET:
            page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        dados = {
            "ultimas": ultimas,
            "noticias": page_obj,
        }

        return render(request, "pages/noticias.html", dados)


def noticia(request, id):
    if not New.objects.filter(id=id).exists():
        messages.success(request, "Postagem não encontrada.")
        return redirect("index")

    new = New.objects.filter(id=id).get()

    if new.visibility == "A":
        if request.user.is_anonymous:
            messages.success(
                request, "Você não tem autorização para acessar esta postagem."
            )
            return redirect("login")
        if new.poster_id != request.user.id:
            messages.success(
                request, "Você não tem autorização para acessar esta postagem."
            )
            return redirect("index")

    new.views = new.views + 1
    new.save()

    return render(request, "pages/noticia.html", {"new": new})
