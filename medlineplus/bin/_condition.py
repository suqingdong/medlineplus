#!/usr/bin/env python
# -*- coding=utf-8 -*-
import os
import sys
import json

import click
import prettytable

from medlineplus.core.genetics.condition import Condition
from medlineplus.utils import safe_open


@click.command(name='condition', help='search genetics conditions')
@click.option('-l', '--list', help='list only', is_flag=True)
@click.option('-s', '--suffix', help='the suffix of condition, eg. 0, a-z')
@click.option('-o', '--out', help='the prefix of output file [stdout]')
def condition_cli(**kwargs):
    cond = Condition()
    genelist = cond.list(kwargs['suffix'])
    if kwargs['list']:
        table = prettytable.PrettyTable(['Term', 'Abbr', 'Url'])
        for context in genelist:
            table.add_row(list(map(context.get, ['term', 'abbr', 'url'])))
        for field in table._field_names:
            table.align[field] = 'l'
        print(table)
    else:
        out = safe_open(kwargs['out'] + '.jl', 'w') if kwargs['out'] else sys.stdout
        with out:
            for context in genelist:
                detail = cond.detail(context['url'])
                context.update(detail)
                out.write(json.dumps(context) + '\n')
            if kwargs['out']:
                cond.logger.info('save file: {out}.jl'.format(**kwargs))
        

if __name__ == '__main__':
    condition_cli()
    

