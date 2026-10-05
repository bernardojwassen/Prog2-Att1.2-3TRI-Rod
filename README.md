# Prog2-Att1.2-3TRI-Rod

# Programação II — Exercícios 16 a 20

## 19 — Perguntas
- **URL:** `https://viacep.com.br/ws/{cep}/json/`
- **Método HTTP:** GET
- **Código de sucesso:** 200 (OK)
- **Formato dos dados:** JSON
- **Requisição x resposta:** a requisição é a mensagem enviada pelo cliente (método, URL, cabeçalhos e, às vezes, corpo) pedindo algo ao servidor; a resposta é o que o servidor devolve (código de status, cabeçalhos e corpo com os dados).

## 20 — Sistema de Tarefas (Flask + SQLite)
Rodar: `cd 20_sistema_tarefas && pip install flask && python app.py` e abrir http://127.0.0.1:5000

1. **Arquitetura cliente-servidor:** o navegador (cliente) carrega HTML/CSS/JS e usa `fetch` para pedir dados; o servidor Flask recebe as requisições HTTP, valida, acessa o SQLite e responde em JSON com o código de status adequado.
2. **Rotas/endpoints:**
   - `GET /` — página
   - `GET /api/tarefas` — lista (READ)
   - `POST /api/tarefas` — cadastra (CREATE)
   - `PUT /api/tarefas/<id>` — altera título ou conclui (UPDATE)
   - `DELETE /api/tarefas/<id>` — exclui (DELETE)
3. **Classe `Tarefa`:** representa a entidade (id, título, concluída). O título é encapsulado numa propriedade com validação (obrigatório, até 100 caracteres), e `to_dict()` converte o objeto para JSON.
4. **Estrutura de dados:** `listar()` devolve uma **lista** de objetos `Tarefa` na ordem de cadastro, que é a estrutura natural para exibir e percorrer as tarefas.
5. **Demonstração do CRUD:** adicionar pelo formulário, concluir/reabrir, editar e excluir pelos botões da tabela.
