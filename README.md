# Sistema de Almoxarifado

Sistema para gerenciamento de almoxarifado desenvolvido em Python/Flask.

## Estrutura do Projeto

```
.
├── app/
│   ├── blueprints/
│   │   ├── admin/
│   │   ├── almoxarifado/
│   │   │   ├── entrada/
│   │   │   │   ├── __init__.py
│   │   │   │   └── routes.py
│   │   │   ├── saida/
│   │   │   │   ├── __init__.py
│   │   │   │   └── routes.py
│   │   │   ├── __init__.py
│   │   │   └── routes.py
│   │   ├── auth/
│   │   ├── main/
│   │   ├── patrimonio/
│   │   └── relatorios/
│   ├── models/
│   ├── services/
│   ├── static/
│   ├── templates/
│   │   ├── admin/
│   │   ├── auth/
│   │   ├── entrada/
│   │   │   ├── form.html
│   │   │   ├── list.html
│   │   │   ├── detail.html
│   │   │   └── print.html
│   │   ├── saidas/
│   │   │   ├── form.html
│   │   │   ├── list.html
│   │   │   ├── detail.html
│   │   │   └── print.html
│   │   ├── patrimonio/
│   │   ├── relatorios/
│   │   └── base.html
│   ├── utils/
│   ├── __init__.py
│   └── config.py
├── migrations/
├── tests/
├── .env
├── .gitignore
├── config.py
├── requirements.txt
└── wsgi.py
```

## Funcionalidades

### Módulo de Almoxarifado

#### Entradas
- Cadastro de entradas de material
- Listagem com filtros e paginação
- Visualização detalhada
- Impressão de comprovante
- Edição e exclusão (apenas para entradas não finalizadas)

#### Saídas
- Cadastro de saídas de material
- Listagem com filtros e paginação
- Visualização detalhada
- Impressão de requisição
- Edição e exclusão (apenas para saídas não finalizadas)

### Módulo de Patrimônio
- Cadastro de bens patrimoniais
- Movimentação de bens
- Relatórios de inventário

### Módulo de Relatórios
- Mapa de fechamento mensal
- Relatório de movimentação por natureza de despesa
- Relatório de estoque

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/sistema-almoxarifado.git
cd sistema-almoxarifado
```

2. Crie um ambiente virtual e ative-o:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

5. Inicialize o banco de dados:
```bash
flask db upgrade
```

6. Execute o servidor de desenvolvimento:
```bash
flask run
```

## Tecnologias Utilizadas

- Python 3.8+
- Flask
- SQLAlchemy
- Bootstrap 5
- jQuery
- DataTables
- Font Awesome

## Contribuição

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Faça commit das suas alterações (`git commit -m 'Adiciona nova feature'`)
4. Faça push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes. 