"""HTML fixtures para os testes de scraping."""

HTML_2_ARTICLES = """
<html><body>
  <div class="bastian-feed-item">
    <a class="feed-post-link" href="https://g1.globo.com/noticia-1">Título Um</a>
    <div class="feed-post-body-resumo">Descrição da notícia um.</div>
    <img class="bstn-fd-picture-image" src="https://img.g1.com/img1.jpg"/>
  </div>
  <div class="bastian-feed-item">
    <a class="feed-post-link" href="https://g1.globo.com/noticia-2">Título Dois</a>
    <div class="feed-post-body-resumo">Descrição da notícia dois.</div>
    <img class="bstn-fd-picture-image" src="https://img.g1.com/img2.jpg"/>
  </div>
</body></html>
"""

HTML_NO_OPTIONAL_FIELDS = """
<html><body>
  <div class="bastian-feed-item">
    <a class="feed-post-link" href="https://g1.globo.com/sem-desc">Sem Descrição</a>
  </div>
</body></html>
"""

HTML_EMPTY_PAGE = """<html><body></body></html>"""

HTML_PAGE_1_WITH_LOAD_MORE = """
<html><body>
  <div class="bastian-feed-item">
    <a class="feed-post-link" href="https://g1.globo.com/p1">Notícia Página 1</a>
    <div class="feed-post-body-resumo">Resumo página 1.</div>
  </div>
  <div class="load-more gui-color-primary-bg">
    <a href="https://g1.globo.com/ultimas-noticias/?page=2">Mais notícias</a>
  </div>
</body></html>
"""

HTML_PAGE_2 = """
<html><body>
  <div class="bastian-feed-item">
    <a class="feed-post-link" href="https://g1.globo.com/p2">Notícia Página 2</a>
    <div class="feed-post-body-resumo">Resumo página 2.</div>
  </div>
</body></html>
"""

HTML_UNICODE = """
<html><body>
  <div class="bastian-feed-item">
    <a class="feed-post-link" href="https://g1.globo.com/unicode">
      Notícia com acentuação: ção, ã, é, ô
    </a>
    <div class="feed-post-body-resumo">Resumo: ção ã é ô ü</div>
  </div>
</body></html>
"""

HTML_MISSING_HREF = """
<html><body>
  <div class="bastian-feed-item">
    <a class="feed-post-link">Título sem href</a>
    <div class="feed-post-body-resumo">Descrição.</div>
  </div>
</body></html>
"""


def make_response(html, status_code=200):
    from unittest.mock import MagicMock
    mock_resp = MagicMock()
    mock_resp.status_code = status_code
    mock_resp.content = html.encode('utf-8')
    return mock_resp
