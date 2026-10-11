# 🧁 Cupcakeria

Aplicação web desenvolvida em **Python com Django** para simular o funcionamento de uma loja virtual de cupcakes.

O sistema permite navegar pelo catálogo, filtrar produtos, visualizar detalhes, montar um carrinho, realizar pedidos, calcular frete, acompanhar o status da compra e gerar recibos em PDF.

O projeto foi desenvolvido como parte do **Projeto Integrador** do curso de Engenharia de Software.

---

## 🌐 Aplicação publicada

A aplicação está disponível em:

https://cupcakeria-django.onrender.com/

---

## 🎥 Demonstrações

### Versão inicial
https://youtu.be/gqKyaG_PF5I

### Versão 2.0
https://youtu.be/hBHUgAp5Fxw

---

## 🚀 Funcionalidades

### Catálogo

- Listagem de cupcakes disponíveis
- Filtros por restrições alimentares
- Página individual de detalhes do produto
- Exibição de preço, descrição e ingredientes

### Carrinho

- Adicionar produtos
- Aumentar quantidade
- Diminuir quantidade
- Remover itens
- Embalagem para presente
- Cálculo automático do subtotal
- Layout responsivo para desktop e dispositivos móveis

### Checkout

- Cadastro dos dados do cliente
- Endereço de entrega
- Preenchimento automático do endereço através do CEP
- Máscaras para telefone e CEP
- Validação dos campos no frontend
- Validação dos dados também no backend
- Seleção da forma de pagamento
- Cálculo de frete sem recarregar a página
- Preservação dos dados preenchidos quando ocorre algum erro

### Pedidos

- Registro do pedido no banco de dados
- Armazenamento dos produtos e quantidades
- Registro do endereço utilizado
- Histórico de alterações de status
- Consulta de pedidos através do e-mail
- Geração de recibo em PDF

### Rastreamento

O pedido possui três etapas:

1. Preparando
2. Saiu para Entrega
3. Entregue

A versão 2.0 adicionou uma **timeline visual**, permitindo identificar rapidamente:

- etapas concluídas;
- etapa atual;
- etapas pendentes;
- histórico cronológico das alterações.

### Administração

A aplicação utiliza o Django Admin para gerenciamento de:

- cupcakes;
- restrições alimentares;
- clientes;
- endereços;
- pedidos;
- itens dos pedidos;
- histórico de status.

---

## ✨ Melhorias da versão 2.0

Após testes de usabilidade, foram identificados alguns pontos de melhoria na primeira versão da aplicação.

As principais alterações implementadas foram:

### 1. Carrinho responsivo

O carrinho anteriormente utilizava uma área muito estreita em computadores.

Na nova versão, a tela foi reorganizada em duas áreas:

- produtos do pedido;
- resumo da compra.

Em dispositivos menores, o layout continua responsivo.

### 2. Preenchimento automático por CEP

O endereço precisava ser preenchido completamente de forma manual.

Agora, ao informar um CEP válido, o sistema preenche automaticamente:

- rua;
- bairro;
- cidade;
- UF.

Os campos continuam editáveis caso seja necessária alguma correção.

### 3. Cálculo de frete sem recarregar a página

Anteriormente, o cálculo do frete recarregava o checkout e poderia apagar informações já digitadas.

O cálculo passou a utilizar uma requisição assíncrona, atualizando:

- valor do frete;
- total do pedido;

sem recarregar o formulário.

### 4. Validações de formulário

Foram adicionadas validações para:

- nome;
- e-mail;
- telefone;
- CEP;
- endereço;
- UF;
- forma de pagamento.

As verificações são realizadas tanto no navegador quanto no servidor.

### 5. Timeline de acompanhamento

O histórico de status já existia, porém não apresentava de forma visual a posição atual do pedido.

A versão 2.0 adicionou uma timeline com as etapas:

**Preparando → Saiu para Entrega → Entregue**

O histórico cronológico continua disponível abaixo da timeline.

---

## 🛠️ Tecnologias utilizadas

### Backend

- Python
- Django

### Banco de dados

- SQLite para desenvolvimento local
- PostgreSQL em produção

### Frontend

- HTML
- CSS
- JavaScript

### Integrações

- ViaCEP

### Geração de documentos

- ReportLab

### Deploy

- Render

### Controle de versão

- Git
- GitHub

---

## 📂 Estrutura principal

```text
projeto_cupcake/
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── loja/
│   ├── migrations/
│   ├── static/
│   │   └── loja/
│   │       ├── css/
│   │       └── img/
│   │
│   ├── templates/
│   │   └── loja/
│   │
│   ├── management/
│   │   └── commands/
│   │
│   ├── admin.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── manage.py
├── requirements.txt
├── build.sh
└── README.md
