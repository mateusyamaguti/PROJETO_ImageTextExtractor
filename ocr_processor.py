"""
Módulo responsável pelo processamento OCR das imagens.
Utiliza Tesseract para extrair texto de imagens.
"""

import pytesseract
from PIL import Image
import cv2
import numpy as np
import os
from typing import Optional, List, Dict

class OCRProcessor:
    """Classe para processamento de OCR em imagens."""
    
    def __init__(self, tesseract_path: Optional[str] = None):
        """
        Inicializa o processador OCR.
        
        Args:
            tesseract_path: Caminho para o executável do Tesseract (Windows)
        """
        self._setup_tesseract_path(tesseract_path)
    
    def _setup_tesseract_path(self, custom_path: Optional[str] = None) -> None:
        """
        Configura o caminho do executável do Tesseract.
        
        Args:
            custom_path: Caminho personalizado para o Tesseract
        """
        # Lista de caminhos comuns do Tesseract no Windows
        common_paths = [
            r"C:\Program Files\Tesseract-OCR\tesseract.exe",
            r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
            r"C:\Users\%s\AppData\Local\Tesseract-OCR\tesseract.exe" % os.getenv('USERNAME', ''),
            r"C:\tesseract\tesseract.exe"
        ]
        
        # Se um caminho personalizado foi fornecido, testa primeiro
        if custom_path:
            common_paths.insert(0, custom_path)
        
        # Tenta encontrar o Tesseract
        tesseract_found = False
        
        for path in common_paths:
            if os.path.exists(path):
                pytesseract.pytesseract.tesseract_cmd = path
                tesseract_found = True
                print(f"✅ Tesseract encontrado em: {path}")
                break
        
        if not tesseract_found:
            print("⚠️  Tesseract não encontrado automaticamente.")
    
    def preprocess_image(self, image_path: str) -> np.ndarray:
        """
        Pré-processa a imagem para melhorar a qualidade do OCR.
        
        Args:
            image_path: Caminho para a imagem
            
        Returns:
            Imagem pré-processada
        """
        # Carrega a imagem
        image = cv2.imread(image_path)
        
        # Converte para escala de cinza
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Aplica desfoque gaussiano para reduzir ruído
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Aplica threshold para binarização
        _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        return thresh
    
    def extract_text(self, image_path: str, lang: str = 'por+eng') -> str:
        """
        Extrai texto da imagem usando OCR.
        
        Args:
            image_path: Caminho para a imagem
            lang: Idiomas para reconhecimento (português + inglês)
            
        Returns:
            Texto extraído da imagem
        """
        try:
            # Pré-processa a imagem
            processed_image = self.preprocess_image(image_path)
            
            # Configura o Tesseract
            config = '--psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789áàâãéèêíìîóòôõúùûçÁÀÂÃÉÈÊÍÌÎÓÒÔÕÚÙÛÇ.,;:!?()[]{}+-*/%=@#$&|_~^\\n '
            
            # Extrai o texto
            text = pytesseract.image_to_string(processed_image, lang=lang, config=config)
            
            return text.strip()
            
        except Exception as e:
            raise Exception(f"Erro ao processar a imagem: {str(e)}")
    
    def extract_data_structured(self, image_path: str, lang: str = 'por+eng') -> List[Dict[str, str]]:
        """
        Extrai dados estruturados da imagem (tabelas, listas, etc.).
        
        Args:
            image_path: Caminho para a imagem
            lang: Idiomas para reconhecimento
            
        Returns:
            Lista de dicionários com os dados estruturados
        """
        try:
            # Extrai o texto
            text = self.extract_text(image_path, lang)
            
            # Processa o texto em linhas
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            
            # Estrutura os dados
            structured_data = []
            for i, line in enumerate(lines):
                structured_data.append({
                    'linha': i + 1,
                    'conteudo': line,
                    'palavras': len(line.split()),
                    'caracteres': len(line)
                })
            
            return structured_data
            
        except Exception as e:
            raise Exception(f"Erro ao extrair dados estruturados: {str(e)}")