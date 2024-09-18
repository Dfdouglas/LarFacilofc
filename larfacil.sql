CREATE DATABASE IF NOT EXISTS larfacil;
USE larfacil;

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    senha VARCHAR(255),
    tipo ENUM('locador', 'locatario')
);

CREATE TABLE locador (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

CREATE TABLE locatario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

CREATE TABLE imoveis (
    id INT AUTO_INCREMENT PRIMARY KEY,
    descricao VARCHAR(255),
    valor_aluguel DECIMAL(10, 2),
    locador_id INT,
    FOREIGN KEY (locador_id) REFERENCES locador(id)
);

CREATE TABLE aluguel (
    id INT AUTO_INCREMENT PRIMARY KEY,
    imovel_id INT,
    locatario_id INT,
    FOREIGN KEY (imovel_id) REFERENCES imoveis(id),
    FOREIGN KEY (locatario_id) REFERENCES locatario(id),
    data_inicio DATE,
    data_fim DATE
);