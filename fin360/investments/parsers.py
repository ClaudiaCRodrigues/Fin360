import pdfplumber
from abc import ABC, abstractmethod
import re
from datetime import datetime

class BaseParser(ABC):
    def __init__(self, arquivo):
        self.arquivo = arquivo

    @abstractmethod
    def parse(self):
        """Retorna lista de dicts com campos normalizados."""
        pass

class BTGParser(BaseParser):
    def parse(self):
        resultados = []
        with pdfplumber.open(self.arquivo) as pdf:
            text = pdf.pages[0].extract_text()
            # Exemplo: extrair Data da Operação (17/05/2025) e títulos
            match = re.search(r'Data da Operação\s+(\d{2}/\d{2}/\d{4})', text)
            data_op = datetime.strptime(match.group(1), '%d/%m/%Y').date() if match else None  # :contentReference[oaicite:0]{index=0}
            # Para tabelas use pdf.pages[i].extract_table()
            table = pdf.pages[2].extract_table()
            # Supondo colunas: Tipo, Quantidade, Preço Unitário, Valor Total, …
            for row in table[1:]:
                resultados.append({
                    'broker': 'BTG',
                    'data_operacao': data_op,
                    'tipo': row[0],
                    'quantidade': float(row[1].replace(',', '.')),
                    'preco_unitario': float(row[2].replace(',', '.')),
                    'valor_total': float(row[3].replace(',', '.')),
                })
        return resultados

class XPParser(BaseParser):
    def parse(self):
        resultados = []
        with pdfplumber.open(self.arquivo) as pdf:
            text = pdf.pages[0].extract_text()
            # Exemplo: Data Solicitação (22/05/2025) e Valor Solicitado (R$ 63,75)
            match_data = re.search(r'Data Solicitação\s+(\d{2}/\d{2}/\d{4})', text)
            match_val = re.search(r'Valor Solicitado\s+R\$ ([\d\.,]+)', text)
            data_req = datetime.strptime(match_data.group(1), '%d/%m/%Y').date() if match_data else None  # :contentReference[oaicite:1]{index=1}
            valor = float(match_val.group(1).replace('.', '').replace(',', '.')) if match_val else None
            resultados.append({
                'broker': 'XP',
                'data_solicitacao': data_req,
                'valor_solicitado': valor,
                # fund, status, etc. também podem ser extraídos
            })
        return resultados
