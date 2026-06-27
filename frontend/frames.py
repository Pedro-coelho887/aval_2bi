import tkinter as tk
from tkinter import ttk
import requests
"""Classe do Frame Principal do App"""
class MainFrame:
    def __init__(self,janela,open_newprofile_window,delete_profile,update_profile):
        self.frame = tk.Frame(janela)
        self.colunas = ("id","nome","CPF/CNPJ","nascimento","contato")

        self.tabela = ttk.Treeview(self.frame,columns=self.colunas,show="headings")
        self.tabela.heading("id",text="ID")
        self.tabela.heading("nome",text="Nome")
        self.tabela.heading("CPF/CNPJ",text="CPF/CNPJ")
        self.tabela.heading("nascimento",text="Data de Nascimento")
        self.tabela.heading("contato",text="Contato")
        
        self.create_profilebutton = tk.Button(self.frame,text="Novo Perfil",command=open_newprofile_window)
        self.deletebutton = tk.Button(self.frame,text="Deletar Perfil",command=delete_profile)
        self.update_profilebutton = tk.Button(self.frame,text="Atualizar Perfil",command=update_profile)
        self.label = tk.Label(self.frame,text="Bem vindo ao catálogo de profissionais!")
    
    def update_table(self,database):
        # Remove todas as linhas atuais
        for row in self.tabela.get_children():
            self.tabela.delete(row)

        # Reinsere com os dados atualizados
        for id, perfil in database.items():
            self.tabela.insert("", tk.END, values=(id, perfil.nome, perfil.cpf_cnpj,perfil.nascimento,perfil.contato))

    def build_window(self):
        self.label.pack(pady=10)
        self.tabela.pack(pady=10)
        self.create_profilebutton.pack(pady=10,side="left")
        self.deletebutton.pack(pady=10,side="left")
        self.update_profilebutton.pack(pady=10,side="left")

"""Classe do Frame utilizado para criar Novo usuário"""
class NewProfileFrame:
    def __init__(self,janela,update_main_window,add_user):
        self.frame = tk.Frame(janela)
        self.label = tk.Label(self.frame,text="Cadastro de novo profissional")
        self.newprofile_label = tk.Label(self.frame,text="")
        self.personal_info = {"Nome": tk.StringVar(),"CPF/CNPJ":tk.StringVar(),"Data de Nascimento":tk.StringVar(),"Contato (Com DDD)": tk.StringVar()}
        self.adress_info = {"CEP":tk.StringVar(),"Rua":tk.StringVar(),"Numero":tk.StringVar(),
                            "Complemento":tk.StringVar(),"Bairro":tk.StringVar(),"Cidade":tk.StringVar(),"UF":tk.StringVar()}
        self.returnbutton = tk.Button(self.frame,text="Retornar",command=update_main_window)
        self.confirmbutton = tk.Button(self.frame,text="Criar Novo Perfil",command= lambda:add_user(self.personal_info,self.adress_info))
        self.searchCEPbutton = tk.Button(self.frame,text="Buscar CEP",command=self.get_address)

    def get_address(self):
        response = requests.get(f"https://viacep.com.br/ws/{self.adress_info["CEP"].get()}/json/")

        if response.status_code != 200:
            return
        
        dados = response.json()
        if "erro" in dados:
            return
        self.adress_info["Rua"].set(dados["logradouro"])
        self.adress_info["Bairro"].set(dados["bairro"])
        self.adress_info["Cidade"].set(dados["localidade"])
        self.adress_info["UF"].set(dados["uf"])
        

    def update_window(self):
        # Limpa todos os campos de input
        for var in self.personal_info.values():
            var.set("")
        self.personal_info["Data de Nascimento"].set("DD/MM/YYYY")

        for var in self.adress_info.values():
            var.set("")
        # Limpa a mensagem de feedback
        self.newprofile_label.config(text="")
    
    def build_window(self):
        self.label.grid(row=0,columnspan=2,pady=10)

        for i, (desc,var) in enumerate(self.personal_info.items()):
            tk.Label(self.frame,text=desc+":").grid(row=i+1,column=0,sticky="e",padx=5,pady=3)
            tk.Entry(self.frame,textvariable=var,width=30).grid(row=i+1,column=1,padx=5,pady=3)
        
        for i, (desc,var) in enumerate(self.adress_info.items()):
            tk.Label(self.frame,text=desc+":").grid(row=i+1,column=2,sticky="e",padx=5,pady=3)
            tk.Entry(self.frame,textvariable=var,width=30).grid(row=i+1,column=3,padx=5,pady=3)

        self.returnbutton.grid(row=6,column=0,pady=10)
        self.confirmbutton.grid(row=6,column=1,pady=10)
        self.newprofile_label.grid(row=7,column=1,pady=10)
        self.searchCEPbutton.grid(row = 1, column=4)

"""Classe do Frame de atualização de Perfil"""
class UpdateProfileFrame:
    def __init__(self,janela,update_main_window,update_profile):
        self.frame = tk.Frame(janela)
        self.label = tk.Label(self.frame,text="Atualização de Cadastro")
        self.updateprofile_label = tk.Label(self.frame,text="")
        self.personal_info = {"Nome": tk.StringVar(),"CPF/CNPJ":tk.StringVar(),"Data de Nascimento":tk.StringVar(),"Contato (Com DDD)": tk.StringVar()}
        self.adress_info = {"CEP":tk.StringVar(),"Rua":tk.StringVar(),"Numero":tk.StringVar(),
                            "Complemento":tk.StringVar(),"Bairro":tk.StringVar(),"Cidade":tk.StringVar(),"UF":tk.StringVar()}
        self.update_id = None
        self.returnbutton = tk.Button(self.frame,text="Retornar",command=update_main_window)
        self.confirmbutton = tk.Button(self.frame,text="Atualizar Perfil",command= lambda:update_profile(self.update_id,self.personal_info,self.adress_info))
        self.searchCEPbutton = tk.Button(self.frame,text="Buscar CEP",command=self.get_address)
    
    def get_address(self):
        response = requests.get(f"https://viacep.com.br/ws/{self.adress_info["CEP"].get()}/json/")

        if response.status_code != 200:
            return
        
        dados = response.json()
        if "erro" in dados:
            return
        self.adress_info["Rua"].set(dados["logradouro"])
        self.adress_info["Bairro"].set(dados["bairro"])
        self.adress_info["Cidade"].set(dados["localidade"])
        self.adress_info["UF"].set(dados["uf"])

    def update_window(self,profile):
        # Atualiza todos os campos de input
        self.update_id = profile.id
        self.personal_info["Nome"].set(profile.nome)
        self.personal_info["CPF/CNPJ"].set(profile.cpf_cnpj)
        self.personal_info["Data de Nascimento"].set(profile.nascimento)
        self.personal_info["Contato (Com DDD)"].set(profile.contato)

        self.adress_info["CEP"].set(profile.CEP)
        self.adress_info["Rua"].set(profile.rua)
        self.adress_info["Numero"].set(profile.numero)
        self.adress_info["Complemento"].set(profile.complemento)
        self.adress_info["Bairro"].set(profile.bairro)
        self.adress_info["Cidade"].set(profile.cidade)
        self.adress_info["UF"].set(profile.UF)

        # Limpa a mensagem de feedback
        self.updateprofile_label.config(text="")

    def build_window(self):
        self.label.grid(row=0,columnspan=2,pady=10)

        for i, (desc,var) in enumerate(self.personal_info.items()):
            tk.Label(self.frame,text=desc+":").grid(row=i+1,column=0,sticky="e",padx=5,pady=3)
            tk.Entry(self.frame,textvariable=var,width=30).grid(row=i+1,column=1,padx=5,pady=3)
        
        for i, (desc,var) in enumerate(self.adress_info.items()):
            tk.Label(self.frame,text=desc+":").grid(row=i+1,column=2,sticky="e",padx=5,pady=3)
            tk.Entry(self.frame,textvariable=var,width=30).grid(row=i+1,column=3,padx=5,pady=3)

        self.returnbutton.grid(row=6,column=0,pady=10)
        self.confirmbutton.grid(row=6,column=1,pady=10)
        self.updateprofile_label.grid(row=7,column=1,pady=10)
        self.searchCEPbutton.grid(row = 1, column=4)





"""Classe do Frame utilizado registrar informação"""
class FillInfoFrame:
    def __init__(self,janela,update_main_window,confirm_func,text_confirmbutton,text_mainlabel):
        self.frame = tk.Frame(janela)
        self.label = tk.Label(self.frame,text=text_mainlabel)
        self.warning_label = tk.Label(self.frame,text="")
        self.id = None
        self.personal_info = {"Nome": tk.StringVar(),"CPF/CNPJ":tk.StringVar(),"Data de Nascimento":tk.StringVar(),"Contato (Com DDD)": tk.StringVar()}
        self.adress_info = {"CEP":tk.StringVar(),"Rua":tk.StringVar(),"Numero":tk.StringVar(),
                            "Complemento":tk.StringVar(),"Bairro":tk.StringVar(),"Cidade":tk.StringVar(),"UF":tk.StringVar()}
        self.returnbutton = tk.Button(self.frame,text="Retornar",command=update_main_window)
        self.confirmbutton = tk.Button(self.frame,text=text_confirmbutton,command= lambda:confirm_func(self.id,self.personal_info,self.adress_info))
        self.searchCEPbutton = tk.Button(self.frame,text="Buscar CEP",command=self.get_address)

    def get_address(self):
        response = requests.get(f"https://viacep.com.br/ws/{self.adress_info["CEP"].get()}/json/")

        if response.status_code != 200:
            return
        
        dados = response.json()
        if "erro" in dados:
            return
        self.adress_info["Rua"].set(dados["logradouro"])
        self.adress_info["Bairro"].set(dados["bairro"])
        self.adress_info["Cidade"].set(dados["localidade"])
        self.adress_info["UF"].set(dados["uf"])
        

    def update_window(self,profile=None):
        if profile is None:
            # Limpa todos os campos de input
            for var in self.personal_info.values():
                var.set("")
            self.personal_info["Data de Nascimento"].set("DD/MM/YYYY")

            for var in self.adress_info.values():
                var.set("")
        else:
            # Atualiza todos os campos de input
            self.id = profile.id
            self.personal_info["Nome"].set(profile.nome)
            self.personal_info["CPF/CNPJ"].set(profile.cpf_cnpj)
            self.personal_info["Data de Nascimento"].set(profile.nascimento)
            self.personal_info["Contato (Com DDD)"].set(profile.contato)

            self.adress_info["CEP"].set(profile.CEP)
            self.adress_info["Rua"].set(profile.rua)
            self.adress_info["Numero"].set(profile.numero)
            self.adress_info["Complemento"].set(profile.complemento)
            self.adress_info["Bairro"].set(profile.bairro)
            self.adress_info["Cidade"].set(profile.cidade)
            self.adress_info["UF"].set(profile.UF)
        # Limpa a mensagem de feedback
        self.warning_label.config(text="")
    
    def build_window(self):
        self.label.grid(row=0,columnspan=2,pady=10)

        for i, (desc,var) in enumerate(self.personal_info.items()):
            tk.Label(self.frame,text=desc+":").grid(row=i+1,column=0,sticky="e",padx=5,pady=3)
            tk.Entry(self.frame,textvariable=var,width=30).grid(row=i+1,column=1,padx=5,pady=3)
        
        for i, (desc,var) in enumerate(self.adress_info.items()):
            tk.Label(self.frame,text=desc+":").grid(row=i+1,column=2,sticky="e",padx=5,pady=3)
            tk.Entry(self.frame,textvariable=var,width=30).grid(row=i+1,column=3,padx=5,pady=3)

        self.returnbutton.grid(row=6,column=0,pady=10)
        self.confirmbutton.grid(row=6,column=1,pady=10)
        self.warning_label.grid(row=7,column=1,pady=10)
        self.searchCEPbutton.grid(row = 1, column=4)