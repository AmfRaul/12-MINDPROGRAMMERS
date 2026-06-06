from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from avaliacoes.models import Avaliacao
from marketplace.models import CategoriaProduto, Produto
from produtores.models import PerfilProdutor

from .models import Pedido


class PedidoFluxoTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.comprador = User.objects.create_user(
            username="comprador",
            email="comprador@example.com",
            password="senha-forte-123",
            tipo_conta=User.TipoConta.COMPRADOR,
        )
        self.produtor_user = User.objects.create_user(
            username="produtor",
            email="produtor@example.com",
            password="senha-forte-123",
            tipo_conta=User.TipoConta.PRODUTOR,
        )
        self.outro_produtor_user = User.objects.create_user(
            username="outroprodutor",
            email="outro@example.com",
            password="senha-forte-123",
            tipo_conta=User.TipoConta.PRODUTOR,
        )
        self.perfil = PerfilProdutor.objects.create(
            user=self.produtor_user,
            nome_negocio="Sitio Verde",
            cidade="Campinas",
            estado="SP",
            tipo_producao="Hortalicas",
        )
        self.outro_perfil = PerfilProdutor.objects.create(
            user=self.outro_produtor_user,
            nome_negocio="Sitio Azul",
            cidade="Limeira",
            estado="SP",
            tipo_producao="Frutas",
        )
        self.categoria = CategoriaProduto.objects.create(nome="Verduras")
        self.produto = Produto.objects.create(
            produtor=self.perfil,
            categoria=self.categoria,
            nome="Alface",
            descricao="Alface fresca",
            quantidade_disponivel="100.00",
            unidade_medida="kg",
            preco="5.50",
            regiao="Campinas",
            data_disponibilidade=date.today(),
        )

    def test_comprador_cria_pedido(self):
        self.client.login(username="comprador", password="senha-forte-123")

        response = self.client.post(
            reverse("pedidos:criar_pedido", args=[self.produto.id]),
            {
                "quantidade": "10.00",
                "mensagem": "Tenho interesse.",
            },
        )

        self.assertRedirects(response, reverse("pedidos:meus_pedidos"))
        self.assertEqual(Pedido.objects.count(), 1)
        self.assertEqual(Pedido.objects.first().comprador, self.comprador)

    def test_produtor_nao_cria_pedido_para_proprio_produto(self):
        self.client.login(username="produtor", password="senha-forte-123")

        response = self.client.post(
            reverse("pedidos:criar_pedido", args=[self.produto.id]),
            {
                "quantidade": "10.00",
                "mensagem": "",
            },
        )

        self.assertRedirects(
            response,
            reverse("marketplace:detalhe_produto", args=[self.produto.id]),
        )
        self.assertEqual(Pedido.objects.count(), 0)

    def test_pedido_nao_permite_quantidade_maior_que_disponivel(self):
        self.client.login(username="comprador", password="senha-forte-123")

        response = self.client.post(
            reverse("pedidos:criar_pedido", args=[self.produto.id]),
            {
                "quantidade": "999.00",
                "mensagem": "Quero comprar tudo.",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "maior que a disponível")
        self.assertEqual(Pedido.objects.count(), 0)

    def test_produtor_dono_aceita_conclui_e_comprador_avalia(self):
        pedido = Pedido.objects.create(
            comprador=self.comprador,
            produto=self.produto,
            quantidade="8.00",
        )

        self.client.login(username="produtor", password="senha-forte-123")
        response = self.client.post(
            reverse("pedidos:decidir_pedido", args=[pedido.id, "aceitar"]),
        )
        self.assertRedirects(response, reverse("pedidos:meus_pedidos"))
        pedido.refresh_from_db()
        self.assertEqual(pedido.status, Pedido.StatusPedido.ACEITO)

        response = self.client.post(
            reverse("pedidos:concluir_pedido", args=[pedido.id]),
        )
        self.assertRedirects(response, reverse("pedidos:meus_pedidos"))
        pedido.refresh_from_db()
        self.assertEqual(pedido.status, Pedido.StatusPedido.CONCLUIDO)

        self.client.login(username="comprador", password="senha-forte-123")
        response = self.client.post(
            reverse("avaliacoes:avaliar_pedido", args=[pedido.id]),
            {
                "nota": "5",
                "comentario": "Excelente produto.",
            },
        )
        self.assertRedirects(response, reverse("pedidos:meus_pedidos"))
        self.assertEqual(Avaliacao.objects.count(), 1)

    def test_produtor_dono_recusa_pedido_pendente(self):
        pedido = Pedido.objects.create(
            comprador=self.comprador,
            produto=self.produto,
            quantidade="8.00",
        )

        self.client.login(username="produtor", password="senha-forte-123")
        response = self.client.post(
            reverse("pedidos:decidir_pedido", args=[pedido.id, "recusar"]),
        )

        self.assertRedirects(response, reverse("pedidos:meus_pedidos"))
        pedido.refresh_from_db()
        self.assertEqual(pedido.status, Pedido.StatusPedido.RECUSADO)

    def test_apenas_dono_edita_produto(self):
        self.client.login(username="outroprodutor", password="senha-forte-123")
        response = self.client.post(
            reverse("marketplace:editar_produto", args=[self.produto.id]),
            {
                "categoria": self.categoria.id,
                "nome": "Alface alterada",
                "descricao": "Descricao",
                "quantidade_disponivel": "90.00",
                "unidade_medida": "kg",
                "preco": "6.00",
                "regiao": "Campinas",
                "data_disponibilidade": date.today().isoformat(),
                "data_entrega_estimada": "",
                "status": Produto.StatusProduto.DISPONIVEL,
            },
        )
        self.assertRedirects(response, reverse("marketplace:lista_produtos"))
        self.produto.refresh_from_db()
        self.assertEqual(self.produto.nome, "Alface")

        self.client.login(username="produtor", password="senha-forte-123")
        response = self.client.post(
            reverse("marketplace:editar_produto", args=[self.produto.id]),
            {
                "categoria": self.categoria.id,
                "nome": "Alface organica",
                "descricao": "Descricao atualizada",
                "quantidade_disponivel": "90.00",
                "unidade_medida": "kg",
                "preco": "6.00",
                "regiao": "Campinas",
                "data_disponibilidade": date.today().isoformat(),
                "data_entrega_estimada": "",
                "status": Produto.StatusProduto.DISPONIVEL,
            },
        )
        self.assertRedirects(
            response,
            reverse("marketplace:detalhe_produto", args=[self.produto.id]),
        )
        self.produto.refresh_from_db()
        self.assertEqual(self.produto.nome, "Alface organica")

# Create your tests here.
