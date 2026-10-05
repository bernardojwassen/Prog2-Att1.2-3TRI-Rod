-- Exercício 16 — Consultas com JOIN (banco da biblioteca)
-- Esquema assumido (exercício 13):
CREATE TABLE autores (id_autor INTEGER PRIMARY KEY, nome VARCHAR(100) NOT NULL);
CREATE TABLE livros (
  id_livro INTEGER PRIMARY KEY, titulo VARCHAR(150) NOT NULL,
  id_autor INTEGER NOT NULL REFERENCES autores(id_autor),
  disponivel BOOLEAN NOT NULL DEFAULT 1);
CREATE TABLE usuarios (id_usuario INTEGER PRIMARY KEY, nome VARCHAR(100) NOT NULL, email VARCHAR(120));
CREATE TABLE emprestimos (
  id_emprestimo INTEGER PRIMARY KEY,
  id_usuario INTEGER NOT NULL REFERENCES usuarios(id_usuario),
  id_livro INTEGER NOT NULL REFERENCES livros(id_livro),
  data_emprestimo DATE NOT NULL, data_devolucao DATE);  -- NULL = não devolvido

-- 1. Nome do usuário e título do livro emprestado
SELECT u.nome, l.titulo
FROM emprestimos e
JOIN usuarios u ON u.id_usuario = e.id_usuario
JOIN livros   l ON l.id_livro   = e.id_livro;

-- 2. Todos os empréstimos realizados
SELECT e.id_emprestimo, u.nome AS usuario, l.titulo, e.data_emprestimo, e.data_devolucao
FROM emprestimos e
JOIN usuarios u ON u.id_usuario = e.id_usuario
JOIN livros   l ON l.id_livro   = e.id_livro
ORDER BY e.data_emprestimo;

-- 3. Empréstimos ainda não devolvidos
SELECT u.nome, l.titulo, e.data_emprestimo
FROM emprestimos e
JOIN usuarios u ON u.id_usuario = e.id_usuario
JOIN livros   l ON l.id_livro   = e.id_livro
WHERE e.data_devolucao IS NULL;

-- 4. Quantidade de empréstimos por usuário (LEFT JOIN inclui quem tem 0)
SELECT u.nome, COUNT(e.id_emprestimo) AS total_emprestimos
FROM usuarios u
LEFT JOIN emprestimos e ON e.id_usuario = u.id_usuario
GROUP BY u.id_usuario, u.nome;

-- 5. Livros que nunca foram emprestados
SELECT l.titulo
FROM livros l
LEFT JOIN emprestimos e ON e.id_livro = l.id_livro
WHERE e.id_emprestimo IS NULL;
