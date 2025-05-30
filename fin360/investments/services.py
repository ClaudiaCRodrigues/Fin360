import requests
from decimal import Decimal
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from .models import Index
from .parsers import BTGParser, XPParser, BaseParser

PARSERS = {
    'BTG': BTGParser,
    'XP': XPParser,
}

# Códigos da API Bacen para cada índice
SERIES_CODES = {
    'selic': 11,
    'ipca': 433,
    'cdi': 12,
    # ... outros índices ...
}

def detectar_corretora(texto_pagina):
    if 'Nota de Negociação de Títulos Privados' in texto_pagina:
        return 'BTG'
    if 'Confirmação de Aplicação' in texto_pagina:
        return 'XP'
    raise ValueError('Corretora não reconhecida')

def processar_importacao(arquivos):
    resultados = []
    for f in arquivos:
        # extrai texto da primeira página
        import pdfplumber
        with pdfplumber.open(f) as pdf:
            primeira_pagina = pdf.pages[0].extract_text()
        broker = detectar_corretora(primeira_pagina)
        parser_cls = PARSERS[broker]
        parser = parser_cls(f)
        dados = parser.parse()
        # ex.: salvar no banco:
        # for d in dados:
        #     Investment.objects.create(**d)
        resultados.append({'arquivo': f.name, 'broker': broker, 'linhas': len(dados)})
    return resultados



def fetch_all_indices_from_bacen(years=10, timeout_seconds=30, retries=2):
    """
    Busca todos os dados de cada índice no Bacen desde 'years' anos atrás até hoje,
    usando cabeçalho Accept JSON, com timeout e re-tentativas.
    """
    results = {}
    data_inicial = (date.today() - relativedelta(years=years)).strftime('%d/%m/%Y')
    data_final = date.today().strftime('%d/%m/%Y')
    headers = {'Accept': 'application/json'}

    for name, code in SERIES_CODES.items():
        url = f'https://api.bcb.gov.br/dados/serie/bcdata.sgs.{code}/dados'
        params = {
            'formato': 'json',
            'dataInicial': data_inicial,
            'dataFinal': data_final,
        }
        last_exc = None
        for attempt in range(retries + 1):
            try:
                resp = requests.get(url, params=params, headers=headers, timeout=timeout_seconds)
                resp.raise_for_status()
                results[name] = resp.json()
                break
            except requests.exceptions.Timeout as e:
                last_exc = e
                continue
            except requests.exceptions.RequestException as e:
                last_exc = e
                break
        else:
            # todas tentativas falharam
            raise last_exc or Exception(f"Erro desconhecido ao buscar {name}")

    return results

def sync_indices(years=10):
    """
    Sincroniza índices: busca no Bacen e insere somente registros novos.
    """
    data = fetch_all_indices_from_bacen(years)
    novos = []
    for name, series in data.items():
        for entry in series:
            d = datetime.strptime(entry['data'], '%d/%m/%Y').date()
            v = Decimal(entry['valor'].replace(',', '.'))
            if not Index.objects.filter(name=name, date=d).exists():
                novos.append(Index(name=name, date=d, value=v))
    if novos:
        Index.objects.bulk_create(novos)
    return len(novos)
