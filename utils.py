from typing import List

import click


def show_results(results: List[dict]) -> None:
    """
    Given a list of objects, it will print these data to the console in a human-readable way.
    """
    click.echo('result:')
    click.echo('----------------')
    for idx, item in enumerate(results):
        click.echo(f'{idx + 1}- {item}')
    click.echo('----------------')
