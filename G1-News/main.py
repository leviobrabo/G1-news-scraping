import argparse

from rich.console import Console
from rich.table import Table

from scraper import export_csv, export_json, get_news


def build_table(news_list):
    table = Table(title='Últimas Notícias — G1', show_lines=True)
    table.add_column('#', style='bold cyan', width=4, justify='right')
    table.add_column('Título', style='bold white', width=50)
    table.add_column('Descrição', width=55)
    table.add_column('Link', style='dim blue', width=40)

    for idx, article in enumerate(news_list, start=1):
        table.add_row(
            str(idx),
            article.get('title', ''),
            article.get('description', ''),
            article.get('link', ''),
        )

    return table


def main():
    parser = argparse.ArgumentParser(
        description='G1 News Scraper — coleta notícias do G1 (globo.com)'
    )
    parser.add_argument(
        '-n', '--limit',
        type=int, default=5,
        help='Quantidade de notícias a coletar (padrão: 5)',
    )
    parser.add_argument(
        '--export',
        choices=['json', 'csv'],
        help='Exportar resultados para arquivo',
    )
    parser.add_argument(
        '--output',
        default=None,
        help='Caminho do arquivo de saída (padrão: noticias.json ou noticias.csv)',
    )
    args = parser.parse_args()

    console = Console()
    news = get_news(args.limit)

    if not news:
        console.print('[red]Nenhuma notícia encontrada.[/red]')
        return

    console.print(build_table(news))

    if args.export == 'json':
        path = args.output or 'noticias.json'
        export_json(news, path)
        console.print(f'[green]Exportado para {path}[/green]')
    elif args.export == 'csv':
        path = args.output or 'noticias.csv'
        export_csv(news, path)
        console.print(f'[green]Exportado para {path}[/green]')


if __name__ == '__main__':
    main()
