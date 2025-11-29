# Página de Mensagens do Fornecedor - Documentação

## 📋 Resumo
Implementação completa de uma página moderna de gerenciamento de mensagens para fornecedores, inspirada no design da home do fornecedor com layout profissional e responsivo.

## 🎨 Componentes Implementados

### 1. **Template HTML** (`templates/fornecedor/mensagens/recebidas.html`)
- **Cabeçalho**: Título e subtítulo descritivos
- **Sistema de Abas**: 3 tabs principais
  - Recebidas (com contador de mensagens)
  - Enviadas (empty state)
  - Arquivo (empty state)
- **Lista de Mensagens**:
  - Avatar do remetente
  - Nome e data da mensagem
  - Preview do conteúdo (2 linhas)
  - Ações rápidas (favoritar, arquivar, deletar)
  - Status visual (indicador de nova mensagem)
- **Cards de Informações**:
  - Conversa Rápida (com botão para nova mensagem)
  - Dicas (responder rapidamente melhora reputação)
- **Modal de Nova Conversa**:
  - Busca de destinatários com autocomplete
  - Campo de mensagem
  - Botão de envio

### 2. **Estilos CSS** (`static/css/mensagens_fornecedor.css`)
- **Cores**: Utiliza paleta da aplicação (azul escuro e laranjas)
- **Efeitos Visuais**:
  - Hover suave com bordas e sombras
  - Ícone animado na esquerda dos itens
  - Transições suaves em todas as ações
  - Scrollbar customizada
- **Responsividade**: 
  - 3 breakpoints (desktop, tablet, mobile)
  - Adaptações de tamanho de fonte e espaçamento
  - Em mobile, ações sempre visíveis
- **Animações**: Entrada suave dos itens com delay

### 3. **JavaScript Interativo** (`static/js/mensagens_fornecedor.js`)
- **Funcionalidades**:
  - Click em mensagens
  - Marcar como favorita (toggle com ícone)
  - Arquivar mensagens (com animação)
  - Deletar mensagens (com confirmação)
  - Sistema de toasts/notificações
  - Busca de destinatários (simulada)
  - Submissão de formulário com validação
- **UX Melhorada**:
  - Feedback visual para todas as ações
  - Desabilitação de botões durante envio
  - Auto-limpeza de listas vazias
  - Notificações toast com auto-dismiss

## 🎯 Características Principais

✅ **Design Moderno**: Inspirado no padrão do projeto
✅ **Responsivo**: Funciona em todos os tamanhos de tela
✅ **Interativo**: JavaScript para melhor UX
✅ **Acessível**: Semântica HTML adequada e ARIA labels
✅ **Animações**: Transições suaves e efeitos visuais
✅ **Integrável**: Pronto para conectar com backend

## 📱 Responsividade

- **Desktop (> 768px)**: Layout completo com ações ocultas no hover
- **Tablet (576px - 768px)**: Ajustes de espaçamento
- **Mobile (< 576px)**: Stack vertical, ações sempre visíveis

## 🔗 Integrações Backend Necessárias

O template espera os seguintes dados do backend:
- `usuario_logado`: Informações do usuário autenticado
- `mensagens`: Lista de mensagens com estrutura:
  ```python
  {
      'id_mensagem': int,
      'nome_remetente': str,
      'conteudo': str,
      'data_hora': datetime,
      'status': str  # opcional
  }
  ```

## 🎨 Paleta de Cores Utilizada

- **Primária**: #171370 (Azul Escuro)
- **Secundária**: #E8894B (Laranja)
- **Acentos**: #F5A767 (Laranja Claro), #FDB750 (Laranja Muito Claro)
- **Neutro**: #F8F9FA (Fundo Claro)

## 📋 Arquivos Criados/Modificados

| Arquivo | Status | Descrição |
|---------|--------|-----------|
| `templates/fornecedor/mensagens/recebidas.html` | ✏️ Modificado | Template principal |
| `static/css/mensagens_fornecedor.css` | ✨ Criado | Estilos customizados |
| `static/js/mensagens_fornecedor.js` | ✨ Criado | Lógica interativa |

## 🚀 Próximas Melhorias

- [ ] Conectar com API backend para envio de mensagens
- [ ] Implementar paginação para listas grandes
- [ ] Adicionar busca/filtro avançado
- [ ] Implementar sistema de notificações em tempo real
- [ ] Adicionar anexo de arquivos
- [ ] Implementar indicador de digitação
- [ ] Suporte para emojis
- [ ] Histórico de conversas completo

## 💡 Como Usar

1. A página está disponível em `/fornecedor/mensagens/recebidas`
2. Os arquivos CSS e JS são carregados automaticamente via template
3. Para testar, acesse como fornecedor autenticado
4. Todos os elementos são interativos no frontend

---
**Versão**: 1.0  
**Data**: 28 de Novembro de 2025
