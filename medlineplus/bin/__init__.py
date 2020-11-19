import click

from medlineplus import version_info
from ._gene import gene_cli
from ._condition import condition_cli


epilog = '''
contact: {author} <{author_email}>
'''.format(**version_info)


@click.group(help='Genetics Home Reference(GHR) from MedlinePlus', epilog=epilog)
@click.version_option(version=version_info['version'], prog_name=version_info['prog'])
def cli(**kwargs):
    pass


def main():
    cli.add_command(gene_cli)
    cli.add_command(condition_cli)
    cli()


if __name__ == '__main__':
    main()
