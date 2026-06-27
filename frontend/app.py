import tkinter as tk
from tkinter import ttk
from backend.storage import Storage
from frontend.frames import MainFrame,NewProfileFrame,UpdateProfileFrame
class App:
    def __init__(self):
        self.janela = tk.Tk()
        self.janela.title("Catálogo de profissionais")
        self.mainframe = MainFrame(self.janela,self.open_newprofile_window,self.delete_profile,self.open_updateprofile_window)
        self.newprofileframe = NewProfileFrame(self.janela,self.open_main_window,self.add_profile)
        self.updateprofileframe = UpdateProfileFrame(self.janela,self.open_main_window,self.update_profile)
        self.storage = Storage("backend/perfis.txt","backend/enderecos.txt")

    def open_main_window(self):
        self.storage.read_database()
        self.mainframe.update_table(self.storage.perfil_database)
        self.mainframe.frame.tkraise()
           
    def open_newprofile_window(self):
        self.newprofileframe.update_window()
        self.newprofileframe.frame.tkraise()

    def open_updateprofile_window(self):
        selected = self.mainframe.tabela.selection()
        if not selected:
            return
        item = selected[0]
        valores = self.mainframe.tabela.item(item, "values")
        self.updateprofileframe.update_window(valores)
        self.updateprofileframe.frame.tkraise()

    def add_profile(self,campos):
        valores = [v.get() for v in campos.values()]
        self.storage.create_profile(valores[0],valores[1],valores[2],valores[3],60810)
        self.newprofileframe.newprofile_label.config(text="Usuário Adicionado!")

    def delete_profile(self):
        selected = self.mainframe.tabela.selection()
        if not selected:
            return
        item = selected[0]
        valores = self.mainframe.tabela.item(item, "values")
        id = valores[0]  

        self.storage.delete_profile(id)

        self.mainframe.tabela.delete(item)

    def update_profile(self,campos):
        valores = [v.get() for v in campos.values()]
        self.storage.update_profile(self.updateprofileframe.update_id,valores[0],valores[1],valores[2],valores[3],60810)
        self.updateprofileframe.updateprofile_label.config(text="Usuário Atualizado!")

    def run(self):
        self.mainframe.frame.grid(row=0,column=0,sticky="nsew")
        self.newprofileframe.frame.grid(row=0,column=0,sticky="nsew")
        self.updateprofileframe.frame.grid(row=0,column=0,sticky="nsew")

        self.mainframe.build_window()
        self.newprofileframe.build_window()
        self.updateprofileframe.build_window()
        
        self.open_main_window()
        self.janela.mainloop()

def main():
    new_app = App()
    new_app.run()

if __name__ == "__main__":
    main()
