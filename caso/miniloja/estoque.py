"""Controle de estoque em memória."""


class EstoqueInsuficiente(Exception):
    pass


class Estoque:
    def __init__(self, saldos=None):
        self.saldos = dict(saldos or {})
        self.reservas = {}

    def reservar(self, sku, qtd, pedido_id):
        """Reserva a quantidade do SKU no estoque."""
        disponivel = self.saldos.get(sku, 0)
        if disponivel < qtd:
            raise EstoqueInsuficiente(sku)
        self.saldos[sku] = disponivel - qtd
        self.reservas[(pedido_id, sku)] = qtd
        return True

    def verificar(self, itens):
        """Confere se todos os itens cabem no saldo, sem reservar nada (R2.2).

        Soma as quantidades por SKU, em ordem, e lança EstoqueInsuficiente
        no primeiro SKU que não cabe.
        """
        pedido_por_sku = {}
        for i in itens:
            sku = i["sku"]
            pedido_por_sku[sku] = pedido_por_sku.get(sku, 0) + i["qtd"]
            if pedido_por_sku[sku] > self.saldos.get(sku, 0):
                raise EstoqueInsuficiente(sku)

    def saldo(self, sku):
        return self.saldos.get(sku, 0)
