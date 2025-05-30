# investments/parsers.py

import pdfplumber
import re
import logging
from decimal import Decimal
from datetime import datetime

logger = logging.getLogger(__name__)

def generic_parse(file_obj, rules: dict) -> list[dict]:
    """
    Lê todo o texto do PDF (todas as páginas), normaliza espaços e quebras,
    e aplica cada regex em `rules` com re.IGNORECASE | re.DOTALL.
    Retorna lista com 1 dict: data_operacao, transaction_type, quantidade,
    preco_unitario, fees, description.
    """
    # 1) extrai texto completo
    pdf = pdfplumber.open(file_obj)
    raw = " ".join(page.extract_text() or "" for page in pdf.pages)
    pdf.close()
    file_obj.seek(0)

    # 2) normaliza NBSP e whitespace
    raw = raw.replace("\xa0", " ")
    text = re.sub(r"\s+", " ", raw).strip()

    logger.debug("generic_parse: texto normalizado (primeiros 200 chars): %r", text[:200])

    # 3) aplica cada regex definida em rules
    extracted = {}
    for field, pattern in rules.items():
        logger.debug("generic_parse: aplicando regex para '%s': /%s/", field, pattern)
        m = re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL)
        if not m:
            raise ValueError(f"Campo '{field}' não encontrado com /{pattern}/ em:\n…{text[:200]}…")
        extracted[field] = m.group(1).strip()
        logger.debug("generic_parse: extraído %s = %r", field, extracted[field])

    # 4) monta a transação
    row = {}

    # data_operacao
    if "data_operacao" in extracted:
        row["data_operacao"] = datetime.strptime(
            extracted["data_operacao"], "%d/%m/%Y"
        ).date()

    # valor → quantidade + preco_unitario=1
    if "valor" in extracted:
        v = extracted["valor"].replace(".", "").replace(",", ".")
        row["quantidade"] = Decimal(v)
        row["preco_unitario"] = Decimal("1")

    # tipo → transaction_type
    if "tipo" in extracted:
        row["transaction_type"] = extracted["tipo"].lower()
    else:
        row["transaction_type"] = "buy"

    # fees (opcional)
    if "fees" in extracted:
        f = extracted["fees"].replace(".", "").replace(",", ".")
        row["fees"] = Decimal(f)
    else:
        row["fees"] = Decimal("0")

    # description (opcional)
    row["description"] = extracted.get("description", "")

    logger.debug("generic_parse: linha final montada: %r", row)
    return [row]
