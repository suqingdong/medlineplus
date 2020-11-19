# -*- coding=utf-8 -*-
import click

from medlineplus.core.genetics.condition import Condition
from medlineplus.utils import safe_open, data2table, save_data


@click.command(name='condition', help='search genetics conditions')
@click.option('-l', '--list', help='list only', is_flag=True)
@click.option('-s', '--suffix', help='the suffix of condition, eg. 0, a-z')
@click.option('-o', '--out', help='the prefix of output file [stdout]')
@click.option('-O', '--outtype', help='the type of output file', default='jl', type=click.Choice(['jl', 'xml']))
def condition_cli(**kwargs):
    cond = Condition()
    condition_list = cond.list(kwargs['suffix'])
    if kwargs['list']:
        table = data2table(condition_list)
        print(table)
    else:
        outfile = '{out}.{outtype}'.format(**kwargs) if kwargs['out'] else None
        save_data(condition_list, cond, outfile=outfile, outtype=kwargs['outtype'], wrapper='MedlinePlusConditions')


if __name__ == '__main__':
    condition_cli()
