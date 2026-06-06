from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from pedidos.models import Pedido

from .forms import AvaliacaoForm
from .models import Avaliacao


@login_required
def avaliar_pedido(request, pedido_id):
    pedido = get_object_or_404(
        Pedido.objects.select_related("comprador", "produto", "produto__produtor"),
        id=pedido_id,
        comprador=request.user,
    )

    if pedido.status != Pedido.StatusPedido.CONCLUIDO:
        messages.error(request, "Apenas pedidos concluidos podem ser avaliados.")
        return redirect("pedidos:meus_pedidos")

    if hasattr(pedido, "avaliacao"):
        messages.info(request, "Este pedido ja foi avaliado.")
        return redirect("pedidos:meus_pedidos")

    if request.method == "POST":
        form = AvaliacaoForm(request.POST)

        if form.is_valid():
            avaliacao = form.save(commit=False)
            avaliacao.pedido = pedido
            avaliacao.comprador = request.user
            avaliacao.save()

            messages.success(request, "Avaliacao registrada com sucesso.")
            return redirect("pedidos:meus_pedidos")
    else:
        form = AvaliacaoForm()

    return render(
        request,
        "avaliacoes/form_avaliacao.html",
        {
            "form": form,
            "pedido": pedido,
        },
    )
