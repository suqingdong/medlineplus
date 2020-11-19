# -*- coding=utf-8 -*-
import click

from medlineplus.core.genetics.gene import Gene
from medlineplus.utils import safe_open, data2table, save_data


@click.command(name='gene', help='search genetics genes')
@click.option('-l', '--list', help='list only', is_flag=True)
@click.option('-s', '--suffix', help='the suffix of gene, eg. a-z')
@click.option('-o', '--out', help='the prefix of output file [stdout]')
@click.option('-O', '--outtype', help='the type of output file', default='jl', type=click.Choice(['jl', 'xml']))
def gene_cli(**kwargs):
    g = Gene()
    g.logger.debug('input arguments: {}'.format(kwargs))

    gene_list = g.list(kwargs['suffix'])

    if kwargs['list']:
        table = data2table(gene_list)
        print(table)
    else:
        outfile = '{out}.{outtype}'.format(**kwargs) if kwargs['out'] else None
        save_data(gene_list, g, outfile=outfile, outtype=kwargs['outtype'], wrapper='MedlinePlusGenes')


if __name__ == '__main__':
    gene_cli()
