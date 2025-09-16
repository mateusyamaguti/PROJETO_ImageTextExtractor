#!/usr/bin/env python3
"""
ImageTextExtractor - Programa principal
Extrai texto de imagens usando OCR, converte para CSV e corrige com IA.

Autor: [Mateus Xavier Yamaguti]
Data: [16/09/2025]
Versão: 3.0
"""

import os
import sys
from typing import Optional
from dotenv import load_dotenv

# Importa os módulos personalizados
from ocr_processor import OCRProcessor
from csv_converter import CSVConverter
from ai_application import Application

class ImageTextExtractor:
    """Classe principal do sistema de extração de texto de imagens."""
    
    def __init__(self):
        """Inicializa o extrator de texto."""
        self.img_dir = "img"
        self.output_dir = "output"
        
        # Inicializa o processador OCR com o caminho do Tesseract
        tesseract_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        self.ocr_processor = OCRProcessor(tesseract_path)
        
        self.csv_converter = CSVConverter(self.output_dir)
        
        # Garante que os diretórios existem
        self._ensure_directories()
    
    def _ensure_directories(self) -> None:
        """Cria os diretórios necessários se não existirem."""
        for directory in [self.img_dir, self.output_dir]:
            if not os.path.exists(directory):
                os.makedirs(directory)
                print(f"📁 Diretório '{directory}' criado.")
    
    def _get_available_images(self) -> list:
        """
        Retorna lista de imagens disponíveis na pasta img/.
        
        Returns:
            Lista com nomes das imagens disponíveis
        """
        supported_formats = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif')
        images = []
        
        if not os.path.exists(self.img_dir):
            return images
        
        for file in os.listdir(self.img_dir):
            if file.lower().endswith(supported_formats):
                images.append(file)
        
        return sorted(images)
    
    def _display_available_images(self, images: list) -> None:
        """Exibe as imagens disponíveis para o usuário."""
        if not images:
            print("❌ Nenhuma imagem encontrada na pasta 'img/'")
            print("   Formatos suportados: JPG, JPEG, PNG, BMP, TIFF, GIF")
            return
        
        print("\n📸 Imagens disponíveis:")
        print("-" * 40)
        for i, image in enumerate(images, 1):
            file_size = self._get_file_size(os.path.join(self.img_dir, image))
            print(f"{i:2d}. {image} ({file_size})")
        print("-" * 40)
    
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
    
    def _get_user_choice(self, images: list) -> Optional[str]:
        """
        Solicita ao usuário a escolha da imagem.
        
        Args:
            images: Lista de imagens disponíveis
            
        Returns:
            Nome da imagem escolhida ou None se cancelar
        """
        while True:
            print(f"\n🔍 Digite o nome da imagem (ou 'voltar' para menu principal):")
            choice = input("➤ ").strip()
            
            if choice.lower() in ['voltar', 'back', 'menu']:
                return None
            
            # Verifica se a imagem existe
            if choice in images:
                return choice
            
            # Verifica se é um número válido
            try:
                index = int(choice) - 1
                if 0 <= index < len(images):
                    return images[index]
            except ValueError:
                pass
            
            print(f"❌ Imagem '{choice}' não encontrada. Tente novamente.")
    
    def process_image(self, image_name: str) -> bool:
        """
        Processa uma imagem específica.
        
        Args:
            image_name: Nome da imagem a ser processada
            
        Returns:
            True se processada com sucesso, False caso contrário
        """
        image_path = os.path.join(self.img_dir, image_name)
        
        try:
            print(f"\n🔄 Processando imagem: {image_name}")
            print("   Extraindo texto...")
            
            # Extrai o texto da imagem
            extracted_text = self.ocr_processor.extract_text(image_path)
            
            if not extracted_text.strip():
                print("⚠️  Nenhum texto foi encontrado na imagem.")
                return False
            
            # Exibe o texto extraído
            print("\n📝 Texto extraído:")
            print("=" * 60)
            print(extracted_text)
            print("=" * 60)
            
            # Converte para CSV
            csv_filename = f"texto_{os.path.splitext(image_name)[0]}.csv"
            csv_path = self.csv_converter.convert_text_to_csv(
                extracted_text, 
                csv_filename, 
                image_name
            )
            
            # Cria arquivo de resumo
            summary_path = self.csv_converter.create_summary_csv(
                image_name, 
                extracted_text, 
                csv_path
            )
            
            print(f"\n✅ Processamento concluído!")
            print(f"📄 Arquivo CSV: {csv_path}")
            print(f"📊 Resumo: {summary_path}")
            
            return True
            
        except Exception as e:
            print(f"❌ Erro ao processar a imagem: {str(e)}")
            return False
    
    def display_banner(self) -> None:
        """Exibe o banner do programa."""
        banner = """
╔══════════════════════════════════════════════════════════╗
║              ImageTextExtractor v3.0                    ║
║         Extração de Texto + Correção por IA             ║
║              OCR → CSV → AI Correction                   ║
╚══════════════════════════════════════════════════════════╝
        """
        print(banner)
    
    def main_menu(self) -> None:
        """Exibe o menu principal do sistema."""
        while True:
            print("\n" + "="*50)
            print("📋 MENU PRINCIPAL")
            print("="*50)
            print("1 - 📸 Processar imagens (OCR → CSV)")
            print("2 - 🤖 Corrigir textos com IA")
            print("0 - 🚪 Sair")
            print("="*50)
            
            try:
                choice = int(input("➤ Escolha uma opção: "))
            except ValueError:
                print("❌ Entrada inválida! Digite apenas números.")
                continue
            
            if choice == 1:
                self.run_ocr_mode()
            elif choice == 2:
                self.run_ai_correction()
            elif choice == 0:
                print("\n👋 Encerrando o programa. Até logo!")
                break
            else:
                print("❌ Opção inválida! Escolha 1, 2 ou 0.")
    
    def run_ocr_mode(self) -> None:
        """Executa o modo de processamento de imagens OCR."""
        print("\n🔍 Modo: Processamento de Imagens")
        
        while True:
            # Lista as imagens disponíveis
            available_images = self._get_available_images()
            self._display_available_images(available_images)
            
            if not available_images:
                print(f"\n💡 Adicione imagens na pasta '{self.img_dir}' e tente novamente.")
                input("Pressione Enter para voltar ao menu principal...")
                break
            
            # Solicita escolha do usuário
            chosen_image = self._get_user_choice(available_images)
            
            if chosen_image is None:
                break
            
            # Processa a imagem escolhida
            success = self.process_image(chosen_image)
            
            if success:
                # Pergunta se deseja processar outra imagem
                print(f"\n❓ Deseja processar outra imagem? (s/n)")
                continue_choice = input("➤ ").strip().lower()
                
                if continue_choice not in ['s', 'sim', 'y', 'yes']:
                    break
            else:
                print(f"\n🔄 Voltando à lista de imagens...")
    
    def run_ai_correction(self) -> None:
        """Executa o modo de correção por IA."""
        load_dotenv()
        
        api_key = os.getenv("API_KEY")
        
        if not api_key:
            print("\n❌ Erro: Chave da API do Google não encontrada!")
            print("💡 Passos para configurar:")
            print("   1. Crie um arquivo .env na pasta do projeto")
            print("   2. Adicione: API_KEY=sua_chave_aqui")
            print("   3. Obtenha sua chave em: https://aistudio.google.com/app/apikey")
            input("\nPressione Enter para voltar ao menu principal...")
            return
        
        try:
            app = Application(api_key=api_key)
            app.menu()
        except Exception as e:
            print(f"❌ Erro na aplicação de IA: {str(e)}")
            input("Pressione Enter para voltar ao menu principal...")


def main():
    """Função principal do programa."""
    try:
        extractor = ImageTextExtractor()
        extractor.display_banner()
        extractor.main_menu()
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Programa interrompido pelo usuário.")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {str(e)}")
    finally:
        print("\n🏁 Obrigado por usar o ImageTextExtractor!")


if __name__ == "__main__":
    main()