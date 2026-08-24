# -*- coding: utf-8 -*-
"""
API de anexos (fotos/arquivos) dos chamados — Central Administrativa Delta.

Só existe pra isso: receber upload de arquivo do formulário de abertura de
chamado e do chat (painel.html / admin.html), salvar em disco na VPS e
devolver a URL. Os chamados, mensagens e status continuam 100% no Firestore,
como já era antes — esta API não lê nem escreve nada lá, exceto para
conferir se quem está enviando o arquivo tem permissão sobre o chamado
(dono do chamado ou técnico cadastrado em "admins").

Rodar em desenvolvimento:
    pip install -r requirements.txt
    cp .env.example .env   # preencher com o caminho da service account
    python app.py

Rodar em produção (VPS), atrás de Nginx:
    gunicorn app:app --bind 0.0.0.0:5001 --workers 2
"""
import os
import time
import uuid

from dotenv import load_dotenv
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename

import firebase_admin
from firebase_admin import credentials, auth, firestore

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

CREDENTIALS_FILE = os.environ.get('FIREBASE_CREDENTIALS_FILE', 'sistema-chamados-firebase-adminsdk.json')
ALLOWED_ORIGIN = os.environ.get('ALLOWED_ORIGIN', '*')
PORT = int(os.environ.get('PORT', '5001'))

MAX_ARQUIVOS = 5
MAX_TAMANHO_MB = 10
MAX_TAMANHO_BYTES = MAX_TAMANHO_MB * 1024 * 1024
PASTAS_VALIDAS = {'abertura', 'mensagens'}
EXTENSOES_PERMITIDAS = {
    'png': 'image/png', 'jpg': 'image/jpeg', 'jpeg': 'image/jpeg',
    'gif': 'image/gif', 'webp': 'image/webp',
    'pdf': 'application/pdf',
    'doc': 'application/msword',
    'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'xls': 'application/vnd.ms-excel',
    'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'txt': 'text/plain',
}

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = MAX_TAMANHO_BYTES * MAX_ARQUIVOS + (1 * 1024 * 1024)
CORS(app, resources={r"/api/*": {"origins": ALLOWED_ORIGIN}})

_cred_path = os.path.join(BASE_DIR, CREDENTIALS_FILE)
if not os.path.exists(_cred_path):
    raise RuntimeError(
        f'Credencial do Firebase Admin não encontrada em "{_cred_path}". '
        'Gere uma em Console do Firebase > Configurações do projeto > Contas de '
        'serviço > Gerar nova chave privada, salve nesta pasta e aponte o nome '
        'em FIREBASE_CREDENTIALS_FILE (.env).'
    )
firebase_admin.initialize_app(credentials.Certificate(_cred_path))
db_firestore = firestore.client()


class ErroRequisicao(Exception):
    def __init__(self, mensagem, status=400):
        super().__init__(mensagem)
        self.mensagem = mensagem
        self.status = status


@app.errorhandler(ErroRequisicao)
def _tratar_erro_requisicao(erro):
    return jsonify({'erro': erro.mensagem}), erro.status


def extensao_de(nome_arquivo):
    return nome_arquivo.rsplit('.', 1)[-1].lower() if '.' in nome_arquivo else ''


def usuario_autenticado():
    """Confere o token de ID do Firebase enviado em 'Authorization: Bearer <token>'.
    Levanta ErroRequisicao(401) se ausente/inválido. Retorna o uid."""
    cabecalho = request.headers.get('Authorization', '')
    if not cabecalho.startswith('Bearer '):
        raise ErroRequisicao('Token de autenticação ausente.', 401)
    token = cabecalho[len('Bearer '):].strip()
    try:
        decodificado = auth.verify_id_token(token)
    except Exception:
        raise ErroRequisicao('Token de autenticação inválido ou expirado.', 401)
    return decodificado['uid']


def usuario_pode_acessar_chamado(uid, chamado_id):
    """Autoriza só o dono do chamado ou um técnico (coleção 'admins') —
    o mesmo isolamento já usado nas regras do Firestore."""
    doc_admin = db_firestore.collection('admins').document(uid).get()
    if doc_admin.exists:
        return True
    doc_chamado = db_firestore.collection('chamados').document(chamado_id).get()
    if not doc_chamado.exists:
        raise ErroRequisicao('Chamado não encontrado.', 404)
    return doc_chamado.to_dict().get('ownerUid') == uid


@app.route('/api/chamados/<chamado_id>/anexos', methods=['POST'])
def enviar_anexos(chamado_id):
    uid = usuario_autenticado()
    if not usuario_pode_acessar_chamado(uid, chamado_id):
        raise ErroRequisicao('Você não tem permissão sobre este chamado.', 403)

    pasta = request.form.get('pasta', 'mensagens')
    if pasta not in PASTAS_VALIDAS:
        raise ErroRequisicao('Pasta de destino inválida.')

    arquivos = request.files.getlist('arquivo')
    if not arquivos:
        raise ErroRequisicao('Nenhum arquivo enviado.')
    if len(arquivos) > MAX_ARQUIVOS:
        raise ErroRequisicao(f'Máximo de {MAX_ARQUIVOS} arquivos por envio.')

    chamado_id_seguro = secure_filename(chamado_id)
    pasta_destino = os.path.join(UPLOAD_FOLDER, 'chamados', chamado_id_seguro, pasta)
    os.makedirs(pasta_destino, exist_ok=True)

    anexos_salvos = []
    for arquivo in arquivos:
        nome_original = arquivo.filename or ''
        ext = extensao_de(nome_original)
        if ext not in EXTENSOES_PERMITIDAS:
            raise ErroRequisicao(f'Tipo de arquivo não permitido: "{nome_original}".')

        arquivo.seek(0, os.SEEK_END)
        tamanho = arquivo.tell()
        arquivo.seek(0)
        if tamanho > MAX_TAMANHO_BYTES:
            raise ErroRequisicao(f'"{nome_original}" excede {MAX_TAMANHO_MB}MB.')

        nome_salvo = f'{int(time.time() * 1000)}_{uuid.uuid4().hex[:8]}_{secure_filename(nome_original)}'
        caminho_absoluto = os.path.join(pasta_destino, nome_salvo)
        arquivo.save(caminho_absoluto)

        caminho_relativo = f'chamados/{chamado_id_seguro}/{pasta}/{nome_salvo}'
        anexos_salvos.append({
            'nome': nome_original,
            'tipo': EXTENSOES_PERMITIDAS[ext],
            'tamanho': tamanho,
            'url': f'/uploads/{caminho_relativo}',
            'path': caminho_relativo,
        })

    return jsonify({'anexos': anexos_salvos})


@app.route('/uploads/<path:caminho_relativo>')
def servir_anexo(caminho_relativo):
    # Uso simples/direto: o Flask serve o arquivo salvo. Em produção, o Nginx
    # pode servir a pasta uploads/ diretamente (mais rápido) — ver README de
    # deploy — mas esta rota funciona sozinha sem depender disso.
    return send_from_directory(UPLOAD_FOLDER, caminho_relativo)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=True)
