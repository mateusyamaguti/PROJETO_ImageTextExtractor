# ImageTextExtractor - Projeto de OCR com conversão para CSV e Correção por IA

## Estrutura de pastas:
```
ImageTextExtractor/
│
├── img/                    # Pasta para armazenar as imagens
│   ├── exemplo1.jpg
│   ├── exemplo2.png
│   └── ...
│
├── output/                 # Pasta para salvar os arquivos CSV gerados
│
├── main.py                 # Arquivo principal do programa
├── ocr_processor.py        # Módulo para processamento OCR
├── csv_converter.py        # Módulo para conversão em CSV
├── ai_application.py       # Aplicação de correção por IA
├── ai_client.py           # Cliente da IA do Google
├── requirements.txt        # Dependências do projeto
├── .env.example           # Exemplo de arquivo de ambiente
└── README.md              # Documentação do projeto
```

## 1. requirements.txt
```
pytesseract==0.3.10
Pillow==10.1.0
opencv-python==4.8.1.78
pandas==2.1.4
python-dotenv==1.0.0
google-genai==0.4.0
```

## 2. .env.example
```
# Copie este arquivo para .env e adicione sua chave da API do Google
API_KEY=sua_chave_api_aqui
```


# ImageTextExtractor com Correção por IA

## Descrição
Projeto Python para extração de texto de imagens usando OCR (Optical Character Recognition),
conversão para CSV e correção automática do texto usando IA do Google Gemini.

## Requisitos do Sistema
- Python 3.8 ou superior
- Tesseract OCR instalado no sistema
- Chave da API do Google Gemini

### Instalação do Tesseract:
- **Windows**: Baixar de https://github.com/UB-Mannheim/tesseract/wiki
- **Linux**: `sudo apt install tesseract-ocr tesseract-ocr-por`
- **macOS**: `brew install tesseract`

### Configuração da API do Google:
1. Acesse https://aistudio.google.com/app/apikey
2. Crie uma nova chave API
3. Copie o arquivo `.env.example` para `.env`
4. Adicione sua chave API no arquivo `.env`

## Instalação
1. Clone/baixe o projeto
2. Navegue até a pasta do projeto
3. Execute: `pip install -r requirements.txt`
4. Configure o arquivo `.env` com sua API key

## Como Usar
1. Coloque suas imagens na pasta `img/`
2. Execute: `python main.py`
3. Escolha entre:
   - Processar imagens (OCR → CSV)
   - Corrigir textos existentes usando IA
4. Para correção, selecione o arquivo CSV da pasta `output/`

## Funcionalidades
- ✅ OCR com múltiplos formatos de imagem
- ✅ Conversão automática para CSV
- ✅ Correção de texto por IA (Google Gemini)
- ✅ Separação automática de palavras grudadas
- ✅ Interface integrada e amigável
