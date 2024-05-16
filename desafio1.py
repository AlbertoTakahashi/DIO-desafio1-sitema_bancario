menu = '''
------ Desafio 01 ------
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair
=> '''

saldo = 0
movimentacoes = []
movimentacoes.append(saldo)
LIMITE_SAQUE = 500 # limite de valor máximo permitido por saque
extrato = ""
numero_saques = 0
LIMITE_DIARIO_QTD_SAQUES = 3 # quantidade máxima de saques realizdos por dia

while True:

    opcao = input(menu)

    match opcao:
        case "d":
            print()
            print("---Depósito---")
            valor_digitado = input("Valor para depósito => R$ ")
            try:
                valor_deposito = float(valor_digitado)
            except:
                print("Para depósito favor indicar valor numérico")
                print("Operação cancelada")
                print()
                continue 
            if (valor_deposito <= 0):
                print("Para depósito o valor deve ser maior ou igual a R$ 0.01")
                print("Operação cancelada")
                print()
                continue
            else:
                saldo += valor_deposito
                movimentacoes.append(valor_deposito)
                print()
                print(f"Realizado depósito de R$ {valor_deposito:.2f} em sua conta.")
                print(f"Seu saldo atual em conta é de R$ {saldo:.2f}")
            continue

        case "s":
            print()
            print("---Saque---")
            if numero_saques >= LIMITE_DIARIO_QTD_SAQUES:
                print()
                print(f'Você já atingiu o limite máximo de {LIMITE_DIARIO_QTD_SAQUES} saques diários')
                print('Operação não permitida')
                print()
                continue
            valor_digitado = input("Valor desejado para saque => R$ ")
            try:
                valor_saque = float(valor_digitado)
            except:
                print("Para saque favor indicar valor numérico")
                print("Operação cancelada")
                print()
                continue 
            valor_saque = abs(valor_saque)
            if valor_saque > LIMITE_SAQUE:
                print()
                print(f'Valor solicitado excedeu limite máximo para esta operação (R$ {LIMITE_SAQUE:.2f})')
                print('Saque cancelado')
                print()
            if valor_saque > saldo:
                print()
                print('Saldo insuficiente para esta operação')
                print('Saque cancelado')
                print()
            else:
                saldo -= valor_saque
                movimentacoes.append(-valor_saque)
                numero_saques += 1
                print()
                print(f"Realizado saque no valor de R$ {valor_saque:.2f} em sua conta.")
                print(f"Seu saldo atual em conta é de R$ {saldo:.2f}")
            continue

        case "e":
            print()
            print("---Extrato---")
            saldo_inicial = True
            for valor in movimentacoes:
                print(f"R$ {valor:6.2f}", end=" ")
                if saldo_inicial:
                    print("(saldo inicial)")
                    saldo_inicial = False
                elif valor > 0:
                    print("(depósito)")
                else:
                    print("(saque)")
            print()
            print(f"Saldo atual: R$ {saldo:6.2f}")
            continue

        case 'q':
            break

    print('Operacao inválida. Por favor selecione novamente a operação desejada.')

print()
print('Obrigado por utilizar o sistema')
print()