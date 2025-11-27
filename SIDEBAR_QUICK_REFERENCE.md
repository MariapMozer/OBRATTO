# Quick Reference: Sidebar Implementation

## 🎯 O Que Foi Implementado

Um sidebar **colapsável** para páginas de fornecedor com **gradientes laranja** e **adaptação automática** do conteúdo.

---

## 📍 Localização dos Arquivos

```
/templates/fornecedor/base.html          ← JavaScript toggle + HTML checkbox
/templates/components/sidebar.html       ← Estrutura do sidebar
/static/css/home_fornecedor.css         ← Todos os estilos CSS
```

---

## 🎨 Cores Utilizadas

| Nome | Hex | Uso |
|------|-----|-----|
| Azul Primário | `#171370` | Fundo sidebar, gradiente principal |
| Laranja Secundário | `#E8894B` | Hover, gradiente |
| Laranja Claro | `#F5A767` | Gradiente secundário |
| Laranja Forte | `#D9722F` | Acentos fortes |

---

## 💻 Como Funciona

### 1️⃣ **Desktop (> 768px)**
```
┌─────────┬──────────────────────┐
│         │                      │
│ SIDEBAR │   CONTEÚDO PRINCIPAL │
│ 250px   │                      │
│         │                      │
└─────────┴──────────────────────┘
```

Quando colapsado:
```
┌───┬──────────────────────────────┐
│   │   CONTEÚDO PRINCIPAL          │
│ 70px (ícones apenas)             │
│   │                              │
└───┴──────────────────────────────┘
```

### 2️⃣ **Mobile (< 768px)**
```
Aberto:                     Fechado:
┌──────────┬───────┐       ┌─────────────┐
│ SIDEBAR  │       │       │             │
│ (overlay)│ CONT. │       │ CONTEÚDO    │
│          │       │       │             │
└──────────┴───────┘       └─────────────┘
```

---

## 🔄 Estados do Sidebar

### Aberto
- Largura: 250px
- Mostra: Ícone + Texto
- Margin-left do conteúdo: 250px

### Fechado
- Largura: 70px
- Mostra: Ícone apenas
- Margin-left do conteúdo: 70px

### Mobile Aberto
- Posicionamento: Fixed + left: 0
- Overlay: 75% da largura da tela
- Conteúdo não se move

### Mobile Fechado
- Posicionamento: Fixed + left: -100%
- Fora da tela
- Sem overlay

---

## 🎛️ Controlos

### Desktop
- Clique no ícone hamburger (se visível)
- Ou use o checkbox `#toggleSidebar`

### Mobile
- Clique no hamburguer no header
- Auto-fecha ao clicar item do menu
- Clique no conteúdo para fechar

---

## ⚙️ Variáveis CSS Principais

```css
:root {
    /* Cores */
    --cor-primaria: #171370;
    --cor-secundaria: #E8894B;
    
    /* Tamanhos do Sidebar */
    --sidebar-width: 250px;
    --sidebar-collapsed: 70px;
    
    /* Gradientes */
    --cor-gradiente-principal: linear-gradient(135deg, #171370 0%, #E8894B 100%);
    --cor-gradiente-secundaria: linear-gradient(135deg, #E8894B 0%, #F5A767 100%);
}
```

---

## 📝 JavaScript Essencial

```javascript
// Toggle sidebar
const checkbox = document.getElementById('toggleSidebar');
checkbox.checked = !checkbox.checked;

// Restaurar estado
const state = localStorage.getItem('sidebarOpen');
checkbox.checked = (state !== 'false');

// Salvar estado
localStorage.setItem('sidebarOpen', checkbox.checked);
```

---

## 🎨 Efeitos CSS

### Hover Item
```css
.sidebar-item:hover {
    background: var(--cor-gradiente-secundaria);  /* Laranja gradient */
    box-shadow: 0 4px 12px rgba(232, 137, 75, 0.3);
    padding-left: 1.25rem;  /* Slide effect */
}
```

### Active Item
```css
.sidebar-item.active {
    background: var(--cor-gradiente-principal);   /* Azul-laranja gradient */
    box-shadow: 0 6px 18px rgba(232, 137, 75, 0.4);
}
```

### Transições
```css
.sidebar {
    transition: width 0.3s ease;
}
.page-content {
    transition: margin-left 0.3s ease;
}
```

---

## 🔍 Seletores CSS Importantes

```css
/* Checkbox checked = sidebar aberto */
#toggleSidebar:checked ~ .sidebar { /* ... */ }

/* Checkbox unchecked = sidebar fechado */
#toggleSidebar:not(:checked) ~ .sidebar { /* ... */ }

/* Adaptar conteúdo */
.page-content.sidebar-open { margin-left: var(--sidebar-width); }
.page-content.sidebar-closed { margin-left: var(--sidebar-collapsed); }
```

---

## 📱 Media Queries

```css
/* Mobile responsividade */
@media (max-width: 768px) {
    .sidebar {
        position: fixed;
        left: -100%;           /* Off-screen por padrão */
        width: 75%;
        max-width: 250px;
    }
    
    #toggleSidebar:checked ~ .sidebar {
        left: 0;               /* On-screen quando checked */
    }
    
    .page-content {
        margin-left: 0;        /* Sem deslocamento */
    }
}
```

---

## 💾 LocalStorage

**Chave:** `sidebarOpen`
**Valores:** `'true'` ou `'false'`

Uso:
```javascript
// Salvar
localStorage.setItem('sidebarOpen', 'true');

// Recuperar
const isOpen = localStorage.getItem('sidebarOpen') !== 'false';
```

---

## 🧪 Teste Rápido

1. **Visual Test**: Abrir `sidebar_visual_test.html`
2. **Toggle**: Clique no botão "Toggle Sidebar"
3. **Hover**: Passe mouse nos itens (deve aparecer gradiente laranja)
4. **Persistência**: Refresh F5 (sidebar deve manter estado)
5. **Mobile**: Redimensionar para < 768px (sidebar vai para fora da tela)

---

## ❌ Troubleshooting

| Problema | Solução |
|----------|---------|
| Sidebar não aparece | Verificar `z-index: 1000` |
| Não persiste estado | Limpar localStorage: `localStorage.clear()` |
| Conteúdo não se move | Verificar classe `sidebar-open/closed` em `.page-content` |
| Mobile sidebar visível | Verificar media query em 768px |
| Cores erradas | Verificar `--cor-*` variables em `:root` |
| Sem gradientes | Verificar browser suporta CSS gradients |

---

## 📚 Documentação Completa

- `SIDEBAR_IMPLEMENTATION.md` - Detalhes técnicos (Inglês)
- `SIDEBAR_IMPLEMENTATION_PT.md` - Guia completo (Português)
- `sidebar_visual_test.html` - Teste visual interativo

---

## 🚀 Próxima Etapa

Para integrar ao projeto:

1. ✅ Arquivos já estão modificados
2. ✅ CSS já está no `home_fornecedor.css`
3. ✅ JavaScript já está em `base.html`
4. Testar em `localhost:8000/fornecedor`
5. Verificar se todos os links do menu funcionam

---

**Status:** ✅ Pronto para produção
