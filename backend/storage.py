from backend.perfis import Perfil
"""Classe que altera o banco de dados"""
class Storage:
    def __init__(self,perfis_filepath,enderecos_filepath):
        self.database = {}
        self.perfis_filepath = perfis_filepath
        self.enderecos_filepath = enderecos_filepath

    def read_database(self):
        """Lê os arquivos de dados e transforma em atributos da classe"""
        with open(self.perfis_filepath) as f:
            perfis = f.readlines()
        
        with open(self.enderecos_filepath) as f:
            enderecos = f.readlines()

        for perfil,endereco in zip(perfis[1:],enderecos[1:]):
            perfil = perfil.strip().split(",")
            id = perfil[0]
            endereco = endereco.strip().split(",")
            self.database[id] = Perfil(id,perfil[1:],endereco[1:])

    def update_database(self):
        with open(self.perfis_filepath,"w") as f:
            f.write("id nome CPF/CNPJ nascimento contato")
            for perfil in self.database:
                f.write(f"\n{perfil}, {self.database[perfil].nome}, {self.database[perfil].cpf_cnpj}, {self.database[perfil].nascimento}, {self.database[perfil].contato}")

        with open(self.enderecos_filepath,"w") as f:
            f.write("id CEP rua numero complemento bairro cidade UF")
            for perfil in self.database:
                f.write(f"\n{perfil}, {self.database[perfil].CEP}, {self.database[perfil].rua}, {self.database[perfil].numero}, {self.database[perfil].complemento}, {self.database[perfil].bairro}, {self.database[perfil].cidade}, {self.database[perfil].UF}")
    
    def create_profile(self,personal_values,adress_values):
        id = "1" if not self.database.keys() else str(int(max(self.database.keys(),key=int)) + 1)
        new_profile = Perfil(id,personal_values,adress_values)
        if not new_profile.valid_profile():
            return False
        self.database[id] = new_profile
        self.update_database()
        return True

    def delete_profile(self,id):
        if id in self.database.keys():
            self.database.pop(id)
            self.update_database()

    def update_profile(self,id,personal_info,adress_info):
        updated_profile = Perfil(id,personal_info,adress_info)
        if not updated_profile.valid_profile():
            return False
        self.database[id] = updated_profile
        self.update_database()
        return True
