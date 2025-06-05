# Corrigido: api.py
from flask import Flask, jsonify
import pandas as pd
import os

# Importa as classes com os nomes corretos dos arquivos
from DataLoader import DataLoader
from ContadorMorte import ContadorMortes
from DataAnalise import DataAnalise

app = Flask(__name__)

# Define o caminho do arquivo
caminho_arquivo = "character-deaths.csv"

# Verifica se o arquivo existe
if not os.path.exists(caminho_arquivo):
    raise FileNotFoundError(f"Erro: Arquivo {caminho_arquivo} não encontrado!")

# Carregar dados usando a classe corrigida
loader = DataLoader(caminho_arquivo, sep=";")
df_raw = loader.load()

if df_raw is None:
    raise ValueError("Erro ao carregar os dados! DataFrame está vazio.")

# Pré-processar os dados usando a classe corrigida
analise = DataAnalise(df_raw)
df_processado, contagem_genero = analise.processar()

# Instanciar o contador com o DataFrame pré-processado
contador = ContadorMortes(df_processado)

@app.route("/api/statistics", methods=["GET"])
def get_statistics():
    """Retorna estatísticas sobre as mortes dos personagens."""
    estatisticas = contador.estatisticas_mortes()
    if "Erro" in estatisticas:
        return jsonify(estatisticas), 500 # Retorna erro se houver problema
    return jsonify(estatisticas)

@app.route("/api/record/<int:record_id>", methods=["GET"])
def get_record(record_id):
    """Retorna informações detalhadas de um personagem pelo ID (índice)."""
    # Usa a coluna "ID" criada pelo DataLoader
    if "ID" not in df_processado.columns:
        return jsonify({"status": "erro", "mensagem": "Coluna ID não encontrada no DataFrame processado."}), 500
        
    registro = df_processado[df_processado["ID"] == record_id]
    
    if not registro.empty:
        # Converte o registro para dicionário, tratando possíveis NaNs para JSON
        # Usar fillna('') pode converter números em strings, melhor usar fillna(None) ou tratar na serialização
        # Convertendo para JSON com tratamento de tipos não serializáveis
        try:
            registro_dict = registro.iloc[0].where(pd.notnull(registro.iloc[0]), None).to_dict()
            return jsonify({"status": "sucesso", "dados": registro_dict})
        except Exception as e:
             return jsonify({"status": "erro", "mensagem": f"Erro ao serializar registro: {str(e)}"}), 500
    else:
        return jsonify({"status": "erro", "mensagem": f"ID {record_id} não encontrado"}), 404

@app.route("/api/gender_count", methods=["GET"])
def get_gender_count():
    """Retorna a contagem de personagens por gênero."""
    return jsonify(contagem_genero)

if __name__ == "__main__":
    # Roda o servidor Flask na porta 5000
    # Desativar debug=True em produção
    app.run(host="0.0.0.0", port=5000, debug=False) 

