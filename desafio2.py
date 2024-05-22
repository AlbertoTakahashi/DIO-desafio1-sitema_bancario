#######################################################################################
def deposito(conta, valor_deposito):
    global movimentacoes
    movimentacoes_original = movimentacoes.copy()
    try:
        movimentacoes[conta]["saldo"] = movimentacoes[conta]["saldo"] + valor_deposito
    except:
        return False
    try:
        movimentacoes[conta]['extrato'].append(valor_deposito)
    except:
        movimentacoes = movimentacoes_original.copy()   # retorna a operação restituindo o valor original do saldo
        return False
    return True

#######################################################################################
def saque(*, conta, valor_saque):
    global movimentacoes
    global numero_saques
    movimentacoes_original = movimentacoes.copy()
    try:
        movimentacoes[conta]["saldo"] = movimentacoes[conta]["saldo"] - valor_saque
    except:
        return False
    try:
        movimentacoes[conta]["extrato"].append(-valor_saque)
    except:
        movimentacoes = movimentacoes_original.copy()   # retorna a operação restituindo o valor original do saldo
        return False
    try:
        numero_saques_realizados[conta] = numero_saques_realizados[conta] + 1
    except:
        movimentacoes = movimentacoes_original.copy()
        return False
    return True

#######################################################################################
def extratoo(cpf, *, conta_corrente): 
    print()
    print('--------------------------------------------------')
    print("--- Extrato de Movimentações em Conta-Corrente ---")
    print('--------------------------------------------------')    
    print(f"CPF: {cpf}")
    print(f"conta corrente: {conta_corrente}")
    print('--------------------------------------------------')
    print()
    # saldo_inicial = True
    # for valor in movimentacoes[conta_corrente]:
    #     print(f"R$ {valor:6.2f}", end=" ")
    #     if saldo_inicial:
    #         print("(saldo inicial)")
    #         saldo_inicial = False
    #     elif valor > 0:
    #         print("(depósito)")
    #     else:
    #         print("(saque)")
    print("\n".join(f"R$ {valor:6.2f}" + " (depósito)" if valor>0 else f"R$ {valor:6.2f}" + " (saque)" if valor<0 else f"R$   0.00 (saldo inicial)" for valor in movimentacoes[conta_corrente]['extrato'] ) )
    print()
    print(f"Saldo atual: R$ {movimentacoes[conta_corrente]['saldo']:6.2f}")    
    return True

#######################################################################################
def novo_cliente(novo_numero_para_cliente, numero_agencia, numero_nova_conta):
    menu_novo_cliente = '''
-------------------------------
-Cadastramento de Novo Cliente-
-------------------------------

CPF => '''
    novo_cpf = input(menu_novo_cliente)
    if novo_cpf in clientes:
        print('CPF já cadastrado no sistema')
        print()
        return False, 0, 0
    novo_nome = input("Nome: ")
    novo_data_nascimento = input("Data de nascimento: ")
    novo_logradouro = input("Endereço: logradouro => ")
    novo_numero = input("          número     => ")
    novo_bairro = input("          bairro     => ")
    novo_cidade = input("Cidade               => ")
    novo_estado = input("Estado               => ")
    try:
        clientes.update({novo_cpf:{"nome":novo_nome,"data_nascimento":novo_data_nascimento,"endereço":{"logradouro":novo_logradouro, "numero":novo_numero, "bairro":novo_bairro, "cidade":novo_cidade, "estado":novo_estado},"num_cliente":novo_numero_para_cliente}})
    except:
        print("Erro ao criar cadastro do cliente")
        print("tente novamente mais tarde")
        print()
        return False, 0, 0
    identif_conta = str(int(numero_agencia)) + '-' + str(numero_nova_conta)
    #contas_correntes.update({novo_numero_cliente:{"agencia":numero_agencia, "conta_corrente":numero_nova_conta, "id_conta":identif_conta}})
    contas_correntes.update({novo_numero_para_cliente:{"id_conta":[]}})
    contas_correntes[novo_numero_para_cliente]["id_conta"].append(identif_conta)
    movimentacoes.update({identif_conta:{'extrato':[],'saldo':0}})
    numero_saques_realizados.update({identif_conta:0})
    print(clientes)
    return True, novo_numero_para_cliente, novo_cpf, novo_nome

#######################################################################################
def ja_cliente():
    global clientes
    menu_ja_cliente = '''
-------------------------------
-- Identificação do Cliente ---
-------------------------------

CPF => '''     
    cpf_cliente = input(menu_ja_cliente)
    if cpf_cliente not in clientes:
        print('CPF não cadastrado no sistema')
        print()
        return False, 0, "", 0
    cliente_numero = clientes[cpf_cliente]["num_cliente"]
    nome_cliente = clientes[cpf_cliente]["nome"]
    print(f'Nome: {nome_cliente}')
    return True, cpf_cliente, nome_cliente, cliente_numero

#######################################################################################
def seleciona_conta_corrente(nome,cpf,idcliente):
    global contas_correntes
    global movimentacoes
    if nome == "":
        print("Necessário antes fazer a seleção do cliente: opções [c] Cadastrado ou [n] novo !!!")
        print()
        return False, ''
    menu_seleciona_cliente = '''
--------------------------------
-- Selecione a Conta-corrente --
--------------------------------

'''
    print()
    print(f'Nome do cliente selecionado: {nome}')
    print(f'CPF do cliente: {cpf}')
    print()
    print('Contas correntes deste cliente: ')
    print('------------------------------')
    print()
    try:
        lista_contas = contas_correntes[idcliente]
    except:
        print('Este cliente não possui contas-correntes abertas')
        print()
        return False, ''
    print("\n".join(f"agência: {id_conta[:id_conta.find('-')]}, conta-corrente: {id_conta[id_conta.find('-')+1:]}" for id_conta in lista_contas['id_conta'] ))
    print()
    agencia = input('Informe a agência desejada: ')
    contacorrente = input('Informe a conta-corrente desejada: ')
    id_conta_selecionada = agencia + '-' + contacorrente
    try:
        teste_valida = id_conta_selecionada in lista_contas['id_conta'] 
    except:
        print('Erro na seleção da agência / conta-corrente')
        print()
        return False, ''
    if not teste_valida:
        print('Erro na seleção da agência / conta-corrente')
        print()
        return False, ''
    return True, id_conta_selecionada
 
#######################################################################################
def abre_conta_corrente(nome,cpf,idcliente,numero_agencia,numero_nova_conta):
    global contas_correntes
    global movimentacoes
    if nome == "":
        print("Necessário antes fazer a seleção do cliente: opções [c] Cadastrado ou [n] novo !!!")
        print()
        return False
    print('--------------------------------')
    print('-- Abertura de Conta-corrente --')
    print('--------------------------------')
    print(f'Nome do cliente: {nome}')
    print(f'CPF: {cpf}')
    print()
    valor_digitado = ""
    while valor_digitado not in ('s','n'):
        valor_digitado = input('Confirma abertura de nova conta-corrente (s/n)? => ')
    if valor_digitado == 'n':
        print('Operação cancelada')
        return False
    identif_conta = str(int(numero_agencia)) + '-' + str(numero_nova_conta)
    contas_correntes[id_cliente]["id_conta"].append(identif_conta)
    movimentacoes.update({identif_conta:{'extrato':[],'saldo':0}})
    numero_saques_realizados.update({identif_conta:0})
    print('Aberta nova conta-corrente:')
    print(f'   Agência: {numero_agencia}')
    print(f'   Conta-corrente: {numero_nova_conta}')
    return True

#######################################################################################
def movimentacoes_na_conta(cpf,conta,id_conta):
    menu2 = '''
-------------------------------
------ Menu de Operações ------
-------------------------------
CPF: ''' + str(cpf) + " agência-conta: " + str(conta) + '''

[d] Depositar
[s] Sacar
[e] Extrato
[v] Voltar

=> '''
    while True:
        opcao = input(menu2)
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
                    if deposito(id_conta,valor_deposito):
                        print()
                        print(f"Realizado depósito de R$ {valor_deposito:.2f} em sua conta.")
                        print(f"Seu saldo atual em conta é de R$ {movimentacoes[id_conta]['saldo']:.2f}")
                    else:
                        print()
                        print("Não foi possível realizar o depósito.")
                        print("Tente novamente mais tarde")
                continue

            case "s":
                print()
                print("---Saque---")
                if numero_saques_realizados[id_conta] >= LIMITE_DIARIO_QTD_SAQUES:
                    print()
                    print(f'Você já atingiu o limite máximo de {LIMITE_DIARIO_QTD_SAQUES} saques diários')
                    print('Operação não permitida')
                    print()
                    continue
                valor_digitado = input("Valor desejado para saque => R$ ")
                try:
                    valor_desejado = float(valor_digitado)
                except:
                    print("Para saque favor indicar valor numérico")
                    print("Operação cancelada")
                    print()
                    continue 
                valor_desejado = abs(valor_desejado)
                if valor_desejado > LIMITE_SAQUE:
                    print()
                    print(f'Valor solicitado excedeu limite máximo para esta operação (R$ {LIMITE_SAQUE:.2f})')
                    print('Saque cancelado')
                    print()
                    continue
                if valor_desejado > movimentacoes[id_conta]["saldo"]:
                    print()
                    print('Saldo insuficiente para esta operação')
                    print('Saque cancelado')
                    print()
                else:
                    if saque(conta=id_conta,valor_saque=valor_desejado):
                        print()
                        print(f"Realizado saque no valor de R$ {valor_desejado:.2f} em sua conta.")
                        print(f"Seu saldo atual em conta é de R$ {movimentacoes[id_conta]['saldo']:.2f}")
                    else:
                        print()
                        print("Não foi possível realizar o saque.")
                        print("Tente novamente mais tarde")                    
                continue

            case "e":
                extratoo(cpf, conta_corrente=id_conta)
                continue

            case 'v':
                break

        print('Operacao inválida. Por favor selecione novamente a operação desejada.')
    print()
    return

#########################################################################################################
#########################################################################################################
#########################################################################################################
id_cliente = 0         # código do usuário
cliente_cpf = 0000  # somente 01 cpf por usuário
cliente_nome = ''
controle_numero_conta = 0           # cada cpf pode estar associado a varias contas
id_conta = ""        # identificador único associando agencia+conta_corrente
contador_clientes = 0

agencia = '0001'     # por definição do exercício sempre usaremos a '0001'
LIMITE_SAQUE = 500 # limite de valor máximo permitido por saque
LIMITE_DIARIO_QTD_SAQUES = 3 # quantidade máxima de saques realizados por dia

menu_1a = '''
------ Identificação do Cliente ------
[c] Cliente já cadastrado
[n] Cliente novo
[s] Seleciona conta-corrente
[a] Abre nova conta-corrente
[q] Sair

=> '''

menu_1b1 = '''
------ Seleção de Usuário Já Cadastrado ------
Digite o CPF (somente números) ou q para voltar

=> '''


clientes = {"cpf":{"nome":"", "data_nascimento":"", "endereço":{"logradouro":"", "numero":"", "bairro":"", "cidade":"", "estado":""}, "num_cliente":0}}
numero_saques_realizados = {"conta_corrente":0}
movimentacoes = {"conta_corrente":{"extrato":[],"saldo":0}}
contas_correntes = {id_cliente:{"id:conta":[]}}

while True:
    opcao1 = input(menu_1a)
    match opcao1:
        case "c":
            cadastrado, cliente_cpf, cliente_nome, id_cliente = ja_cliente()
            if not cadastrado:
                print('Cadastro não localizado')
        case "n":
            cadastrado, id_cliente, cliente_cpf, cliente_nome = novo_cliente(contador_clientes + 1,agencia,controle_numero_conta + 1)
            if cadastrado:
                contador_clientes = id_cliente
                print('Cliente cadastrado:')
                print(f'    Nome: {cliente_nome}')
                print(f'    CPF: {cliente_cpf}')
                print(f'    Agência: {agencia}')
                print(f'    Conta-corrente: {controle_numero_conta}')
                print('\n')
                controle_numero_conta += 1  
        case 's':
            valido, id_conta = seleciona_conta_corrente(cliente_nome,cliente_cpf,id_cliente)
            if valido:
                movimentacoes_na_conta(cliente_cpf,id_conta,id_conta)
        case "a":
            if abre_conta_corrente(cliente_nome,cliente_cpf,id_cliente,agencia,controle_numero_conta+1):
                controle_numero_conta += 1
        case "q":
            exit()



