from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from db import conectar  # Importa a conexão do arquivo db.py

# Função para verificar o login
def verificar_login(email, senha):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    query = "SELECT * FROM usuarios WHERE email=%s AND senha=%s"
    cursor.execute(query, (email, senha))
    usuario = cursor.fetchone()
    cursor.close()
    conexao.close()
    return usuario

# Função para listar imóveis do locador
def listar_imoveis(locador_id):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    query = "SELECT * FROM imoveis WHERE locador_id=%s"
    cursor.execute(query, (locador_id,))
    imoveis = cursor.fetchall()
    cursor.close()
    conexao.close()
    return imoveis

# Função para listar o imóvel alugado pelo locatário
def listar_imovel_alugado(locatario_id):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    query = """
    SELECT i.* FROM imoveis i
    JOIN aluguel a ON i.id = a.imovel_id
    WHERE a.locatario_id = %s
    """
    cursor.execute(query, (locatario_id,))
    imovel = cursor.fetchone()
    cursor.close()
    conexao.close()
    return imovel

class Servidor(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/login':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            dados = json.loads(post_data)
            
            email = dados['email']
            senha = dados['senha']
            
            usuario = verificar_login(email, senha)
            
            if usuario:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(usuario).encode('utf-8'))
            else:
                self.send_response(401)
                self.end_headers()
                self.wfile.write(b'{"error": "Login falhou"}')

    def do_GET(self):
        if self.path.startswith('/imoveis'):
            locador_id = self.headers.get('Locador-ID')  # Esperando o ID do locador no cabeçalho
            imoveis = listar_imoveis(locador_id)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(imoveis).encode('utf-8'))

        elif self.path.startswith('/aluguel'):
            locatario_id = self.headers.get('Locatario-ID')  # Esperando o ID do locatário no cabeçalho
            imovel = listar_imovel_alugado(locatario_id)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(imovel).encode('utf-8'))

if __name__ == '__main__':
    servidor = HTTPServer(('localhost', 8080), Servidor)
    print("Servidor rodando na porta 8080...")
    servidor.serve_forever()