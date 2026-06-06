import os
import shutil
import urllib.request
from datetime import date, timedelta
from decimal import Decimal

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.conf import settings  # noqa: E402
from django.contrib.auth import get_user_model  # noqa: E402
from PIL import Image  # noqa: E402

from avaliacoes.models import Avaliacao  # noqa: E402
from marketplace.models import CategoriaProduto, Produto  # noqa: E402
from pedidos.models import Pedido  # noqa: E402
from produtores.models import PerfilProdutor  # noqa: E402


PASSWORD = "senha12345"
SEED_IMAGE_DIR = "marketplace/produtos/seed"

PRODUCT_IMAGE_SOURCES = {
    "alface": {
        "filename": "alface-crespa.jpg",
        "url": "https://upload.wikimedia.org/wikipedia/commons/3/3c/Lettuce_%284988502522%29.jpg",
    },
    "tomate": {
        "filename": "tomate-italiano.jpg",
        "url": "https://upload.wikimedia.org/wikipedia/commons/3/3c/Tomato_%281%29.jpg",
    },
    "morango": {
        "filename": "morango-selecionado.jpg",
        "url": "https://upload.wikimedia.org/wikipedia/commons/e/e1/Strawberries.jpg",
    },
    "queijo": {
        "filename": "queijo-minas-artesanal.jpg",
        "url": "https://upload.wikimedia.org/wikipedia/commons/3/32/Queijo_Minas_Frescal.JPG",
    },
}


def reset_data():
    Avaliacao.objects.all().delete()
    Pedido.objects.all().delete()
    Produto.objects.all().delete()
    CategoriaProduto.objects.all().delete()
    PerfilProdutor.objects.all().delete()
    get_user_model().objects.all().delete()

    seed_path = settings.MEDIA_ROOT / SEED_IMAGE_DIR
    if seed_path.exists():
        for item in seed_path.glob("*"):
            if item.is_file():
                item.unlink(missing_ok=True)
        shutil.rmtree(seed_path, ignore_errors=True)


def create_user(username, email, tipo_conta, telefone="", is_staff=False, is_superuser=False):
    User = get_user_model()
    user = User.objects.create_user(
        username=username,
        email=email,
        password=PASSWORD,
        tipo_conta=tipo_conta,
        telefone=telefone,
    )
    user.is_staff = is_staff
    user.is_superuser = is_superuser
    user.save()
    return user


def download_real_product_image(key, source):
    seed_path = settings.MEDIA_ROOT / SEED_IMAGE_DIR
    seed_path.mkdir(parents=True, exist_ok=True)

    output_path = seed_path / source["filename"]
    request = urllib.request.Request(
        source["url"],
        headers={"User-Agent": "FieldReach seed script/1.0"},
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            with open(output_path, "wb") as image_file:
                image_file.write(response.read())
    except Exception as exc:
        raise RuntimeError(
            f"Nao foi possivel baixar a foto real do produto '{key}'."
        ) from exc

    normalize_product_image(output_path)
    return f"{SEED_IMAGE_DIR}/{source['filename']}"


def normalize_product_image(path):
    target_width, target_height = 1200, 760

    with Image.open(path) as image:
        image = image.convert("RGB")
        image_ratio = image.width / image.height
        target_ratio = target_width / target_height

        if image_ratio > target_ratio:
            new_width = int(image.height * target_ratio)
            left = (image.width - new_width) // 2
            image = image.crop((left, 0, left + new_width, image.height))
        else:
            new_height = int(image.width / target_ratio)
            top = (image.height - new_height) // 2
            image = image.crop((0, top, image.width, top + new_height))

        image = image.resize((target_width, target_height), Image.Resampling.LANCZOS)
        image.save(path, "JPEG", quality=88, optimize=True)


def create_seed_images():
    return {
        key: download_real_product_image(key, source)
        for key, source in PRODUCT_IMAGE_SOURCES.items()
    }


def create_data():
    User = get_user_model()

    admin = create_user(
        username="admin",
        email="admin@fieldreach.com",
        tipo_conta=User.TipoConta.COMPRADOR,
        telefone="11999990000",
        is_staff=True,
        is_superuser=True,
    )

    comprador_ana = create_user(
        username="ana_compradora",
        email="ana@compradora.com",
        tipo_conta=User.TipoConta.COMPRADOR,
        telefone="11988887777",
    )
    comprador_bruno = create_user(
        username="bruno_comprador",
        email="bruno@comprador.com",
        tipo_conta=User.TipoConta.COMPRADOR,
        telefone="21977776666",
    )

    produtor_joao = create_user(
        username="joao_produtor",
        email="joao@produtor.com",
        tipo_conta=User.TipoConta.PRODUTOR,
        telefone="19966665555",
    )
    produtor_maria = create_user(
        username="maria_produtora",
        email="maria@produtora.com",
        tipo_conta=User.TipoConta.PRODUTOR,
        telefone="31955554444",
    )

    perfil_joao = PerfilProdutor.objects.create(
        user=produtor_joao,
        nome_negocio="Sitio Boa Terra",
        descricao="Producao familiar de hortalicas frescas.",
        cidade="Campinas",
        estado="SP",
        tipo_producao="Hortalicas",
        capacidade_producao="800 kg por semana",
        contato_comercial="WhatsApp: (19) 96666-5555",
    )
    perfil_maria = PerfilProdutor.objects.create(
        user=produtor_maria,
        nome_negocio="Fazenda Vale Verde",
        descricao="Frutas, leite e derivados para entregas recorrentes.",
        cidade="Pouso Alegre",
        estado="MG",
        tipo_producao="Frutas e leite",
        capacidade_producao="2 toneladas por mes",
        contato_comercial="comercial@valeverde.com",
    )

    verduras = CategoriaProduto.objects.create(
        nome="Verduras",
        descricao="Folhas e hortalicas frescas.",
    )
    frutas = CategoriaProduto.objects.create(
        nome="Frutas",
        descricao="Frutas selecionadas para compra direta.",
    )
    laticinios = CategoriaProduto.objects.create(
        nome="Laticinios",
        descricao="Leite e derivados de produtores locais.",
    )

    hoje = date.today()
    imagens = create_seed_images()

    alface = Produto.objects.create(
        produtor=perfil_joao,
        categoria=verduras,
        nome="Alface crespa",
        descricao="Alface crespa fresca, colhida sob demanda.",
        quantidade_disponivel=Decimal("120.00"),
        unidade_medida="kg",
        preco=Decimal("5.50"),
        regiao="Campinas - SP",
        data_disponibilidade=hoje,
        data_entrega_estimada=hoje + timedelta(days=2),
        imagem=imagens["alface"],
    )
    tomate = Produto.objects.create(
        produtor=perfil_joao,
        categoria=verduras,
        nome="Tomate italiano",
        descricao="Tomates maduros para restaurantes e mercados.",
        quantidade_disponivel=Decimal("300.00"),
        unidade_medida="kg",
        preco=Decimal("8.90"),
        regiao="Campinas - SP",
        data_disponibilidade=hoje + timedelta(days=1),
        data_entrega_estimada=hoje + timedelta(days=3),
        status=Produto.StatusProduto.SOB_ENCOMENDA,
        imagem=imagens["tomate"],
    )
    morango = Produto.objects.create(
        produtor=perfil_maria,
        categoria=frutas,
        nome="Morango selecionado",
        descricao="Morangos doces, embalados em caixas de 1 kg.",
        quantidade_disponivel=Decimal("80.00"),
        unidade_medida="caixa",
        preco=Decimal("18.00"),
        regiao="Pouso Alegre - MG",
        data_disponibilidade=hoje,
        data_entrega_estimada=hoje + timedelta(days=4),
        imagem=imagens["morango"],
    )
    queijo = Produto.objects.create(
        produtor=perfil_maria,
        categoria=laticinios,
        nome="Queijo minas artesanal",
        descricao="Queijo minas produzido artesanalmente.",
        quantidade_disponivel=Decimal("45.00"),
        unidade_medida="unidade",
        preco=Decimal("32.00"),
        regiao="Pouso Alegre - MG",
        data_disponibilidade=hoje + timedelta(days=2),
        data_entrega_estimada=hoje + timedelta(days=5),
        imagem=imagens["queijo"],
    )

    pedido_concluido = Pedido.objects.create(
        comprador=comprador_ana,
        produto=alface,
        quantidade=Decimal("20.00"),
        mensagem="Preciso para entrega semanal.",
        status=Pedido.StatusPedido.CONCLUIDO,
    )
    Pedido.objects.create(
        comprador=comprador_bruno,
        produto=tomate,
        quantidade=Decimal("50.00"),
        mensagem="Gostaria de negociar recorrencia.",
        status=Pedido.StatusPedido.PENDENTE,
    )
    Pedido.objects.create(
        comprador=comprador_ana,
        produto=queijo,
        quantidade=Decimal("10.00"),
        mensagem="Pedido para emporio local.",
        status=Pedido.StatusPedido.ACEITO,
    )

    Avaliacao.objects.create(
        pedido=pedido_concluido,
        comprador=comprador_ana,
        nota=5,
        comentario="Produto muito fresco e entrega combinada corretamente.",
    )

    return {
        "admin": admin,
        "compradores": [comprador_ana, comprador_bruno],
        "produtores": [produtor_joao, produtor_maria],
        "produtos": [alface, tomate, morango, queijo],
    }


def main():
    reset_data()
    data = create_data()

    print("Banco populado com sucesso.")
    print("")
    print("Senha de todos os usuarios:", PASSWORD)
    print("")
    print("Admin:")
    print(f"- {data['admin'].username}")
    print("")
    print("Compradores:")
    for user in data["compradores"]:
        print(f"- {user.username}")
    print("")
    print("Produtores:")
    for user in data["produtores"]:
        print(f"- {user.username}")
    print("")
    print("Produtos cadastrados:", len(data["produtos"]))
    print("Fotos reais seed baixadas em:", settings.MEDIA_ROOT / SEED_IMAGE_DIR)


if __name__ == "__main__":
    main()
