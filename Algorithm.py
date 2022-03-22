import argparse
import random
import socket
from typing import Tuple


class AlgoritmoHamming:
    """
    Classe que calcula o algoritmo de hamming
    """

    def __init__(self, algarismo_decimal: int) -> None:
        """
        Recebe um valor decimal inteiro como parâmetro, maior que zero.
        :param algarismo_decimal: int
        """
        assert algarismo_decimal <= 15
        self.__algarismo_decimal: int = algarismo_decimal
        self.__binario: list = []

    def converteBinario(self) -> list:
        """
        Converte para binario
        :return: list
        """
        """
         13 /2 = 6 (1)
            6 / 2 = 3 (0)
            3 / 2 = 1 (1)
            1 """
        quociente: int = 1
        valor = self.__algarismo_decimal
        resto: int = 0
        print(f"Enviando o número {self.__algarismo_decimal}")
        while quociente > 0:
            quociente = self.__algarismo_decimal // 2  # pega o quociente
            resto = self.__algarismo_decimal % 2  # pega o resto
            self.__binario.append(resto)  # armazena o binario
            self.__algarismo_decimal = quociente

        # inverte o vetor
        auxiliar: list = []
        for bit in range(len(self.__binario) - 1, -1, -1):
            auxiliar.append(self.__binario[bit])
        print(f"[*] {valor} convertido para binário: {auxiliar}")
        return auxiliar

    def acrescentaPreNumeros(self) -> list:
        """
        Pega um vetor com binario e coloca numeros de haming nas posicoes
        :return: list
        """
        binario: list = self.converteBinario()
        potencias_2: list = [2 ** num for num in range(len(binario) - 1)]
        contador: int = 0
        potencias_2.insert(0, 0)
        for numeros in range(1, 5):
            if contador in potencias_2:
                binario.insert(contador, "*")
            if numeros == 3:
                contador += 1
            contador += 1
        print(binario[1:])
        return binario[1:]

    def incrementaNumHamming(self) -> list:
        """
        Incrementa numeros de hamming ao vetor
        :return: list
        """
        bytes_modificados: list = self.acrescentaPreNumeros()
        posicao_base: int = 2
        b1: list = [bytes_modificados[posicao_base], bytes_modificados[posicao_base + 2],
                    bytes_modificados[posicao_base + 4]]
        b2: list = [bytes_modificados[posicao_base], bytes_modificados[posicao_base + 3],
                    bytes_modificados[posicao_base + 4]]
        b3: list = [bytes_modificados[posicao_base + 2], bytes_modificados[posicao_base + 3],
                    bytes_modificados[posicao_base + 4]]
        resultado_b1: int
        resultado_b2: int
        resultado_b3: int

        # multiplicacao XOR
        # b1
        if b1[0] == b1[1]:
            resultado_b1 = 0
        else:
            resultado_b1 = 1
        if resultado_b1 == b1[2]:
            resultado_b1 = 0
        else:
            resultado_b1 = 1
        # b2
        if b2[0] == b2[1]:
            resultado_b2 = 0
        else:
            resultado_b2 = 1
        if resultado_b2 == b2[2]:
            resultado_b2 = 0
        else:
            resultado_b2 = 1
        # b3
        if b3[0] == b3[1]:
            resultado_b3 = 0
        else:
            resultado_b3 = 1
        if resultado_b3 == b3[2]:
            resultado_b3 = 0
        else:
            resultado_b3 = 1

        numeros_hamming_encontrados: list = [resultado_b1, resultado_b2, resultado_b3]
        contador: int = 0
        for index, bits in enumerate(bytes_modificados):
            if "*" == bits:
                bytes_modificados[index] = numeros_hamming_encontrados[contador]
                contador += 1
        ruindo_em: int = self.geraRuido()

        if bytes_modificados[ruindo_em] == 0:
            bytes_modificados[ruindo_em] = 1
        else:
            bytes_modificados[ruindo_em] = 0
        return bytes_modificados

    def verificacaoReceptor(self, hamming: list):
        """
        faz a verificacao dos números de hamming, se zerar, está correto
        :return:
        """
        print(f"HAMMING: {hamming}")
        if len(hamming) == 0:
            hamming = self.incrementaNumHamming()
        posicoes: list = ["001", "010", "011", "100", "101", "110", "111"]
        h1: list = []
        h2: list = []
        h3: list = []
        for index, itens in enumerate(posicoes):
            if "1" in itens[2]:
                h1.append(index)
            if "1" in itens[1]:
                h2.append(index)
            if "1" in itens[0]:
                h3.append(index)

        resultado_h1: int
        resultado_h2: int
        resultado_h3: int
        # multiplicacao XOR
        # h1
        if hamming[h1[0]] == hamming[h1[1]]:
            resultado_h1 = 0
        else:
            resultado_h1 = 1
        if resultado_h1 == hamming[h1[2]]:
            resultado_h1 = 0
        else:
            resultado_h1 = 1
        if resultado_h1 == hamming[h1[3]]:
            resultado_h1 = 0
        else:
            resultado_h1 = 1
        # h2
        if hamming[h2[0]] == hamming[h2[1]]:
            resultado_h2 = 0
        else:
            resultado_h2 = 1
        if resultado_h2 == hamming[h2[2]]:
            resultado_h2 = 0
        else:
            resultado_h2 = 1
        if resultado_h2 == hamming[h2[3]]:
            resultado_h2 = 0
        else:
            resultado_h2 = 1
        # h3
        if hamming[h3[0]] == hamming[h3[1]]:
            resultado_h3 = 0
        else:
            resultado_h3 = 1

        if resultado_h3 == hamming[h3[2]]:
            resultado_h3 = 0
        else:
            resultado_h3 = 1
        if resultado_h3 == hamming[h3[3]]:
            resultado_h3 = 0
        else:
            resultado_h3 = 1
        resultado: list = []
        potencias_2: list = [2 ** num for num in range(len(self.__binario) - 1)]
        if resultado_h3 == 0 and resultado_h1 == 0 and resultado_h3 == 0:
            print(f"MENSAGEM RECEBIDA COM SUCESSO!\nContent: {hamming}\nValor original transmitido: {self.voltaAoResultado(hamming)}")
            return str(hamming) + f" Valor original transmitido: {self.voltaAoResultado(hamming)}"
        else:

            indentificador: str = str(resultado_h3) + str(resultado_h2) + str(resultado_h1)
            local_do_erro: int = 0

            for index, valor in enumerate(posicoes):
                if valor == indentificador:
                    print(index, valor)
                    local_do_erro = index
                    break
            if hamming[local_do_erro] == 0:
                hamming[local_do_erro] = 1
            else:
                hamming[local_do_erro] = 0
            print(f"MENSAGEM RECEBIDA COM SUCESSO!\nContent: {hamming}")
            return str(hamming) + f" Valor original transmitido: {self.voltaAoResultado(hamming)}"

    def geraRuido(self) -> int:
        """
        Gera ruido, valor aleatorio
        :return:
        """
        return random.randint(0, 6)

    def voltaAoResultado(self, hamming) -> int:
        """
        Pega o numero de hamming e volta ao original
        :return: -> int
        """
        novo_vetor: list = [hamming[2], hamming[4], hamming[5], hamming[6]]
        novo_vetor.reverse()
        decimal = sum([(2 ** num) * novo_vetor[num] for num in range(len(novo_vetor))])
        return decimal

    def servidor(self, ip, port):
        """
        Servidor tcp
        :return:
        """
        host: str = ip
        port: int = port

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # servidor tcp
        sock.bind((host, port))
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.listen(5)
        print(f"[*] Escutando no endereço {host, port}")
        while True:
            soc, addr = sock.accept()

            try:
                while True:
                    msg = soc.recv(2024).decode()  # 1024 bytes
                    if not msg:
                        raise EOFError("Socket fechado!")
                    else:
                        #print("AQ", type())
                        response = self.verificacaoReceptor(eval(msg))
                        #print("respinse", response)
                       # print(f"{addr} diz: {msg.decode()}")
                    soc.sendall(str(response).encode())  # envio da resposta
            except EOFError:
                print(f"Soquete do cliente {addr} foi fechado")
            finally:
                soc.close()

    def client(self, ip, port):
        """
        Cliente que envia a mensagem
        :return:
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # cliente tcp
        sock.connect((ip, port))  # ip e porta do servidor
        msg: bytes = str(self.incrementaNumHamming()).encode()
        sock.sendall(msg)
        resposta: str = ""
        resposta += sock.recv(2024).decode()
        print(f"[*] O servidor diz: {resposta}")
        sock.close()


class ArgumentLine:
    """Lê a linha de comandos"""

    @staticmethod
    def arg(choices):
        parser = argparse.ArgumentParser(description="Servidor e cliente simples para testar o uso de multiprocessos")
        parser.add_argument("funcao", choices=choices, metavar="Servidor/Cliente", help="Informe se quer executar "
                                                                                        "cliente ou servidor",
                            type=str)
        parser.add_argument("--H", "-host", metavar="ip", required=False, help="Se quiser, informe um endereço para o "
                                                                               "servidor", type=str,
                            default="localhost")
        parser.add_argument("--p", "-port", metavar="porta", required=False, help="Se quiser, defina uma porta de "
                                                                                  "comunicação, acima de 7000",
                            type=int, default=7000)
        args = parser.parse_args()
        function = choices[args.funcao]
        return function(args.H, args.p)


if __name__ == '__main__':
    """ algoritmo = AlgoritmoHamming(13)
    algoritmo.verificacaoReceptor("")
    algoritmo.geraRuido()"""

    algoritmo = AlgoritmoHamming(13)
    choices: dict = {
        "servidor": algoritmo.servidor,
        "cliente": algoritmo.client
    }
    ArgumentLine.arg(choices=choices)
