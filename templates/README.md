# Estrutura de Templates do Sistema de Almoxarifado

Este diretório contém todos os templates HTML do sistema, organizados em subdiretórios por funcionalidade.

## Estrutura de Diretórios

### Templates Base
- `/base/` - Templates base e utilitários
  - `base.html` - Template base com menu lateral
  - `base_simplificada.html` - Template base sem menu
  - `base_impressao.html` - Template base para impressão
  - `index.html` - Página inicial
  - `em_construcao.html` - Página de funcionalidade em desenvolvimento
  - `verificar_dados.html` - Página de verificação de dados

### Autenticação e Usuários
- `/usuarios/` - Templates relacionados a autenticação
  - `login.html` - Tela de login
  - `esqueci_senha.html` - Recuperação de senha
  - `trocar_senha.html` - Alteração de senha
  - `list.html` - Lista de usuários
  - `form.html` - Formulário de usuário

### Dashboard e Telas Principais
- `/painel/` - Templates de dashboard
  - `home.html` - Dashboard principal (admin)
  - `home_solicitante.html` - Dashboard do solicitante
  - `home_consultor.html` - Dashboard do consultor
  - `almoxarifado.html` - Gestão do almoxarifado
  - `links_uteis.html` - Links úteis

### Gestão de Itens
- `/itens/` - Templates de itens
  - `list.html` - Lista de itens
  - `form.html` - Formulário de item
  - `detail.html` - Detalhes do item

### Movimentações
- `/entradas/` - Templates de entrada de material
  - `list.html` - Lista de entradas
  - `form.html` - Formulário de entrada
  - `detail.html` - Detalhes da entrada
  - `print.html` - Impressão de entrada

- `/saidas/` - Templates de saída de material
  - `list.html` - Lista de saídas
  - `form.html` - Formulário de saída
  - `detail.html` - Detalhes da saída
  - `print.html` - Impressão de saída

### Relatórios
- `/relatorios/` - Templates de relatórios
  - `mensal_nd.html` - Relatório mensal por ND
  - `inventario.html` - Relatório de inventário

### Cadastros Auxiliares
- `/naturezas_despesa/` - Templates de NDs
  - `list.html` - Lista de NDs
  - `form.html` - Formulário de ND
  - `saldo.html` - Saldo por ND

- `/fornecedor/` - Templates de fornecedores
  - `list.html` - Lista de fornecedores
  - `form.html` - Formulário de fornecedor
  - `detail.html` - Detalhes do fornecedor

### Componentes
- `/partials/` - Componentes parciais reutilizáveis
  - `sidebar.html` - Menu lateral
  - `header.html` - Cabeçalho
  - `footer.html` - Rodapé

## Padrões de Nomenclatura

Os templates seguem um padrão de nomenclatura consistente:
- `list.html` - Listagem de registros
- `form.html` - Formulário (novo/edição)
- `detail.html` - Visualização detalhada
- `print.html` - Versão para impressão 