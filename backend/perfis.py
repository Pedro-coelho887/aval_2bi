from datetime import datetime as dt
from validate_docbr import CPF,CNPJ
import phonenumbers
import requests
"""Classe que representa o Perfil"""
class Perfil:
    def __init__(self,id:str,personal_info,adress_info):
        self.id = id.strip()
        self.nome = personal_info[0].strip()
        self.cpf_cnpj = personal_info[1].strip()
        self.nascimento = personal_info[2].strip()
        self.contato = personal_info[3].strip()
        
        self.CEP = adress_info[0].replace("-","").strip()
        self.rua = adress_info[1]
        self.numero = adress_info[2]
        self.complemento = adress_info[3]
        self.bairro = adress_info[4]
        self.cidade = adress_info[5]
        self.UF = adress_info[6]

    def valid_birthdate(self):
        try:
            self.nascimento = dt.strptime(str(self.nascimento),"%d/%m/%Y")
            if 1920<self.nascimento.year<2005:
                self.nascimento = self.nascimento.strftime("%d/%m/%Y")
                return True
            return False
        except ValueError:
            return False
        
    def valid_cpf_cnpj(self):
        cpf = CPF()
        cnpj = CNPJ()
        if cpf.validate(self.cpf_cnpj):
            self.cpf_cnpj = cpf.mask(self.cpf_cnpj)
            return True
        elif cnpj.validate(self.cpf_cnpj):
            self.cpf_cnpj = cnpj.mask(self.cpf_cnpj)
            return True
        return False

    def valid_phonenumber(self):
        try:
            self.contato = phonenumbers.parse(str(self.contato),"BR")
            if not phonenumbers.is_valid_number(self.contato):
                return False
            self.contato = str(self.contato.national_number)
            return True
        except:
            return False

    def valid_profile(self):
        if not self.valid_birthdate() or not self.valid_cpf_cnpj() or not self.valid_phonenumber():
            return False
        return True
        