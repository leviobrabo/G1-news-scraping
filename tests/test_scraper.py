import json
import os
import unittest
from unittest.mock import MagicMock, patch

import requests as req
from rich.table import Table

from scraper import build_table, export_csv, export_json, get_news
from fixtures import (
    HTML_2_ARTICLES,
    HTML_EMPTY_PAGE,
    HTML_MISSING_HREF,
    HTML_NO_OPTIONAL_FIELDS,
    HTML_PAGE_1_WITH_LOAD_MORE,
    HTML_PAGE_2,
    HTML_UNICODE,
    make_response,
)


class TestGetNewsSuccessPath(unittest.TestCase):

    @patch('scraper.requests.get')
    def test_returns_list(self, mock_get):
        mock_get.return_value = make_response(HTML_2_ARTICLES)
        result = get_news(limit=2)
        self.assertIsInstance(result, list)

    @patch('scraper.requests.get')
    def test_correct_count_when_limit_equals_available(self, mock_get):
        mock_get.return_value = make_response(HTML_2_ARTICLES)
        result = get_news(limit=2)
        self.assertEqual(len(result), 2)

    @patch('scraper.requests.get')
    def test_limit_cuts_below_available(self, mock_get):
        mock_get.return_value = make_response(HTML_2_ARTICLES)
        result = get_news(limit=1)
        self.assertEqual(len(result), 1)

    @patch('scraper.requests.get')
    def test_limit_larger_than_available_returns_all(self, mock_get):
        mock_get.return_value = make_response(HTML_2_ARTICLES)
        result = get_news(limit=100)
        self.assertEqual(len(result), 2)

    @patch('scraper.requests.get')
    def test_article_has_required_keys(self, mock_get):
        mock_get.return_value = make_response(HTML_2_ARTICLES)
        article = get_news(limit=1)[0]
        for key in ('title', 'description', 'link', 'image'):
            self.assertIn(key, article)

    @patch('scraper.requests.get')
    def test_article_title_extracted_correctly(self, mock_get):
        mock_get.return_value = make_response(HTML_2_ARTICLES)
        result = get_news(limit=1)
        self.assertEqual(result[0]['title'], 'Título Um')

    @patch('scraper.requests.get')
    def test_article_description_extracted_correctly(self, mock_get):
        mock_get.return_value = make_response(HTML_2_ARTICLES)
        result = get_news(limit=1)
        self.assertEqual(result[0]['description'], 'Descrição da notícia um.')

    @patch('scraper.requests.get')
    def test_article_link_extracted_correctly(self, mock_get):
        mock_get.return_value = make_response(HTML_2_ARTICLES)
        result = get_news(limit=1)
        self.assertEqual(result[0]['link'], 'https://g1.globo.com/noticia-1')

    @patch('scraper.requests.get')
    def test_article_image_extracted_correctly(self, mock_get):
        mock_get.return_value = make_response(HTML_2_ARTICLES)
        result = get_news(limit=1)
        self.assertEqual(result[0]['image'], 'https://img.g1.com/img1.jpg')

    @patch('scraper.requests.get')
    def test_unicode_titles_preserved(self, mock_get):
        mock_get.return_value = make_response(HTML_UNICODE)
        result = get_news(limit=1)
        self.assertIn('ção', result[0]['title'])
        self.assertIn('ção', result[0]['description'])

    @patch('scraper.requests.get')
    def test_missing_href_yields_empty_string(self, mock_get):
        mock_get.return_value = make_response(HTML_MISSING_HREF)
        result = get_news(limit=1)
        self.assertEqual(result[0]['link'], '')


class TestGetNewsOptionalFields(unittest.TestCase):

    @patch('scraper.requests.get')
    def test_missing_description_defaults_to_empty_string(self, mock_get):
        mock_get.return_value = make_response(HTML_NO_OPTIONAL_FIELDS)
        result = get_news(limit=1)
        self.assertEqual(result[0]['description'], '')

    @patch('scraper.requests.get')
    def test_missing_image_defaults_to_empty_string(self, mock_get):
        mock_get.return_value = make_response(HTML_NO_OPTIONAL_FIELDS)
        result = get_news(limit=1)
        self.assertEqual(result[0]['image'], '')


class TestGetNewsErrorHandling(unittest.TestCase):

    @patch('scraper.requests.get')
    def test_http_error_returns_empty_list(self, mock_get):
        mock_get.return_value = make_response('', status_code=403)
        result = get_news(limit=5)
        self.assertEqual(result, [])

    @patch('scraper.requests.get')
    def test_http_500_returns_empty_list(self, mock_get):
        mock_get.return_value = make_response('', status_code=500)
        result = get_news(limit=5)
        self.assertEqual(result, [])

    @patch('scraper.requests.get')
    def test_empty_page_returns_empty_list(self, mock_get):
        mock_get.return_value = make_response(HTML_EMPTY_PAGE)
        result = get_news(limit=5)
        self.assertEqual(result, [])

    @patch('scraper.requests.get')
    def test_connection_error_returns_empty_list(self, mock_get):
        mock_get.side_effect = req.ConnectionError('connection refused')
        result = get_news(limit=5)
        self.assertEqual(result, [])

    @patch('scraper.requests.get')
    def test_timeout_returns_empty_list(self, mock_get):
        mock_get.side_effect = req.Timeout('timed out')
        result = get_news(limit=5)
        self.assertEqual(result, [])

    @patch('scraper.requests.get')
    def test_unexpected_exception_returns_partial_results(self, mock_get):
        mock_get.side_effect = RuntimeError('unexpected')
        result = get_news(limit=5)
        self.assertIsInstance(result, list)


class TestGetNewsPagination(unittest.TestCase):

    @patch('scraper.requests.get')
    def test_follows_load_more_link(self, mock_get):
        mock_get.side_effect = [
            make_response(HTML_PAGE_1_WITH_LOAD_MORE),
            make_response(HTML_PAGE_2),
        ]
        result = get_news(limit=2)
        self.assertEqual(len(result), 2)

    @patch('scraper.requests.get')
    def test_pagination_preserves_article_order(self, mock_get):
        mock_get.side_effect = [
            make_response(HTML_PAGE_1_WITH_LOAD_MORE),
            make_response(HTML_PAGE_2),
        ]
        result = get_news(limit=2)
        self.assertEqual(result[0]['title'], 'Notícia Página 1')
        self.assertEqual(result[1]['title'], 'Notícia Página 2')

    @patch('scraper.requests.get')
    def test_stops_when_no_load_more(self, mock_get):
        mock_get.return_value = make_response(HTML_2_ARTICLES)
        result = get_news(limit=50)
        self.assertEqual(len(result), 2)
        self.assertEqual(mock_get.call_count, 1)

    @patch('scraper.requests.get')
    def test_does_not_fetch_next_page_when_limit_reached(self, mock_get):
        mock_get.side_effect = [
            make_response(HTML_PAGE_1_WITH_LOAD_MORE),
            make_response(HTML_PAGE_2),
        ]
        result = get_news(limit=1)
        self.assertEqual(len(result), 1)
        self.assertEqual(mock_get.call_count, 1)


class TestExportJson(unittest.TestCase):

    _PATH = '_test_export.json'

    def tearDown(self):
        if os.path.exists(self._PATH):
            os.remove(self._PATH)

    def _sample(self):
        return [{'title': 'A', 'description': 'B', 'link': 'C', 'image': 'D'}]

    def test_file_is_created(self):
        export_json(self._sample(), self._PATH)
        self.assertTrue(os.path.exists(self._PATH))

    def test_content_is_valid_json(self):
        export_json(self._sample(), self._PATH)
        with open(self._PATH, encoding='utf-8') as f:
            loaded = json.load(f)
        self.assertEqual(loaded, self._sample())

    def test_unicode_characters_preserved(self):
        data = [{'title': 'Notícia çom ação', 'description': '', 'link': '', 'image': ''}]
        export_json(data, self._PATH)
        with open(self._PATH, encoding='utf-8') as f:
            content = f.read()
        self.assertIn('Notícia çom ação', content)

    def test_multiple_articles_exported(self):
        data = [
            {'title': f'T{i}', 'description': '', 'link': '', 'image': ''}
            for i in range(5)
        ]
        export_json(data, self._PATH)
        with open(self._PATH, encoding='utf-8') as f:
            loaded = json.load(f)
        self.assertEqual(len(loaded), 5)


class TestExportCsv(unittest.TestCase):

    _PATH = '_test_export.csv'

    def tearDown(self):
        if os.path.exists(self._PATH):
            os.remove(self._PATH)

    def _sample(self):
        return [
            {'title': 'T1', 'description': 'D1', 'link': 'L1', 'image': 'I1'},
            {'title': 'T2', 'description': 'D2', 'link': 'L2', 'image': 'I2'},
        ]

    def test_file_is_created(self):
        export_csv(self._sample(), self._PATH)
        self.assertTrue(os.path.exists(self._PATH))

    def test_header_row_matches_keys(self):
        export_csv(self._sample(), self._PATH)
        with open(self._PATH, encoding='utf-8') as f:
            header = f.readline().strip()
        self.assertEqual(header, 'title,description,link,image')

    def test_data_rows_present(self):
        export_csv(self._sample(), self._PATH)
        with open(self._PATH, encoding='utf-8') as f:
            lines = f.read().splitlines()
        self.assertEqual(len(lines), 3)  # header + 2 rows

    def test_values_in_csv(self):
        export_csv(self._sample(), self._PATH)
        with open(self._PATH, encoding='utf-8') as f:
            content = f.read()
        self.assertIn('T1', content)
        self.assertIn('T2', content)

    def test_empty_list_does_not_create_file(self):
        export_csv([], self._PATH)
        self.assertFalse(os.path.exists(self._PATH))

    def test_unicode_preserved(self):
        data = [{'title': 'Notícia ação', 'description': '', 'link': '', 'image': ''}]
        export_csv(data, self._PATH)
        with open(self._PATH, encoding='utf-8') as f:
            content = f.read()
        self.assertIn('Notícia ação', content)


class TestBuildTable(unittest.TestCase):

    def test_returns_rich_table(self):
        self.assertIsInstance(build_table([]), Table)

    def test_empty_list_produces_zero_rows(self):
        table = build_table([])
        self.assertEqual(table.row_count, 0)

    def test_row_count_matches_input_length(self):
        data = [{'title': f'T{i}', 'description': ''} for i in range(4)]
        table = build_table(data)
        self.assertEqual(table.row_count, 4)

    def test_table_has_three_columns(self):
        table = build_table([])
        self.assertEqual(len(table.columns), 3)

    def test_missing_keys_do_not_raise(self):
        try:
            build_table([{}])
        except KeyError:
            self.fail('build_table() raised KeyError on missing keys')

    def test_single_article_renders(self):
        data = [{'title': 'Notícia X', 'description': 'Desc X'}]
        table = build_table(data)
        self.assertEqual(table.row_count, 1)


if __name__ == '__main__':
    unittest.main(verbosity=2)
