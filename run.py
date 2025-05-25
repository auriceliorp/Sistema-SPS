import os
from app import create_app
from app.extensions import db
from app.models import Usuario, Perfil, Item, Grupo, NaturezaDespesa, \
    EntradaMaterial, EntradaItem, SaidaMaterial, SaidaItem, \
    Fornecedor, Local, UnidadeLocal, BemPatrimonial, GrupoPatrimonio, AuditLog

app = create_app(os.getenv('FLASK_ENV') or 'default')

@app.shell_context_processor
def make_shell_context():
    """Configura o contexto do shell Flask."""
    return {
        'db': db,
        'Usuario': Usuario,
        'Perfil': Perfil,
        'Item': Item,
        'Grupo': Grupo,
        'NaturezaDespesa': NaturezaDespesa,
        'EntradaMaterial': EntradaMaterial,
        'EntradaItem': EntradaItem,
        'SaidaMaterial': SaidaMaterial,
        'SaidaItem': SaidaItem,
        'Fornecedor': Fornecedor,
        'Local': Local,
        'UnidadeLocal': UnidadeLocal,
        'BemPatrimonial': BemPatrimonial,
        'GrupoPatrimonio': GrupoPatrimonio,
        'AuditLog': AuditLog
    }

if __name__ == '__main__':
    app.run() 