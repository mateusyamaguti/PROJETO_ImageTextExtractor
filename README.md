# ImageTextExtractor

## Descrição
Projeto Python para extração de texto de imagens usando OCR (Optical Character Recognition) 
e conversão dos dados extraídos para formato CSV.

## Requisitos do Sistema
- Python 3.8 ou superior
- Tesseract OCR instalado no sistema

### Instalação do Tesseract:
- **Windows**: Baixar de https://github.com/UB-Mannheim/tesseract/wiki
- **Linux**: `sudo apt install tesseract-ocr tesseract-ocr-por`
- **macOS**: `brew install tesseract`

## Instalação
1. Clone/baixe o projeto
2. Navegue até a pasta do projeto
3. Execute: `pip install -r requirements.txt`

## Como Usar
1. Coloque suas imagens na pasta `img/`
2. Execute: `python main.py`
3. Digite o nome da imagem quando solicitado
4. O texto extraído será exibido no terminal e salvo como CSV na pasta `output/`

## Formatos Suportados
- JPG, JPEG, PNG, BMP, TIFF

## Estrutura do Projeto
- `main.py`: Interface principal do usuário
- `ocr_processor.py`: Processamento de OCR
- `csv_converter.py`: Conversão para CSV
- `img/`: Pasta para imagens de entrada
- `output/`: Pasta para arquivos CSV gerados