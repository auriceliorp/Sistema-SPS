import os
from app import create_app
from app.extensions import db
from app.models import (
    Usuario, Perfil, Item, Grupo, NaturezaDespesa,
    EntradaMaterial, EntradaItem, SaidaMaterial, SaidaItem,
    Fornecedor, Local, UnidadeLocal,
    BemPatrimonial, GrupoPatrimonio,
    AuditLog, Estoque
)

def init_db():
    # Garante que o diretório instance existe
    instance_path = os.path.abspath('instance')
    if not os.path.exists(instance_path):
        os.makedirs(instance_path)

    app = create_app()
    
    # Força o uso do SQLite local
    db_path = os.path.join(instance_path, 'app.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    
    with app.app_context():
        # Apaga o banco de dados se existir
        if os.path.exists(db_path):
            os.remove(db_path)
            print(f'Banco de dados antigo removido: {db_path}')
        
        print('Criando tabelas...')
        db.create_all()
        print('Tabelas criadas com sucesso!')
        
        print('Criando perfil de administrador...')
        try:
            admin_role = Perfil(nome='Administrador')
            db.session.add(admin_role)
            db.session.commit()
            print('Perfil de administrador criado com sucesso!')
        except Exception as e:
            print(f'Erro ao criar perfil: {str(e)}')
            db.session.rollback()
            admin_role = Perfil.query.filter_by(nome='Administrador').first()
            if not admin_role:
                print('Erro fatal: não foi possível criar ou recuperar o perfil de administrador')
                return
        
        print('Criando usuário administrador...')
        try:
            admin_user = Usuario.query.filter_by(email='admin@admin.com').first()
            if admin_user:
                print('Usuário administrador já existe!')
            else:
                admin_user = Usuario(
                    nome='Administrador',
                    email='admin@admin.com',
                    matricula='ADMIN',
                    perfil_id=admin_role.id
                )
                admin_user.set_password('admin123')
                db.session.add(admin_user)
                db.session.commit()
                print('Usuário administrador criado com sucesso!')
                print('Email: admin@admin.com')
                print('Senha: admin123')
        except Exception as e:
            print(f'Erro ao criar usuário: {str(e)}')
            db.session.rollback()

if __name__ == '__main__':
    init_db() 