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
            self.perfil_database[perfil_parts[0]] = perfil_parts[1:]

        with open(self.enderecos_filepath) as f:
            enderecos = f.readlines()

        for endereco in enderecos[1:]:
            endereco_parts = endereco.strip().split(",")
            self.enderecos_database[endereco_parts[0]] = endereco_parts[1:]

        for perfil in self.perfil_database:
            print(self.perfil_database[perfil])
    
    def update_database(self):
        with open(self.perfis_filepath,"w") as f:
            f.write("id nome CPF/CNPJ nascimento contato")
            for perfil in self.perfil_database:
                f.write(f"\n{perfil}, {self.perfil_database[perfil][0]}, {self.perfil_database[perfil][1]}, {self.perfil_database[perfil][2]}, {self.perfil_database[perfil][3]}")


    def create_profile(self,nome,cpf_cnpj,nascimento,contato,CEP):
        id = "1" if not self.perfil_database.keys() else str(int(max(self.perfil_database.keys())) + 1)
        self.perfil_database[id] = [nome,cpf_cnpj,nascimento,contato]
        self.update_database()

    def delete_profile(self,id):
        if id in self.perfil_database.keys():
            self.perfil_database.pop(id)
            self.update_database()

    def update_profile(self,id,novo_nome=None,novo_cpf_cnpj=None,novo_nascimento=None,novo_contato=None,novo_CEP=None):
        novos_dados = [novo_nome,novo_cpf_cnpj,novo_nascimento,novo_contato]
        for i,novo_dado in enumerate(novos_dados):
            if novo_dado is None:
                novos_dados[i] = self.perfil_database[id][i]
        self.perfil_database[id] = novos_dados
        self.update_database()


        