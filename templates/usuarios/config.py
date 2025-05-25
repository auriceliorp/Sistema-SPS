"""
Configurações específicas para o módulo de usuários.
"""

# Configurações de upload de fotos
FOTO_UPLOAD_FOLDER = 'static/uploads/fotos'
FOTO_ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
FOTO_MAX_SIZE = 5 * 1024 * 1024  # 5MB

# Configurações de senha
SENHA_MIN_LENGTH = 8
SENHA_MAX_LENGTH = 32
SENHA_REGEX = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
SENHA_REGEX_MSG = 'A senha deve conter pelo menos 8 caracteres, incluindo maiúsculas, minúsculas, números e caracteres especiais'

# Perfis de usuário
PERFIL_ADMIN = 'admin'
PERFIL_GESTOR = 'gestor'
PERFIL_USUARIO = 'usuario'

PERFIS = [
    (PERFIL_ADMIN, 'Administrador'),
    (PERFIL_GESTOR, 'Gestor'),
    (PERFIL_USUARIO, 'Usuário')
]

# Permissões
PERMISSOES = {
    'usuarios': {
        'listar': 'Listar Usuários',
        'criar': 'Criar Usuários',
        'editar': 'Editar Usuários',
        'excluir': 'Excluir Usuários',
        'visualizar': 'Visualizar Usuários'
    },
    'itens': {
        'listar': 'Listar Itens',
        'criar': 'Criar Itens',
        'editar': 'Editar Itens',
        'excluir': 'Excluir Itens',
        'visualizar': 'Visualizar Itens'
    },
    'movimentacoes': {
        'entrada': 'Registrar Entrada',
        'saida': 'Registrar Saída',
        'visualizar': 'Visualizar Movimentações',
        'relatorios': 'Gerar Relatórios'
    },
    'setores': {
        'listar': 'Listar Setores',
        'criar': 'Criar Setores',
        'editar': 'Editar Setores',
        'excluir': 'Excluir Setores',
        'visualizar': 'Visualizar Setores'
    }
}

# Configurações de paginação
USUARIOS_POR_PAGINA = 25

# Configurações de log
LOG_ACOES = {
    'login': 'Login no Sistema',
    'logout': 'Logout do Sistema',
    'criar': 'Criação de Usuário',
    'editar': 'Edição de Usuário',
    'excluir': 'Exclusão de Usuário',
    'alterar_senha': 'Alteração de Senha',
    'redefinir_senha': 'Redefinição de Senha',
    'bloquear': 'Bloqueio de Usuário',
    'desbloquear': 'Desbloqueio de Usuário'
}

# Mensagens
MENSAGENS = {
    'criar_sucesso': 'Usuário criado com sucesso!',
    'editar_sucesso': 'Usuário atualizado com sucesso!',
    'excluir_sucesso': 'Usuário excluído com sucesso!',
    'senha_alterada': 'Senha alterada com sucesso!',
    'senha_redefinida': 'Uma nova senha foi enviada para o e-mail do usuário.',
    'usuario_bloqueado': 'Usuário bloqueado com sucesso!',
    'usuario_desbloqueado': 'Usuário desbloqueado com sucesso!',
    'erro_criar': 'Erro ao criar usuário. Por favor, tente novamente.',
    'erro_editar': 'Erro ao atualizar usuário. Por favor, tente novamente.',
    'erro_excluir': 'Erro ao excluir usuário. Por favor, tente novamente.',
    'erro_senha': 'Erro ao alterar senha. Por favor, tente novamente.',
    'erro_foto': 'Erro ao fazer upload da foto. Por favor, tente novamente.',
    'erro_permissao': 'Você não tem permissão para realizar esta ação.',
    'erro_usuario_inexistente': 'Usuário não encontrado.',
    'erro_email_existente': 'Este e-mail já está em uso.',
    'erro_senha_atual': 'Senha atual incorreta.',
    'erro_senhas_diferentes': 'As senhas não conferem.',
    'erro_formato_foto': 'Formato de arquivo não permitido. Use apenas: {}'.format(
        ', '.join(FOTO_ALLOWED_EXTENSIONS)
    ),
    'erro_tamanho_foto': 'A foto deve ter no máximo {}MB'.format(
        FOTO_MAX_SIZE / (1024 * 1024)
    )
} 