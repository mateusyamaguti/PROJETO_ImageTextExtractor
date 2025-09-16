from google import genai

class PythonAI:
    
    def __init__(self, api_key, model="gemini-2.5-flash"):
        self.client = genai.Client(api_key=api_key)
        self.model = model


    def ask(self, prompt):
        prompt += " Por favor, formate e corrija o texto a seguir. "
        "Muitas palavras estão juntas, então preciso que você as separe, "
        "ajuste a pontuação, corrija a ortografia e a gramática para que fique legível. O texto é este:"
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )

        return response.text