import logging

import click

from .parser import parse


@click.command()
@click.option('-c', '--char', is_flag=True)
@click.option('-s', '--seed')
@click.option('-v', '--verbose', count=True)
@click.argument('formula', required=False, nargs=-1)
def roll(char, seed, verbose, formula):
    if char and not formula:
        formula = '6x3d6'
    elif not formula:
        formula = "4d6M3"
    if verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    formula = ''.join(formula)
    summation = 0
    linebreak = '-' * 50
    print(f'{linebreak}')
    print(f' Formula: {formula}')
    print(f'{linebreak}')
    stats = ['str', 'dex', 'con', 'wis', 'int', 'cha']
    for count, value in enumerate(parse(formula, seed=seed)):
        summation += value
        if char:
            print(f' {stats[count]}: {value}')
        else:
            print(f' {value}')
    print(f'{linebreak}')
    print(' Sum:', summation)
    print(' Ave:', int(summation / (count + 1)))
    print(f'{linebreak}')
