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
        for book in soup.select('div.mp-exp[data-bookmark]'):
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
                detail[mark] = book.select_one('section .mp-content').text0
        return detail


class Gene(Genetics):
    def __init__(self):
        super(Gene, self).__init__()
        self.logger = SimpleLogger('Genetics-Gene')

    def list(self, suffix=None):
        """List the genes

        Params
            suffix: a-z, default is None for all genes

        Return
            an iterator of dict, like {'term': term, 'abbr': abbr, 'url': url}
        """
        suffix_list = list(string.ascii_lowercase)
        if suffix and suffix not in suffix_list:
            self.logger.error('bad suffix: {}. choose from: {}'.format(suffix, suffix_list))
            exit(1)
        elif suffix:
            suffix_list = [suffix]
        
        for name in suffix_list:
            url = self.base_url + 'gene-{}/'.format(name).replace('-a', '')
            self.logger.debug('>>> {}: {}'.format(name, url))
            soup = WR.get_soup(url)
            for li in soup.select('.breaklist li'):
                if len(li.contents) != 2:
                    continue
                fullname = li.contents[-1].lstrip(': ')
                gene = li.find('a').text
                url = li.find('a').attrs['href']
                yield {'gene': gene, 'fullname': fullname, 'url': url}


class Condition(Genetics):
    def __init__(self):
        super(Condition, self).__init__()
        self.logger = SimpleLogger('Genetics-Condition')

    def list(self, suffix=None):
        """List the conditions

        Params
            suffix: 0, a-z, default is None for all conditions

        Return
            an iterator of dict, like {'term': term, 'abbr': abbr, 'url': url}
        """
        suffix_list = ['0'] + list(string.ascii_lowercase)
        if suffix and suffix not in suffix_list:
            self.logger.error('bad suffix: {}. choose from: {}'.format(suffix, suffix_list))
            exit(1)
        elif suffix:
            suffix_list = [suffix]
        
        for name in suffix_list:
            url = self.base_url + 'condition-{}/'.format(name).replace('-a', '')
            self.logger.debug('>>> {}: {}'.format(name, url))
            soup = WR.get_soup(url)
            for li in soup.select('.breaklist li'):
                if len(li.contents) != 4:
                    continue
                condition_abbr = li.contents[0].rstrip(', ')
                condition_full = li.find('a').text
                condition_url = li.find('a').attrs['href']
                yield {'term': condition_full, 'abbr': condition_abbr, 'url': condition_url}

if __name__ == '__main__':
    gene = Gene()
    for context in gene.list('b'):
        detail = gene.detail(context['url'])
        context.update(detail)
        print(json.dumps(context, indent=2))
        break

    cond = Condition()
    for context in cond.list('b'):
        detail = cond.detail(context['url'])
        context.update(detail)
        print(json.dumps(context, indent=2))
        break

    