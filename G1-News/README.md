# Web Scraping de Notícias do G1

Este código Python coleta as últimas notícias do site G1 (globo.com), utilizando as bibliotecas `requests` e `BeautifulSoup` para extrair informações das páginas web.

## Função `get_news(limit=5)`

A função `get_news()` realiza o scraping das notícias:

### Configuração Inicial:

-   Importa as bibliotecas: `requests`, `BeautifulSoup` e `logging`.
-   Configura o logger para registrar informações e erros durante o scraping.

### Acesso à Página do G1:

-   Define a URL e cabeçalhos (headers) para simular um navegador.
-   Envia uma solicitação GET com `requests.get()` e verifica o código de status.

### Extração de Notícias:

-   Utiliza o `BeautifulSoup` para analisar o HTML e encontrar elementos das notícias.
-   Extrai título, descrição, link, imagem, autor e texto completo das notícias.

### Tratamento de Erros:

-   Utiliza blocos `try` e `except` para lidar com exceções.
-   Registra detalhes de erros no logger.

### Teste da Função:

-   Testa a função `get_news()` obtendo 5 notícias e exibindo os títulos.

Este código é um exemplo simples de web scraping para coletar notícias do G1. Verifique os termos de serviço do site antes de realizar scraping.
