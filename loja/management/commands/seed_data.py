from django.core.management.base import BaseCommand

from loja.models import Cupcake, Restricao


class Command(BaseCommand):
    help = "Cria ou atualiza os dados iniciais da Cupcakeria."

    def handle(self, *args, **options):
        self.stdout.write(
            "Criando dados iniciais..."
        )

        vegano, _ = Restricao.objects.get_or_create(
            nome="Vegano"
        )

        sem_gluten, _ = Restricao.objects.get_or_create(
            nome="Sem Glúten"
        )

        zero_acucar, _ = Restricao.objects.get_or_create(
            nome="Zero Açúcar"
        )

        cupcakes = [
            {
                "nome": "Cupcake de Baunilha",
                "descricao": (
                    "Cupcake clássico de baunilha "
                    "com cobertura cremosa."
                ),
                "ingredientes": (
                    "Farinha, ovos, leite, açúcar "
                    "e essência de baunilha."
                ),
                "preco": "8.50",
                "restricoes": [],
            },

            {
                "nome": "Cupcake de Chocolate",
                "descricao": (
                    "Cupcake de chocolate com "
                    "massa macia e cobertura cremosa."
                ),
                "ingredientes": (
                    "Farinha, ovos, leite, açúcar, "
                    "cacau e chocolate."
                ),
                "preco": "9.00",
                "restricoes": [],
            },

            {
                "nome": "Red Velvet",
                "descricao": (
                    "Cupcake Red Velvet com massa "
                    "aveludada e cobertura cremosa."
                ),
                "ingredientes": (
                    "Farinha, ovos, leite, açúcar, "
                    "cacau e corante alimentício."
                ),
                "preco": "10.00",
                "restricoes": [],
            },

            {
                "nome": "Cupcake de Limão",
                "descricao": (
                    "Cupcake leve de limão com "
                    "sabor cítrico."
                ),
                "ingredientes": (
                    "Farinha, ovos, leite, açúcar "
                    "e limão."
                ),
                "preco": "8.00",
                "restricoes": [],
            },

            {
                "nome": "Cupcake Vegano",
                "descricao": (
                    "Cupcake preparado sem "
                    "ingredientes de origem animal."
                ),
                "ingredientes": (
                    "Farinha, açúcar, óleo vegetal, "
                    "bebida vegetal e cacau."
                ),
                "preco": "9.50",
                "restricoes": [
                    vegano,
                ],
            },

            {
                "nome": "Cupcake Sem Glúten",
                "descricao": (
                    "Cupcake preparado sem farinha "
                    "de trigo."
                ),
                "ingredientes": (
                    "Farinha de arroz, ovos, leite, "
                    "açúcar e cacau."
                ),
                "preco": "10.50",
                "restricoes": [
                    sem_gluten,
                ],
            },

            {
                "nome": "Cupcake Zero Açúcar",
                "descricao": (
                    "Cupcake sem adição de açúcar."
                ),
                "ingredientes": (
                    "Farinha, ovos, leite, cacau "
                    "e adoçante culinário."
                ),
                "preco": "10.50",
                "restricoes": [
                    zero_acucar,
                ],
            },
        ]

        for dados in cupcakes:
            restricoes = dados.pop(
                "restricoes"
            )

            cupcake, criado = (
                Cupcake.objects.update_or_create(
                    nome=dados["nome"],
                    defaults={
                        "descricao":
                            dados["descricao"],

                        "ingredientes":
                            dados["ingredientes"],

                        "preco":
                            dados["preco"],

                        "ativo": True,
                    }
                )
            )

            cupcake.restricoes.set(
                restricoes
            )

            if criado:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Criado: {cupcake.nome}"
                    )
                )

            else:
                self.stdout.write(
                    f"Atualizado: {cupcake.nome}"
                )

        self.stdout.write(
            self.style.SUCCESS(
                "Dados iniciais configurados com sucesso."
            )
        )