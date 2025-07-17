from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Permet les requêtes depuis d'autres domaines (CORS)

DOSSIER_JSON = "json_sorties"
os.makedirs(DOSSIER_JSON, exist_ok=True)

@app.route("/enregistrer_sortie", methods=["POST"])
def enregistrer_sortie():
    try:
        data = request.get_json()

        requis = {"codeProduit", "quantite", "operateur", "motif", "dateHeure", "date"}
        if not requis.issubset(data):
            return jsonify({"erreur": "Champs manquants"}), 400

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        code = data.get("codeProduit", "inconnu")
        nom_fichier = f"{code}_{timestamp}.json"
        chemin_fichier = os.path.join(DOSSIER_JSON, nom_fichier)

        with open(chemin_fichier, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return jsonify({"message": "✅ Mouvement sauvegardé", "fichier": nom_fichier})
    except Exception as e:
        return jsonify({"erreur": str(e)}), 500
    
    @app.route("/list_json", methods=["GET"])
def lister_fichiers_json():
    try:
        fichiers = os.listdir("json_sorties")
        fichiers_json = [f for f in fichiers if f.endswith(".json")]
        return jsonify(fichiers_json)
    except Exception as e:
        return jsonify({"erreur": str(e)}), 500

# === AJOUT ESSENTIEL POUR RENDER ===
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
