import os
from dotenv import load_dotenv
from ai_client import PythonAI

class Application:
    
    def __init__(self, api_key):
        self.ai = PythonAI(api_key)

    def menu(self):
        print("Bem-vindo Corretor PythonAI!")
        print("=========================")

        while True:
            print("Escolha uma das opções:")
            print("1 - Corrigir texto, escolha o texto que desejado.")
            print("0 - Sair.")
            print("=========================")

            try:
                op = int(input("Opção: "))
            except ValueError:
                print("Entrada inválida! Digite apenas números.")
                continue

            if op == 1:
                prompt = input("Faça uma pergunta: ")
                response = self.ai.ask(prompt)
                print(response)

            elif op == 0:
                print("Até mais!")
                break

            else:
                print("Opção inválida!")

            print("=========================")


if __name__ == "__main__":

    load_dotenv()
    
    api_key = os.getenv("API_KEY")

    if not api_key:
        raise ValueError("A variável de ambiente API_KEY não foi definida! "
                         "Crie um arquivo .env baseado em .env.example.")
    
    app = Application(api_key=api_key)
    app.menu()