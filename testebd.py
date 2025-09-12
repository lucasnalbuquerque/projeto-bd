import sqlite3

conexao = sqlite3.connect("projeto.db")

#Entidade cliente
class cliente:
	def __init__(self, nome, idade, telefone, email):
		self.nome = nome
		self.idade = idade
		self.telefone = telefone
		self.email = email

#Entidade cabeleireiro
class cabeleireiro:
	def __init__(self, nome, idade, telefone, email, especializacao):
		self.nome = nome
		self.idade = idade
		self.telefone = telefone
		self.email = email
		self.especializacao = especializacao

#Entidade serviço
class servico:
	def __init__(self, id_serv, nome_serv, preco):
		self.id_serv = id_serv
		self.nome_serv = nome_serv
		self.preco = preco

#Entidade agendamento
class agendamento:
	def __init__(self, data, hora):
		self.data = data
		self.hora = hora

#Classe para gerenciar as relações
class gerencia:
	#Função para criar, alterar e deletar
	def executa(conexao, comando):
		cursor = conexao.cursor()
		try:
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
			
			
		
		