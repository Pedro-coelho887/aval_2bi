from backend.perfis import Perfil
"""Classe que altera o banco de dados"""
class Storage:
    def __init__(self,perfis_filepath,enderecos_filepath):
        self.perfil_database = {}
        self.enderecos_database = {}
        self.perfis_filepath = perfis_filepath
        self.enderecos_filepath = enderecos_filepath
    def read_database(self):
        """Lê os arquivos de dados e transforma em atributos da classe"""
        with open(self.perfis_filepath) as f:
            perfis = f.readlines()
        
        for perfil in perfis[1:]:
            perfil_parts = perfil.strip().split(",")
            self.perfil_database[perfil_parts[0]] = Perfil(perfil_parts[0],perfil_parts[1],perfil_parts[2],perfil_parts[3],perfil_parts[4],"60810786")

        with open(self.enderecos_filepath) as f:
            enderecos = f.readlines()

        for endereco in enderecos[1:]:
            endereco_parts = endereco.strip().split(",")
            self.enderecos_database[endereco_parts[0]] = endereco_parts[1:]

    def update_database(self):
        with open(self.perfis_filepath,"w") as f:
            f.write("id nome CPF/CNPJ nascimento contato")
            for perfil in self.perfil_database:
                f.write(f"\n{perfil}, {self.perfil_database[perfil].nome}, {self.perfil_database[perfil].cpf_cnpj}, {self.perfil_database[perfil].nascimento}, {self.perfil_database[perfil].contato}")

    def create_profile(self,nome,cpf_cnpj,nascimento,contato,CEP):
        id = "1" if not self.perfil_database.keys() else str(int(max(self.perfil_database.keys(),key=int)) + 1)
        new_profile = Perfil(id,nome,cpf_cnpj,nascimento,contato,CEP)
        if not new_profile.valid_profile():
            return False
        self.perfil_database[id] = new_profile
        self.update_database()
        return True

    def delete_profile(self,id):
        if id in self.perfil_database.keys():
            self.perfil_database.pop(id)
            self.update_database()

    def update_profile(self,id,novos_dados):
        updated_profile = Perfil(id,*novos_dados,"60810")
        if not updated_profile.valid_profile():
            return False
        self.perfil_database[id] = updated_profile
        self.update_database()
        return True
