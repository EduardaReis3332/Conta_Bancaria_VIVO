import textwrap

def menu(conta_selecionada):
    if conta_selecionada:
        return input(textwrap.dedent("""
            [d] Depositar
            [s] Sacar
            [e] Extrato
            [c] Criar Conta
            [l] Selecionar Conta
            [q] Sair
            => """))
    else:
        return input(textwrap.dedent("""
            [c] Criar Conta
            [l] Selecionar Conta
            [q] Sair
            => """))

def depositar(saldo, valor, extrato):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
    else:
        print("Operação falhou! O valor informado é inválido.")
    return saldo, extrato

def sacar(saldo, valor, extrato, limite, numero_saques, limite_saques):
    if valor > saldo:
        print("Operação falhou! Você não tem saldo suficiente.")
    elif valor > limite:
        print("Operação falhou! O valor do saque excede o limite.")
    elif numero_saques >= limite_saques:
        print("Operação falhou! Número máximo de saques excedido.")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
    else:
        print("Operação falhou! O valor informado é inválido.")
    return saldo, extrato, numero_saques

def exibir_extrato(saldo, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")

def criar_usuario(usuarios):
    nome = input("Digite o nome do usuário: ")
    cpf = input("Digite o CPF do usuário: ")
    if cpf in usuarios:
        print("CPF já cadastrado!")
    else:
        usuarios[cpf] = {'nome': nome, 'contas': []}
        print("Usuário criado com sucesso!")

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Digite o CPF do usuário vinculado à conta: ")
    if cpf not in usuarios:
        print("Usuário não encontrado.")
        return None
    tipo_conta = input("Digite o tipo da conta (ex: corrente, poupança): ")
    saldo_inicial = float(input("Digite o saldo inicial da conta: "))
    nova_conta = {'agencia': agencia, 'numero_conta': numero_conta, 'tipo_conta': tipo_conta, 'saldo': saldo_inicial, 'extrato': "", 'numero_saques': 0}
    usuarios[cpf]['contas'].append(nova_conta)
    print("Conta criada com sucesso!")
    return nova_conta

def selecionar_conta(usuarios):
    cpf = input("Digite o CPF do usuário: ")
    if cpf not in usuarios:
        print("Usuário não encontrado.")
        return None
    contas = usuarios[cpf]['contas']
    if not contas:
        print("Usuário não possui contas.")
        return None
    for i, conta in enumerate(contas, start=1):
        print(f"{i}. Agência: {conta['agencia']}, Número da Conta: {conta['numero_conta']}, Tipo: {conta['tipo_conta']}, Saldo: {conta['saldo']}")
    opcao = int(input("Selecione o número da conta: "))
    return contas[opcao - 1] if 1 <= opcao <= len(contas) else None

def main():
    usuarios = {}
    criar_usuario(usuarios)
    conta_selecionada = None
    while True:
        opcao = menu(conta_selecionada)
        if opcao == "c":
            conta_selecionada = criar_conta("1234", "00001", usuarios)
        elif opcao == "l":
            conta_selecionada = selecionar_conta(usuarios)
        elif opcao == "q":
            break
        elif conta_selecionada:
            saldo = conta_selecionada['saldo']
            extrato = conta_selecionada['extrato']
            numero_saques = conta_selecionada['numero_saques']
            limite_saques = 3
            limite = 500
            if opcao == "d":
                valor = float(input("Informe o valor do depósito: "))
                saldo, extrato = depositar(saldo, valor, extrato)
            elif opcao == "s":
                valor = float(input("Informe o valor do saque: "))
                saldo, extrato, numero_saques = sacar(saldo, valor, extrato, limite, numero_saques, limite_saques)
            elif opcao == "e":
                exibir_extrato(saldo, extrato)
            conta_selecionada['saldo'] = saldo
            conta_selecionada['extrato'] = extrato
            conta_selecionada['numero_saques'] = numero_saques
        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

if __name__ == "__main__":
    main()