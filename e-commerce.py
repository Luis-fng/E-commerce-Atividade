from abc import ABC, abstractmethod


class Pagamento(ABC):

    @abstractmethod
    def pagar(self, valor):
        pass


class PagamentoCartao(Pagamento):

    def pagar(self, valor):
        print(f"Pagamento de R$ {valor:.2f} realizado com CARTÃO.")


class PagamentoPix(Pagamento):

    def pagar(self, valor):
        print(f"Pagamento de R$ {valor:.2f} realizado com PIX.")


class PagamentoBoleto(Pagamento):

    def pagar(self, valor):
        print(f"Pagamento de R$ {valor:.2f} realizado com BOLETO.")


class FabricaPagamento:

    @staticmethod
    def criar_pagamento(tipo):

        if tipo == "cartao":
            return PagamentoCartao()

        elif tipo == "pix":
            return PagamentoPix()

        elif tipo == "boleto":
            return PagamentoBoleto()

        else:
            raise ValueError("Tipo de pagamento inválido.")


class Validador:

    def __init__(self):
        self.proximo = None

    def definir_proximo(self, proximo):
        self.proximo = proximo
        return proximo

    def processar(self, pedido):

        if self.proximo:
            return self.proximo.processar(pedido)

        return True


class ValidarEstoque(Validador):

    def processar(self, pedido):

        if pedido["estoque"] <= 0:
            print("Produto sem estoque.")
            return False

        print("Estoque validado.")
        return super().processar(pedido)


class ValidarValorMinimo(Validador):

    def processar(self, pedido):

        if pedido["valor"] < 10:
            print("Pedido abaixo do valor mínimo.")
            return False

        print("Valor mínimo validado.")
        return super().processar(pedido)


class ValidarCPF(Validador):

    def validar_cpf(self, cpf):

        cpf = ''.join(filter(str.isdigit, cpf))

        if len(cpf) != 11 or cpf == cpf[0] * 11:
            return False

        soma = 0
        for i in range(9):
            soma += int(cpf[i]) * (10 - i)

        digito1 = (soma * 10 % 11) % 10

        soma = 0
        for i in range(10):
            soma += int(cpf[i]) * (11 - i)

        digito2 = (soma * 10 % 11) % 10

        return digito1 == int(cpf[9]) and digito2 == int(cpf[10])

    def processar(self, pedido):

        if not self.validar_cpf(pedido["cpf"]):
            print("CPF inválido.")
            return False

        print("CPF validado.")
        return super().processar(pedido)


class SistemaPedido:

    def finalizar_pedido(self, pedido, tipo_pagamento):

        print("Iniciando pedido...\n")

        estoque = ValidarEstoque()
        valor = ValidarValorMinimo()
        cpf = ValidarCPF()

        estoque.definir_proximo(valor).definir_proximo(cpf)

        if estoque.processar(pedido):

            print("\nPedido aprovado.")

            pagamento = FabricaPagamento.criar_pagamento(
                tipo_pagamento
            )

            pagamento.pagar(pedido["valor"])

            print("Pedido finalizado com sucesso.")

        else:
            print("\nPedido cancelado.")


pedido = {
    "valor": 150,
    "estoque": 10,
    "cpf": "52998224725"
}

sistema = SistemaPedido()

sistema.finalizar_pedido(
    pedido,
    "boleto"
)