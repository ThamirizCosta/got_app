# Corrigido: ContadorMorte.py
import pandas as pd

class ContadorMortes:
    def __init__(self, dataframe):
        """Inicializa o contador com o DataFrame pré-processado."""
        # Garante que está trabalhando com uma cópia
        self.df = dataframe.copy()
        # Garante que as colunas necessárias são numéricas
        if 'Death_Year' in self.df.columns:
            self.df['Death_Year'] = pd.to_numeric(self.df['Death_Year'], errors='coerce').fillna(0)
        if 'Morreu' in self.df.columns:
            self.df['Morreu'] = pd.to_numeric(self.df['Morreu'], errors='coerce').fillna(0).astype(int)
        else:
            # Se a coluna 'Morreu' não existir (caso DataAnalise não tenha sido executado completamente antes)
            # tenta criá-la a partir de 'Death_Year'
            if 'Death_Year' in self.df.columns:
                self.df['Morreu'] = self.df['Death_Year'].apply(lambda x: 1 if x > 0 else 0)
                print("Aviso: Coluna 'Morreu' criada em ContadorMortes.")
            else:
                 # Se nem 'Morreu' nem 'Death_Year' existem, inicializa 'Morreu' com 0
                 self.df['Morreu'] = 0
                 print("Aviso: Colunas 'Morreu' e 'Death_Year' não encontradas. Contagem de mortes será 0.")

    def contar_mortes(self):
        """Conta o número de mortes registradas usando a coluna 'Morreu'."""
        if 'Morreu' not in self.df.columns:
             print("Erro: Coluna 'Morreu' não encontrada para contagem.")
             return 0 # Retorna 0 se a coluna não existe
        
        total_mortes = self.df['Morreu'].sum()
        print(f"Total de mortes contadas: {total_mortes}")
        return total_mortes

    def estatisticas_mortes(self):
        """Retorna estatísticas das mortes usando 'Death_Year'."""
        # Verifica se as colunas necessárias existem
        if 'Morreu' not in self.df.columns or 'Death_Year' not in self.df.columns:
            return {"Erro": "Colunas 'Morreu' ou 'Death_Year' não encontradas."}

        # Filtra o DataFrame para incluir apenas personagens que morreram
        df_mortes = self.df[self.df['Morreu'] == 1].copy()
        
        if df_mortes.empty:
            print("Nenhuma morte registrada para calcular estatísticas.")
            return {
                "Total de Mortes": 0,
                "Mensagem": "Nenhuma morte registrada."
            }
        
        # Calcula as estatísticas sobre o ano da morte ('Death_Year')
        # Garante que Death_Year é numérico para estatísticas
        df_mortes['Death_Year'] = pd.to_numeric(df_mortes['Death_Year'], errors='coerce')
        # Remove NaNs que podem ter surgido da coerção, se houver
        df_mortes.dropna(subset=['Death_Year'], inplace=True)

        if df_mortes.empty:
             print("Nenhuma morte com ano válido registrada para calcular estatísticas.")
             return {
                "Total de Mortes": self.contar_mortes(), # Ainda retorna o total de mortes
                "Mensagem": "Nenhuma morte com ano válido para calcular estatísticas."
            }

        stats = {
            "Total de Mortes": int(self.contar_mortes()), # Usa o método de contagem atualizado
            "Média do Ano das Mortes": round(df_mortes['Death_Year'].mean(), 2),
            "Mediana do Ano das Mortes": df_mortes['Death_Year'].median(),
            "Desvio Padrão do Ano das Mortes": round(df_mortes['Death_Year'].std(), 2),
            "Ano Mínimo de Morte": int(df_mortes['Death_Year'].min()),
            "Ano Máximo de Morte": int(df_mortes['Death_Year'].max())
        }
        print(f"Estatísticas de mortes calculadas: {stats}")
        return stats

# Exemplo de uso (adaptado para novas colunas)
if __name__ == "__main__":
    dados = {
        'Name': ['Arya Stark', 'Jon Snow', 'Robb Stark', 'Catelyn Tully'],
        'Gender': [0, 1, 1, 0],
        'Death_Year': [0, 0, 299, 299],
        'Allegiances': ['Stark', "Night's Watch", 'Stark', 'Stark']
    }
    df_exemplo = pd.DataFrame(dados)
    
    # Simula o pré-processamento que adicionaria 'Morreu'
    df_exemplo['Morreu'] = df_exemplo['Death_Year'].apply(lambda x: 1 if x > 0 else 0)
    
    contador = ContadorMortes(df_exemplo)
    
    print(f"\nTotal de Mortes: {contador.contar_mortes()}")
    print("\nEstatísticas das Mortes:")
    print(contador.estatisticas_mortes())

