import abc

import requests


class HolidaysClient(abc.ABC):
    BASE_URL = None

    def get_holidays(self, country_code: str, year: int):
        raise NotImplemented()


class NagerHolidaysClient(HolidaysClient):
    BASE_URL = 'https://date.nager.at'

    def get_holidays(self, country_code: str, year: int):
        url = f'{self.BASE_URL}/api/v3/PublicHolidays/{year}/{country_code}'
        response = requests.get(url)
        response.raise_for_status()
        response_data = response.json()
        return response_data
