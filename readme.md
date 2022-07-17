## Public Holidays
a CLI that fetches public holidays from the existing API, https://date.nager.at, and show the next 5 occurring holidays.
- In order to avoid fetching the data too frequently, the endpoint shouldn't be called more than once a day.
- The country code should be passed as a cli argument.
- The output should contain the following information: Date, name, counties, types


# How to Run
```
docker-compose build
docker-compose run command python main.py --country-code DE --max-num 5
```

# How it works
It's Simple CLI for getting the Public holidays of a country by country code. It tries to fetch
holidays from https://date.nager.at API for a specific country (by country code) and a year then save
this data to Redis cache, so it can be used again if needed.
