#!/usr/bin/env python
# -*- coding=utf-8 -*-
import os
import sys
import json

import click
import prettytable

from medlineplus.core.genetics.gene import Gene
from medlineplus.utils import safe_open


@click.command(name='gene', help='search genetics genes')
@click.option('-l', '--list', help='list only', is_flag=True)
@click.option('-s', '--suffix', help='the suffix of gene, eg. a-z')
@click.option('-o', '--out', help='the prefix of output file [stdout]')
def gene_cli(**kwargs):
    g = Gene()
    genelist = g.list(kwargs['suffix'])
    if kwargs['list']:
        table = prettytable.PrettyTable(['Gene', 'Fullname', 'Url'])
        for context in genelist:
            table.add_row(list(map(context.get, ['gene', 'fullname', 'url'])))
        for field in table._field_names:
            table.align[field] = 'l'
        print(table)
    else:
        out = safe_open(kwargs['out'] + '.jl', 'w') if kwargs['out'] else sys.stdout
        with out:
            for context in genelist:
                detail = g.detail(context['url'])
                context.update(detail)
                out.write(json.dumps(context) + '\n')
            if kwargs['out']:
                g.logger.info('save file: {out}.jl'.format(**kwargs))
        

if __name__ == '__main__':
    gene_cli()
    

