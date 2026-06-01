# G1 News Scraping

Ferramenta de web scraping em Python para coletar as últimas notícias do portal G1 (globo.com). Exibe os resultados no terminal com formatação rica e permite exportar para JSON ou CSV.

## Funcionalidades

- Coleta notícias da página de últimas notícias do G1
- Exibe tabela formatada no terminal via `rich`
- Exportação para **JSON** ou **CSV**
- Modo ao vivo (`--live`) com atualização automática a cada 10 minutos
- Controle do número de notícias via argumento `-n`

## Requisitos

- Python 3.8+
- Dependências listadas em `requirements.txt`

## Instalação

```bash
# Crie e ative um ambiente virtual
python -m venv .venv

# Linux / macOS
source .venv/bin/activate

# Windows
.venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt
```

## Uso

### Via `main.py` (entrada principal)

```bash
# 5 notícias (padrão)
python G1-News/main.py

# 20 notícias
python G1-News/main.py -n 20

# Exportar para JSON
python G1-News/main.py -n 10 --export json

# Exportar para CSV com caminho personalizado
python G1-News/main.py -n 15 --export csv --output saida/noticias.csv
```

### Via `scraper.py` (com modo ao vivo)

```bash
# Exibição única
python G1-News/scraper.py -n 10

# Modo ao vivo — atualiza a cada 10 minutos
python G1-News/scraper.py --live -n 20

# Exportar JSON
python G1-News/scraper.py -n 10 --export json --output noticias.json
```

### Argumentos disponíveis

| Argumento         | Padrão          | Descrição                                   |
|-------------------|-----------------|---------------------------------------------|
| `-n`, `--limit`   | `5` / `10`      | Quantidade de notícias a coletar            |
| `--export`        | —               | Formato de exportação: `json` ou `csv`      |
| `--output`        | `noticias.json` | Caminho do arquivo de saída                 |
| `--live`          | —               | Modo ao vivo (somente `scraper.py`)         |

## Estrutura do Projeto

```
G1-news-scraping/
├── G1-News/
│   ├── main.py        # Entrada principal com CLI
│   └── scraper.py     # Lógica de scraping, exportação e modo ao vivo
├── requirements.txt   # Dependências do projeto
└── README.md          # Documentação
```

## Dados Coletados

Cada notícia retorna um dicionário com os seguintes campos:

| Campo         | Descrição                         |
|---------------|-----------------------------------|
| `title`       | Título da notícia                 |
| `description` | Resumo do conteúdo                |
| `link`        | URL completa para a notícia       |
| `image`       | URL da imagem de capa             |

## Avisos

- **Uso responsável:** projeto desenvolvido para fins educacionais. Respeite os termos de serviço do G1.
- **Dependência de estrutura HTML:** scrapers são sensíveis a mudanças no layout do site. Se parar de funcionar, a estrutura HTML do G1 pode ter sido alterada.
- **Rate limiting:** o modo ao vivo aguarda 10 minutos entre cada ciclo para não sobrecarregar o servidor.
