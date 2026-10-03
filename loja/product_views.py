from django.shortcuts import get_object_or_404, render

from .models import Cupcake


def detalhe_cupcake(request, cupcake_id):
    cupcake = get_object_or_404(
        Cupcake.objects.prefetch_related(
            "restricoes"
        ),
        id=cupcake_id,
        ativo=True
    )

    contexto = {
        "cupcake": cupcake,
    }

    return render(
        request,
        "loja/detalhe_cupcake.html",
        contexto
    )