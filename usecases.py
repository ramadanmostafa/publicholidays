from typing import List, Optional

import requests
from datetime import datetime

from cache import get_data_from_cache, save_data_to_cache
from client import NagerHolidaysClient


def get_next_occurring_holidays(data: List[dict], max_num: int = 5) -> List[dict]:
    now = datetime.now()
    today_date = now.date()
    result = []
    for holiday in data:
        holiday_date = datetime.strptime(holiday['date'], '%Y-%m-%d').date()
        if len(result) >= max_num:
            break
        if today_date > holiday_date:
            continue
        result.append({
            'date': holiday['date'],
            'name': holiday['name'],
            'counties': holiday['counties'],
            'types': holiday['types'],
        })

    return result


def get_next_holidays_by_country_code(country_code, max_num=5, year=None) -> (Optional[str], Optional[List[dict]]):
    cache_key = f'{year};{country_code}'
    data_from_cache = get_data_from_cache(cache_key)
    if data_from_cache:
        print(f'Getting data from cache for country: {country_code} and year: {year}')
        result = get_next_occurring_holidays(data_from_cache, max_num)
        return None, result

    try:
        response_data = NagerHolidaysClient().get_holidays(country_code, year)
    except requests.exceptions.HTTPError:
        return 'HTTPError', None
    except requests.exceptions.JSONDecodeError:
        return 'JSONDecodeError', None

    print(f'saving data to cache for country: {country_code} and year: {year}')
    save_data_to_cache(cache_key, response_data)
    result = get_next_occurring_holidays(response_data, max_num)
    return None, result
