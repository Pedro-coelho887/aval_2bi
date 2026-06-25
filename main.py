from backend.storage import Storage

def main():
    storage = Storage("backend/perfis.txt","backend/enderecos.txt")
    storage.read_database()
    storage.create_profile("Pedro","450","21-02-03","998932152","873348")
    storage.create_profile("Renan","3223","03-02-04","986254624","30030")
    storage.create_profile("Ana","898","04-04-09","612571","029323")
    storage.create_profile("Victor","9093","04-05-99","3535","03453")
    storage.delete_profile("2")
    storage.update_profile("4","Vitinho")
    storage.read_database()

if __name__ == "__main__":
    main()