from io import BytesIO

from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import (
    ParagraphStyle,
    getSampleStyleSheet,
)
from reportlab.lib.units import cm
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from .models import Pedido


def recibo_pedido_pdf(request, pedido_id):
    pedido = get_object_or_404(
        Pedido.objects
        .select_related(
            "cliente",
            "endereco"
        )
        .prefetch_related(
            "itens__cupcake"
        ),
        id=pedido_id
    )

    buffer = BytesIO()

    documento = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
        title=f"Recibo Pedido #{pedido.id}",
        author="Cupcakeria",
    )

    estilos = getSampleStyleSheet()

    titulo = ParagraphStyle(
        "TituloCupcakeria",
        parent=estilos["Heading1"],
        alignment=TA_CENTER,
        fontSize=20,
        spaceAfter=8,
    )

    subtitulo = ParagraphStyle(
        "Subtitulo",
        parent=estilos["Normal"],
        alignment=TA_CENTER,
        fontSize=10,
        textColor=colors.grey,
        spaceAfter=20,
    )

    elementos = []

    elementos.append(
        Paragraph(
            "CUPCAKERIA",
            titulo
        )
    )

    elementos.append(
        Paragraph(
            f"Recibo do Pedido #{pedido.id}",
            subtitulo
        )
    )

    elementos.append(
        Paragraph(
            "<b>Dados do cliente</b>",
            estilos["Heading2"]
        )
    )

    elementos.append(
        Paragraph(
            f"Nome: {pedido.cliente.nome}",
            estilos["Normal"]
        )
    )

    elementos.append(
        Paragraph(
            f"E-mail: {pedido.cliente.email}",
            estilos["Normal"]
        )
    )

    if pedido.cliente.telefone:
        elementos.append(
            Paragraph(
                f"Telefone: {pedido.cliente.telefone}",
                estilos["Normal"]
            )
        )

    elementos.append(
        Spacer(1, 16)
    )

    elementos.append(
        Paragraph(
            "<b>Entrega</b>",
            estilos["Heading2"]
        )
    )

    endereco = (
        f"{pedido.endereco.rua}, "
        f"{pedido.endereco.numero}"
    )

    if pedido.endereco.complemento:
        endereco += (
            f" - {pedido.endereco.complemento}"
        )

    elementos.append(
        Paragraph(
            endereco,
            estilos["Normal"]
        )
    )

    elementos.append(
        Paragraph(
            (
                f"{pedido.endereco.bairro} - "
                f"{pedido.endereco.cidade}/"
                f"{pedido.endereco.estado}"
            ),
            estilos["Normal"]
        )
    )

    elementos.append(
        Paragraph(
            f"CEP: {pedido.endereco.cep}",
            estilos["Normal"]
        )
    )

    elementos.append(
        Spacer(1, 20)
    )

    elementos.append(
        Paragraph(
            "<b>Itens do pedido</b>",
            estilos["Heading2"]
        )
    )

    dados_itens = [
        [
            "Produto",
            "Qtd.",
            "Unitário",
            "Total",
        ]
    ]

    for item in pedido.itens.all():
        dados_itens.append(
            [
                item.cupcake.nome,
                str(item.quantidade),
                (
                    f"R$ "
                    f"{item.preco_unitario:.2f}"
                ),
                (
                    f"R$ "
                    f"{item.subtotal():.2f}"
                ),
            ]
        )

    tabela_itens = Table(
        dados_itens,
        colWidths=[
            8 * cm,
            1.5 * cm,
            3 * cm,
            3 * cm,
        ]
    )

    tabela_itens.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor(
                        "#F52C91"
                    ),
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white,
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold",
                ),
                (
                    "ALIGN",
                    (1, 0),
                    (-1, -1),
                    "CENTER",
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.lightgrey,
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [
                        colors.white,
                        colors.HexColor(
                            "#F9FAFB"
                        ),
                    ],
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    8,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    8,
                ),
            ]
        )
    )

    elementos.append(
        tabela_itens
    )

    elementos.append(
        Spacer(1, 20)
    )

    resumo = [
        [
            "Subtotal",
            f"R$ {pedido.subtotal:.2f}",
        ],
        [
            "Frete",
            f"R$ {pedido.frete:.2f}",
        ],
    ]

    if pedido.embalagem_presente:
        resumo.append(
            [
                "Embalagem para presente",
                "R$ 5.00",
            ]
        )

    resumo.append(
        [
            "TOTAL",
            f"R$ {pedido.total:.2f}",
        ]
    )

    tabela_resumo = Table(
        resumo,
        colWidths=[
            10 * cm,
            5.5 * cm,
        ]
    )

    tabela_resumo.setStyle(
        TableStyle(
            [
                (
                    "ALIGN",
                    (1, 0),
                    (1, -1),
                    "RIGHT",
                ),
                (
                    "LINEABOVE",
                    (0, -1),
                    (-1, -1),
                    1,
                    colors.black,
                ),
                (
                    "FONTNAME",
                    (0, -1),
                    (-1, -1),
                    "Helvetica-Bold",
                ),
                (
                    "TEXTCOLOR",
                    (1, -1),
                    (1, -1),
                    colors.HexColor(
                        "#F00079"
                    ),
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
            ]
        )
    )

    elementos.append(
        tabela_resumo
    )

    elementos.append(
        Spacer(1, 22)
    )

    elementos.append(
        Paragraph(
            (
                "<b>Forma de pagamento:</b> "
                f"{pedido.get_forma_pagamento_display()}"
            ),
            estilos["Normal"]
        )
    )

    elementos.append(
        Paragraph(
            (
                "<b>Status:</b> "
                f"{pedido.get_status_display()}"
            ),
            estilos["Normal"]
        )
    )

    elementos.append(
        Paragraph(
            (
                "<b>Data do pedido:</b> "
                f"{pedido.criado_em.strftime('%d/%m/%Y %H:%M')}"
            ),
            estilos["Normal"]
        )
    )

    if pedido.mensagem_personalizada:
        elementos.append(
            Spacer(1, 18)
        )

        elementos.append(
            Paragraph(
                "<b>Mensagem:</b>",
                estilos["Normal"]
            )
        )

        elementos.append(
            Paragraph(
                pedido.mensagem_personalizada,
                estilos["Normal"]
            )
        )

    documento.build(
        elementos
    )

    pdf = buffer.getvalue()

    buffer.close()

    resposta = HttpResponse(
        pdf,
        content_type="application/pdf"
    )

    resposta[
        "Content-Disposition"
    ] = (
        f'attachment; '
        f'filename="recibo_pedido_{pedido.id}.pdf"'
    )

    return resposta