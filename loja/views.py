from decimal import Decimal
import re

from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)

from .models import (
    Cliente,
    Cupcake,
    Endereco,
    HistoricoStatus,
    ItemPedido,
    Pedido,
    Restricao,
)


def somente_numeros(valor):
    return re.sub(r"\D", "", valor or "")


def home(request):
    cupcakes = Cupcake.objects.filter(
        ativo=True
    )

    restricao = request.GET.get(
        "restricao"
    )

    if restricao:
        cupcakes = cupcakes.filter(
            restricoes__nome__iexact=restricao
        )

    restricoes = Restricao.objects.all()

    contexto = {
        "cupcakes": cupcakes,
        "restricoes": restricoes,
        "restricao_ativa": restricao,
    }

    return render(
        request,
        "loja/home.html",
        contexto
    )


def adicionar_carrinho(
    request,
    cupcake_id
):
    cupcake = get_object_or_404(
        Cupcake,
        id=cupcake_id,
        ativo=True
    )

    carrinho = request.session.get(
        "carrinho",
        {}
    )

    cupcake_id = str(
        cupcake.id
    )

    if cupcake_id in carrinho:
        carrinho[cupcake_id] += 1
    else:
        carrinho[cupcake_id] = 1

    request.session["carrinho"] = carrinho
    request.session.modified = True

    return redirect(
        "loja:carrinho"
    )


def carrinho(request):
    carrinho_session = request.session.get(
        "carrinho",
        {}
    )

    itens = []
    subtotal = Decimal("0.00")

    cupcakes = Cupcake.objects.filter(
        id__in=carrinho_session.keys()
    )

    for cupcake in cupcakes:
        quantidade = carrinho_session[
            str(cupcake.id)
        ]

        total_item = (
            cupcake.preco
            * quantidade
        )

        subtotal += total_item

        itens.append({
            "cupcake": cupcake,
            "quantidade": quantidade,
            "total_item": total_item,
        })

    embalagem_presente = request.session.get(
        "embalagem_presente",
        False
    )

    valor_embalagem = (
        Decimal("5.00")
        if embalagem_presente
        else Decimal("0.00")
    )

    total = (
        subtotal
        + valor_embalagem
    )

    contexto = {
        "itens": itens,
        "subtotal": subtotal,
        "embalagem_presente":
            embalagem_presente,
        "valor_embalagem":
            valor_embalagem,
        "total": total,
    }

    return render(
        request,
        "loja/carrinho.html",
        contexto
    )


def aumentar_quantidade(
    request,
    cupcake_id
):
    carrinho = request.session.get(
        "carrinho",
        {}
    )

    cupcake_id = str(
        cupcake_id
    )

    if cupcake_id in carrinho:
        carrinho[cupcake_id] += 1

    request.session["carrinho"] = carrinho
    request.session.modified = True

    return redirect(
        "loja:carrinho"
    )


def diminuir_quantidade(
    request,
    cupcake_id
):
    carrinho = request.session.get(
        "carrinho",
        {}
    )

    cupcake_id = str(
        cupcake_id
    )

    if cupcake_id in carrinho:
        carrinho[cupcake_id] -= 1

        if carrinho[cupcake_id] <= 0:
            del carrinho[cupcake_id]

    request.session["carrinho"] = carrinho
    request.session.modified = True

    return redirect(
        "loja:carrinho"
    )


def remover_carrinho(
    request,
    cupcake_id
):
    carrinho = request.session.get(
        "carrinho",
        {}
    )

    cupcake_id = str(
        cupcake_id
    )

    if cupcake_id in carrinho:
        del carrinho[cupcake_id]

    request.session["carrinho"] = carrinho
    request.session.modified = True

    return redirect(
        "loja:carrinho"
    )


def alternar_embalagem(request):
    atual = request.session.get(
        "embalagem_presente",
        False
    )

    request.session[
        "embalagem_presente"
    ] = not atual

    request.session.modified = True

    return redirect(
        "loja:carrinho"
    )


def calcular_totais(request):
    carrinho_session = request.session.get(
        "carrinho",
        {}
    )

    subtotal = Decimal("0.00")

    cupcakes = Cupcake.objects.filter(
        id__in=carrinho_session.keys()
    )

    for cupcake in cupcakes:
        quantidade = carrinho_session[
            str(cupcake.id)
        ]

        subtotal += (
            cupcake.preco
            * quantidade
        )

    embalagem_presente = request.session.get(
        "embalagem_presente",
        False
    )

    valor_embalagem = (
        Decimal("5.00")
        if embalagem_presente
        else Decimal("0.00")
    )

    frete = Decimal(
        str(
            request.session.get(
                "frete",
                "0.00"
            )
        )
    )

    total = (
        subtotal
        + valor_embalagem
        + frete
    )

    return {
        "subtotal": subtotal,
        "valor_embalagem": valor_embalagem,
        "frete": frete,
        "total": total,
    }


def checkout(request):
    carrinho_session = request.session.get(
        "carrinho",
        {}
    )

    if not carrinho_session:
        return redirect(
            "loja:home"
        )

    totais = calcular_totais(
        request
    )

    erro = None

    dados_formulario = {
        "nome": "",
        "email": "",
        "telefone": "",
        "cep": "",
        "rua": "",
        "numero": "",
        "complemento": "",
        "bairro": "",
        "cidade": "",
        "estado": "",
        "forma_pagamento": "",
        "mensagem_personalizada": "",
    }

    if request.method == "POST":
        nome = request.POST.get(
            "nome",
            ""
        ).strip()

        email = request.POST.get(
            "email",
            ""
        ).strip()

        telefone = request.POST.get(
            "telefone",
            ""
        ).strip()

        cep = request.POST.get(
            "cep",
            ""
        ).strip()

        rua = request.POST.get(
            "rua",
            ""
        ).strip()

        numero = request.POST.get(
            "numero",
            ""
        ).strip()

        complemento = request.POST.get(
            "complemento",
            ""
        ).strip()

        bairro = request.POST.get(
            "bairro",
            ""
        ).strip()

        cidade = request.POST.get(
            "cidade",
            ""
        ).strip()

        estado = request.POST.get(
            "estado",
            ""
        ).strip().upper()

        forma_pagamento = request.POST.get(
            "forma_pagamento",
            ""
        )

        mensagem = request.POST.get(
            "mensagem_personalizada",
            ""
        ).strip()

        dados_formulario = {
            "nome": nome,
            "email": email,
            "telefone": telefone,
            "cep": cep,
            "rua": rua,
            "numero": numero,
            "complemento": complemento,
            "bairro": bairro,
            "cidade": cidade,
            "estado": estado,
            "forma_pagamento":
                forma_pagamento,
            "mensagem_personalizada":
                mensagem,
        }

        if len(nome) < 3:
            erro = (
                "Informe um nome válido "
                "com pelo menos 3 caracteres."
            )

        if not erro:
            try:
                validate_email(
                    email
                )

            except ValidationError:
                erro = (
                    "Informe um endereço "
                    "de e-mail válido."
                )

        telefone_numeros = somente_numeros(
            telefone
        )

        if (
            not erro
            and telefone
            and len(telefone_numeros)
            not in (10, 11)
        ):
            erro = (
                "Informe um telefone válido "
                "com DDD."
            )

        cep_numeros = somente_numeros(
            cep
        )

        if (
            not erro
            and len(cep_numeros) != 8
        ):
            erro = (
                "Informe um CEP válido "
                "com 8 dígitos."
            )

        if (
            not erro
            and not rua
        ):
            erro = (
                "Informe a rua do endereço."
            )

        if (
            not erro
            and not numero
        ):
            erro = (
                "Informe o número "
                "do endereço."
            )

        if (
            not erro
            and not bairro
        ):
            erro = (
                "Informe o bairro."
            )

        if (
            not erro
            and not cidade
        ):
            erro = (
                "Informe a cidade."
            )

        if (
            not erro
            and (
                len(estado) != 2
                or not estado.isalpha()
            )
        ):
            erro = (
                "Informe uma UF válida "
                "com 2 letras."
            )

        if (
            not erro
            and forma_pagamento
            not in ("pix", "cartao")
        ):
            erro = (
                "Selecione uma forma "
                "de pagamento válida."
            )

        if not erro:
            request.session[
                "checkout"
            ] = {
                "nome": nome,
                "email": email,
                "telefone": telefone,
                "cep": cep,
                "rua": rua,
                "numero": numero,
                "complemento":
                    complemento,
                "bairro": bairro,
                "cidade": cidade,
                "estado": estado,
                "forma_pagamento":
                    forma_pagamento,
                "mensagem_personalizada":
                    mensagem,
            }

            request.session.modified = True

            return redirect(
                "loja:finalizar_pedido"
            )

    contexto = {
        "subtotal":
            totais["subtotal"],

        "valor_embalagem":
            totais["valor_embalagem"],

        "embalagem_presente":
            request.session.get(
                "embalagem_presente",
                False
            ),

        "frete":
            totais["frete"],

        "total":
            totais["total"],

        "erro":
            erro,

        "dados":
            dados_formulario,
    }

    return render(
        request,
        "loja/checkout.html",
        contexto
    )


def calcular_frete(request):
    if request.method != "POST":
        return JsonResponse(
            {
                "sucesso": False,
                "erro": "Método inválido."
            },
            status=405
        )

    cep = request.POST.get(
        "cep",
        ""
    ).strip()

    cep_numeros = somente_numeros(
        cep
    )

    if len(cep_numeros) != 8:
        return JsonResponse(
            {
                "sucesso": False,
                "erro":
                    "Informe um CEP válido."
            },
            status=400
        )

    request.session[
        "frete"
    ] = "12.00"

    request.session.modified = True

    totais = calcular_totais(
        request
    )

    return JsonResponse({
        "sucesso": True,
        "frete": (
            f"{totais['frete']:.2f}"
        ),
        "total": (
            f"{totais['total']:.2f}"
        ),
    })


def finalizar_pedido(request):
    carrinho_session = request.session.get(
        "carrinho",
        {}
    )

    checkout_session = request.session.get(
        "checkout"
    )

    if not carrinho_session:
        return redirect(
            "loja:home"
        )

    if not checkout_session:
        return redirect(
            "loja:checkout"
        )

    totais = calcular_totais(
        request
    )

    cliente, criado = Cliente.objects.get_or_create(
        email=checkout_session[
            "email"
        ],

        defaults={
            "nome":
                checkout_session[
                    "nome"
                ],

            "telefone":
                checkout_session[
                    "telefone"
                ],
        }
    )

    if not criado:
        cliente.nome = checkout_session[
            "nome"
        ]

        cliente.telefone = checkout_session[
            "telefone"
        ]

        cliente.save()

    endereco = Endereco.objects.create(
        cliente=cliente,

        cep=checkout_session["cep"],
        rua=checkout_session["rua"],
        numero=checkout_session[
            "numero"
        ],

        complemento=checkout_session[
            "complemento"
        ],

        bairro=checkout_session[
            "bairro"
        ],

        cidade=checkout_session[
            "cidade"
        ],

        estado=checkout_session[
            "estado"
        ],
    )

    pedido = Pedido.objects.create(
        cliente=cliente,
        endereco=endereco,

        status="preparando",

        forma_pagamento=
            checkout_session[
                "forma_pagamento"
            ],

        embalagem_presente=
            request.session.get(
                "embalagem_presente",
                False
            ),

        mensagem_personalizada=
            checkout_session[
                "mensagem_personalizada"
            ],

        subtotal=totais[
            "subtotal"
        ],

        frete=totais[
            "frete"
        ],

        total=totais[
            "total"
        ],
    )

    cupcakes = Cupcake.objects.filter(
        id__in=carrinho_session.keys()
    )

    for cupcake in cupcakes:
        quantidade = carrinho_session[
            str(cupcake.id)
        ]

        ItemPedido.objects.create(
            pedido=pedido,
            cupcake=cupcake,
            quantidade=quantidade,
            preco_unitario=
                cupcake.preco,
        )

    HistoricoStatus.objects.create(
        pedido=pedido,
        status="preparando"
    )

    request.session[
        "ultimo_pedido_id"
    ] = pedido.id

    request.session[
        "cliente_email"
    ] = cliente.email

    request.session.pop(
        "carrinho",
        None
    )

    request.session.pop(
        "checkout",
        None
    )

    request.session.pop(
        "frete",
        None
    )

    request.session.pop(
        "embalagem_presente",
        None
    )

    request.session.modified = True

    return redirect(
        "loja:pedido_sucesso",
        pedido_id=pedido.id
    )


def pedido_sucesso(
    request,
    pedido_id
):
    pedido = get_object_or_404(
        Pedido.objects.prefetch_related(
            "historico_status",
            "itens__cupcake"
        ),
        id=pedido_id
    )

    contexto = {
        "pedido": pedido,
    }

    return render(
        request,
        "loja/pedido_sucesso.html",
        contexto
    )


def meus_pedidos(request):
    email = request.GET.get(
        "email",
        ""
    ).strip()

    if not email:
        email = request.session.get(
            "cliente_email",
            ""
        )

    pedidos = Pedido.objects.none()

    if email:
        pedidos = (
            Pedido.objects
            .filter(
                cliente__email__iexact=
                    email
            )
            .select_related(
                "cliente"
            )
            .order_by(
                "-criado_em"
            )
        )

    contexto = {
        "email": email,
        "pedidos": pedidos,
    }

    return render(
        request,
        "loja/meus_pedidos.html",
        contexto
    )


def detalhe_pedido(
    request,
    pedido_id
):
    pedido = get_object_or_404(
        Pedido.objects
        .select_related(
            "cliente",
            "endereco"
        )
        .prefetch_related(
            "itens__cupcake",
            "historico_status"
        ),
        id=pedido_id
    )

    contexto = {
        "pedido": pedido,
    }

    return render(
        request,
        "loja/detalhe_pedido.html",
        contexto
    )