# Registro individual — AV1.2

Estudante: Gabriel Pedroza Rodrigues — Data: 17/10/2026
Origem: `caso/miniloja/calculo.py` fictício; modalidade: execução própria.

**Golden master:** 504 entradas (9 carrinhos × 7 cupons × 4 UFs × flag NATAL 0/1); gerado por `caso/golden_master/golden_master.py gravar` sobre o código antes da refatoração; comparação exata por `==` sem tolerância, checando também o tipo (`golden_master.py comparar`). Resultado: 0 divergências antes e depois da rodada 1.

| Medida | Rodada 1 (sem escopo) | Rodada 2 (com escopo) |
| --- | --- | --- |
| Linhas adicionadas/removidas | 24 linhas a mais e 58 a menos | 29 a mais e 58 a menos |
| Arquivos alterados (e quais estavam fora do esperado) | 1 (`caso/miniloja/calculo.py`); nenhum fora do esperado | 1 (`caso/miniloja/calculo.py`); nenhum fora do esperado (`AGENTS.md` é entregável novo, na raiz) |
| Mudou comportamento? (golden master) | Não: 0 divergências em 504 entradas; verificações do caso 8/11 como no início, suíte existente 26/26 | Não: 0 divergências em 504 entradas; verificações do caso 8/11 |
| Tempo de revisão | ≈ 3 min (2 min 54 s): da entrega da refatoração até a conferência do golden master | ≈ 1 min (1 min 21 s): do início da rodada 2 até a conferência do golden master |
| Idas e vindas | 2 (1 pedido e 0 correções da refatoração, aceita na primeira entrega; a ida e vinda relacionada ao contexto foi rodar o golden master) | 3 (1 pedido de plano, 1 aprovação do plano, 1 execução); 0 correções da refatoração após a entrega |

**Escopo da rodada 2:** objetivo separar desconto, frete e taxa de `calcular_total` em funções privadas, usando as tabelas `FRETE_POR_UF`/`TAXA_POR_UF`; pode tocar só `caso/miniloja/calculo.py`; não pode tocar assinatura pública ou qualquer outro arquivo, diff só em `calculo.py`; pare e pergunte se achar algo que pareça bug ou divergência com o contrato, ou se precisar tocar outro arquivo ou mudar uma saída do golden master.

**Plano do agente: o que eu cortei ou corrigi antes de executar:** nada: o plano foi aprovado como escrito, sem cortes nem correções (plano: extrair `_subtotal`, `_aplicar_desconto`, `_calcular_frete`, `_aplicar_taxa`; manter `calcular_total`; rodar golden master. O plano já excluía: renomear API, type hints, mexer em testes, corrigir `> 200`/arredondamento, `Decimal`. Fora do plano, o agente também removeu a variável morta `desconto_aplicado`, que só notei na execução e aceitei por ser código sem efeito dentro do arquivo permitido.)

**Algo que parecia bug e eu apenas reportei:** (1) frete usa `total > 200`, mas R1.3 diz "maior ou igual a R$ 200,00".

**`AGENTS.md` mínimo:** criado na raiz, 5 linhas: comando das verificações e do golden master, limites (`testes/`, `regras.md`, `golden_master/`; só `calculo.py`), contrato acima do código, e a convenção não óbvia (golden master grava o comportamento atual; bug → reportar, não corrigir).

**Trecho essencial de evidência:** `golden_master.py comparar` → `0 divergência(s)`; `git diff --numstat` → `29 58 caso/miniloja/calculo.py`; suíte existente `Ran 26 tests ... OK`; verificações `Ran 11 tests ... FAILED (failures=3)` (mesmas 3 do início). **Limite e condição para rever o escopo:** o golden master só cobre 9 carrinhos × 7 cupons × 4 UFs × flag; entradas fora dessa grade (UF minúscula, preço negativo, itens malformados) não estão cobertas. Rever o escopo se o objetivo passar a corrigir o contrato (`>= 200`, arredondamento): aí o golden master deve mudar de propósito, em tarefa separada.

**Procedência/IA:** ferramenta e modelo visíveis: Claude Code, Sonnet 5.5; tarefa delegada e contexto: rodada 1, pedido "refatore `calcular_total`" sem escopo declarado; rodada 2, mesma refatoração com os seis campos, plano pedido antes e executado após aprovação, mais o `AGENTS.md`; trecho aproveitado: `calculo.py` refatorado (funções privadas e tabelas por UF) e `AGENTS.md`; minha verificação/intervenção: golden master antes e depois, verificações do caso, suíte existente e diff por arquivo; revisão do plano: aprovado sem cortes. O raciocínio e a decisão registrados são meus.

**Revisão:** [x] golden master; [x] duas rodadas com números; [x] seis campos; [x] AGENTS.md; [x] até uma página.
