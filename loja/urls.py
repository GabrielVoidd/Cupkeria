from django.urls import path

from . import views
from . import product_views
from . import pdf_views


app_name = "loja"


urlpatterns = [
    path(
        "",
        views.home,
        name="home"
    ),

    path(
        "cupcakes/<int:cupcake_id>/",
        product_views.detalhe_cupcake,
        name="detalhe_cupcake"
    ),

    path(
        "carrinho/",
        views.carrinho,
        name="carrinho"
    ),

    path(
        "carrinho/adicionar/<int:cupcake_id>/",
        views.adicionar_carrinho,
        name="adicionar_carrinho"
    ),

    path(
        "carrinho/aumentar/<int:cupcake_id>/",
        views.aumentar_quantidade,
        name="aumentar_quantidade"
    ),

    path(
        "carrinho/diminuir/<int:cupcake_id>/",
        views.diminuir_quantidade,
        name="diminuir_quantidade"
    ),

    path(
        "carrinho/remover/<int:cupcake_id>/",
        views.remover_carrinho,
        name="remover_carrinho"
    ),

    path(
        "carrinho/embalagem/",
        views.alternar_embalagem,
        name="alternar_embalagem"
    ),

    path(
        "checkout/",
        views.checkout,
        name="checkout"
    ),

    path(
        "checkout/calcular-frete/",
        views.calcular_frete,
        name="calcular_frete"
    ),

    path(
        "pedido/finalizar/",
        views.finalizar_pedido,
        name="finalizar_pedido"
    ),

    path(
        "pedido/<int:pedido_id>/sucesso/",
        views.pedido_sucesso,
        name="pedido_sucesso"
    ),

    path(
        "pedido/<int:pedido_id>/recibo/",
        pdf_views.recibo_pedido_pdf,
        name="recibo_pedido"
    ),

    path(
        "pedido/<int:pedido_id>/",
        views.detalhe_pedido,
        name="detalhe_pedido"
    ),

    path(
        "meus-pedidos/",
        views.meus_pedidos,
        name="meus_pedidos"
    ),
]