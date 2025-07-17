from flask import Flask, request, jsonify
import os
import json

app = Flask(__name__)

# === Route principale pour enregistrer une sortie ===
@app.route("/enregistrer_sortie", methods=["POST"])
def enregistrer_sortie():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"erreur": "Données JSON manquantes"}), 400

        # Récupération des champs
        code = data.get("codeProduit") or data.get("code_produit")  # accepte les deux variantes
        date = data.get("date")
        heure = data.get("heure")

        # Vérification des champs
        if not code or not date or not heure:
            return jsonify({"erreur": "Champs codeProduit, date ou heure manquants"}), 400

        # Concaténation pour créer dateHeure
        date_heure = f"{date} {heure}"

        # Génération du nom de fichier
        nom_fichier = f"{code}_{date_heure.replace(':', '').replace('-', '').replace(' ', '_')}.json"
        chemin = os.path.join("json_sorties", nom_fichier)

        # Sauvegarde du fichier
        with open(chemin, "w") as f:
            json.dump(data, f, indent=2)

        return jsonify({"message": "✅ Mouvement sauvegardé", "fichier": nom_fichier})
    except Exception as e:
        return jsonify({"erreur": str(e)}), 500


# ✅ === Nouvelle route pour lister les fichiers JSON ===
@app.route("/list_json")
def liste_fichiers_json():
    try:
        chemin_dossier = os.path.join(os.getcwd(), "json_sorties")
        fichiers = os.listdir(chemin_dossier)
        fichiers_json = [f for f in fichiers if f.endswith(".json")]
        return jsonify(fichiers_json)
    except Exception as e:
        return jsonify({"erreur": str(e)})


# === Lancer en local si besoin ===
if __name__ == "__main__":
    app.run(debug=True, port=5001)
