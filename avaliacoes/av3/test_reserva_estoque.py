"""Testes de R2.2: pedido recusado por falta de estoque não deixa reserva.

Uso, na raiz do repositório:
    python3 -B avaliacoes/av3/test_reserva_estoque.py
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "caso"))

from miniloja.estoque import Estoque, EstoqueInsuficiente  # noqa: E402
from miniloja.pagamentos import GatewayFake  # noqa: E402
from miniloja.pedidos import PedidoService  # noqa: E402
from miniloja.repositorio import RepositorioPedidos  # noqa: E402


def item(sku, qtd, preco=10.0):
    return {"sku": sku, "qtd": qtd, "preco": preco}


class TestReservaEstoque(unittest.TestCase):
    def setUp(self):
        self.estoque = Estoque({"A": 5, "B": 2})
        self.repo = RepositorioPedidos()
        self.service = PedidoService(self.repo, self.estoque, GatewayFake())

    def test_item_sem_estoque_nao_deixa_reserva_do_item_anterior(self):
        """R2.2: A tem estoque, B não; nenhuma reserva pode permanecer."""
        with self.assertRaises(EstoqueInsuficiente) as ctx:
            self.service.criar(1, [item("A", 3), item("B", 9)])
        self.assertEqual(str(ctx.exception), "B")
        self.assertEqual(self.estoque.saldo("A"), 5)
        self.assertEqual(self.estoque.saldo("B"), 2)
        self.assertEqual(self.estoque.reservas, {})
        self.assertEqual(self.repo.todos(), [])

    def test_mesmo_sku_repetido_acima_do_saldo_nao_deixa_reserva(self):
        """R2.2: duas linhas de A (3 + 3) passam do saldo 5; sem reserva parcial."""
        with self.assertRaises(EstoqueInsuficiente) as ctx:
            self.service.criar(1, [item("A", 3), item("A", 3)])
        self.assertEqual(str(ctx.exception), "A")
        self.assertEqual(self.estoque.saldo("A"), 5)
        self.assertEqual(self.estoque.reservas, {})

    def test_sku_inexistente_recusa_sem_reserva_nem_saldo_novo(self):
        """R2.2: SKU que não existe no estoque recusa o pedido e não deixa nada."""
        with self.assertRaises(EstoqueInsuficiente) as ctx:
            self.service.criar(1, [item("A", 1), item("X", 1)])
        self.assertEqual(str(ctx.exception), "X")
        self.assertEqual(self.estoque.saldos, {"A": 5, "B": 2})
        self.assertEqual(self.estoque.reservas, {})

    def test_quantidade_zero_seguida_de_falha_nao_deixa_entrada_de_reserva(self):
        """R2.2: item com qtd 0 antes de um item sem estoque não pode deixar entrada em reservas."""
        with self.assertRaises(EstoqueInsuficiente):
            self.service.criar(1, [item("A", 0), item("B", 9)])
        self.assertEqual(self.estoque.reservas, {})

    def test_409_na_camada_http_mantem_sku_e_nao_deixa_reserva(self):
        """R2.2 pela camada HTTP: status 409, SKU no corpo e saldos intactos."""
        from miniloja import handlers

        antes = dict(handlers._estoque.saldos)
        reservas_antes = dict(handlers._estoque.reservas)
        status, corpo = handlers.post_pedidos(
            1, {"itens": [item("BOLA-01", 3), item("CAMISA-M", 9999)]}
        )
        self.assertEqual(status, 409)
        self.assertEqual(corpo["sku"], "CAMISA-M")
        self.assertEqual(handlers._estoque.saldos, antes)
        self.assertEqual(handlers._estoque.reservas, reservas_antes)

    def test_pedido_valido_continua_reservando(self):
        """Invariante: pedido com estoque reserva e salva como antes."""
        pedido = self.service.criar(1, [item("A", 2), item("B", 1)])
        self.assertEqual(pedido["status"], "pago")
        self.assertEqual(self.estoque.saldo("A"), 3)
        self.assertEqual(self.estoque.saldo("B"), 1)
        self.assertEqual(len(self.estoque.reservas), 2)

    @unittest.expectedFailure
    def test_pagamento_recusado_nao_deixa_reserva(self):
        """Achado fora do escopo (R2.3): hoje a reserva permanece. Registrado, não corrigido."""
        resultado = self.service.criar(1, [item("A", 2)], token="recusado")
        self.assertEqual(resultado["status"], "pagamento_recusado")
        self.assertEqual(self.estoque.saldo("A"), 5)
        self.assertEqual(self.estoque.reservas, {})


if __name__ == "__main__":
    unittest.main()
