import sqlite3

#Entidade cliente
class Cliente:
	def __init__(self, nome, idade, telefone, email):
		self.nome = nome
		self.idade = idade
		self.telefone = telefone
		self.email = email

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
	def __init__(self, id_serv, nome_serv, preco):
		self.id_serv = id_serv
		self.nome_serv = nome_serv
		self.preco = preco

#Entidade agendamento
class Agendamento:
	def __init__(self, cliente, servico, data, hora):
		self.cliente = cliente
		self.servico = servico
		self.data = data
		self.hora = hora

#Classe para gerenciar as relações
class Gerencia:
	def inserir(conexao, tabela, objeto):
		cursor = conexao.cursor()
		
		#Inserir na Tabela Cliente
		if tabela == 1:
			comando = "INSERT INTO Cliente VALUES (?, ?, ?, ?)"
			values = (objeto.nome, objeto.idade, objeto.telefone, objeto.email)
		
		#Inserir na Tabela Cabeleireiro
		elif tabela == 2:
			comando = "INSERT INTO Cabeleireiro VALUES (?, ?, ?, ?, ?)"
			values = (objeto.nome, objeto.idade, objeto.telefone, objeto.email, objeto.especializacao)
		
		#Inserir na Tabela Serviço
		elif tabela == 3:
			comando = "INSERT INTO Servico VALUES (?, ?, ?)"
			values = (objeto.id_serv, objeto.nome_serv, objeto.preco)
		
		#Inserir na Tabela Agendamento
		elif tabela == 4:
			comando = "INSERT INTO Agendamento VALUES (?, ?, ?, ?)"
			values = (objeto.cliente, objeto.servico, objeto.data, objeto.hora)
		
		try:
			cursor.execute(comando, values)
			conexao.commit()
		except sqlite3.Error as err:
			print(f"Erro: {err}")
	
	#Alterar tupla em uma tabela
	def alterar(conexao, tabela, coluna,novo_dado, condicao):
		cursor = conexao.cursor()
		comando = f"UPDATE {tabela} SET {coluna} = {novo_dado} WHERE {condicao}"
		try:
			cursor.execute(comando)
			conexao.commit()
		except sqlite3.Error as err:
			print(f"Erro: {err}")
		
	#Remover tupla de alguma tabela pela condicao
	def remover(conexao, tabela, condicao):
		cursor = conexao.cursor()
		comando = f"DELETE FROM {tabela} WHERE {condicao}"
		try:
			cursor.execute(comando)
			conexao.commit()
		except sqlite3.Error as err:
			print(f"Erro: {err}")

	#Recuperar uma tupla de alguma tabela por um nome(condicao)
	def pesquisar_por_nome(conexao, tabela, cond_nome):
		cursor = conexao.cursor()
		comando = f"SELECT * FROM {tabela} WHERE {cond_nome}"
		try:
			cursor.execute(comando)
			resultado = cursor.fetchall()
		except sqlite3.Error as err:
			print(f"Erro: {err}")
		
		for linha in resultado:
			print(linha)
		
	#Exibir todas tabelas
	def listar_todos(conexao, tabela):
		cursor = conexao.cursor()
		comando = f"SELECT * FROM {tabela}"
		try:
			cursor.execute(comando)
			resultado = cursor.fetchall()
		except sqlite3.Error as err:
			print(f"Erro: {err}")
			
		for linha in resultado:
			print(linha)
		
	#Exibir uma tabela 
	def exibir_um(conexao, tabela):
		cursor = conexao.cursor()
		comando = f"SELECT * FROM {tabela}"
		try:
			cursor.execute(comando)
			resultado = cursor.fetchall()
		except sqlite3.Error as err:
			print(f"Erro: {err}")
			
		for linha in resultado:
			print(linha)
	

		
		
def menu(conexao):
		continua = True
		while(continua):
			opcao = int(input("  Digite o que deseja fazer:\n\t• 1 - Para criar um novo Cliente\n\t• 2 - Para criar um novo Cabeleireiro\n\t• 3 - Para criar um novo Serviço\n\t• 4 - Para criar um novo Agendamento\n\t• 5 - Para atualizar alguma informação\n\t• 6 - Para apagar alguma informação\n\t• 7 - Para exibir algum dado\n\t"))
			
			if(opcao == 1):
				cliente_nome = input("Digite o nome do cliente: ")
				cliente_idade = int(input("Idade: "))
				cliente_tel = input("Telefone: ")
				cliente_email = input("Email: ")
				
				clienti = Cliente(cliente_nome, 					cliente_idade, cliente_tel, cliente_email)
				Gerencia.inserir(conexao, opcao, clienti)

			
			elif(opcao == 2):
				cab_nome = input("Digite o nome do cabeleireiro: ")
				cab_idade = int(input("Idade: "))
				cab_telefone = input("Telefone: ")
				cab_email = input("Email: ")
				cab_esp = input("Especializacao: ")
				
				cabel = Cabeleireiro(cab_nome, cab_idade, cab_telefone, cab_email, cab_esp)
				Gerencia.inserir(conexao, opcao, cabel)
				
			
			elif(opcao == 3):
				serv_id = int(input("Digite o ID do Serviço: "))
				serv_nome = input("Digite o Nome do serviço: ")
				serv_preco = float(input("Preço: "))
				
				serv = Servico(serv_id, serv_nome, serv_preco)
				Gerencia.inserir(conexao, opcao, serv)
				
			
			elif(opcao == 4):
				ag_cliente = input("Digite o email do cliente a ser agendado: ")
				ag_serv = int(input("Digite o ID do Serviço: "))
				ag_data = input("Data: ")
				ag_horario = input("Horario: ")
				
				agenda = Agendamento(ag_cliente, ag_serv, ag_data, ag_horario)
				Gerencia.inserir(conexao, opcao, agenda)
				
			
			elif(opcao == 5):
				tabela = input("Digite qual tabela deseja atualizar: ")
				coluna = input("Digite a coluna a ser atualizada: ")
				novo_valor = input("Digite o novo valor: ")
				condicao = input("Digite a condição (use aspas, ex: nome = 'Fulano'): ")
				
				Gerencia.alterar(conexao, tabela, coluna, novo_valor, condicao)
			
			
			elif(opcao == 6):
				tabela = input("Digite a tabela o qual deseja apagar: ")
				condicao = input("Digite a condição (use aspas, ex: nome = 'Fulano'): ")
				
				Gerencia.remover(conexao, tabela, condicao)
				
				
			elif(opcao == 7):
				x = input("Você deseja Pesquisar por nome? (s/n): ")
				x = x.lower()
				
				if(x == 's'):
					tabela = input("Qual tabela deseja pesquisar? ")
					condicao_nome = input("Digite a condição para pesquisar (use aspas, ex: nome = 'Fulano'): ")
					
					Gerencia.pesquisar_por_nome(conexao, tabela, condicao_nome)
					
					
				else:
					y = input("Você deseja exibir tudo ou apenas um? (tudo/um) ")
					y = y.lower()
					
					if(y=='tudo'):
						tabelas = ['Cliente', 'Cabeleireiro', 'Servico', 'Agendamento']
						for i in tabelas:
							Gerencia.listar_todos(conexao, i)

			
					else:
						tabela = input("Digite a tabela que deseja exibir: ")
						Gerencia.exibir_um(conexao, tabela)
			
			
			else:
				continua = False



conexao = sqlite3.connect("projp1.db")
menu(conexao)