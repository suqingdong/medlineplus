import json
import string

from webrequests import WebRequest as WR
from simple_loggers import SimpleLogger

from . import Genetics


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
    cond = Condition()
    for context in cond.list('b'):
        detail = cond.detail(context['url'])
        context.update(detail)
        print(json.dumps(context, indent=2))
        break

    