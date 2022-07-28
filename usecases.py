from typing import List, Optional

import requests
from datetime import datetime

from cache import get_data_from_cache, save_data_to_cache
from client import NagerHolidaysClient


def get_next_occurring_holidays(data: List[dict], max_num: int = 5) -> List[dict]:
    """
    parse Holidays API response and get next n holidays
    :param data: Holidays API response
    :param max_num: number of holidays in the response
    :return: list of holidays
    """
    # get today's date
    today_date = datetime.now().date()

    # init the results
    result = []

    # for each holiday in the holiday api response
    for holiday in data:

        # break if we already reached the required number of holidays in the result
        if len(result) >= max_num:
            break

        # get the date of the current holiday
        holiday_date = datetime.strptime(holiday['date'], '%Y-%m-%d').date()

        # skip if the holiday date is in the past
        if today_date > holiday_date:
            continue

        # save the result
        result.append({
            'date': holiday['date'],
            'name': holiday['name'],
            'counties': holiday['counties'],
            'types': holiday['types'],
        })

    return result


def get_next_holidays_by_country_code(country_code, max_num=5, year=None) -> (Optional[str], Optional[List[dict]]):
    """
    given a country code and a year, it gets holidays from external API (or cache).
    :param country_code: 2 letters country code. case-insensitive
    :param max_num: number of holidays we want to get
    :param year: the year we want to get holidays for
    :return: error string if any error happens and list of results if there is no error
    """
    # caching key should be something like this `2022;DE`
    cache_key = f'{year};{country_code}'

    # check if the data is already cached
    data_from_cache = get_data_from_cache(cache_key)
    if data_from_cache:
        # if the data is in the cache then we don't need to call the external API
        print(f'Getting data from cache for country: {country_code} and year: {year}')
        result = get_next_occurring_holidays(data_from_cache, max_num)
        return None, result

    try:
        # getting the holidays from Nager Holidays API
        response_data = NagerHolidaysClient().get_holidays(country_code, year)
    except requests.exceptions.HTTPError:
        return 'HTTPError', None
    except requests.exceptions.JSONDecodeError:
        return 'JSONDecodeError', None

    print(f'saving data to cache for country: {country_code} and year: {year}')
    save_data_to_cache(cache_key, response_data)
    result = get_next_occurring_holidays(response_data, max_num)
    return None, result
