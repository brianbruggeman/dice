import logging
import random
from functools import reduce
from operator import add, mul, sub, truediv as div
from pathlib import Path

import pandas as pd
import numpy as np
from lark import Lark
from lark.tree import Tree

__all__ = ('parse', )

logger = logging.getLogger(__name__)


class DiceError(Exception):
    pass


class ParseError(DiceError):
    pass


class Parser(object):

    def _reduce_tree(self, tree):
        for value in self._split_tree(tree=tree):
            if isinstance(value, int):
                count = value
            elif isinstance(value, Tree):
                sub_tree = value
        values = next(self.parse(tree=sub_tree))
        count = min(len(values), count)
        return count, values

    def _split_tree(self, tree):
        for child in tree.children:
            if child.data == 'number':
                # Reduce to a value
                yield next(self.parse(tree=child))
            else:
                yield child

    def __init__(self, grammer):
        self.grammer = grammer
        self.ebnf_tokenizer = Lark(grammer, start='expr', parser='lalr')


class DiceParser(Parser):

    def add(self, tree):
        yield from self._op(tree=tree)

    def dice(self, tree):
        data = {}
        keys = ['multiplier', 'die_value']
        for child, key in zip(tree.children, keys):
            data[key] = next(self.parse(tree=child))
        if 'die_value' not in data:
            data['die_value'] = data['multiplier']
            data['multiplier'] = 1
        multiplier = data['multiplier']
        die_value = data['die_value']
        if die_value == 1:
            die_value += 1
        values = pd.DataFrame(np.random.choice(range(1, die_value or 2), [multiplier or 1]), columns=['rolls'])
        values['index'] = values.index
        logger.debug(f'   {multiplier}d{die_value} =>  {values.rolls.values}')
        yield values

    def div(self, tree):
        yield from self._op(tree=tree)

    def eq(self, tree):
        value, data = self._reduce_tree(tree=tree)
        result = data[data.rolls == value]
        logger.debug(f'   eq({data.rolls.values}, {value}) => {result.rolls.values}')
        yield result

    def ge(self, tree):
        value, data = self._reduce_tree(tree=tree)
        result = data[data.rolls >= value]
        logger.debug(f'   ge({data.rolls.values}, {value}) => {result.rolls.values}')
        yield result

    def gt(self, tree):
        value, data = self._reduce_tree(tree=tree)
        result = data[data.rolls > value]
        logger.debug(f'   gt({data.rolls.values}, {value}) => {result.rolls.values}')
        yield result

    def le(self, tree):
        value, data = self._reduce_tree(tree=tree)
        result = data[data.rolls <= value]
        logger.debug(f'   le({data.rolls.values}, {value}) => {result.rolls.values}')
        yield result

    def lt(self, tree):
        value, data = self._reduce_tree(tree=tree)
        result = data[data.rolls < value]
        logger.debug(f'   lt({data.rolls.values}, {value}) => {result.rolls.values}')
        yield result

    def max(self, tree):
        count, values = self._reduce_tree(tree=tree)
        result = (
            values
            .sort_values('rolls', ascending=[0])
            .head(count)
            .sort_values('index', ascending=[1])
        )
        logger.debug(f'   max({values.rolls.values}, {count}) => {result.rolls.values}')
        yield result

    def min(self, tree):
        count, values = self._reduce_tree(tree=tree)
        result = (
            values
            .sort_values('rolls', ascending=[1])
            .head(count)
            .sort_values('index', ascending=[1])
        )
        logger.debug(f'   min({values.rolls.values}, {count}) => {result.rolls.values}')
        yield result

    def mul(self, tree):
        yield from self._op(tree=tree)

    def ne(self, tree):
        value, data = self._reduce_tree(tree=tree)
        result = data[data.rolls != value]
        logger.debug(f'   ne({data.rolls.values}, {value}) => {result.rolls.values}')
        yield result

    def number(self, tree):
        value = int(tree.children[0])
        logger.debug(f'   number => {value}')
        yield value

    def parse(self, formula=None, tree=None):
        if formula:
            logger.debug(f'{formula}')
        else:
            logger.debug(f'pretty:\n{tree.pretty()}')
        tree = tree or self.ebnf_tokenizer.parse(formula)
        node_name = tree.data

        # lookup node's function
        func = self.__class__.__dict__.get(node_name)
        if not func:
            raise ParseError(f'Could not parse node of type "{node_name}"')

        data = list(func(self, tree))
        yield from data

    def perc(self, tree):
        yield 100

    def repeat(self, tree):
        sub_tree = None
        for child in tree.children:
            if child.data == 'number':
                count = next(self.parse(tree=child))
            else:
                sub_tree = child
        logger.debug(f' repeat {count}')
        for cnt in range(count):
            data = self.parse(tree=sub_tree)
            logger.debug('')
            logger.debug(f'-- Round: {cnt} --')
            yield from data
        logger.debug('')

    def sub(self, tree):
        yield from self._op(tree=tree)

    def sum(self, tree):
        for child in tree.children:
            values = next(self.parse(tree=child))
            yield values['rolls'].sum()

    def _op(self, tree):
        mapping = {
            'add': add,
            'div': div,
            'mul': mul,
            'sub': sub
        }
        func_name = tree.data
        func = mapping.get(func_name)
        if not func:
            raise InvalidOperation(f'Could not perform operation on {func_name}')
        data = tuple(value for child in tree.children for value in self.parse(tree=child))
        result = reduce(func, data[1:], data[0])
        logger.debug(f'   reduce({func_name}, {data}, 0) => {result}')
        yield result


def parse(formula, seed=None, grammer=None):
    if seed:
        random.seed(seed)
        np.random.seed(seed)
    if not grammer:
        grammer_filepath = Path(__file__).parent / 'dice.lark'
        with grammer_filepath.open('r') as stream:
            grammer = stream.read()
    parser = DiceParser(grammer=grammer)
    yield from parser.parse(formula)
