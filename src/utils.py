import calendar
import locale
from datetime import datetime

import pytz
import requests

br_tz = pytz.timezone("America/Sao_Paulo")


def real_currency(value):
    locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")
    value = locale.currency(value, grouping=True, symbol=False)
    return value


def get_last_9_months(mode="abbr"):
    today = datetime.now()
    months = []
    for i in range(9):
        month = (today.month - i - 1) % 12 + 1
        if mode == "abbr":
            months.append(calendar.month_abbr[month])
        elif mode == "number":
            months.append(month)
    return list(reversed(months))


def get_ipca(dataInicial, dataFinal):
    url = (
        f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados"
        f"?formato=json&dataInicial={dataInicial}&dataFinal={dataFinal}"
    )
    res = requests.get(url)
    if res.status_code != 200:
        return 0
    dados = res.json()
    ipca_acumulado = sum(float(item["valor"]) for item in dados)
    return ipca_acumulado


def get_min_salary(dataInicial, dataFinal):
    url = (
        f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.1619/dados?"
        f"formato=json&dataInicial={dataInicial}&dataFinal={dataFinal}"
    )
    res = requests.get(url)
    if res.status_code != 200:
        return 0
    dados = res.json()
    return float(dados[0]["valor"])
