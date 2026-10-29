# B3: não deixar reserva de estoque quando um item falha (R2.2)

## Intenção
Pelo contrato (`caso/regras.md`, R2.2), se algum item do pedido não tem estoque, o pedido é recusado com 409 e **nenhuma reserva pode permanecer**. Hoje `PedidoService.criar` reserva item a item; se o item 2 falha, a reserva do item 1 fica (saldo menor e entrada em `reservas`).

## Escopo
- **Altera:** `caso/miniloja/estoque.py` (método novo `verificar`), `caso/miniloja/pedidos.py` (uma chamada).
- **Adiciona:** `avaliacoes/av3/test_reserva_estoque.py`.
- **Não toca:** `testes/`, `caso/regras.md`, `handlers.py`, `calculo.py`, demais módulos.
- **Fora de escopo (achados, não corrigidos):** reserva que permanece com pagamento recusado (R2.3, teste `expectedFailure`); colisão do id `tmp-{usuario_id}` entre pedidos do mesmo usuário; sobrescrita de `reservas` com SKU repetido.

## Plano
Verificar todo o estoque **antes** de reservar qualquer item. `Estoque.verificar(itens)` soma as quantidades por SKU, em ordem, e lança `EstoqueInsuficiente` no primeiro SKU que não cabe. `criar` chama o método antes do laço de reserva. O SKU do 409 continua o mesmo de antes.

Cortei do plano do agente: API transacional com desfazer, correção do id temporário, correção do R2.3 e validação de `qtd`.

## Como foi verificado
```
python3 -B avaliacoes/av3/test_reserva_estoque.py        # Python 3.14.4
  antes:  FAILED (failures=5, expected failures=1)   # ex.: AssertionError: 2 != 5 (saldo de A caiu)
  depois: OK (expected failures=1)                   # 7 testes
python3 -B testes/test_miniloja.py --codigo caso
  igual ao material inicial: 8 passam, 3 falham (CPF e payload)
python3 -B testes/test_miniloja.py --codigo caso --existentes
  OK (26 testes)
```
Sabotagem: trocar `self.estoque.verificar(itens)` por `pass` volta a fazer os testes falharem.

## Teste que falharia sem a mudança
Cinco testes de R2.2: item sem estoque após item com estoque, mesmo SKU repetido acima do saldo, SKU inexistente, quantidade 0 seguida de falha e o 409 pela camada HTTP (SKU no corpo).

## Dependências novas
Nenhuma (biblioteca padrão).

## Modo de interação e por quê
Plano primeiro, depois passos pequenos com aprovação. Raio de impacto baixo, oráculo claro (R2.2) e código ainda desconhecido para mim. Alternativa comparada: pedir a correção direto ao agente; descartada porque tende a ampliar o diff.

## Limites
A checagem prévia não protege contra concorrência (em memória, sem threads). Com o estoque mockado, `verificar` é uma chamada vazia, então a suíte existente não exercita a checagem; a proteção está nos testes novos. A regra "cabe no saldo" existe em `verificar` e em `reservar`. Achados fora de escopo, ainda abertos: R2.3 (pagamento recusado), colisão do id `tmp-{usuario_id}` e sobrescrita de `reservas` com SKU repetido.
