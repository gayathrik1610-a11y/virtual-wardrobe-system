from flask import Flask, request, jsonify
from utils import store_metadata_in_supabase
from ai_model.recommender import recommend_full_outfit
from supabase import create_client, Client
supabase_Url = 'your supabase url'
supabase_Key = 'your supabase key'
supabase = create_client(supabase_Url, supabase_Key)

app = Flask(__name__)

@app.route ('/upload', methods=['POST'])
def upload_outfit():
    data = request.json
    user_id = data.get('user_id')
    image_url = data.get('image_url')
    metadata = {
        "type": data.get("type"),
        "color": data.get("color"),
        "event": data.get("event"),
        "sub_type": data.get("sub_type")  
    }
    user_id = data.get('user_id')
    store_metadata_in_supabase(user_id, image_url, metadata)
    return jsonify({'status': 'success'})

@app.route('/recommend', methods=['POST'])
def get_recommendation():
    data = request.json

    user_id = data.get("user_id")
    input_type = data.get("input_type")
    input_color = data.get("input_color")
    input_event = data.get("input_event")

    if not user_id or not input_type or not input_color or not input_event:
        return jsonify({"message": "Missing input values"}), 400

    result = recommend_full_outfit(user_id, input_type, input_color, input_event)
    if isinstance(result, dict) and result.get("error") == "not_found":
        return jsonify(result), 404

    return jsonify(result), 200




@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    exist = supabase.table("users").select("*").eq("email", email).execute()

    if exist.data:
        return jsonify({"message": "Email already registered"}), 400

    supabase.table("users").insert({
        "email": email,
        "password": password
    }).execute()

    return jsonify({"message": "Signup successful"}), 200



@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')


    user = supabase.table("users").select("*").eq("email", email).execute()

    if len(user.data) == 0:
        return jsonify({"success": False, "message": "Email not found"}), 400

    stored_password = user.data[0]["password"]

    
    if stored_password != password:
        return jsonify({"success": False, "message": "Wrong password"}), 401

    
    return jsonify({"success": True, "message": "Login successful", "user_id": user.data[0]["id"]}), 200



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


