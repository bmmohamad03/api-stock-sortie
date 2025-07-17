from flask import Flask, request, jsonify, send_from_directory
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
        code = data.get("codeProduit") or data.get("code_produit")
        date = data.get("date")
        heure = data.get("heure")

        if not code or not date or not heure:
            return jsonify({"erreur": "Champs codeProduit, date ou heure manquants"}), 400

        # Concaténation date + heure
        date_heure = f"{date} {heure}"
        nom_fichier = f"{code}_{date_heure.replace(':', '').replace('-', '').replace(' ', '_')}.json"
        chemin = os.path.join("json_sorties", nom_fichier)

        # Écriture du fichier JSON
        with open(chemin, "w") as f:
            json.dump(data, f, indent=2)

        return jsonify({"message": "✅ Mouvement sauvegardé", "fichier": nom_fichier})
    except Exception as e:
        return jsonify({"erreur": str(e)}), 500


# ✅ Route pour lister tous les fichiers JSON disponibles
@app.route("/list_json")
def liste_fichiers_json():
    try:
        chemin_dossier = os.path.join(os.getcwd(), "json_sorties")
        fichiers = os.listdir(chemin_dossier)
        fichiers_json = [f for f in fichiers if f.endswith(".json")]
        return jsonify(fichiers_json)
    except Exception as e:
        return jsonify({"erreur": str(e)})


# ✅ Route pour télécharger un fichier JSON en ligne
@app.route("/fichiers/<nom_fichier>")
def fichiers_json(nom_fichier):
    try:
        chemin_dossier = os.path.join(os.getcwd(), "json_sorties")
        return send_from_directory(chemin_dossier, nom_fichier)
    except Exception as e:
        return jsonify({"erreur": str(e)}), 500


# === Exécution locale (facultatif) ===
if __name__ == "__main__":
    app.run(debug=True, port=5001)
