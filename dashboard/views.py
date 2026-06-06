from django.shortcuts import render

from marketplace.models import Produto
from pedidos.models import Pedido
from produtores.models import PerfilProdutor


def home(request):
    context = {
        "produtos_recentes": Produto.objects.select_related("categoria", "produtor")[:6],
        "total_produtos": Produto.objects.count(),
    }

    if request.user.is_authenticated:
        context["pedidos_comprador"] = Pedido.objects.filter(
            comprador=request.user,
        ).select_related("produto")[:5]

        if request.user.is_produtor:
            try:
                perfil = request.user.perfil_produtor
            except PerfilProdutor.DoesNotExist:
                perfil = None

            context["perfil_produtor"] = perfil

            if perfil:
                produtos_produtor = Produto.objects.filter(produtor=perfil)
                pedidos_recebidos = Pedido.objects.filter(
                    produto__produtor=perfil,
                ).select_related("comprador", "produto")

                context.update(
                    {
                        "total_meus_produtos": produtos_produtor.count(),
                        "pedidos_pendentes": pedidos_recebidos.filter(
                            status=Pedido.StatusPedido.PENDENTE,
                        ).count(),
                        "pedidos_recebidos": pedidos_recebidos[:5],
                    }
                )

    return render(request, "dashboard/home.html", context)
