"""
Cliente para integração com a API do Google Gemini para correção de texto.
"""

from google import genai

class PythonAI:
    """Cliente da IA do Google para correção de texto."""
    
    def __init__(self, api_key: str, model: str = "gemini-2.0-flash-exp"):
        """
        Inicializa o cliente da IA.
        
        Args:
            api_key: Chave da API do Google
            model: Modelo do Gemini a ser usado
        """
        self.client = genai.Client(api_key=api_key)
        self.model = model
    
    def correct_text(self, text: str) -> str:
        """
        Corrige um texto usando IA.
        
        Args:
            text: Texto a ser corrigido
            
        Returns:
            Texto corrigido pela IA
        """
        prompt = self._build_correction_prompt(text)
        
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            return response.text
            
        except Exception as e:
            raise Exception(f"Erro na correção por IA: {str(e)}")
    
    def _build_correction_prompt(self, text: str) -> str:
        """
        Constrói o prompt para correção de texto.
        
        Args:
            text: Texto a ser corrigido
            
        Returns:
            Prompt formatado
        """
        prompt = f"""
Por favor, corrija e formate o texto a seguir que foi extraído por OCR de uma imagem.

Problemas comuns a corrigir:
- Palavras grudadas (ex: "palavraoutra" → "palavra outra")
- Caracteres mal reconhecidos
- Falta de espaçamento adequado
- Pontuação incorreta
- Erros ortográficos e gramaticais

Mantenha o sentido original do texto, mas torne-o legível e bem formatado.

TEXTO A CORRIGIR:
{text}

TEXTO CORRIGIDO:
"""
        return prompt
    
    def ask(self, prompt: str) -> str:
        """
        Método compatível com a versão anterior.
        
        Args:
            prompt: Pergunta ou texto
            
        Returns:
            Resposta da IA
        """
        correction_prompt = prompt + """ Por favor, formate e corrija o texto a seguir. 
Muitas palavras estão juntas, então preciso que você as separe, 
ajuste a pontuação, corrija a ortografia e a gramática para que fique legível. O texto é este:"""
        
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=correction_prompt
            )
            return response.text
            
        except Exception as e:
            raise Exception(f"Erro na consulta à IA: {str(e)}")