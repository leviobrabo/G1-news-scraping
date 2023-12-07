import requests
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def get_news(limit=5):
    logger.info('Obtendo notícias...')
    url = 'https://g1.globo.com/ultimas-noticias/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
        '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    try:
        response = requests.get(url, timeout=10, headers=headers)
        if response.status_code != 200:
            logger.error(
                f'Erro ao obter notícias. Status Code: {response.status_code}'
            )
            return []

        soup = BeautifulSoup(response.content, 'html.parser')
        post_sections = soup.find_all('div', {'class': 'bastian-feed-item'})

        news_list = []
        for section in post_sections:
            logger.info('Notícia recebida')

            title_element = section.find('a', {'class': 'feed-post-link'})
            description_element = section.find(
                'div', {'class': 'feed-post-body-resumo'}
            )
            link_element = section.find('a', {'class': 'feed-post-link'})
            image_element = section.find(
                'img', {'class': 'bstn-fd-picture-image'}
            )

            if link_element:
                link_response = requests.get(
                    link_element['href'], timeout=10, headers=headers
                )
            else:
                logger.warning('Link não encontrado')
                continue

            link_content = BeautifulSoup(link_response.content, 'html.parser')

            full_text_content = link_content.find_all(
                'div', {'class': 'mc-column content-text active-extra-styles'}
            )
            media_content = link_content.find_all(
                'div', {'class': 'mc-column content-media__container'}
            )

            full_text = ''
            media_links = []
            for text_section in full_text_content:
                text = text_section.get_text(strip=True)
                if text:
                    full_text += text + '\n\n'

            for media_section in media_content:
                media_element = media_section.find('img')
                if media_element and 'src' in media_element.attrs:
                    media_links.append(media_element['src'])
                    full_text += f'<img src="{media_element["src"]}">\n\n''src'

            autor_element = link_content.find(
                'p', {'class': 'content-publication-data__from'}
            )

            if (
                title_element
                and link_element
                and description_element
                and image_element
            ):
                title = title_element.text.strip()
                link = link_element['href']
                description = description_element.text.strip()
                image_url = image_element['src']

                if autor_element:
                    autor = autor_element.text
                else:
                    autor = None

                news_list.append(
                    {
                        'title': title,
                        'description': description,
                        'link': link,
                        'image': image_url,
                        'autor': autor,
                        'full_text': full_text,
                    }
                )
                if len(news_list) >= limit:
                    break

        logger.info(f'{len(news_list)} notícias obtidas.')
        return news_list

    except Exception as e:
        logger.exception(f'Erro ao obter notícias: {str(e)}')
        return []


if __name__ == "__main__":
    news = get_news(limit=5)
    for idx, article in enumerate(news, start=1):
        print(f"Notícia {idx}: {article['title']}")
