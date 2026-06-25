from datetime import datetime as dt
"""Classe que representa o Usuário"""
class Perfil:
    def __init__(self,id:str,nome:str,cpf_cnpj:str,nascimento:str,CEP:str,contato:str):
        self.id = id
        self.nome = nome
        self.cpf_cnpj = cpf_cnpj
        self.nascimento = nascimento
        self.CEP = CEP
        self.contato = contato
    
    def check_birthdate(self):
        pass
        # try:
        #     self.nascimento = dt.strptime(self.nascimento,"%d/%m/%Y")
        