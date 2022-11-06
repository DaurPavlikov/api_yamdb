import datetime as dt


def validate_year(year):
    current_year = dt.datetime.today().year
    if year > current_year:
        raise ValueError(f'Некорректный год {year}')
