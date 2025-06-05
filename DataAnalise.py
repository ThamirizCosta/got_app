# Corrigido: DataAnalise.py
import pandas as pd

class DataAnalise:
    def __init__(self, dataframe):
        """Inicializa a análise de dados."""
        self.df = dataframe.copy()  # Faz uma cópia para evitar modificar o original

    def tratar_nulos_e_brancos(self):
        """Substitui strings vazias ou contendo apenas espaços por NaN e preenche NaN com 0."""
        # Substitui strings vazias ou com espaços por NaN
        self.df.replace(r'^\s*$', pd.NA, regex=True, inplace=True)
        # Preenche valores NA/NaN com 0 (cuidado: isso pode não ser ideal para todas as colunas)
        # Vamos preencher apenas colunas numéricas relevantes com 0 ou mediana/média se apropriado
        colunas_numericas = ["Death_Year", "Book of Death", "Death Chapter", "Book Intro Chapter", "GoT", "CoK", "SoS", "FfC", "DwD"]
        for col in colunas_numericas:
            if col in self.df.columns:
                # Converte para numérico, forçando erros para NaN
                self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
                # Preenche NaN com 0
                self.df[col].fillna(0, inplace=True)
        
        # Preenche NaN em colunas categóricas com 'Desconhecido' ou ''
        if 'Allegiances' in self.df.columns:
            self.df['Allegiances'].fillna('Desconhecido', inplace=True)
        if 'Gender' in self.df.columns:
             # Gender já é numérico (0 ou 1), preenche NaN com um valor padrão (ex: -1 ou mantém NaN)
             self.df['Gender'].fillna(-1, inplace=True) # Usando -1 para indicar desconhecido/não preenchido
        if 'Nobility' in self.df.columns:
             self.df['Nobility'].fillna(-1, inplace=True)

    def codificar_genero(self):
        """Codifica a coluna 'Gender' e retorna contagem dos valores."""
        if 'Gender' in self.df.columns:
            # Garante que a coluna é numérica
            self.df['Gender'] = pd.to_numeric(self.df['Gender'], errors='coerce').fillna(-1).astype(int)
            # Mapeia os valores numéricos para strings descritivas
            gender_map = {1: 'Masculino', 0: 'Feminino', -1: 'Desconhecido'}
            self.df['Gender_Str'] = self.df['Gender'].map(gender_map)
            print("Coluna 'Gender_Str' criada.")
            return self.df['Gender_Str'].value_counts().to_dict()
        else:
            print("Aviso: Coluna 'Gender' não encontrada no DataFrame.")
            return {}

    def contabilizar_morte(self):
        """Cria uma coluna 'Morreu' (1 se Death_Year > 0, senão 0)."""
        if 'Death_Year' in self.df.columns:
             # Garante que Death_Year é numérico
            self.df['Death_Year'] = pd.to_numeric(self.df['Death_Year'], errors='coerce').fillna(0)
            self.df['Morreu'] = self.df['Death_Year'].apply(lambda x: 1 if x > 0 else 0)
            print("Coluna 'Morreu' criada.")
        else:
            print("Aviso: Coluna 'Death_Year' não encontrada no DataFrame.")

    def processar(self):
        """Executa pré-processamento dos dados e retorna o DataFrame atualizado."""
        print("Iniciando pré-processamento...")
        self.tratar_nulos_e_brancos()
        contagem_genero = self.codificar_genero()
        self.contabilizar_morte()
        print("Pré-processamento concluído.")
        return self.df, contagem_genero  # Retorna o DataFrame atualizado e a contagem de gênero

# Exemplo de uso (adaptado para novas colunas)
if __name__ == "__main__":
    dados = {
        'Name': ['Arya Stark', 'Jon Snow', 'Robb Stark', 'Catelyn Tully'],
        'Gender': [0, 1, 1, 0], # 0 para Feminino, 1 para Masculino
        'Death_Year': [0, 0, 299, 299], # 0 se vivo no final dos livros
        'Allegiances': ['Stark', "Night's Watch", 'Stark', 'Stark']
    }

    df_exemplo = pd.DataFrame(dados)
    analise = DataAnalise(df_exemplo)
    df_processado, contagem_genero = analise.processar()

    print("\nDataFrame atualizado:")
    print(df_processado)
    print("\nContagem de Gênero:")
    print(contagem_genero)

