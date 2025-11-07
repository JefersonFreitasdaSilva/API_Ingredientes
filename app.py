from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)  # ✅ Permite que o HTML acesse a API

# Caminho absoluto para o JSON
json_path = os.path.join(os.path.dirname(__file__), 'ingredientes_macros.json')

# Carregar dados do arquivo JSON
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        ingredientes_data = json.load(f)
except FileNotFoundError:
    ingredientes_data = []
    print("⚠️  Arquivo 'ingredientes_macros.json' não encontrado!")

@app.route('/')
def home():
    """Rota inicial informativa"""
    return jsonify({
        "mensagem": "API de ingredientes ativa!",
        "rotas": {
            "listar_ingredientes": "/ingredientes",
            "ingrediente_exemplo": "/ingrediente/1?gramas=150"
        }
    })

@app.route('/ingredientes', methods=['GET'])
def listar_ingredientes():
    """Retorna todos os ingredientes"""
    return jsonify(ingredientes_data)

@app.route('/ingrediente/<int:id_ingrediente>', methods=['GET'])
def obter_ingrediente(id_ingrediente):
    """Retorna o ingrediente com cálculo proporcional dos macronutrientes"""
    ingrediente = next((i for i in ingredientes_data if i["idIngrediente"] == id_ingrediente), None)
    if not ingrediente:
        return jsonify({"erro": "Ingrediente não encontrado"}), 404

    # Pega a quantidade em gramas informada na query (ex: /ingrediente/1?gramas=150)
    gramas = request.args.get('gramas', default=100, type=float)

    # Calcula os valores ajustados proporcionalmente
    macros_calculados = []
    for macro in ingrediente["macronutrientes"]:
        valor_ajustado = macro["valor"] * gramas / 100
        macros_calculados.append({
            "macronutriente": macro["macronutriente"],
            "valor": round(valor_ajustado, 6),  # não arredonda excessivamente
            "unidade": macro["unidade"]
        })

    resultado = {
        "idIngrediente": ingrediente["idIngrediente"],
        "nomeIngrediente": ingrediente["nomeIngrediente"],
        "idImage": ingrediente["idImage"],
        "gramas": gramas,
        "macronutrientes": macros_calculados
    }

    return jsonify(resultado)


if __name__ == '__main__':
    # Railway define a porta automaticamente
    port = int(os.environ.get('PORT', 8080))
    host = '0.0.0.0'

    # Obtém o domínio público do Railway (se existir)
    railway_url = os.environ.get('RAILWAY_STATIC_URL') or os.environ.get('RAILWAY_PUBLIC_DOMAIN') or 'http://localhost:8080'

    print("\n🚀 API de ingredientes iniciando...\n")
    print(f"✅ Todos os ingredientes: {railway_url}/ingredientes")
    print(f"✅ Ingrediente específico (exemplo com 150g): {railway_url}/ingrediente/1?gramas=150\n")

    app.run(debug=False, host=host, port=port)
