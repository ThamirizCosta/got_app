# Corrigido: DataLoader.py
import pandas as pd
import os

class DataLoader:
    def __init__(self, caminho_arquivo, sep=";"):
        self.caminho_arquivo = caminho_arquivo
        self.sep = sep

    def load(self):
        """Carrega dados do arquivo CSV e adiciona uma coluna ID."""
        if not os.path.exists(self.caminho_arquivo):
            raise FileNotFoundError(f"Arquivo CSV não encontrado: {self.caminho_arquivo}")
        
        try:
            df = pd.read_csv(self.caminho_arquivo, sep=self.sep, encoding="utf-8")
            # Adiciona uma coluna ID baseada no índice
            df["ID"] = df.index
            print(f"Dados carregados de {self.caminho_arquivo}. Colunas: {df.columns.tolist()}")
            return df
        except Exception as e:
            print(f"Erro ao carregar o arquivo CSV: {e}")
            return None

