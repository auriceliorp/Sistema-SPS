from datetime import datetime
from flask import render_template, request, send_file, url_for, flash, redirect
from flask_login import login_required
from app.blueprints.relatorios import bp
from app.services.relatorios import RelatoriosService
from app.models.item import Grupo
from app.models.patrimonio import GrupoPatrimonio
from app.models.user import Usuario
from app.utils.decorators import perfil_required

@bp.route('/')
@login_required
def index():
    """Página inicial de relatórios."""
    return render_template('relatorios/index.html')

@bp.route('/estoque', methods=['GET', 'POST'])
@login_required
@perfil_required(['ALMOXARIFE', 'ADMIN'])
def relatorio_estoque():
    """Relatório de estoque."""
    if request.method == 'POST':
        try:
            grupo_id = request.form.get('grupo_id', type=int)
            abaixo_minimo = request.form.get('abaixo_minimo') == 'on'
            
            df = RelatoriosService.gerar_relatorio_estoque(
                grupo_id=grupo_id,
                abaixo_minimo=abaixo_minimo
            )
            
            arquivo = RelatoriosService.exportar_para_excel(df, 'relatorio_estoque')
            return redirect(url_for('relatorios.download', arquivo=arquivo))
            
        except Exception as e:
            flash(f'Erro ao gerar relatório: {str(e)}', 'danger')
    
    grupos = Grupo.query.all()
    return render_template('relatorios/estoque.html', grupos=grupos)

@bp.route('/movimentacao', methods=['GET', 'POST'])
@login_required
@perfil_required(['ALMOXARIFE', 'ADMIN'])
def relatorio_movimentacao():
    """Relatório de movimentação."""
    if request.method == 'POST':
        try:
            data_inicio = datetime.strptime(request.form.get('data_inicio'), '%Y-%m-%d').date()
            data_fim = datetime.strptime(request.form.get('data_fim'), '%Y-%m-%d').date()
            tipo_movimento = request.form.get('tipo_movimento')
            
            relatorios = RelatoriosService.gerar_relatorio_movimentacao(
                data_inicio=data_inicio,
                data_fim=data_fim,
                tipo_movimento=tipo_movimento
            )
            
            # Exporta cada tipo de movimento
            arquivos = []
            for tipo, df in relatorios.items():
                arquivo = RelatoriosService.exportar_para_excel(
                    df, f'relatorio_movimentacao_{tipo}'
                )
                arquivos.append((tipo, arquivo))
            
            return render_template(
                'relatorios/download_multiplo.html',
                arquivos=arquivos
            )
            
        except Exception as e:
            flash(f'Erro ao gerar relatório: {str(e)}', 'danger')
    
    return render_template('relatorios/movimentacao.html')

@bp.route('/patrimonio', methods=['GET', 'POST'])
@login_required
@perfil_required(['PATRIMONIO', 'ADMIN'])
def relatorio_patrimonio():
    """Relatório de patrimônio."""
    if request.method == 'POST':
        try:
            grupo_bem = request.form.get('grupo_bem')
            detentor_id = request.form.get('detentor_id', type=int)
            localizacao = request.form.get('localizacao')
            
            df = RelatoriosService.gerar_relatorio_patrimonio(
                grupo_bem=grupo_bem,
                detentor_id=detentor_id,
                localizacao=localizacao
            )
            
            arquivo = RelatoriosService.exportar_para_excel(df, 'relatorio_patrimonio')
            return redirect(url_for('relatorios.download', arquivo=arquivo))
            
        except Exception as e:
            flash(f'Erro ao gerar relatório: {str(e)}', 'danger')
    
    grupos = GrupoPatrimonio.query.all()
    usuarios = Usuario.query.filter_by(ativo=True).all()
    return render_template(
        'relatorios/patrimonio.html',
        grupos=grupos,
        usuarios=usuarios
    )

@bp.route('/fornecedores', methods=['GET', 'POST'])
@login_required
@perfil_required(['ALMOXARIFE', 'ADMIN'])
def relatorio_fornecedores():
    """Relatório de fornecedores."""
    if request.method == 'POST':
        try:
            df = RelatoriosService.gerar_relatorio_fornecedores()
            arquivo = RelatoriosService.exportar_para_excel(df, 'relatorio_fornecedores')
            return redirect(url_for('relatorios.download', arquivo=arquivo))
            
        except Exception as e:
            flash(f'Erro ao gerar relatório: {str(e)}', 'danger')
    
    return render_template('relatorios/fornecedores.html')

@bp.route('/download')
@login_required
def download():
    """Download do arquivo de relatório."""
    arquivo = request.args.get('arquivo')
    if not arquivo:
        flash('Arquivo não especificado.', 'danger')
        return redirect(url_for('relatorios.index'))
    
    try:
        import os
        from app.extensions import app
        
        # Remove o prefixo /static/ se existir
        if arquivo.startswith('/static/'):
            arquivo = arquivo[8:]
        
        caminho = os.path.join(app.root_path, 'static', arquivo)
        return send_file(
            caminho,
            as_attachment=True,
            download_name=os.path.basename(arquivo)
        )
        
    except Exception as e:
        flash(f'Erro ao baixar arquivo: {str(e)}', 'danger')
        return redirect(url_for('relatorios.index')) 