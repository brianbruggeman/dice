# dice
A [DSL](https://en.wikipedia.org/wiki/Domain-specific_language) for dice notation built in python using [Lark](https://github.com/erezsh/lark).

## Motivation

I wanted a chance to build a meaningful DSL using a library (Lark) that
I haven't tried previously.


## Usage


### CLI

The following represents how to run the parser from the command-line
interface:

    $ roll 6x4d6M3
    --------------------------------------------------
     Formula: 6x4d6M3
    --------------------------------------------------
     10
     10
     12
     8
     10
     11
    --------------------------------------------------
     Sum: 61
     Ave: 10
    --------------------------------------------------


### API

The following represents an example usage if using dice's API:


    #!/usr/bin/env python3
    from dice import parse


    def roll(formula, seed=10):
        """Rolls dice based on formula

        Args:
            formula (str): formula to roll [e.g. 3d6]
            seed (int): random number generator seed

        Returns:
            List[int]: values rolled

        """
        values = [value for value in parse(formula=formula, seed=seed)]
        return values


## Installation

This can be installed directly into a virtual environment using pip:

    pip install git+git://github.com/brianbruggeman/dice.git#egg=dice-dev



## Rules

There's a nice [wiki page](https://en.wikipedia.org/wiki/Dice_notation) on dice notation.

The current grammar (in case this document doesn't get updated well) can be found
under dice/dice.lark.

### Math

Basic math operations are as follows

| Rule     | Notation | Example | Description                                               |
|----------|----------|---------|-----------------------------------------------------------|
| dice     | d        | 3d6     | Rolls a dice (e.g. 6) a specific number of times (e.g. 3) |
| plus     | +        | 1 + 2   | Simple add                                                |
| minus    | -        | 1 - 2   | Simple subtraction                                        |
| multiply | *        | 1 * 2   | Simple multiplication                                     |
| division | /        | 2 / 2   | Simple division                                           |


### Filtering

Additionally, the following provides a mechanism for filtering data

| Rule       | Notation | Example | Description                                                        |
|------------|----------|---------|--------------------------------------------------------------------|
| maximum    | M        | 4d6M3   | Pick the highest rolls from formula (e.g. best 3 rolls out of 4)   |
| minimum    | m        | 4d6m3   | Pick the lowest rolls from formula (e.g. worst 3 rolls out of 4)   |
| over       | >        | 4d6>3   | Pick only the rolls over a threshold from formula                  |
| under      | <        | 4d6<4   | Pick only the rolls under a threshold from formula                 |
| equal      | ==       | 4d6==5  | Pick only the rolls that equal a value from formula                |
| notequal   | !=       | 4d6!=5  | Pick only the rolls that don't equal a value from formula          |
| overequal  | >        | 4d6>=3  | Pick only the rolls over or equal to a threshold from formula      |
| underequal | <=       | 4d6<=3  | Pick only the rolls under or equal to a threshold from formula     |


### Control

Finally, there are ways of controlling output

| Rule       | Notation | Example | Description                                                             |
|------------|----------|---------|-------------------------------------------------------------------------|
| iteration  | x        | 6x4d6M3 | Repeat the formula multiple times (e.g. create 6 values using 4d6M3 )   |
