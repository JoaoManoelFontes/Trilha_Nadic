-- # Criando o banco de dados
CREATE DATABASE Nadic;
USE Nadic;


-- #Criando a tabela de categoria
CREATE TABLE category(id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255) NOT NULL,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ,
updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP);


-- # Criando a tabela de livros
CREATE TABLE book(id INT AUTO_INCREMENT PRIMARY KEY, category_id INT,
title VARCHAR(255) NOT NULL,
synopsis TEXT,
author_name VARCHAR(255) NOT NULL,
publishing_company_name VARCHAR(255) NOT NULL,
release_year DATE NOT NULL, FOREIGN KEY (category_id) REFERENCES category(id),
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ,
updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP );


-- # Inserindo valores nas duas tabelas
INSERT INTO category (name) VALUES("Comédia"), ("Terror"), ("Romance"), ("Exemplo");

INSERT INTO book (category_id, title, synopsis, author_name, publishing_company_name, release_year)
VALUES("4", "titulo_exemplo", "sinópse_exemplo", "nome_autor_exemplo", "nome_editora_exemplo", "2000-10-10");

-- # Selecionando todos os livros e categorias
SELECT * FROM book;
SELECT * FROM category;


-- # Selecionando todos os livros e sua respectiva categoria
SELECT  title, category.name, synopsis, author_name, publishing_company_name, release_year
FROM book inner join category on category_id = category.id;


-- # Mostrando quantas vezes cada categoria foi atribuida a um livro
SELECT category.name, COUNT(*) AS total FROM book
inner join category on category_id = category.id GROUP BY category_id;


-- # Atualizando valores
UPDATE category SET name="Ex" WHERE id="4"


-- # Deletando valores
DELETE from category WHERE id="4";
DELETE from book WHERE id="1";