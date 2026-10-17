# Registro individual — AV1.1

Estudante: Gabriel Pedroza — Data: 16/10/2026
Origem: tarefas T1–T3 fictícias do enunciado; modalidade: **execução própria**

| Tarefa | Modo | Tempo até 1ª versão | Tempo até pronto e verificado | Idas e vindas | % corrigido à mão | O que a IA errou | Como verifiquei |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T1 | A: plano revisado antes de editar (modo plano), depois execução | ≈ 3 min (início 21:25; `cadastro.py` gravado às 21:28:07) | ≈ 5 min, estimativa (as suítes rodaram após 21:28:07, sem hora registrada) | 1 pedido, 1 plano aprovado, 1 reexecução | 0% (código aplicado sem edição manual) | Não leu `caso/testes_existentes/` antes de editar: ao trocar `400` por `422` e exigir `cpf`, 2 dos 26 testes existentes passaram a falhar (`test_cadastro_sem_nome_e_rejeitado` espera `400`; `test_cadastro_valido` dá `422 != 201`, causa provável payload sem `cpf`, não confirmada). | Li R3 de `caso/regras.md`; rodei as 11 verificações (todas `ok`, v08–v10 antes falhavam) e a suíte existente (`FAILED (failures=2)`). Não rodei os CPFs de `caso/dados/cpfs.json` fora dos testes. |
| T1 | B: execução direta, sem plano revisado antes de editar | ≈ 2 min (início 21:32; `cadastro.py` gravado às 21:33:57) | não concluído: v10 ainda falha (v08/v09 passam); sem hora registrada para as execuções dos testes | 1 pedido, 0 planos, 1 pergunta da IA (fechar v10?), 1 reexecução (`python` do Git Bash apontava para a Store; usei `py -3`) | 0% (código aplicado sem edição manual) | Não leu `caso/testes_existentes/` nem rodou a suíte existente: a troca de `400` por `422` e a exigência de `cpf` provavelmente quebram os mesmos testes existentes vistos em A (não verificado em B). Deixou a v10 de fora: coletou todos os erros, mas não validou o formato do e-mail (R3.3). | Rodei as 11 verificações: 10 `ok`, v10 `FAIL` (`['cpf', 'nome'] != ['cpf', 'email', 'nome']`). Não rodei a suíte existente nem `caso/dados/cpfs.json`. |
| T2 | Plano revisado (modo plano) antes de editar; a IA leu `regras.md`, `cadastro.py`, `handlers.py` e `test_cadastro.py` e rodou as verificações antes de propor | ≈ 1 min após o início (início 21:40; `cadastro.py` gravado às 21:40:40) | ≈ 2 min, estimativa (`test_cadastro.py` gravado às 21:40:43; as suítes rodaram depois, sem hora registrada) | 1 pedido, 1 plano aprovado, 0 reexecuções do pedido | 0% (código aplicado sem edição manual) | Partiu do `422` e do CPF já presentes (alteração minha, não commitada) e só a v10 falhava: o e-mail era checado por presença, não por formato (R3.3). Dois testes existentes precisaram de ajuste ao contrato: `test_cadastro_sem_nome_e_rejeitado` (`400` → `422`) e `test_cadastro_valido` (incluído CPF válido de `cpfs.json`). Esses ajustes foram a IA que decidiu; o motivo (contrato `400` → `422`) está previsto em `exercicios/aula-1/README.md`. | `py -3 -B testes/test_miniloja.py --codigo caso`: 11 `ok` (v10 antes: `['cpf', 'nome'] != ['cpf', 'email', 'nome']`); `--existentes`: 26 `ok`. Não testei e-mails de borda (espaços, múltiplos `@`) fora dos testes. |

**Trecho essencial de evidência (comando e saída que sustentam "verificado"):** 
py -B testes/test_miniloja.py --codigo caso
test_v01_total_simples_em_pe (__main__.TestMiniLoja.test_v01_total_simples_em_pe) ... ok
test_v02_cupom_promo10_aplica_dez_por_cento (__main__.TestMiniLoja.test_v02_cupom_promo10_aplica_dez_por_cento) ... ok
test_v03_cupom_fretegratis_zera_o_frete (__main__.TestMiniLoja.test_v03_cupom_fretegratis_zera_o_frete) ... ok
test_v04_pedido_bem_acima_de_200_nao_paga_frete (__main__.TestMiniLoja.test_v04_pedido_bem_acima_de_200_nao_paga_frete) ... ok
test_v05_pedido_sem_itens_e_rejeitado (__main__.TestMiniLoja.test_v05_pedido_sem_itens_e_rejeitado) ... ok
test_v06_estoque_insuficiente_responde_409 (__main__.TestMiniLoja.test_v06_estoque_insuficiente_responde_409) ... ok
test_v07_cadastro_com_cpf_valido_e_aceito (__main__.TestMiniLoja.test_v07_cadastro_com_cpf_valido_e_aceito) ... ok
test_v08_cpf_com_digito_verificador_errado (__main__.TestMiniLoja.test_v08_cpf_com_digito_verificador_errado) ... ok
test_v09_cpf_com_todos_os_digitos_iguais (__main__.TestMiniLoja.test_v09_cpf_com_todos_os_digitos_iguais) ... ok
test_v10_payload_invalido_lista_todos_os_erros (__main__.TestMiniLoja.test_v10_payload_invalido_lista_todos_os_erros) ... ok
test_v11_cadastro_valido_recebe_identificador (__main__.TestMiniLoja.test_v11_cadastro_valido_recebe_identificador) ... ok

----------------------------------------------------------------------
Ran 11 tests in 0.008s

**T3 (hipotética): raio de impacto** médio: produção às 02h é pouco utilizada, o que limita o dano, mas não o elimina; **oráculo disponível** parcial: consigo conferir o que a IA lê (logs, métricas); **permissões que concederia** somente leitura; **modo e por quê** agente somente leitura, porque o sistema em produção é crítico demais para permitir escrita e, com oráculo parcial, eu não conseguiria verificar uma alteração antes que ela tivesse efeito.

**Alternativa para T1:** completar no editor, com a IA sugerindo trechos e eu decidindo cada edição, em vez de agente com plano (A) ou sem plano (B). 
**Comparação com minha escolha (restrição e consequência):** nos dois modos de agente a IA editou sem ler `caso/testes_existentes/`; em A o plano revisado me deixou ver o escopo antes da edição, mas os 2 testes existentes quebraram do mesmo jeito. Em B, sem plano, a v10 ficou de fora e T1 não foi concluído. Completar no editor limitaria a mudança a um arquivo por vez, ao custo de mais idas e vindas e mais edição à mão. **Limite da comparação e condição para rever a escolha:** uma execução por modo não prova nada sobre a ferramenta; os tempos são estimados, B parou antes de v10 e a ordem A→B pode ter ajudado B. Reveria a escolha se, em tarefas futuras, o agente voltar a editar sem rodar a suíte existente: nesse caso exigiria plano que inclua essa suíte antes de editar.

**Procedência/IA:** ferramenta e modelo visíveis: Claude Code; modelo das execuções originais: não informado (o código de `caso/` foi refeito depois com Claude Code, Sonnet 5.5, e as duas suítes passam); tarefa delegada e contexto: T1 (modos A e B) e T2, com acesso ao repositório do caso; trecho aproveitado: alterações em `caso/miniloja/cadastro.py` e, em T2, nos dois testes existentes, aplicadas sem edição manual; minha verificação/intervenção: rodei as 11 verificações e, quando indicado, a suíte existente, e decidi o modo e as permissões de T3. Respostas simuladas de `apoio/respostas-simuladas/`: não utilizadas (execução própria). O raciocínio e a decisão registrados são meus.

**Revisão:** [x] dois modos em T1; [x] evidência localizada; [x] T3 decidida; [x] alternativa e limite; [x] até uma página.