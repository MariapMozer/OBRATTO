# Guia de Componentes Jinja2 - OBRATTO

**Data:** 21/10/2025
**Versão:** 2.0
**Projeto:** OBRATTO - Plataforma de Construção Civil

---

## Índice

1. [Introdução](#introdução)
2. [Estrutura de Componentes](#estrutura-de-componentes)
3. [Componentes de Navegação](#componentes-de-navegação)
4. [Componentes de Exibição](#componentes-de-exibição)
5. [Componentes de Formulário](#componentes-de-formulário)
6. [Componentes de Feedback](#componentes-de-feedback)
7. [Componentes Utilitários](#componentes-utilitários)
8. [Hierarquia de Templates](#hierarquia-de-templates)
9. [Boas Práticas](#boas-práticas)
10. [Exemplos Completos](#exemplos-completos)

---

## Introdução

Este guia documenta todos os componentes Jinja2 reutilizáveis disponíveis na aplicação OBRATTO. Os componentes foram desenvolvidos seguindo as melhores práticas de:

- **DRY (Don't Repeat Yourself):** Eliminar duplicação de código
- **Componentização:** Criar elementos reutilizáveis e configuráveis
- **Consistência:** Manter padrão visual e de código em toda aplicação
- **Manutenibilidade:** Facilitar atualizações e correções

### Como Usar Este Guia

1. Identifique o componente que precisa
2. Importe o macro no seu template
3. Configure os parâmetros conforme necessário
4. Veja exemplos de uso

---

## Estrutura de Componentes

```
templates/components/
├── alert.html                    # Alertas e mensagens
├── breadcrumbs.html              # Navegação breadcrumb
├── chat_message.html            # Sistema de chat com mensagens
├── confirmation_modal.html       # Modais de confirmação
├── data_table.html              # Tabelas de dados
├── empty_state.html             # Estados vazios
├── footer.html                  # Footer (include)
├── form_input.html              # Inputs de formulário
├── pagination.html              # Paginação
├── product_card.html            # Cards de produto
├── search_form.html             # Formulários de busca
├── service_card.html            # Cards de serviço
├── sidebar.html                 # Sidebar de navegação
├── stats_card.html              # Cards de estatísticas (dashboards)
├── timeline.html                # Linha do tempo de eventos
├── toast-handler.html           # Handler de toasts
└── user_dropdown.html           # Dropdown de usuário
```

---

## Componentes de Navegação

### 1. Sidebar

**Arquivo:** `components/sidebar.html`
**Tipo:** Macro
**Descrição:** Sidebar de navegação lateral com itens configuráveis

#### Parâmetros

| Parâmetro | Tipo | Obrigatório | Padrão | Descrição |
|-----------|------|-------------|--------|-----------|
| `items` | List[Dict] | Sim | - | Lista de itens do menu |
| `active_item` | String | Não | '' | ID do item ativo |
| `logo_text` | String | Não | '' | Texto do logo |
| `logo_url` | String | Não | '/' | URL do logo |

#### Estrutura do Item

```python
{
    'id': 'identificador',      # ID único do item
    'url': '/path',             # URL do link
    'icon': 'bi-icon-name',     # Ícone Bootstrap Icons (sem 'bi-')
    'label': 'Texto'            # Texto do label
}
```

#### Exemplo de Uso

```jinja2
{% from 'components/sidebar.html' import sidebar %}

{% set menu_items = [
    {'id': 'home', 'url': '/home', 'icon': 'house', 'label': 'Home'},
    {'id': 'produtos', 'url': '/produtos', 'icon': 'box-seam', 'label': 'Produtos'},
    {'id': 'config', 'url': '/config', 'icon': 'gear', 'label': 'Configurações'}
] %}

{{ sidebar(menu_items, active_item='produtos', logo_text='MINHA LOJA') }}
```

---

### 2. User Dropdown

**Arquivo:** `components/user_dropdown.html`
**Tipo:** Macro
**Descrição:** Dropdown de usuário com avatar e menu

#### Parâmetros

| Parâmetro | Tipo | Obrigatório | Padrão | Descrição |
|-----------|------|-------------|--------|-----------|
| `user` | Object | Sim | - | Objeto do usuário (.nome, .foto) |
| `menu_items` | List[Dict] | Sim | - | Itens do menu dropdown |
| `default_avatar` | String | Não | '/static/img/user.jpg' | Avatar padrão |
| `default_label` | String | Não | 'Usuário' | Label padrão |

#### Estrutura do Menu Item

```python
{
    'url': '/path',           # URL do link
    'icon': 'icon-name',      # Ícone Bootstrap (sem 'bi-')
    'label': 'Texto',         # Texto do link
    'divider': False,         # Se True, cria um divisor
    'danger': False           # Se True, aplica estilo danger (vermelho)
}
```

#### Exemplo de Uso

```jinja2
{% from 'components/user_dropdown.html' import user_dropdown %}

{% set menu = [
    {'url': '/perfil', 'icon': 'person', 'label': 'Perfil'},
    {'url': '/config', 'icon': 'gear', 'label': 'Configurações'},
    {'divider': True},
    {'url': '/logout', 'icon': 'box-arrow-right', 'label': 'Sair', 'danger': True}
] %}

{{ user_dropdown(usuario_logado, menu) }}
```

---

### 3. Breadcrumbs

**Arquivo:** `components/breadcrumbs.html`
**Tipo:** Macro
**Descrição:** Navegação breadcrumb

#### Parâmetros

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| `items` | List[Dict] | Sim | Lista de itens do breadcrumb |

#### Estrutura do Item

```python
{
    'label': 'Texto',    # Texto do item
    'url': '/path'       # URL (opcional no último item)
}
```

#### Exemplo de Uso

```jinja2
{% from 'components/breadcrumbs.html' import breadcrumbs %}

{{ breadcrumbs([
    {'label': 'Home', 'url': '/'},
    {'label': 'Produtos', 'url': '/produtos'},
    {'label': 'Editar Produto'}  # Último item sem URL
]) }}
```

---

### 4. Pagination

**Arquivo:** `components/pagination.html`
**Tipo:** Macro
**Descrição:** Paginação de lista

#### Parâmetros

| Parâmetro | Tipo | Obrigatório | Padrão | Descrição |
|-----------|------|-------------|--------|-----------|
| `current_page` | Integer | Sim | - | Página atual |
| `total_pages` | Integer | Sim | - | Total de páginas |
| `base_url` | String | Sim | - | URL base |
| `show_ends` | Boolean | Não | True | Mostrar primeira/última |
| `max_pages` | Integer | Não | 5 | Máx de páginas visíveis |

#### Exemplo de Uso

```jinja2
{% from 'components/pagination.html' import pagination %}

{{ pagination(
    current_page=3,
    total_pages=10,
    base_url='/produtos'
) }}
```

---

## Componentes de Exibição

### 5. Product Card

**Arquivo:** `components/product_card.html`
**Tipo:** Macro
**Descrição:** Card para exibir produtos

#### Parâmetros

| Parâmetro | Tipo | Obrigatório | Padrão | Descrição |
|-----------|------|-------------|--------|-----------|
| `produto` | Object | Sim | - | Objeto produto |
| `show_actions` | Boolean | Não | True | Mostrar botões de ação |
| `card_class` | String | Não | '' | Classes CSS adicionais |
| `edit_url` | String | Não | Auto | URL de edição |
| `delete_handler` | String | Não | 'confirmDelete' | Função JS de exclusão |
| `show_quantity` | Boolean | Não | True | Mostrar quantidade |

#### Propriedades do Produto

```python
{
    'id': 1,
    'nome': 'Produto',
    'descricao': 'Descrição',
    'preco': 99.90,
    'foto': 'path/to/image.jpg',  # Opcional
    'quantidade': 10,              # Opcional
    'status': 'ativo'              # Opcional
}
```

#### Exemplo de Uso

```jinja2
{% from 'components/product_card.html' import product_card %}

{% for produto in produtos %}
    {{ product_card(produto) }}
{% endfor %}

{# Sem ações #}
{{ product_card(produto, show_actions=False) }}
```

---

### 6. Service Card

**Arquivo:** `components/service_card.html`
**Tipo:** Macro
**Descrição:** Card para exibir serviços

#### Parâmetros

| Parâmetro | Tipo | Obrigatório | Padrão | Descrição |
|-----------|------|-------------|--------|-----------|
| `servico` | Object | Sim | - | Objeto serviço |
| `show_actions` | Boolean | Não | True | Mostrar botões de ação |
| `card_class` | String | Não | '' | Classes CSS adicionais |
| `edit_url` | String | Não | Auto | URL de edição |
| `delete_handler` | String | Não | 'confirmDelete' | Função JS de exclusão |
| `show_category` | Boolean | Não | True | Mostrar categoria |
| `show_rating` | Boolean | Não | False | Mostrar avaliação |
| `rating` | Float | Não | 0 | Nota (0-5) |

#### Exemplo de Uso

```jinja2
{% from 'components/service_card.html' import service_card %}

{% for servico in servicos %}
    {{ service_card(servico, show_rating=True, rating=4.5) }}
{% endfor %}
```

---

### 7. Empty State

**Arquivo:** `components/empty_state.html`
**Tipo:** Macro
**Descrição:** Estado vazio quando não há dados

#### Parâmetros

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| `icon` | String | Sim | Ícone Bootstrap (sem 'bi-') |
| `title` | String | Sim | Título da mensagem |
| `description` | String | Sim | Descrição |
| `action_url` | String | Não | URL do botão de ação |
| `action_text` | String | Não | Texto do botão |
| `action_icon` | String | Não | Ícone do botão |

#### Exemplo de Uso

```jinja2
{% from 'components/empty_state.html' import empty_state %}

{% if not produtos %}
    {{ empty_state(
        icon='box-seam',
        title='Nenhum produto encontrado',
        description='Você ainda não cadastrou nenhum produto.',
        action_url='/produtos/criar',
        action_text='Cadastrar Produto',
        action_icon='plus-circle'
    ) }}
{% endif %}
```

---

### 8. Data Table

**Arquivo:** `components/data_table.html`
**Tipo:** Macro
**Descrição:** Tabela de dados responsiva

#### Parâmetros

| Parâmetro | Tipo | Obrigatório | Padrão | Descrição |
|-----------|------|-------------|--------|-----------|
| `headers` | List[Dict] | Sim | - | Cabeçalhos da tabela |
| `rows` | List[Object] | Sim | - | Linhas de dados |
| `actions` | Boolean | Não | False | Mostrar coluna de ações |
| `action_buttons` | List[Dict] | Não | [] | Botões de ação |
| `table_class` | String | Não | '' | Classes CSS adicionais |
| `striped` | Boolean | Não | True | Linhas zebradas |
| `hover` | Boolean | Não | True | Efeito hover |
| `bordered` | Boolean | Não | False | Bordas |
| `responsive` | Boolean | Não | True | Wrapper responsivo |

#### Estrutura de Headers

```python
{
    'label': 'Nome da Coluna',
    'key': 'campo_do_objeto',
    'sortable': True  # Opcional
}
```

#### Estrutura de Action Buttons

```python
{
    'icon': 'pencil',              # Ícone Bootstrap
    'label': 'Editar',             # Label (oculto em mobile)
    'class': 'btn-sm btn-primary', # Classes CSS
    'url': '/users/edit/',         # URL base (será concatenado com row.id)
    'onclick': 'funcao()',         # Ou função JS onclick
    'title': 'Editar registro'     # Opcional, tooltip
}
```

#### Exemplo de Uso

```jinja2
{% from 'components/data_table.html' import data_table %}

{{ data_table(
    headers=[
        {'label': 'ID', 'key': 'id'},
        {'label': 'Nome', 'key': 'nome'},
        {'label': 'Email', 'key': 'email'}
    ],
    rows=usuarios,
    actions=True,
    action_buttons=[
        {'icon': 'pencil', 'label': 'Editar', 'class': 'btn-sm btn-primary', 'url': '/users/edit/'},
        {'icon': 'trash', 'label': 'Excluir', 'class': 'btn-sm btn-danger', 'onclick': 'deleteUser(this)'}
    ]
) }}
```

---

## Componentes de Formulário

### 9. Form Input (Text, Email, Number, etc)

**Arquivo:** `components/form_input.html`
**Tipo:** Múltiplos Macros
**Descrição:** Componentes de formulário com validação Bootstrap

#### Macros Disponíveis

- `text_input`: Input de texto/email/number/password
- `textarea_input`: Textarea
- `select_input`: Select dropdown
- `checkbox_input`: Checkbox
- `radio_input`: Radio buttons
- `file_input`: Input de arquivo

#### Exemplo de Uso - Text Input

```jinja2
{% from 'components/form_input.html' import text_input, textarea_input, select_input %}

{{ text_input(
    name='nome',
    label='Nome Completo',
    placeholder='Digite seu nome',
    required=True,
    icon='person'
) }}

{{ text_input(
    name='email',
    label='E-mail',
    type='email',
    placeholder='seu@email.com',
    required=True,
    icon='envelope'
) }}
```

#### Exemplo de Uso - Textarea

```jinja2
{{ textarea_input(
    name='descricao',
    label='Descrição',
    rows=4,
    placeholder='Descreva o produto...',
    maxlength=500
) }}
```

#### Exemplo de Uso - Select

```jinja2
{{ select_input(
    name='categoria',
    label='Categoria',
    options=[
        {'value': '1', 'label': 'Construção'},
        {'value': '2', 'label': 'Reformas'},
        {'value': '3', 'label': 'Acabamento'}
    ],
    selected='2',
    required=True
) }}
```

#### Exemplo de Uso - Checkbox

```jinja2
{{ checkbox_input(
    name='aceito_termos',
    label='Aceito os termos e condições',
    checked=False
) }}
```

#### Exemplo de Uso - File

```jinja2
{{ file_input(
    name='foto',
    label='Foto do Produto',
    accept='image/*',
    help_text='Tamanho máximo: 5MB',
    required=True
) }}
```

---

### 10. Search Form

**Arquivo:** `components/search_form.html`
**Tipo:** Macro
**Descrição:** Formulário de busca com múltiplos campos

#### Parâmetros

| Parâmetro | Tipo | Obrigatório | Padrão | Descrição |
|-----------|------|-------------|--------|-----------|
| `action` | String | Sim | - | URL de ação do formulário |
| `fields` | List[Dict] | Sim | - | Campos do formulário |
| `submit_text` | String | Não | 'Buscar' | Texto do botão submit |
| `clear_url` | String | Não | None | URL para limpar busca |
| `method` | String | Não | 'GET' | Método HTTP |

#### Estrutura de Fields

```python
{
    'name': 'campo',
    'type': 'text',               # text, number, date, etc
    'label': 'Label',
    'placeholder': 'Placeholder',
    'value': ''                   # Opcional, valor inicial
}
```

#### Exemplo de Uso

```jinja2
{% from 'components/search_form.html' import search_form %}

{{ search_form(
    action='/produtos/buscar',
    fields=[
        {'name': 'id', 'type': 'number', 'label': 'ID', 'placeholder': 'Digite o ID'},
        {'name': 'nome', 'type': 'text', 'label': 'Nome', 'placeholder': 'Nome do produto'}
    ],
    clear_url='/produtos'
) }}
```

---

## Componentes de Feedback

### 11. Alert

**Arquivo:** `components/alert.html`
**Tipo:** Macro
**Descrição:** Alertas de feedback

#### Parâmetros

| Parâmetro | Tipo | Obrigatório | Padrão | Descrição |
|-----------|------|-------------|--------|-----------|
| `message` | String | Sim | - | Mensagem (suporta HTML) |
| `type` | String | Não | 'info' | Tipo: success, danger, warning, info |
| `dismissible` | Boolean | Não | True | Pode ser fechado |
| `icon` | String | Não | None | Ícone Bootstrap |

#### Exemplo de Uso

```jinja2
{% from 'components/alert.html' import alert %}

{{ alert('Produto cadastrado com sucesso!', type='success', icon='check-circle') }}
{{ alert('Erro ao processar dados', type='danger', icon='exclamation-triangle') }}
{{ alert('Atenção: verifique os campos', type='warning', dismissible=False) }}
```

---

### 12. Confirmation Modal

**Arquivo:** `components/confirmation_modal.html`
**Tipo:** Macro
**Descrição:** Modal de confirmação de ações

#### Parâmetros

| Parâmetro | Tipo | Obrigatório | Padrão | Descrição |
|-----------|------|-------------|--------|-----------|
| `modal_id` | String | Não | 'confirmModal' | ID único do modal |
| `title` | String | Não | 'Confirmar Ação' | Título |
| `icon` | String | Não | 'exclamation-triangle' | Ícone |
| `icon_class` | String | Não | 'text-warning' | Classe do ícone |
| `message` | String | Não | 'Tem certeza?' | Mensagem (HTML) |
| `confirm_text` | String | Não | 'Confirmar' | Texto botão confirmar |
| `confirm_class` | String | Não | 'btn-primary' | Classe botão confirmar |
| `cancel_text` | String | Não | 'Cancelar' | Texto botão cancelar |

#### Exemplo de Uso

```jinja2
{% from 'components/confirmation_modal.html' import confirmation_modal %}

{{ confirmation_modal(
    modal_id='deleteModal',
    title='Confirmar Exclusão',
    icon='trash',
    icon_class='text-danger',
    message='<p>Deseja excluir <strong id="itemName"></strong>?</p>',
    confirm_text='Excluir',
    confirm_class='btn-danger'
) }}

<script>
function confirmDelete(id, name) {
    document.getElementById('itemName').textContent = name;
    const modal = new bootstrap.Modal(document.getElementById('deleteModal'));
    document.getElementById('deleteModalConfirmBtn').onclick = () => deleteItem(id);
    modal.show();
}
</script>
```

---

## Componentes Utilitários

### 13. Footer

**Arquivo:** `components/footer.html`
**Tipo:** Include
**Descrição:** Footer padrão da aplicação

#### Exemplo de Uso

```jinja2
{% include 'components/footer.html' %}
```

---

### 14. Toast Handler

**Arquivo:** `components/toast-handler.html`
**Tipo:** Include
**Descrição:** Sistema de notificações toast

#### Exemplo de Uso

```jinja2
{# Já incluído em base_root.html #}
```

---

## Componentes Avançados

### 15. Stats Card

**Arquivo:** `components/stats_card.html`
**Tipo:** Macro
**Descrição:** Card de estatísticas para dashboards com suporte a ícones, valores, tendências e links

#### Parâmetros

| Parâmetro | Tipo | Obrigatório | Padrão | Descrição |
|-----------|------|-------------|--------|-----------|
| `title` | String | Sim | - | Título do card |
| `value` | String/Number | Sim | - | Valor principal a exibir |
| `icon` | String | Sim | - | Ícone Bootstrap (sem 'bi-') |
| `icon_class` | String | Não | 'text-primary' | Classe CSS do ícone |
| `subtitle` | String | Não | '' | Subtítulo/descrição |
| `trend` | Number | Não | None | Tendência em % (positivo/negativo) |
| `trend_label` | String | Não | '' | Label da tendência |
| `card_class` | String | Não | '' | Classes CSS adicionais |
| `link_url` | String | Não | '' | URL para mais detalhes |
| `link_text` | String | Não | 'Ver detalhes' | Texto do link |

#### Macros Disponíveis

- `stats_card`: Card individual de estatística
- `stats_row`: Container responsivo para múltiplos cards

#### Exemplo de Uso

```jinja2
{% from 'components/stats_card.html' import stats_card, stats_row %}

{% call stats_row() %}
    {{ stats_card(
        title='Total de Vendas',
        value='R$ 12.450,00',
        icon='currency-dollar',
        icon_class='text-success',
        trend=15.3,
        trend_label='vs mês anterior',
        link_url='/fornecedor/vendas'
    ) }}

    {{ stats_card(
        title='Produtos Ativos',
        value='127',
        icon='box-seam',
        icon_class='text-primary',
        subtitle='Em estoque',
        trend=-3.2,
        trend_label='vs mês anterior'
    ) }}

    {{ stats_card(
        title='Novos Clientes',
        value='45',
        icon='people',
        icon_class='text-info',
        trend=22.5
    ) }}

    {{ stats_card(
        title='Avaliação Média',
        value='4.8/5.0',
        icon='star-fill',
        icon_class='text-warning'
    ) }}
{% endcall %}
```

---

### 16. Timeline

**Arquivo:** `components/timeline.html`
**Tipo:** Macro
**Descrição:** Linha do tempo para exibir eventos cronológicos com suporte a ícones, status e metadados

#### Parâmetros do timeline_item

| Parâmetro | Tipo | Obrigatório | Padrão | Descrição |
|-----------|------|-------------|--------|-----------|
| `title` | String | Sim | - | Título do evento |
| `timestamp` | String | Sim | - | Data/hora do evento |
| `icon` | String | Sim | - | Ícone Bootstrap (sem 'bi-') |
| `type` | String | Não | 'primary' | Tipo/cor ('success', 'info', 'warning', 'danger', 'primary', 'secondary') |
| `description` | String | Não | '' | Descrição detalhada |
| `user` | String | Não | '' | Nome do usuário responsável |
| `user_avatar` | String | Não | '' | URL do avatar |
| `metadata` | List[Dict] | Não | [] | Metadados adicionais |

#### Macros Disponíveis

- `timeline_item`: Item individual da timeline
- `timeline_container`: Container com título opcional
- `simple_timeline`: Versão simplificada para eventos básicos

#### Exemplo de Uso

```jinja2
{% from 'components/timeline.html' import timeline_container, timeline_item %}

{% call timeline_container(title='Histórico do Pedido #1234') %}
    {{ timeline_item(
        title='Pedido Criado',
        description='Pedido criado com sucesso pelo cliente',
        timestamp='15/01/2024 10:30',
        icon='cart-plus',
        type='success',
        user='João Silva',
        metadata=[
            {'label': 'Total', 'value': 'R$ 1.250,00'},
            {'label': 'Itens', 'value': '5 produtos'}
        ]
    ) }}

    {{ timeline_item(
        title='Pagamento Confirmado',
        description='Pagamento via PIX aprovado',
        timestamp='15/01/2024 10:35',
        icon='credit-card',
        type='info',
        user='Sistema'
    ) }}

    {{ timeline_item(
        title='Em Separação',
        description='Produtos sendo separados no estoque',
        timestamp='15/01/2024 11:20',
        icon='box',
        type='warning',
        user='Maria Santos'
    ) }}

    {{ timeline_item(
        title='Pedido Enviado',
        timestamp='15/01/2024 14:00',
        icon='truck',
        type='primary',
        metadata=[
            {'label': 'Transportadora', 'value': 'Correios'},
            {'label': 'Código de Rastreio', 'value': 'BR123456789'}
        ]
    ) }}
{% endcall %}
```

#### Exemplo de Timeline Simples

```jinja2
{% from 'components/timeline.html' import simple_timeline %}

{{ simple_timeline(events=[
    {'title': 'Pedido criado', 'time': '10:30', 'icon': 'cart', 'type': 'success'},
    {'title': 'Em processamento', 'time': '11:00', 'icon': 'hourglass', 'type': 'info'},
    {'title': 'Enviado', 'time': '14:30', 'icon': 'truck', 'type': 'primary'}
]) }}
```

---

### 17. Chat Message

**Arquivo:** `components/chat_message.html`
**Tipo:** Macro
**Descrição:** Sistema completo de mensagens chat com suporte a anexos, status de leitura e indicador de digitação

#### Parâmetros do chat_message

| Parâmetro | Tipo | Obrigatório | Padrão | Descrição |
|-----------|------|-------------|--------|-----------|
| `message` | String | Sim | - | Texto da mensagem |
| `sender_name` | String | Sim | - | Nome do remetente |
| `timestamp` | String | Sim | - | Data/hora da mensagem |
| `sender_avatar` | String | Não | '' | URL do avatar |
| `is_own` | Boolean | Não | False | Se true, mensagem do usuário atual |
| `status` | String | Não | '' | Status ('sent', 'delivered', 'read') |
| `attachment` | String | Não | '' | URL do anexo |
| `attachment_type` | String | Não | '' | Tipo ('image', 'file') |
| `message_class` | String | Não | '' | Classes CSS adicionais |

#### Macros Disponíveis

- `chat_message`: Mensagem individual
- `chat_container`: Container para mensagens
- `chat_input`: Campo de entrada de mensagens
- `typing_indicator`: Indicador de digitação animado
- `chat_date_separator`: Separador de data

#### Exemplo Completo de Chat

```jinja2
{% from 'components/chat_message.html' import chat_container, chat_message, chat_input, chat_date_separator, typing_indicator %}

{% call chat_container() %}
    {{ chat_date_separator('Hoje') }}

    {{ chat_message(
        message='Olá! Gostaria de saber mais sobre o produto.',
        sender_name='João Silva',
        sender_avatar='/static/img/user1.jpg',
        timestamp='10:30',
        is_own=False
    ) }}

    {{ chat_message(
        message='Olá João! Claro, posso te ajudar.',
        sender_name='Você',
        timestamp='10:32',
        is_own=True,
        status='read'
    ) }}

    {{ chat_message(
        message='Veja nossa lista de preços',
        sender_name='Você',
        timestamp='10:33',
        is_own=True,
        attachment='/files/lista_precos.pdf',
        attachment_type='file',
        status='delivered'
    ) }}

    {{ chat_message(
        message='Perfeito, obrigado!',
        sender_name='João Silva',
        sender_avatar='/static/img/user1.jpg',
        timestamp='10:35',
        is_own=False
    ) }}

    {{ typing_indicator(
        sender_name='João Silva',
        sender_avatar='/static/img/user1.jpg'
    ) }}
{% endcall %}

{{ chat_input(
    action='/fornecedor/mensagens/enviar',
    placeholder='Digite sua mensagem...',
    show_attachment=True
) }}
```

#### Exemplo com Imagem

```jinja2
{{ chat_message(
    message='Aqui está a foto do produto',
    sender_name='Fornecedor',
    timestamp='11:00',
    is_own=True,
    attachment='/static/img/produto123.jpg',
    attachment_type='image',
    status='read'
) }}
```

---

## Hierarquia de Templates

```
base_root.html (HTML + Bootstrap + Scripts)
├── base_authenticated.html (Navbar + Footer + Toasts)
│   ├── cliente/base.html
│   ├── prestador/base.html
│   ├── fornecedor/base.html (+ Sidebar)
│   └── publico/base.html
└── publico/base2.html (Versão simplificada)
    └── administrador/base_admin.html
```

---

## Boas Práticas

### 1. Sempre Importe os Macros

```jinja2
{# CORRETO #}
{% from 'components/product_card.html' import product_card %}
{{ product_card(produto) }}

{# INCORRETO - Não funciona #}
{% include 'components/product_card.html' %}
```

### 2. Use Parâmetros Nomeados

```jinja2
{# CORRETO - Mais legível #}
{{ product_card(produto, show_actions=False, card_class='mb-3') }}

{# EVITAR - Menos legível #}
{{ product_card(produto, False, '', None, 'confirmDelete', True) }}
```

### 3. Valide Dados Antes de Passar

```jinja2
{# CORRETO #}
{% if produtos %}
    {% for produto in produtos %}
        {{ product_card(produto) }}
    {% endfor %}
{% else %}
    {{ empty_state(...) }}
{% endif %}
```

### 4. Use CSS Classes do Bootstrap

```jinja2
{# CORRETO - Usa classes Bootstrap #}
{{ product_card(produto, card_class='shadow-sm') }}

{# EVITAR - Estilos inline #}
<div style="box-shadow: 0 2px 4px rgba(0,0,0,0.1)">
```

### 5. Documente Parâmetros Customizados

```python
# No backend, ao passar dados para template
return templates.TemplateResponse("page.html", {
    "request": request,
    "produtos": produtos,  # Lista de objetos Produto
    # Cada produto deve ter: id, nome, descricao, preco, foto (opcional)
})
```

---

## Exemplos Completos

### Exemplo 1: Página de Listagem de Produtos

```jinja2
{% extends "fornecedor/base.html" %}

{% from 'components/product_card.html' import product_card %}
{% from 'components/search_form.html' import search_form %}
{% from 'components/empty_state.html' import empty_state %}
{% from 'components/breadcrumbs.html' import breadcrumbs %}
{% from 'components/confirmation_modal.html' import confirmation_modal %}

{% block fornecedor_titulo %}Meus Produtos{% endblock %}
{% block sidebar_active %}produtos{% endblock %}

{% block fornecedor_conteudo %}
<div class="container-fluid px-4">
    <!-- Breadcrumbs -->
    {{ breadcrumbs([
        {'label': 'Home', 'url': '/fornecedor/home'},
        {'label': 'Produtos'}
    ]) }}

    <!-- Busca -->
    {{ search_form(
        action='/fornecedor/produtos/buscar',
        fields=[
            {'name': 'id', 'type': 'number', 'label': 'ID', 'placeholder': 'ID'},
            {'name': 'nome', 'type': 'text', 'label': 'Nome', 'placeholder': 'Nome'}
        ],
        clear_url='/fornecedor/produtos'
    ) }}

    <!-- Lista -->
    {% if produtos %}
    <div class="products-grid">
        {% for produto in produtos %}
            {{ product_card(produto) }}
        {% endfor %}
    </div>
    {% else %}
    {{ empty_state(
        icon='box-seam',
        title='Nenhum produto',
        description='Cadastre seu primeiro produto',
        action_url='/fornecedor/produtos/criar',
        action_text='Criar Produto'
    ) }}
    {% endif %}
</div>

<!-- Modal -->
{{ confirmation_modal(
    modal_id='deleteModal',
    title='Excluir Produto',
    icon='trash',
    icon_class='text-danger',
    message='<p>Confirma exclusão?</p>',
    confirm_text='Excluir',
    confirm_class='btn-danger'
) }}
{% endblock %}
```

### Exemplo 2: Formulário Completo

```jinja2
{% extends "fornecedor/base.html" %}

{% from 'components/form_input.html' import text_input, textarea_input, select_input, file_input %}
{% from 'components/breadcrumbs.html' import breadcrumbs %}

{% block fornecedor_titulo %}Cadastrar Produto{% endblock %}

{% block fornecedor_conteudo %}
<div class="container-fluid px-4">
    {{ breadcrumbs([
        {'label': 'Home', 'url': '/fornecedor/home'},
        {'label': 'Produtos', 'url': '/fornecedor/produtos'},
        {'label': 'Cadastrar'}
    ]) }}

    <form method="POST" enctype="multipart/form-data">
        {{ text_input(
            name='nome',
            label='Nome do Produto',
            placeholder='Ex: Cimento CP-II',
            required=True,
            icon='box-seam'
        ) }}

        {{ textarea_input(
            name='descricao',
            label='Descrição',
            rows=4,
            placeholder='Descreva o produto...'
        ) }}

        {{ text_input(
            name='preco',
            label='Preço',
            type='number',
            placeholder='0.00',
            required=True,
            icon='currency-dollar'
        ) }}

        {{ select_input(
            name='categoria',
            label='Categoria',
            options=[
                {'value': '1', 'label': 'Construção'},
                {'value': '2', 'label': 'Acabamento'}
            ],
            required=True
        ) }}

        {{ file_input(
            name='foto',
            label='Foto',
            accept='image/*',
            help_text='Máximo 5MB'
        ) }}

        <button type="submit" class="btn btn-primary">
            <i class="bi bi-check-circle me-2"></i>Cadastrar
        </button>
    </form>
</div>
{% endblock %}
```

---

## Conclusão

Este guia documenta todos os componentes disponíveis. Para suporte adicional:

1. Veja os arquivos fonte em `templates/components/`
2. Consulte exemplos em templates refatorados
3. Revise a documentação Bootstrap 5.3

**Última atualização:** 21/10/2025
**Mantido por:** Equipe de Desenvolvimento OBRATTO
