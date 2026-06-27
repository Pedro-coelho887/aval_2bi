import tkinter as tk
from tkinter import ttk
from backend.storage import Storage
from frontend.frames import MainFrame,FillInfoFrame,InfoFrame
"""Classe principal do App"""
class App:
    def __init__(self):
        self.janela = tk.Tk()
        self.janela.title("Catálogo de profissionais")
        self.mainframe = MainFrame(self.janela,self.open_newprofile_window,self.delete_profile,self.open_updateprofile_window)
        self.newprofileframe = FillInfoFrame(self.janela,self.open_main_window,self.add_profile,"Criar Novo Perfil","Criação de Perfil")
        self.updateprofileframe = FillInfoFrame(self.janela,self.open_main_window,self.update_profile,"Atualizar Perfil","Atualização Perfil")
        self.infoframe = InfoFrame(self.janela,self.open_main_window)
        self.storage = Storage("backend/perfis.txt","backend/enderecos.txt")

    def open_main_window(self):
        self.storage.read_database()
        self.mainframe.update_table(self.storage.database)
        self.mainframe.frame.tkraise()
           
    def open_newprofile_window(self):
        self.newprofileframe.update_window()
        self.newprofileframe.frame.tkraise()

    def open_updateprofile_window(self):
        selected = self.mainframe.tabela.selection()
        if not selected:
            return
        item = selected[0]
        id = self.mainframe.tabela.item(item, "values")[0]
        profile = self.storage.database[id]
        self.updateprofileframe.update_window(profile)
        self.updateprofileframe.frame.tkraise()

    def add_profile(self,id,personal_info,adress_info):
        personal_values = [v.get() for v in personal_info.values()]
        adress_values = [v.get() for v in adress_info.values()]
        if self.storage.create_profile(personal_values,adress_values):
            self.newprofileframe.warning_label.config(text="Perfil Adicionado!")
        else:
            self.newprofileframe.warning_label.config(text="Perfil inválido. Revise as informações.")

    def delete_profile(self):
        selected = self.mainframe.tabela.selection()
        if not selected:
            return
        item = selected[0]
        valores = self.mainframe.tabela.item(item, "values")
        id = valores[0]  

        self.storage.delete_profile(id)

        self.mainframe.tabela.delete(item)

    def update_profile(self,id,personal_info,adress_info):
        personal_values = [v.get() for v in personal_info.values()]
        adress_values = [v.get() for v in adress_info.values()]
        if not self.storage.update_profile(id,personal_values,adress_values):
            self.updateprofileframe.warning_label.config(text="Perfil Inválido. Revise as informações")
        else:
            self.updateprofileframe.warning_label.config(text="Perfil Atualizado!")

    def display_infoframe(self,event):
        selected = self.mainframe.tabela.selection()

        if not selected:
            return
        item = selected[0]
        id = self.mainframe.tabela.item(item, "values")[0]
        profile = self.storage.database[id]

        self.infoframe.update_window(profile)
        self.infoframe.frame.tkraise()

    def run(self):
        self.mainframe.frame.grid(row=0,column=0,sticky="nsew")
        self.newprofileframe.frame.grid(row=0,column=0,sticky="nsew")
        self.updateprofileframe.frame.grid(row=0,column=0,sticky="nsew")
        self.infoframe.frame.grid(row=0,column=0,sticky="nsew")

        self.mainframe.build_window(self.display_infoframe)
        self.newprofileframe.build_window()
        self.updateprofileframe.build_window()
        self.infoframe.build_window()

        self.open_main_window()
        self.janela.mainloop()

def main():
    new_app = App()
    new_app.run()

if __name__ == "__main__":
    main()
