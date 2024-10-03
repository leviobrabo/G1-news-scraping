import requests
from bs4 import BeautifulSoup
import logging
import time
from rich.console import Console
from rich.live import Live
from rich.table import Table

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def get_news(limit=5):
    logger.info('Obtendo notícias...')
    url = 'https://g1.globo.com/ultimas-noticias/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    news_list = []

    try:
        while len(news_list) < limit:
            response = requests.get(url, timeout=10, headers=headers)
            if response.status_code != 200:
                logger.error(f'Erro ao obter notícias. Status Code: {response.status_code}')
                return news_list

            soup = BeautifulSoup(response.content, 'html.parser')
            post_sections = soup.find_all('div', {'class': 'bastian-feed-item'})

            for section in post_sections:
                logger.info('Notícia recebida')

                title_element = section.find('a', {'class': 'feed-post-link'})
                description_element = section.find('div', {'class': 'feed-post-body-resumo'})
                link_element = section.find('a', {'class': 'feed-post-link'})
                image_element = section.find('img', {'class': 'bstn-fd-picture-image'})

                if title_element and link_element and description_element and image_element:
                    title = title_element.text.strip()
                    link = link_element['href']
                    description = description_element.text.strip()
                    image_url = image_element['src']

                    news_list.append({
                        'title': title,
                        'description': description,
                        'link': link,
                        'image': image_url,
                    })

                    if len(news_list) >= limit:
                        break

            logger.info(f'{len(news_list)} notícias obtidas.')

            load_more_button = soup.find('div', {'class': 'load-more gui-color-primary-bg'})
            if load_more_button and load_more_button.find('a'):
                url = load_more_button.find('a')['href']
            else:
                break

        return news_list

    except Exception as e:
        logger.exception(f'Erro ao obter notícias: {str(e)}')
        return news_list

def display_news(news):
    table = Table(title="Notícias")

    table.add_column("Título", style="bold", width=50)
    table.add_column("Descrição", width=100)

    for article in news:
        table.add_row(article['title'], article['description'] + '\n')
        table.add_row('-----------------------')

    return table

if __name__ == "__main__":
    while True:
        console = Console()
        news = get_news(limit=50)
        news_to_display = []

        with Live(display_news(news_to_display), console=console, refresh_per_second=1) as live:
            for idx, article in enumerate(news, start=1):
                news_to_display.append(article)
                live.update(display_news(news_to_display))  # Atualiza a tabela com nova notícia
                time.sleep(10)  # Espera 10 segundos antes de adicionar outra notícia
                # LIMPA EM MULTIPLOS DE 5
                if len(news_to_display) % 5 == 0:
                    console.clear()
        # 10 Minutos
        time.sleep(600)