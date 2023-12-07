from scraper import get_news


def display_news(news_list):
    """Exibe as notícias obtidas no console."""
    if news_list:
        print("\nÚltimas Notícias do G1:\n")
        for idx, article in enumerate(news_list, start=1):
            print(f"Notícia {idx}:")
            print(f"Título: {article['title']}")
            print(f"Descrição: {article['description']}")
            print(f"Link: {article['link']}")
            print(f"Imagem: {article['image']}")
            print(f"Autor: {article['autor']}")
            print(f"Texto Completo: {article['full_text']}")
            print("=" * 50)
    else:
        print("Nenhuma notícia encontrada.")


def main():
    limit = 5  # Defina o número de notícias que deseja obter
    news = get_news(limit)

    display_news(news)


if __name__ == "__main__":
    main()
