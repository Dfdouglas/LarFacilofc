import mysql.connector

def conectar():
    conexao = mysql.connector.connect(
        host="127.0.0.1",  # Mantenha "localhost" se o banco estiver localmente
        user="root",  # Substitua pelo seu usuário do MySQL
        password="190928",  # Substitua pela sua senha do MySQL
        database="larfacil"  # Nome do banco de dados
    )
    return conexao