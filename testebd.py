import mysql.connector
from decimal import Decimal

#Entidade cliente
class Cliente:
    def __init__(self, nome, idade, telefone, email, is_flamengo=False, is_one_piece=False, cidade=''):
        self.nome = nome
        self.idade = idade
        self.telefone = telefone
        self.email = email
        self.is_flamengo = is_flamengo
        self.is_one_piece = is_one_piece
        self.cidade = cidade

#Entidade cabeleireiro
class Cabeleireiro:
    def __init__(self, nome, idade, telefone, email, especializacao):
        self.nome = nome
        self.idade = idade
        self.telefone = telefone
        self.email = email
        self.especializacao = especializacao

#Entidade serviço
class Servico:
    def __init__(self, nome_serv, preco):
        self.nome_serv = nome_serv
        self.preco = preco

#Entidade agendamento
class Agendamento:
    def __init__(self, cliente_id, servico_id, data, hora):
        self.cliente_id = cliente_id
        self.servico_id = servico_id
        self.data = data
        self.hora = hora

#Entidade VendaServico
class VendaServico:
    def __init__(self, agendamento_id, cabeleireiro_id, forma_pagamento, status_pagamento, valor_final):
        self.agendamento_id = agendamento_id
        self.cabeleireiro_id = cabeleireiro_id
        self.forma_pagamento = forma_pagamento
        self.status_pagamento = status_pagamento
        self.valor_final = valor_final

# Função para calcular desconto automático
def calcular_desconto(conexao, agendamento_id):
    cursor = conexao.cursor()
    cursor.execute("SELECT cliente_id, servico FROM Agendamento WHERE id = %s", (agendamento_id,))
    agendamento = cursor.fetchone()
    if not agendamento:
        return 0
    cliente_id, servico_id = agendamento
    cursor.execute("SELECT is_flamengo, is_one_piece, cidade FROM Cliente WHERE id = %s", (cliente_id,))
    cliente = cursor.fetchone()
    cursor.execute("SELECT preco FROM Servico WHERE id_serv = %s", (servico_id,))
    preco_servico = cursor.fetchone()[0]
    desconto = 0
    if cliente:
        if cliente[0]:  # is_flamengo
            desconto += 0.10
        if cliente[1]:  # is_one_piece
            desconto += 0.10
        if cliente[2].lower() == "sousa":
            desconto += 0.10
    desconto_decimal = Decimal(str(desconto))  # Convertendo para Decimal
    preco_final = preco_servico * (Decimal('1.0') - desconto_decimal)
    return preco_final

#Classe para gerenciar as relações
class Gerencia:
    def inserir(conexao, tabela, objeto):
        cursor = conexao.cursor()
        if tabela == 1:
            comando = "INSERT INTO Cliente (nome, idade, telefone, email, is_flamengo, is_one_piece, cidade) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            values = (objeto.nome, objeto.idade, objeto.telefone, objeto.email, objeto.is_flamengo, objeto.is_one_piece, objeto.cidade)
        elif tabela == 2:
            comando = "INSERT INTO Cabeleireiro (nome, idade, telefone, email, especializacao) VALUES (%s, %s, %s, %s, %s)"
            values = (objeto.nome, objeto.idade, objeto.telefone, objeto.email, objeto.especializacao)
        elif tabela == 3:
            comando = "INSERT INTO Servico (nome_serv, preco) VALUES (%s, %s)"
            values = (objeto.nome_serv, objeto.preco)
        elif tabela == 4:
            comando = "INSERT INTO Agendamento (cliente_id, servico, data, hora) VALUES (%s, %s, %s, %s)"
            values = (objeto.cliente_id, objeto.servico_id, objeto.data, objeto.hora)
        elif tabela == 5:
            comando = "INSERT INTO VendaServico (agendamento_id, cabeleireiro_id, forma_pagamento, status_pagamento, valor_final) VALUES (%s, %s, %s, %s, %s)"
            values = (objeto.agendamento_id, objeto.cabeleireiro_id, objeto.forma_pagamento, objeto.status_pagamento, objeto.valor_final)
        try:
            cursor.execute(comando, values)
            conexao.commit()
        except mysql.connector.Error as err:
            print(f"Erro: {err}")

    def alterar(conexao, tabela, coluna, novo_dado, condicao):
        cursor = conexao.cursor()
        comando = f"UPDATE {tabela} SET {coluna} = {novo_dado} WHERE {condicao}"
        try:
            cursor.execute(comando)
            conexao.commit()
        except mysql.connector.Error as err:
            print(f"Erro: {err}")

    def remover(conexao, tabela, condicao):
        cursor = conexao.cursor()
        comando = f"DELETE FROM {tabela} WHERE {condicao}"
        try:
            cursor.execute(comando)
            conexao.commit()
        except mysql.connector.Error as err:
            print(f"Erro: {err}")

    def pesquisar_por_nome(conexao, tabela, cond_nome):
        cursor = conexao.cursor()
        comando = f"SELECT * FROM {tabela} WHERE {cond_nome}"
        try:
            cursor.execute(comando)
            resultado = cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Erro: {err}")
        for linha in resultado:
            print(linha)

    def listar_todos(conexao, tabela):
        cursor = conexao.cursor()
        for tab in tabela:
            comando = f"SELECT * FROM {tab}"
            try:
                cursor.execute(comando)
                resultado = cursor.fetchall()
            except mysql.connector.Error as err:
                print(f"Erro: {err}")
            for linha in resultado:
                print(linha)

    def exibir_um(conexao, tabela):
        cursor = conexao.cursor()
        comando = f"SELECT * FROM {tabela}"
        try:
            cursor.execute(comando)
            resultado = cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Erro: {err}")
        for linha in resultado:
            print(linha)

    def relatorio(self, conexao):
        cursor = conexao.cursor()
        print("\n--- Relatório de Clientes ---")
        try:
            cursor.execute("SELECT COUNT(*) FROM Cliente")
            total_clientes = cursor.fetchone()[0]
            print(f"Total de clientes cadastrados: {total_clientes}")
        except mysql.connector.Error as err:
            print(f"Erro: {err}")

        print("\n--- Relatório de Cabeleireiros ---")
        try:
            cursor.execute("SELECT COUNT(*) FROM Cabeleireiro")
            total_cabeleireiros = cursor.fetchone()[0]
            print(f"Total de cabeleireiros cadastrados: {total_cabeleireiros}")
        except mysql.connector.Error as err:
            print(f"Erro: {err}")

        print("\n--- Relatório de Serviços ---")
        try:
            cursor.execute("SELECT COUNT(*), SUM(preco) FROM Servico")
            resultado = cursor.fetchone()
            total_servicos = resultado[0]
            valor_total_servicos = resultado[1] if resultado[1] is not None else 0
            print(f"Total de serviços cadastrados: {total_servicos}")
            print(f"Valor total dos serviços: R$ {valor_total_servicos:.2f}")
        except mysql.connector.Error as err:
            print(f"Erro: {err}")

        print("\n--- Relatório de Agendamentos ---")
        try:
            cursor.execute("SELECT COUNT(*) FROM Agendamento")
            total_agendamentos = cursor.fetchone()[0]
            print(f"Total de agendamentos feitos: {total_agendamentos}")
        except mysql.connector.Error as err:
            print(f"Erro: {err}")

        print("\n--- Relatório de Vendas de Serviços ---")
        try:
            cursor.execute("""
                SELECT v.id, a.cliente_id, c.nome AS cliente, cb.nome AS cabeleireiro, s.nome_serv AS servico, a.data, v.forma_pagamento, v.status_pagamento, v.valor_final
                FROM VendaServico v
                JOIN Agendamento a ON v.agendamento_id = a.id
                JOIN Cliente c ON a.cliente_id = c.id
                JOIN Cabeleireiro cb ON v.cabeleireiro_id = cb.id
                JOIN Servico s ON a.servico = s.id_serv
                ORDER BY v.id DESC
            """)
            vendas = cursor.fetchall()
            total_arrecadado = sum([venda[8] for venda in vendas])
            print(f"Total de vendas de serviços realizadas: {len(vendas)}")
            print(f"Valor arrecadado com vendas: R$ {total_arrecadado:.2f}")
            print("ID | ClienteID | Cliente | Cabeleireiro | Serviço | Data | Pagamento | Status | Valor Final")
            print("-"*100)
            for venda in vendas:
                print(f"{venda[0]} | {venda[1]} | {venda[2]} | {venda[3]} | {venda[4]} | {venda[5]} | {venda[6]} | {venda[7]} | R$ {venda[8]:.2f}")
        except mysql.connector.Error as err:
            print(f"Erro: {err}")

        print("\n--- Vendas por cabeleireiro (mês atual) ---")
        try:
            cursor.execute("""
                           SELECT c.id, c.nome, COUNT(vs.id) AS total_vendas, SUM(vs.valor_final) AS total_arrecadado
                           FROM Cabeleireiro c
                           JOIN VendaServico vs ON vs.cabeleireiro_id = c.id
                           JOIN Agendamento a ON a.id = vs.agendamento_id
                           WHERE MONTH(a.data) = MONTH(CURDATE()) AND YEAR(a.data) = YEAR(CURDATE())
                           GROUP BY c.id, c.nome
                           ORDER BY total_arrecadado DESC;
                           """)
            resultados = cursor.fetchall()
            if resultados:
                for (id_cab, nome, total_vendas, total_arrecadado) in resultados:
                    print(f"Cabeleireiro: {nome} | Vendas no mês: {total_vendas} | Arrecadado: R$ {total_arrecadado:.2f}")
            else:
                print("Nenhuma venda realizada no mês atual.")
        except Exception as e:
            print(f"Erro ao gerar relatório: {e}")

def consultar_servicos(conexao):
    print("\n--- Consulta de Serviços ---")
    print("1 - Consultar por nome")
    print("2 - Consultar por faixa de preço")
    escolha = int(input("Escolha a opção: "))
    cursor = conexao.cursor()
    if escolha == 1:
        nome = input("Digite o nome do serviço: ")
        # Usando View
        cursor.execute("SELECT * FROM ServicosView WHERE nome_serv LIKE %s", (f"%{nome}%",))
        resultados = cursor.fetchall()
        print("id_serv | nome_serv | preco")
        print("-"*30)
        for linha in resultados:
            print(f"{linha[0]} | {linha[1]} | R$ {linha[2]:.2f}")
    elif escolha == 2:
        min_preco = float(input("Preço mínimo: "))
        max_preco = float(input("Preço máximo: "))
        # Usando Stored Procedure
        cursor.callproc('ConsultaFaixaPreco', (min_preco, max_preco))
        for result in cursor.stored_results():
            resultados = result.fetchall()
            print("id_serv | nome_serv | preco")
            print("-"*30)
            for linha in resultados:
                print(f"{linha[0]} | {linha[1]} | R$ {linha[2]:.2f}")
    else:
        print("Opção inválida.")

def menu(conexao):
    continua = True
    while(continua):
        opcao = int(input("  Digite o que deseja fazer:\n\t• 1 - Para criar um novo Cliente\n\t• 2 - Para criar um novo Cabeleireiro\n\t• 3 - Para criar um novo Serviço\n\t• 4 - Para criar um novo Agendamento\n\t• 5 - Para registrar uma Venda de Servico\n\t• 6 - Para atualizar alguma informação\n\t• 7 - Para apagar alguma informação\n\t• 8 - Para exibir algum dado\n\t• 9 - Para gerar relatório\n\t• 10 - Consultar serviços\n\t• 0 - Sair\n\t"))
        if(opcao == 1):
            cliente_nome = input("Digite o nome do cliente: ")
            cliente_idade = int(input("Idade: "))
            cliente_tel = input("Telefone: ")
            cliente_email = input("Email: ")
            is_flamengo = input("Torcedor do Flamengo? (s/n): ").lower() == 's'
            is_one_piece = input("Assiste One Piece? (s/n): ").lower() == 's'
            cidade = input("Cidade: ")
            cliente = Cliente(cliente_nome, cliente_idade, cliente_tel, cliente_email, is_flamengo, is_one_piece, cidade)
            Gerencia.inserir(conexao, opcao, cliente)
        elif(opcao == 2):
            cab_nome = input("Digite o nome do cabeleireiro: ")
            cab_idade = int(input("Idade: "))
            cab_telefone = input("Telefone: ")
            cab_email = input("Email: ")
            cab_esp = input("Especializacao: ")
            cabel = Cabeleireiro(cab_nome, cab_idade, cab_telefone, cab_email, cab_esp)
            Gerencia.inserir(conexao, opcao, cabel)
        elif(opcao == 3):
            serv_nome = input("Digite o Nome do serviço: ")
            serv_preco = float(input("Preço: "))
            serv = Servico(serv_nome, serv_preco)
            Gerencia.inserir(conexao, opcao, serv)
        elif(opcao == 4):
            ag_cliente_id = int(input("Digite o ID do cliente a ser agendado: "))
            ag_serv = int(input("Digite o ID do Serviço: "))
            ag_data = input("Data (YYYY-MM-DD): ")
            ag_horario = input("Horario (HH:MM): ")
            agenda = Agendamento(ag_cliente_id, ag_serv, ag_data, ag_horario)
            Gerencia.inserir(conexao, opcao, agenda)
        elif(opcao == 5):
            agendamento_id = int(input("ID do agendamento relacionado: "))
            cabeleireiro_id = int(input("ID do cabeleireiro: "))
            print("Escolha a forma de pagamento:")
            print("1 - Cartão de crédito")
            print("2 - Cartão de débito")
            print("3 - Pix")
            print("4 - Boleto")
            print("5 - Berries")
            escolha = int(input("Digite o número da forma de pagamento: "))
            formas = {
                1: "cartao_credito",
                2: "cartao_debito",
                3: "pix",
                4: "boleto",
                5: "berries"
            }
            forma_pagamento = formas.get(escolha, "pix")
            status_pagamento = input("Status do pagamento (confirmado, pendente, etc): ")
            valor_final = calcular_desconto(conexao, agendamento_id)
            venda = VendaServico(agendamento_id, cabeleireiro_id, forma_pagamento, status_pagamento, valor_final)
            Gerencia.inserir(conexao, opcao, venda)
            print(f"Venda registrada com valor final: R$ {valor_final:.2f}")
        elif(opcao == 6):
            tabela = input("Digite qual tabela deseja atualizar: ")
            coluna = input("Digite a coluna a ser atualizada: ")
            novo_valor = input("Digite o novo valor: ")
            condicao = input("Digite a condição (use aspas, ex: nome = 'Fulano'): ")
            Gerencia.alterar(conexao, tabela, coluna, novo_valor, condicao)
        elif(opcao == 7):
            tabela = input("Digite a tabela o qual deseja apagar: ")
            condicao = input("Digite a condição (use aspas, ex: nome = 'Fulano'): ")
            Gerencia.remover(conexao, tabela, condicao)
        elif(opcao == 8):
            x = input("Você deseja Pesquisar por nome? (s/n): ").lower()
            if(x == 's'):
                tabela = input("Qual tabela deseja pesquisar? ")
                condicao_nome = input("Digite a condição para pesquisar (use aspas, ex: nome = 'Fulano'): ")
                Gerencia.pesquisar_por_nome(conexao, tabela, condicao_nome)
            else:
                y = input("Você deseja exibir tudo ou apenas um? (tudo/um) ").lower()
                if(y=='tudo'):
                    tabelas = ['Cliente', 'Cabeleireiro', 'Servico', 'Agendamento', 'VendaServico']
                    Gerencia.listar_todos(conexao, tabelas)
                else:
                    tabela = input("Digite a tabela que deseja exibir: ")
                    Gerencia.exibir_um(conexao, tabela)
        elif(opcao == 9):
            gerencia = Gerencia()
            gerencia.relatorio(conexao)
        elif(opcao == 10):
            consultar_servicos(conexao)
        else:
            continua = False

# Conectando ao MySQL
conexao = mysql.connector.connect(
    host="localhost",
    user="root",
    password="bd02069900782932",
    database="projeto_bd"
)

menu(conexao)