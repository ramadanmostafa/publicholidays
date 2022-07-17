from typing import List

import click


def show_results(results: List[dict]) -> None:
    click.echo('result:')
    click.echo('----------------')
    for idx, item in enumerate(results):
        click.echo(f'{idx + 1}- {item}')
