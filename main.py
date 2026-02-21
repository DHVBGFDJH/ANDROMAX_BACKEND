from flask import Flask, request, jsonify
from flask_cors import CORS
from pyairtable import Table
from pyairtable.formulas import match
import os
import hashlib

app = Flask(__name__)
CORS(app)


@app.route("/AndromaxBDD", methods=["POST"])
def receive_data():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "Aucune donnée reçue"}), 400

        # GET DATA
        usermail = data.get("email")
        userinformation = data.get("questionnaire")
        userpassword = data.get("password")

        if not usermail or not userpassword:
            return jsonify({"error": "Email ou mot de passe manquant"}), 400

        # ENV VARIABLES
        api_key = os.getenv("AIRTABLE_API_KEY")
        base_id = os.getenv("AIRTABLE_BASE_ID")
        table_name = os.getenv("AIRTABLE_TABLE_NAME")

        if not api_key or not base_id or not table_name:
            return jsonify({"error": "Variables d'environnement Airtable manquantes"}), 500

        # INIT AIRTABLE
        table = Table(api_key, base_id, table_name)

        # HASH PASSWORD
        secured_password = hashlib.sha256(userpassword.encode()).hexdigest()

        saving_dictionary = {
            "Usermail": usermail,
            "UserData": str(userinformation),
            "Password": secured_password
        }

        # CHECK IF EMAIL EXISTS
        formula = match({"Usermail": usermail})
        existing_record = table.first(formula=formula)

        if existing_record:
            return jsonify({"status": "Error", "message": "Email déjà utilisé"}), 409

        # CREATE RECORD
        table.create(saving_dictionary)

        return jsonify({"status": "success"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
