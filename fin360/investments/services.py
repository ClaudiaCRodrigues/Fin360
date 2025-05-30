import pdfplumber
import requests
import re
import logging
from decimal import Decimal
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

from .parsers import generic_parse
from .models import (
    FinancialInstitution,
    Category,
    Investment,
    InvestmentTransaction,
    Index,
)

logger = logging.getLogger(__name__)

def detectar_instituicao(texto: str, file_name: str) -> FinancialInstitution | None:
    t = (texto or "").lower()
    for inst in FinancialInstitution.objects.all():
        name = inst.name.lower()
        code = (inst.code or "").lower()
        if name in t or (code and code in t):
            return inst
        if code and code in file_name.lower():
            return inst
    return None

def processar_importacao(arquivos, overrides=None) -> list[dict]:
    """
    Processa múltiplos PDFs:
      - detecta instituição (ou usa override)
      - carrega parsing_rules
      - chama generic_parse
      - persiste InvestmentTransaction
    Retorna lista de dicts: arquivo, broker, linhas, erro.
    """
    overrides = overrides or {}
    resultados = []

    default_cat = Category.objects.first()
    if not default_cat:
        raise RuntimeError("Cadastre ao menos uma Categoria antes de importar.")

    for f in arquivos:
        # 1) extrai só a 1ª página para detectar a instituição
        with pdfplumber.open(f) as pdf:
            texto = pdf.pages[0].extract_text() or ""
        f.seek(0)

        inst = overrides.get(f.name) or detectar_instituicao(texto, f.name)
        if not inst:
            resultados.append({
                "arquivo": f.name,
                "broker": None,
                "linhas": 0,
                "erro": "Instituição não identificada"
            })
            continue

        rules = inst.parsing_rules or {}
        if not rules:
            resultados.append({
                "arquivo": f.name,
                "broker": inst.name,
                "linhas": 0,
                "erro": "Nenhuma parsing_rules configurada"
            })
            continue

        # Log indicando com quais regras vamos parsear
        logger.debug(
            "processar_importacao: Arquivo=%s, Broker=%s, Rules=%s",
            f.name, inst.name, rules
        )

        # 2) parsing genérico
        try:
            dados = generic_parse(f, rules)
        except Exception as e:
            logger.error(
                "processar_importacao: falha ao parsear %s (%s): %s",
                f.name, inst.name, e
            )
            resultados.append({
                "arquivo": f.name,
                "broker": inst.name,
                "linhas": 0,
                "erro": str(e)
            })
            continue

        # 3) cria/obtém o Investment “agrupador”
        inv_name = f"Importação {inst.name}"
        investimento, _ = Investment.objects.get_or_create(
            broker=inst,
            name=inv_name,
            defaults={
                "category": default_cat,
                "ticker": "",
                "initial_value": Decimal("0"),
                "current_value": Decimal("0"),
                "quantidade": Decimal("0"),
                "preco_unitario": Decimal("0"),
                "valor_total": Decimal("0"),
            }
        )

        # 4) persiste cada transação
        for row in dados:
            InvestmentTransaction.objects.create(
                investment=investimento,
                date=row["data_operacao"],
                transaction_type=row["transaction_type"],
                quantity=row["quantidade"],
                price=row["preco_unitario"],
                fees=row.get("fees", Decimal("0")),
                description=row.get("description", ""),
            )

        resultados.append({
            "arquivo": f.name,
            "broker": inst.name,
            "linhas": len(dados),
            "erro": None
        })

    return resultados


# --- Sincronização de Índices via API do Bacen ---

SERIES_CODES = {"selic": 11, "ipca": 433, "cdi": 12}

def fetch_all_indices_from_bacen(years=10, timeout_seconds=30, retries=2) -> dict:
    results = {}
    data_inicial = (date.today() - relativedelta(years=years)).strftime("%d/%m/%Y")
    data_final = date.today().strftime("%d/%m/%Y")
    headers = {"Accept": "application/json"}

    for name, code in SERIES_CODES.items():
        url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{code}/dados"
        params = {"formato": "json", "dataInicial": data_inicial, "dataFinal": data_final}
        last_exc = None
        for _ in range(retries + 1):
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
            raise last_exc or Exception(f"Erro ao buscar série {name}")

    return results


def sync_indices(years=10) -> int:
    data = fetch_all_indices_from_bacen(years)
    novos = []
    for name, series in data.items():
        for entry in series:
            d = datetime.strptime(entry["data"], "%d/%m/%Y").date()
            v = Decimal(entry["valor"].replace(",", "."))
            if not Index.objects.filter(name=name, date=d).exists():
                novos.append(Index(name=name, date=d, value=v))
    if novos:
        Index.objects.bulk_create(novos)
    return len(novos)
