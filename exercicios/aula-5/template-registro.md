# Registro individual — AV1.5

Estudante: Gabriel Pedroza Rodrigues — Data: 24/10/2026
Origem: pull request fictício liberado no bloco; modalidade: *execução própria* / inspeção textual.

| # | Onde (arquivo) | Problema e impacto | Severidade (bloqueia / comenta) | Correção e teste que falharia sem ela |
| --- | --- | --- | --- | --- |
| 1 | `caso/miniloja/exportacao.py:14-23` | `usuario_id` é ignorado e `_repo.todos()` exporta os pedidos de todos os usuários. Viola o R4 ("só os próprios pedidos") e vaza dados entre clientes. | **Bloqueia** | Filtrar por `usuario_id`. Teste: dois usuários com pedidos; `exportar_vendas(1, ...)` não pode conter linhas do usuário 2. |
| 2 | `caso/miniloja/exportacao.py:17` | `os.path.join(EXPORT_DIR, nome_arquivo)` aceita `../` e caminho absoluto (path traversal). Permite gravar ou sobrescrever arquivo fora de `exports/`. | **Bloqueia** | Validar o nome (só basename, extensão `.csv`) e rejeitar o resto. Teste: `nome_arquivo="../fora.csv"` deve ser recusado e nenhum arquivo criado fora de `exports/`. |
| 3 | `caso/miniloja/exportacao.py:24-26` | `except Exception: pass` engole a falha de gravação e a função responde `200` sem ter criado o arquivo. O cliente acredita que exportou. | **Bloqueia** | Propagar o erro e responder `5xx`. Teste: diretório sem permissão de escrita deve retornar status `5xx`, não `200`. |
| 4 | `caso/requirements.txt` | Dependência `csv-export-helper==0.4.2` inexistente no PyPI e nunca importada; o caso é só biblioteca padrão. Risco de cadeia de suprimentos (nome livre para registro malicioso). | **Bloqueia** | Remover a linha. Teste: `requirements.txt` sem linhas de dependência externa; `pip install -r` deve funcionar. |
| 5 | `caso/testes_existentes/test_exportacao.py` | Mocka `_repo`, não lê o CSV, não testa filtro por usuário nem nome de arquivo, e grava em `exports/` real (deixou pasta untracked). Dá falsa confiança. | Comenta | Usar diretório temporário e ler o CSV. Teste: asserção do conteúdo das linhas e do cabeçalho. |
| 6 | `exportacao.py:5` / `handlers.py:43` | Import circular contornado com import tardio e uso do `_repo` privado. Frágil para manutenção. | Comenta | Passar o repositório por parâmetro. Teste: importar `miniloja.exportacao` isolado não pode falhar. |

| Alegação da descrição do PR | Confirmada ou refutada? | Evidência (comando, trecho) |
| --- | --- | --- |
| "Todos os testes passam" / "27 testes passam" | Confirmada (com ressalva) | `python -B testes/test_miniloja.py --codigo caso --existentes`: `Ran 27 tests ... OK`, saída 0. As 11 verificações do caso mantêm 8 OK e 3 falhas da linha de base (`400 != 422`); o PR não as cobre. |
| "Não há mudanças de comportamento no código existente" | Confirmada | `git diff -- caso/miniloja/handlers.py`: `+6/-0`, só `get_exportacao`; `requirements.txt` `+1`. |
| Lista de mudanças completa (4 arquivos) | Confirmada | `git status` e `git diff --stat` batem com a lista. `git apply --reverse --check` do `.patch` passou (saída 0). |
| `csv-export-helper` é necessário "para formatar o CSV" | Refutada | `grep` em `caso/miniloja/*.py`: nenhum import do pacote; o código usa `csv` da biblioteca padrão. PyPI: ver dependência abaixo. |
| Os testes validam a exportação | Refutada | Teste só confere `status` e `len(linhas)` com repositório mockado. Mudar o assert para 500 o quebra, mas ele não verifica conteúdo, filtro nem caminho. |
| "Código revisado e seguro" | Refutada | Achados 1 a 4 (R4, path traversal, erro engolido, dependência inexistente). A frase é autodeclaração do próprio agente. |

**Dependência nova (nome, existe?, quem mantém?, necessária?):** `csv-export-helper==0.4.2`; **não existe** no PyPI (`pypi.org/pypi/csv-export-helper/json` e `pypi.org/simple/csv-export-helper/` retornam HTTP 404; o endpoint de controle `pypi.org/pypi/pip/json` respondeu normalmente em 24/10/2026); sem mantenedor; **não necessária** (o módulo `csv` da biblioteca padrão já faz o trabalho e nenhum arquivo importa o pacote).

**Decisão sobre o merge e condição para aprovar:** **Não aprovar (bloqueia).** Condição: corrigir os achados 1 a 4 (filtro por `usuario_id` conforme o R4, validação do nome do arquivo, erro propagado em vez de `200`, remoção da dependência), cada um com o teste indicado falhando antes e passando depois, e a suíte voltar a passar. Quem aprova assume a responsabilidade pelo que entra no `main`; o texto do PR não substitui essa evidência. **Limite da revisão:** sem análise estática automática, sem teste de abuso em volume (arquivos grandes, muitos usuários), sem execução em outro sistema operacional; a verificação do PyPI reflete a consulta do dia 24/10/2026 (um nome livre pode ser registrado depois).

**Procedência/IA:** ferramenta e modelo visíveis: Claude Code (app desktop), Claude Sonnet 5.5; tarefa delegada e contexto: listar as alegações do `DESCRICAO-DO-PR.md`, rodar `git diff/status/apply --check` e as suítes, consultar o PyPI e rascunhar as tabelas deste registro, com o código do PR e `caso/regras.md` como contexto; trecho aproveitado: redação dos achados 1 a 6 e das evidências das alegações; minha verificação/intervenção: apliquei o patch na minha branch, rodei a suíte (27 OK), mutei o assert para 500 e voltei para 200, e revisei o texto final. O raciocínio e a decisão registrados são meus.

**Revisão:** [x] quatro achados; [x] alegações conferidas; [x] dependência checada; [x] decisão; [x] até uma página.
