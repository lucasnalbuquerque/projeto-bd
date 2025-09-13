import sqlite3

conexao = sqlite3.connect("projeto.db")

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
		self.cliente = cliente.nome
		self.servico = servico.id_serv
		self.data = data
		self.hora = hora

#Classe para gerenciar as relações
class Gerencia:
	#Função para criar, alterar e deletar
	def executa(conexao, comando, ob=None):
		cursor = conexao.cursor()
		try:
			if(ob):
				cursor.execute(comando, ob)
			else:
				cursor.execute(comando)
			conexao.commit()
			print("Comando executado com sucesso!")
		except sqlite3.Error as err:
			print(f"Error: {err}")
			
	#Função para leitura (seleção)
	def select(conexao, comando):
		cursor = conexao.cursor()
		result = None
		try:
			cursor.execute(comando)
			result = cursor.fetchall()
			return result
		except sqlite3.Error as err:
			print(f"Error: {err}")
			
			
continua=True
while(continua):
	print("Digite: • 0 para parar\n\t• 1 para criar um Cliente\n\t• 2 para criar um Cabeleireiro\n\t• 3 para criar um Servico\n\t• 4 para criar um Agendamento\n\t• 5 para executar um comando SQL\n\t• 6 para recuperar alguma informacao")
	x = int(input())
	
	match x:
		case 0:
			continua=False
			
		case 1:
			cliente_nome = input("Digite o nome do cliente: ")
			cliente_idade = int(input("Idade: "))
			cliente_tel = input("Telefone: ")
			cliente_email = input("Email: ")
			clienti = Cliente(cliente_nome, cliente_idade, cliente_tel, cliente_email)
			
			inserir = "INSERT INTO Cliente VALUES (?, ?, ?, ?)"
			Gerencia.executa(conexao, inserir, (clienti.nome, clienti.idade, clienti.telefone, clienti.email))
				
		case 2:
			cab_nome = input("Digite o nome do cabeleireiro: ")
			cab_idade = int(input("Idade: "))
			cab_telefone = input("Telefone: ")
			cab_email = input("Email: ")
			cab_esp = input("Especializacao: ")
			cab = Cabeleireiro(cab_nome, cab_idade, cab_telefone, cab_email, cab_esp)
			
			inserir = "INSERT INTO Cabeleireiro VALUES (?, ?, ?, ?, ?)"
			Gerencia.executa(conexao, inserir, (cab.nome, cab.idade, cab.telefone, cab.email, cab.especializacao))
				
		case 3:
			serv_id = int(input("Digite o ID do serviço: "))
			serv_nome = input("Nome do serviço: ")
			serv_preco = float(input("Preço: "))
			serv = Servico(serv_id, serv_nome, serv_preco)
			
			inserir = "INSERT INTO Servico VALUES (?, ?,() ?)"
			Gerencia.executa(conexao, inserir, (serv.id, serv.nome, serv.preco))
		
		case 4:
			ag_data = input("Data: ")
			ag_horario = input("Horario: ")
			agenda = Agendamento(ag_cliente, ag_serv, ag_data, ag_horario)
			
			inserir = "INSERIR INTO Agendamento VALUES (?, ?, ?, ?)"
			Gerencia.executa(conexao, inserir, (clienti, serv, agenda.data, agenda.horario))
		
		case 5:
			print("Digite o comando: ")
			comando = input()
			Gerencia.executa(conexao, comando)
		
		case 6:
			print("Digite o select: ")
			comando = input()
			result = Gerencia.select(conexao, comando)
			
			for linha in result:
				print(linha)