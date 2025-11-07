from flask import Flask, jsonify, request
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)  # ✅ Permite que o HTML acesse a API

# Carregar dados do arquivo JSON
with open('ingredientes_macros.json', 'r', encoding='utf-8') as f:
    ingredientes_data = json.load(f)

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
            "valor": round(valor_ajustado, 6),
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
    host = '127.0.0.1'
    port = 5000

    print("\n🚀 API de ingredientes iniciando...\n")
    print(f"✅ Todos os ingredientes: http://{host}:{port}/ingredientes")
    print(f"✅ Ingrediente específico (exemplo com 150g): http://{host}:{port}/ingrediente/1?gramas=150\n")

    app.run(debug=True, host=host, port=port)
