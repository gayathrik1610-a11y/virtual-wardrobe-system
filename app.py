from flask import Flask, request, jsonify
from utils import store_metadata_in_supabase
from ai_model.recommender import recommend_full_outfit

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_outfit():
    data = request.json
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
    user_id = request.json.get('user_id')
    input_type = request.json.get('type')
    input_color = request.json.get('color')
    input_event = request.json.get('event')  

    result = recommend_full_outfit(user_id, input_type, input_color, input_event)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)

