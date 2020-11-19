import json
import string

from webrequests import WebRequest as WR
from simple_loggers import SimpleLogger

from . import Genetics


class Gene(Genetics):
    def __init__(self):
        super(Gene, self).__init__()
        self.logger = SimpleLogger('Genetics-Gene')

    def list(self, suffix=None):
        """List the genes

        Params
            suffix: a-z, default is None for all genes

        Return
            an iterator of dict, like {'gene': gene, 'fullname': fullname, 'url': url}
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


if __name__ == '__main__':
    gene = Gene()
    for context in gene.list('b'):
        detail = gene.detail(context['url'])
        context.update(detail)
        print(json.dumps(context, indent=2))
        break

    