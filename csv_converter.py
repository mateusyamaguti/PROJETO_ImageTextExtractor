"""
Módulo responsável pela conversão de dados extraídos para formato CSV.
"""

import pandas as pd
import os
from typing import List, Dict, Optional
from datetime import datetime

class CSVConverter:
    """Classe para conversão de dados para CSV."""
    
    def __init__(self, output_dir: str = "output"):
        """
        Inicializa o conversor CSV.
        
        Args:
            output_dir: Diretório de saída para os arquivos CSV
        """
        self.output_dir = output_dir
        self._ensure_output_dir()
    
    def _ensure_output_dir(self) -> None:
        """Garante que o diretório de saída existe."""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def convert_text_to_csv(self, text: str, filename: str, image_name: str) -> str:
        """
        Converte texto simples para CSV com metadados.
        
        Args:
            text: Texto extraído da imagem
            filename: Nome do arquivo CSV de saída
            image_name: Nome da imagem original
            
        Returns:
            Caminho completo do arquivo CSV gerado
        """
        # Processa o texto em linhas
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        # Cria DataFrame com os dados
        data = []
        for i, line in enumerate(lines, 1):
            data.append({
                'Linha': i,
                'Conteúdo': line,
                'Palavras': len(line.split()),
                'Caracteres': len(line),
                'Imagem_Origem': image_name,
                'Data_Extração': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
        
        df = pd.DataFrame(data)
        
        # Salva como CSV
        output_path = os.path.join(self.output_dir, filename)
        df.to_csv(output_path, index=False, encoding='utf-8-sig', sep=';')
        
        return output_path
    
    def convert_structured_data_to_csv(self, structured_data: List[Dict], filename: str, image_name: str) -> str:
        """
        Converte dados estruturados para CSV.
        
        Args:
            structured_data: Lista de dicionários com os dados
            filename: Nome do arquivo CSV de saída
            image_name: Nome da imagem original
            
        Returns:
            Caminho completo do arquivo CSV gerado
        """
        # Adiciona metadados
        for item in structured_data:
            item['imagem_origem'] = image_name
            item['data_extracao'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Cria DataFrame
        df = pd.DataFrame(structured_data)
        
        # Salva como CSV
        output_path = os.path.join(self.output_dir, filename)
        df.to_csv(output_path, index=False, encoding='utf-8-sig', sep=';')
        
        return output_path
    
    def create_summary_csv(self, image_name: str, text: str, output_file: str) -> str:
        """
        Cria um CSV resumo com estatísticas da extração.
        
        Args:
            image_name: Nome da imagem processada
            text: Texto extraído
            output_file: Arquivo CSV principal gerado
            
        Returns:
            Caminho do arquivo de resumo
        """
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        words = text.split()
        
        summary_data = {
            'Imagem': [image_name],
            'Total_Linhas': [len(lines)],
            'Total_Palavras': [len(words)],
            'Total_Caracteres': [len(text)],
            'Arquivo_CSV_Gerado': [os.path.basename(output_file)],
            'Data_Processamento': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
        }
        
        df_summary = pd.DataFrame(summary_data)
        summary_path = os.path.join(self.output_dir, f"resumo_{os.path.splitext(image_name)[0]}.csv")
        df_summary.to_csv(summary_path, index=False, encoding='utf-8-sig', sep=';')
        
        return summary_path