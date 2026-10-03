from django.db import models


class Restricao(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome


class Cupcake(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    ingredientes = models.TextField(blank=True)
    preco = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    imagem = models.ImageField(
        upload_to="cupcakes/",
        blank=True,
        null=True
    )

    restricoes = models.ManyToManyField(
        Restricao,
        blank=True,
        related_name="cupcakes"
    )

    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome


class Cliente(models.Model):
    nome = models.CharField(max_length=100)

    email = models.EmailField(
        unique=True
    )

    telefone = models.CharField(
        max_length=20,
        blank=True
    )

    def __str__(self):
        return self.nome


class Endereco(models.Model):
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name="enderecos"
    )

    cep = models.CharField(max_length=9)
    rua = models.CharField(max_length=150)
    numero = models.CharField(max_length=20)

    complemento = models.CharField(
        max_length=100,
        blank=True
    )

    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)

    def __str__(self):
        return (
            f"{self.rua}, {self.numero} "
            f"- {self.cidade}"
        )


class Pedido(models.Model):
    STATUS_CHOICES = [
        (
            "preparando",
            "Preparando"
        ),
        (
            "saiu_entrega",
            "Saiu para Entrega"
        ),
        (
            "entregue",
            "Entregue"
        ),
    ]

    PAGAMENTO_CHOICES = [
        (
            "pix",
            "PIX"
        ),
        (
            "cartao",
            "Cartão de Crédito"
        ),
    ]

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        related_name="pedidos"
    )

    endereco = models.ForeignKey(
        Endereco,
        on_delete=models.PROTECT
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="preparando"
    )

    forma_pagamento = models.CharField(
        max_length=20,
        choices=PAGAMENTO_CHOICES
    )

    embalagem_presente = models.BooleanField(
        default=False
    )

    mensagem_personalizada = models.TextField(
        blank=True
    )

    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    frete = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    criado_em = models.DateTimeField(
        auto_now_add=True
    )

    atualizado_em = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"Pedido #{self.id}"


class ItemPedido(models.Model):
    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        related_name="itens"
    )

    cupcake = models.ForeignKey(
        Cupcake,
        on_delete=models.PROTECT
    )

    quantidade = models.PositiveIntegerField(
        default=1
    )

    preco_unitario = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    def subtotal(self):
        return (
            self.preco_unitario
            * self.quantidade
        )

    def __str__(self):
        return (
            f"{self.quantidade}x "
            f"{self.cupcake.nome}"
        )


class HistoricoStatus(models.Model):
    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        related_name="historico_status"
    )

    status = models.CharField(
        max_length=20,
        choices=Pedido.STATUS_CHOICES
    )

    data = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["data"]

    def __str__(self):
        return (
            f"{self.pedido} - "
            f"{self.get_status_display()}"
        )