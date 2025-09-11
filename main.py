#!/usr/bin/env python3
"""
ImageTextExtractor - Programa principal
Extrai texto de imagens usando OCR e converte para CSV.

Autor: [Mateus Xavier Yamaguti]
Data: [09/09/2025]
Versão: 1.0
"""

import os
import sys
from typing import Optional

# Importa os módulos personalizados
from ocr_processor import OCRProcessor
from csv_converter import CSVConverter

class ImageTextExtractor:
    """Classe principal do sistema de extração de texto de imagens."""
    
    def __init__(self):
        """Inicializa o extrator de texto."""
        self.img_dir = "img"
        self.output_dir = "output"
        
        # Inicializa o processador OCR com o caminho do Tesseract
        # Se você instalou em um local diferente, altere aqui:
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
            print(f"\n🔍 Digite o nome da imagem (ou 'sair' para encerrar):")
            choice = input("➤ ").strip()
            
            if choice.lower() in ['sair', 'exit', 'quit']:
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
║                  ImageTextExtractor                      ║
║              Extração de Texto de Imagens               ║
║                     versão 1.0                          ║
╚══════════════════════════════════════════════════════════╝
        """
        print(banner)
    
    def run(self) -> None:
        """Executa o programa principal."""
        self.display_banner()
        
        while True:
            # Lista as imagens disponíveis
            available_images = self._get_available_images()
            self._display_available_images(available_images)
            
            if not available_images:
                print(f"\n💡 Adicione imagens na pasta '{self.img_dir}' e execute novamente.")
                break
            
            # Solicita escolha do usuário
            chosen_image = self._get_user_choice(available_images)
            
            if chosen_image is None:
                print("\n👋 Encerrando o programa. Até logo!")
                break
            
            # Processa a imagem escolhida
            success = self.process_image(chosen_image)
            
            if success:
                # Pergunta se deseja processar outra imagem
                print(f"\n❓ Deseja processar outra imagem? (s/n)")
                continue_choice = input("➤ ").strip().lower()
                
                if continue_choice not in ['s', 'sim', 'y', 'yes']:
                    print("\n👋 Programa encerrado. Obrigado!")
                    break
            else:
                print(f"\n🔄 Voltando ao menu principal...")

def main():
    """Função principal do programa."""
    try:
        extractor = ImageTextExtractor()
        extractor.run()
    except KeyboardInterrupt:
        print("\n\n⚠️  Programa interrompido pelo usuário.")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {str(e)}")
    finally:
        print("\n🏁 Fim da execução.")

if __name__ == "__main__":
    main()