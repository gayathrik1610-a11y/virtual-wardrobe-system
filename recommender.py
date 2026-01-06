from utils import get_user_outfits
def recommend_full_outfit(user_id, input_type, input_color, input_event):
    data = get_user_outfits(user_id)
    if not data:
        return {"message": "No outfit data available."}


    input_type_norm = (input_type or "").strip().lower()
    input_color_norm = (input_color or "").strip().lower()
    input_event_norm = (input_event or "").strip().lower()


    TOP_TYPES = ["shirt", "shirts", "dress", "dresses"]
    BOTTOM_TYPES = ["pants"]


    for d in data:
        d["type_norm"] = (d.get("type", "") or "").strip().lower()
        d["color_norm"] = (d.get("color", "") or "").strip().lower()
        d["event_norm"] = (d.get("event", "casual") or "casual").strip().lower()
        d["sub_type_norm"] = (d.get("sub_type", "") or "").strip().lower()
        d["image_url"] = d.get("image_url", "")

#makes cleaned versions to make comparison easier *norm
    tops = [d for d in data if d["type_norm"] in TOP_TYPES]
    bottoms = [d for d in data if d["type_norm"] in BOTTOM_TYPES]
    shoes_list = [d for d in data if d["type_norm"] == "shoes"]
    accessories_list = [d for d in data if d["type_norm"] in ["accessory", "accessories"]]

    outfit = {"Occasion": input_event_norm.capitalize()}

    is_top_input = input_type_norm in TOP_TYPES
    is_bottom_input = input_type_norm in BOTTOM_TYPES

    top = None
    if is_top_input:
        top = next((d for d in tops if d["type_norm"] == input_type_norm and d["color_norm"] == input_color_norm and d["event_norm"] == input_event_norm), None)
        if not top:
            top = next((d for d in tops if d["type_norm"] == input_type_norm and d["event_norm"] == input_event_norm), None)
        if not top:
            top = next((d for d in tops if d["type_norm"] == input_type_norm), None)
    else:
        top = next((d for d in tops if d["event_norm"] == input_event_norm), None)

    if top:
        outfit["Top"] = {
            "type": top["type"].capitalize(),
            "color": top["color"].capitalize(),
            "image_url": top.get("image_url", "")
        }

    bottom = None
    if is_bottom_input:
        bottom = next((d for d in bottoms if d["type_norm"] == input_type_norm and d["color_norm"] == input_color_norm and d["event_norm"] == input_event_norm), None)
        if not bottom:
            bottom = next((d for d in bottoms if d["type_norm"] == input_type_norm), None)
    else:
        bottom = next((d for d in bottoms if d["event_norm"] == input_event_norm), None)
        if not bottom and bottoms:
            bottom = bottoms[0]

    if bottom:
        outfit["Bottom"] = {
            "type": bottom["type"].capitalize(),
            "color": bottom["color"].capitalize(),
            "image_url": bottom.get("image_url", "")
        }
    else:
        outfit["Bottom"] = {
            "type": "Pants",
            "color": "",
            "image_url": ""
        }


    shoes = next((d for d in shoes_list if d["event_norm"] == input_event_norm), None)
    if not shoes and shoes_list:
        shoes = shoes_list[0]

    if shoes:
        outfit["Shoes"] = {
            "type": shoes["type"].capitalize(),
            "color": shoes["color"].capitalize(),
            "image_url": shoes.get("image_url", "")
        }

    accessories = [d for d in accessories_list if d["event_norm"] == input_event_norm]
    if not accessories:
        accessories = accessories_list  

    outfit["Accessories"] = [
        {
            "type": d.get("type", "").capitalize(),
            "sub_type": d.get("sub_type", "").capitalize(),
            "color": d.get("color", "").capitalize(),
            "image_url": d.get("image_url", "")
        } for d in accessories[:3]
    ]

    return outfit







    