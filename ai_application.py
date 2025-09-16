"""
Aplicação para correção de texto usando IA do Google.
Integrada com os arquivos CSV gerados pelo OCR.
"""

import os
from dotenv import load_dotenv
from ai_client import PythonAI
from csv_converter import CSVConverter

class Application:
    """Aplicação principal para correção de texto por IA."""
    
    def __init__(self, api_key: str):
        """
        Inicializa a aplicação.
        
        Args:
            api_key: Chave da API do Google
        """
        self.ai = PythonAI(api_key)
        self.csv_converter = CSVConverter()
    
    def get_csv_files(self) -> list:
        """
        Obtém lista de arquivos CSV disponíveis na pasta output.
        
        Returns:
            Lista de arquivos CSV
        """
        output_dir = "output"
        if not os.path.exists(output_dir):
            return []
        
        csv_files = []
        for file in os.listdir(output_dir):
            if file.lower().endswith('.csv') and not file.startswith('resumo_'):
                csv_files.append(file)
        
        return sorted(csv_files)
    
    def display_csv_files(self, csv_files: list) -> None:
        """
        Exibe os arquivos CSV disponíveis.
        
        Args:
            csv_files: Lista de arquivos CSV
        """
        if not csv_files:
            print("❌ Nenhum arquivo CSV encontrado na pasta 'output/'")
            print("   Execute primeiro a extração de texto das imagens.")
            return
        
        print("\n📄 Arquivos CSV disponíveis:")
        print("-" * 50)
        for i, file in enumerate(csv_files, 1):
            file_path = os.path.join("output", file)
            file_size = self._get_file_size(file_path)
            print(f"{i:2d}. {file} ({file_size})")
        print("-" * 50)
    
    def _get_file_size(self, file_path: str) -> str:
        """Retorna o tamanho do arquivo formatado."""
        try:
            size_bytes = os.path.getsize(file_path)
            if size_bytes < 1024:
                return f"{size_bytes} B"
            elif size_bytes < 1024 * 1024:
                return f"{size_bytes / 1024:.1f} KB"
            else:
                return f"{size_bytes / (1024 * 1024):.1f} MB"
        except:
            return "Tamanho desconhecido"
    
    def get_user_choice(self, csv_files: list) -> str:
        """
        Solicita ao usuário a escolha do arquivo CSV.
        
        Args:
            csv_files: Lista de arquivos CSV disponíveis
            
        Returns:
            Nome do arquivo escolhido ou None se cancelar
        """
        while True:
            print(f"\n🔍 Digite o nome do arquivo CSV ou número (1-{len(csv_files)}):")
            print("   Digite 'voltar' para retornar ao menu principal")
            choice = input("➤ ").strip()
            
            if choice.lower() in ['voltar', 'back', 'sair']:
                return None
            
            # Verifica se é um número válido
            try:
                index = int(choice) - 1
                if 0 <= index < len(csv_files):
                    return csv_files[index]
            except ValueError:
                pass
            
            # Verifica se é um nome de arquivo válido
            if choice in csv_files:
                return choice
            
            # Verifica se é um nome parcial
            matches = [f for f in csv_files if choice.lower() in f.lower()]
            if len(matches) == 1:
                return matches[0]
            elif len(matches) > 1:
                print(f"❌ Múltiplos arquivos encontrados: {', '.join(matches)}")
                print("   Seja mais específico.")
            else:
                print(f"❌ Arquivo '{choice}' não encontrado.")
    
    def correct_csv_text(self, csv_filename: str) -> bool:
        """
        Corrige o texto de um arquivo CSV usando IA.
        
        Args:
            csv_filename: Nome do arquivo CSV
            
        Returns:
            True se sucesso, False caso contrário
        """
        csv_path = os.path.join("output", csv_filename)
        
        try:
            print(f"\n📖 Lendo arquivo: {csv_filename}")
            
            # Lê o conteúdo do CSV
            text_content = self.csv_converter.read_csv_content(csv_path)
            
            if not text_content.strip():
                print("⚠️  O arquivo CSV está vazio ou não contém texto.")
                return False
            
            print("📝 Texto original:")
            print("=" * 60)
            print(text_content[:500] + ("..." if len(text_content) > 500 else ""))
            print("=" * 60)
            
            print("\n🤖 Enviando para correção por IA...")
            
            # Corrige o texto usando IA
            corrected_text = self.ai.correct_text(text_content)
            
            print("\n✨ Texto corrigido:")
            print("=" * 60)
            print(corrected_text)
            print("=" * 60)
            
            # Salva o texto corrigido
            corrected_filename = f"corrigido_{csv_filename}"
            corrected_path = os.path.join("output", corrected_filename)
            
            with open(corrected_path.replace('.csv', '.txt'), 'w', encoding='utf-8') as f:
                f.write(corrected_text)
            
            print(f"\n✅ Texto corrigido salvo em: {corrected_path.replace('.csv', '.txt')}")
            
            return True
            
        except Exception as e:
            print(f"❌ Erro ao corrigir o texto: {str(e)}")
            return False
    
    def menu(self):
        """Menu principal da aplicação."""
        print("\n" + "="*60)
        print("🤖 Corretor de Texto por IA - Google Gemini")
        print("="*60)
        
        while True:
            print("\nEscolha uma das opções:")
            print("1 - Corrigir texto de arquivo CSV")
            print("2 - Correção manual (digite o texto)")
            print("0 - Voltar ao menu principal")
            print("="*40)
            
            try:
                op = int(input("➤ Opção: "))
            except ValueError:
                print("❌ Entrada inválida! Digite apenas números.")
                continue
            
            if op == 1:
                # Correção de arquivo CSV
                csv_files = self.get_csv_files()
                self.display_csv_files(csv_files)
                
                if csv_files:
                    chosen_file = self.get_user_choice(csv_files)
                    if chosen_file:
                        self.correct_csv_text(chosen_file)
            
            elif op == 2:
                # Correção manual
                print("\n📝 Digite o texto a ser corrigido:")
                manual_text = input("➤ ")
                if manual_text.strip():
                    try:
                        corrected = self.ai.correct_text(manual_text)
                        print("\n✨ Texto corrigido:")
                        print("=" * 40)
                        print(corrected)
                        print("=" * 40)
                    except Exception as e:
                        print(f"❌ Erro na correção: {str(e)}")
                else:
                    print("⚠️  Nenhum texto foi inserido.")
            
            elif op == 0:
                print("🔙 Voltando ao menu principal...")
                break
            
            else:
                print("❌ Opção inválida!")
            
            print("="*40)


def main():
    """Função principal da aplicação de IA."""
    load_dotenv()
    
    api_key = os.getenv("API_KEY")
    
    if not api_key:
        print("❌ Erro: A variável de ambiente API_KEY não foi definida!")
        print("💡 Crie um arquivo .env baseado em .env.example")
        return
    
    try:
        app = Application(api_key=api_key)
        app.menu()
    except Exception as e:
        print(f"❌ Erro na aplicação: {str(e)}")


if __name__ == "__main__":
    main()