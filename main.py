from flask import Flask,request,jsonify
from flask_cors import CORS
from pyairtable import Table
from pyairtable.formulas import match
import os
app = Flask(__name__)
CORS(app)
@app.route("/AndromaxBDD",methods=['POST'])
def receive_data():
    data = request.get_json()
    print(data)
    #GET ESSENTIAL DATA
    usermail = data['email']
    userinformation = data['questionnaire']
    userpassword = data['password']
    #INIT DATABASE (AIRTABLE DATABASE)
    api_key = os.getenv("AIRTABLE_API_KEY")
    base_id_table_information = os.getenv("AIRTABLE_BASE_ID")
    table_name = os.getenv("AIRTABLE_TABLE_NAME")
    init_table = Table(api_key,base_id_table_information,table_name)
    #PASSWORD TREATEMENT
    import hashlib
    secured_password = hashlib.sha256(userpassword.encode()).hexdigest()
    saving_dictionnary = {"Usermail":usermail,"UserData":str(userinformation),"Password":secured_password}
    #A LITTLE VERIFICATION
    formula = match({"Usermail": usermail})
    existing_record = init_table.first(formula=formula)

    if existing_record:
        return jsonify({"status": "Error", "message": "Email déjà utilisé"}), 409

    # Création si libre
    init_table.create(saving_dictionnary)
    return jsonify({"status": "success"}), 201  # 201 = Created



