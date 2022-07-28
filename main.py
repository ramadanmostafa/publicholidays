from datetime import datetime

import click

from usecases import get_next_holidays_by_country_code


__author__ = "Ramadan Khalifa"

from utils import show_results


@click.command()
@click.option(
    "--country-code",
    prompt="Country Code",
    help="Country code. complete list is here https://date.nager.at/Country."
)
@click.option(
    "--max-num",
    prompt="Max num of holidays returned",
    help="Max num of holidays returned.",
    default=5,
)
def main(country_code, max_num=5):
    """
    Simple CLI for getting the Public holidays of a country by country code.
    """
    # initialize the target year with the current year
    target_year = datetime.now().year
    results = []

    # loop until we reach our target number of holidays
    while len(results) < max_num:
        error, next_result = get_next_holidays_by_country_code(
            country_code, max_num=max_num - len(results), year=target_year
        )

        # show the error if there is any
        if error:
            click.echo(error)
            return

        # next
        results += next_result
        target_year += 1

    # print results to the user
    show_results(results)


if __name__ == "__main__":
    main()
