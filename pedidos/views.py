from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, redirect, render

from marketplace.models import Produto

from .forms import PedidoForm
from .models import Pedido


@login_required
def criar_pedido(request, produto_id):
    produto = get_object_or_404(
        Produto.objects.select_related("produtor", "produtor__user"),
        id=produto_id,
    )

    if request.user.is_produtor and produto.produtor.user == request.user:
        messages.error(request, "Você não pode criar pedido para o próprio produto.")
        return redirect("marketplace:detalhe_produto", id=produto.id)

    if request.method == "POST":
        form = PedidoForm(request.POST, produto=produto)

        if form.is_valid():
            pedido = form.save(commit=False)
            pedido.comprador = request.user
            pedido.produto = produto
            pedido.save()

            messages.success(request, "Pedido enviado ao produtor.")
            return redirect("pedidos:meus_pedidos")
    else:
        form = PedidoForm(produto=produto)

    return render(
        request,
        "pedidos/form_pedido.html",
        {
            "form": form,
            "produto": produto,
        },
    )


@login_required
def meus_pedidos(request):
    pedidos_comprador = Pedido.objects.filter(comprador=request.user).select_related(
        "produto",
        "produto__produtor",
    )
    pedidos_produtor = Pedido.objects.none()

    if request.user.is_produtor:
        try:
            perfil = request.user.perfil_produtor
            pedidos_produtor = Pedido.objects.filter(produto__produtor=perfil).select_related(
                "comprador",
                "produto",
            )
        except ObjectDoesNotExist:
            pedidos_produtor = Pedido.objects.none()

    return render(
        request,
        "pedidos/meus_pedidos.html",
        {
            "pedidos_comprador": pedidos_comprador,
            "pedidos_produtor": pedidos_produtor,
        },
    )


def _get_pedido_do_produtor(request, pedido_id):
    pedido = get_object_or_404(
        Pedido.objects.select_related("produto", "produto__produtor"),
        id=pedido_id,
    )

    if not request.user.is_produtor or pedido.produto.produtor.user != request.user:
        return None

    return pedido


@login_required
def decidir_pedido(request, pedido_id, acao):
    if request.method != "POST":
        return redirect("pedidos:meus_pedidos")

    pedido = _get_pedido_do_produtor(request, pedido_id)

    if pedido is None:
        messages.error(request, "Você não tem permissão para decidir este pedido.")
        return redirect("pedidos:meus_pedidos")

    if pedido.status != Pedido.StatusPedido.PENDENTE:
        messages.warning(request, "Este pedido já foi decidido.")
        return redirect("pedidos:meus_pedidos")

    if acao == "aceitar":
        pedido.status = Pedido.StatusPedido.ACEITO
        pedido.save(update_fields=["status", "atualizado_em"])
        messages.success(request, "Pedido aceito com sucesso.")
    elif acao == "recusar":
        pedido.status = Pedido.StatusPedido.RECUSADO
        pedido.save(update_fields=["status", "atualizado_em"])
        messages.success(request, "Pedido recusado.")
    else:
        messages.error(request, "Acao invalida para este pedido.")

    return redirect("pedidos:meus_pedidos")


@login_required
def concluir_pedido(request, pedido_id):
    if request.method != "POST":
        return redirect("pedidos:meus_pedidos")

    pedido = _get_pedido_do_produtor(request, pedido_id)

    if pedido is None:
        messages.error(request, "Você não tem permissão para concluir este pedido.")
        return redirect("pedidos:meus_pedidos")

    if pedido.status != Pedido.StatusPedido.ACEITO:
        messages.warning(request, "Apenas pedidos aceitos podem ser concluídos.")
        return redirect("pedidos:meus_pedidos")

    pedido.status = Pedido.StatusPedido.CONCLUIDO
    pedido.save(update_fields=["status", "atualizado_em"])
    messages.success(request, "Pedido concluído.")

    return redirect("pedidos:meus_pedidos")
