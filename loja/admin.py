from django.contrib import admin

from .models import (
    Restricao,
    Cupcake,
    Cliente,
    Endereco,
    Pedido,
    ItemPedido,
    HistoricoStatus,
)


@admin.register(Restricao)
class RestricaoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "nome",
    )

    search_fields = (
        "nome",
    )


@admin.register(Cupcake)
class CupcakeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "nome",
        "preco",
        "ativo",
        "imagem_estatica",
    )

    list_filter = (
        "ativo",
        "restricoes",
    )

    search_fields = (
        "nome",
    )

    filter_horizontal = (
        "restricoes",
    )


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "nome",
        "email",
        "telefone",
    )

    search_fields = (
        "nome",
        "email",
    )


@admin.register(Endereco)
class EnderecoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "cliente",
        "cidade",
        "estado",
        "cep",
    )

    search_fields = (
        "cliente__nome",
        "cliente__email",
        "cidade",
        "cep",
    )


class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0

    readonly_fields = (
        "cupcake",
        "quantidade",
        "preco_unitario",
    )

    can_delete = False


class HistoricoStatusInline(admin.TabularInline):
    model = HistoricoStatus
    extra = 0

    readonly_fields = (
        "status",
        "data",
    )

    can_delete = False


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "cliente",
        "status",
        "forma_pagamento",
        "total",
        "criado_em",
    )

    list_filter = (
        "status",
        "forma_pagamento",
        "criado_em",
    )

    search_fields = (
        "cliente__nome",
        "cliente__email",
    )

    readonly_fields = (
        "subtotal",
        "frete",
        "total",
        "criado_em",
        "atualizado_em",
    )

    inlines = [
        ItemPedidoInline,
        HistoricoStatusInline,
    ]

    def save_model(
        self,
        request,
        obj,
        form,
        change
    ):
        status_anterior = None

        if change:
            pedido_anterior = Pedido.objects.get(
                pk=obj.pk
            )

            status_anterior = pedido_anterior.status

        super().save_model(
            request,
            obj,
            form,
            change
        )

        if (
            change
            and status_anterior != obj.status
        ):
            HistoricoStatus.objects.create(
                pedido=obj,
                status=obj.status
            )


@admin.register(ItemPedido)
class ItemPedidoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "pedido",
        "cupcake",
        "quantidade",
        "preco_unitario",
    )

    list_filter = (
        "pedido",
    )


@admin.register(HistoricoStatus)
class HistoricoStatusAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "pedido",
        "status",
        "data",
    )

    list_filter = (
        "status",
    )

    readonly_fields = (
        "pedido",
        "status",
        "data",
    )