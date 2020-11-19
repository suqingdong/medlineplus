import json
import string

try:
    from urllib.parse import unquote as url_unquote
except ImportError:
    from urllib import unquote as url_unquote

from webrequests import WebRequest as WR
from simple_loggers import SimpleLogger


class Genetics(object):
    base_url = 'https://medlineplus.gov/genetics/'

    def detail(self, url):
        """Get the details of given url
        """
        soup = WR.get_soup(url)
        detail = {}
        # for book in soup.select('div.mp-exp[data-bookmark]'):  # not work for python2
        for book in soup.select('div.mp-exp'):
            if 'data-bookmark' not in book.attrs:
                continue
            mark = book.attrs['data-bookmark']
            if mark == 'causes':
                detail[mark] = book.select_one('section .mp-content').text
                genes = [a.text for a in book.select('.related-genes ul li a')]
                detail['related_genes'] = genes
            elif mark == 'synonyms':
                synonyms = [li.text for li in book.select('section ul li')]
                detail['synonyms'] = synonyms
            elif mark == 'resources':
                detail['resources'] = {}
                for resource in book.select('.mp-content'):
                    database = resource.find('h2').text
                    data = [{'href': url_unquote(a.attrs['href']), 'term': a.text} for a in resource.select('ul li a')]
                    detail['resources'][database] = data
            elif mark == 'references':
                pmids = [a.attrs['href'].rsplit('/', 1)[-1] for a in book.select('ul li a') if 'pubmed' in a.attrs['href']]
                detail['references'] = pmids
            elif mark == 'conditions':
                conditions = {}
                for condition in book.select('.mp-content'):
                    term = condition.find('h3').text
                    text = condition.find('p').text
                    conditions[term] = text
                detail['conditions'] = conditions
            else:
                detail[mark] = book.select_one('section .mp-content').text
        return detail

    