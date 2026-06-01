import requests
from bs4 import BeautifulSoup
import logging
import time
import json
import csv
from rich.console import Console
from rich.live import Live
from rich.table import Table

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
)
logger = logging.getLogger(__name__)

_USER_AGENT = (
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
)
_BASE_URL = 'https://g1.globo.com/ultimas-noticias/'


def get_news(limit=5):
    logger.info('Buscando notícias...')
    headers = {'User-Agent': _USER_AGENT}
    url = _BASE_URL
    news_list = []

    try:
        while len(news_list) < limit:
            response = requests.get(url, timeout=10, headers=headers)
            if response.status_code != 200:
                logger.error('Erro HTTP %d ao buscar %s', response.status_code, url)
                break

            soup = BeautifulSoup(response.content, 'html.parser')
            sections = soup.find_all('div', {'class': 'bastian-feed-item'})

            if not sections:
                logger.warning('Nenhum item encontrado. A estrutura do site pode ter mudado.')
                break

            for section in sections:
                title_el = section.find('a', {'class': 'feed-post-link'})
                if not title_el:
                    continue

                desc_el = section.find('div', {'class': 'feed-post-body-resumo'})
                img_el = section.find('img', {'class': 'bstn-fd-picture-image'})

                news_list.append({
                    'title': title_el.text.strip(),
                    'description': desc_el.text.strip() if desc_el else '',
                    'link': title_el.get('href', ''),
                    'image': img_el.get('src', '') if img_el else '',
                })
                logger.debug('Notícia coletada: %s', news_list[-1]['title'])

                if len(news_list) >= limit:
                    break

            load_more = soup.find('div', {'class': 'load-more gui-color-primary-bg'})
            if load_more and load_more.find('a'):
                url = load_more.find('a')['href']
            else:
                break

        logger.info('%d notícia(s) coletada(s).', len(news_list))
        return news_list

    except requests.RequestException as e:
        logger.error('Erro de rede: %s', e)
        return news_list
    except Exception as e:
        logger.exception('Erro inesperado: %s', e)
        return news_list


def export_json(news_list, filepath='noticias.json'):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(news_list, f, ensure_ascii=False, indent=2)
    logger.info('Exportado para %s', filepath)


def export_csv(news_list, filepath='noticias.csv'):
    if not news_list:
        return
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=news_list[0].keys())
        writer.writeheader()
        writer.writerows(news_list)
    logger.info('Exportado para %s', filepath)


def build_table(news_list):
    table = Table(title='Últimas Notícias — G1', show_lines=True)
    table.add_column('#', style='bold cyan', width=4, justify='right')
    table.add_column('Título', style='bold white', width=50)
    table.add_column('Descrição', width=70)

    for idx, article in enumerate(news_list, start=1):
        table.add_row(
            str(idx),
            article.get('title', ''),
            article.get('description', ''),
        )

    return table


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Scraper de notícias do G1')
    parser.add_argument('-n', '--limit', type=int, default=10,
                        help='Quantidade de notícias (padrão: 10)')
    parser.add_argument('--export', choices=['json', 'csv'],
                        help='Exportar resultados para arquivo')
    parser.add_argument('--output', default=None,
                        help='Caminho do arquivo de saída')
    parser.add_argument('--live', action='store_true',
                        help='Modo ao vivo — atualização contínua a cada 10 min')
    args = parser.parse_args()

    console = Console()

    if args.live:
        while True:
            news = get_news(limit=args.limit)
            displayed = []
            with Live(build_table(displayed), console=console, refresh_per_second=1) as live:
                for article in news:
                    displayed.append(article)
                    live.update(build_table(displayed))
                    time.sleep(5)
            time.sleep(600)
    else:
        news = get_news(limit=args.limit)
        console.print(build_table(news))

        if args.export == 'json':
            path = args.output or 'noticias.json'
            export_json(news, path)
            console.print(f'[green]Salvo em {path}[/green]')
        elif args.export == 'csv':
            path = args.output or 'noticias.csv'
            export_csv(news, path)
            console.print(f'[green]Salvo em {path}[/green]')
