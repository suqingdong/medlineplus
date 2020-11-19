#!/usr/bin/env python
# -*- coding=utf-8 -*-
import os
import sys
import json

import prettytable
from json2xml import json2xml


def safe_open(filename, mode='r'):
    
    if 'w' in mode:
        dirname = os.path.dirname(filename)
        if dirname and not os.path.exists(dirname):
            os.makedirs(dirname)

    if filename.endswith('.gz'):
        import gzip
        return gzip.open(filename, mode=mode)

    return open(filename, mode=mode)


def data2table(data, align='l'):
    table = prettytable.PrettyTable()

    for n, context in enumerate(data, 1):
        if n == 1:
            table.field_names = list(context.keys())
        table.add_row(list(context.values()))

    for field in table._field_names:
        table.align[field] = align
    
    return table


def save_data(item_list, obj, outfile=None, outtype='jl', wrapper='MedlinePlus'):
    out = safe_open(outfile, 'w') if outfile else sys.stdout
    with out:
        data = []
        for context in item_list:
            detail = obj.detail(context['url'])
            context.update(detail)
            if outtype == 'xml':
                data.append(context)
            else:
                out.write(json.dumps(context) + '\n')
        if data:
            xml = json2xml.Json2xml(data, wrapper=wrapper).to_xml()
            out.write(xml + '\n')

        if outfile:
            obj.logger.info('save file: {}'.format(outfile))
