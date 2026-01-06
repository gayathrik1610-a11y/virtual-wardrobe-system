import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import NearestNeighbors
from utils import get_user_outfits

def recommend_full_outfit(user_id, input_type, input_color, input_event, n_neighbors=3):
    data = get_user_outfits(user_id)
    if not data:
        return {"message": "No outfit data available."}


    input_type_norm = (input_type or "").strip().lower()
    input_color_norm = (input_color or "").strip().lower()
    input_event_norm = (input_event or "").strip().lower()


    for d in data:
        d["type_norm"] = (d.get("type", "") or "").strip().lower()
        d["color_norm"] = (d.get("color", "") or "").strip().lower()
        d["event_norm"] = (d.get("event", "casual") or "casual").strip().lower()
        d["sub_type_norm"] = (d.get("sub_type", "") or "").strip().lower()
        d["image_url"] = d.get("image_url", "")


    df_event = pd.DataFrame([d for d in data if d["event_norm"] == input_event_norm])
    if df_event.empty:
        return {"message": f"No items found for event '{input_event}' in your wardrobe."}

    
    TOP_TYPES = {
        "shirt": ["shirt", "shirts"],
        "dress": ["dress", "dresses"]
    }
    BOTTOM_TYPES = ["pants"]
    ACCESSORY_TYPES = ["accessory", "accessories"]
    SHOES_TYPES = ["shoes"]

    all_types = sum(TOP_TYPES.values(), []) + BOTTOM_TYPES + ACCESSORY_TYPES + SHOES_TYPES

    if input_type_norm not in all_types:
        return {"message": f"No items of type '{input_type}' found in your wardrobe."}
    if input_type_norm in sum(TOP_TYPES.values(), []):
        type_items = df_event[df_event["type_norm"].isin([input_type_norm])]
    elif input_type_norm in BOTTOM_TYPES:
        type_items = df_event[df_event["type_norm"] == input_type_norm]
    else:
        type_items = pd.DataFrame()
    type_items_color = type_items[type_items["color_norm"] == input_color_norm]
    if type_items_color.empty:
        available_colors = type_items["color"].unique().tolist()
        if available_colors:
            return {"message": f"You don't have this color for '{input_type}' in your wardrobe. Available colors: {', '.join(available_colors)}"}
        else:
            return {"message": f"You don't have any '{input_type}' for '{input_event}' in your wardrobe."}
    def knn_recommend(df_sub, target_type, target_color):
        if df_sub.empty:
            return None
        df_sub = df_sub.copy()
        le_type = LabelEncoder()
        le_color = LabelEncoder()
        df_sub["type_enc"] = le_type.fit_transform(df_sub["type_norm"])
        df_sub["color_enc"] = le_color.fit_transform(df_sub["color_norm"])
        X = df_sub[["type_enc", "color_enc"]].values

        knn = NearestNeighbors(n_neighbors=min(n_neighbors, len(df_sub)))
        knn.fit(X)

        try:
            input_vec = [[
                le_type.transform([target_type])[0],
                le_color.transform([target_color])[0]
            ]]
        except ValueError:
            input_vec = [[df_sub["type_enc"].iloc[0], df_sub["color_enc"].iloc[0]]]

        distances, indices = knn.kneighbors(input_vec)
        return df_sub.iloc[indices[0][0]]

    outfit = {"Occasion": input_event.capitalize()}

    tops_df = df_event[df_event["type_norm"].isin(sum(TOP_TYPES.values(), []))]
    if not tops_df.empty:
        top_item = knn_recommend(tops_df, tops_df["type_norm"].iloc[0], input_color_norm)
        outfit["Top"] = {
            "type": top_item["type"].capitalize(),
            "color": top_item["color"].capitalize(),
            "image_url": top_item.get("image_url", "")
        }
    bottoms_df = df_event[df_event["type_norm"].isin(BOTTOM_TYPES)]
    bottom_item = knn_recommend(bottoms_df, input_type_norm, input_color_norm)
    if bottom_item is not None:
        outfit["Bottom"] = {
            "type": bottom_item["type"].capitalize(),
            "color": bottom_item["color"].capitalize(),
            "image_url": bottom_item.get("image_url", "")
        }
    else:
        outfit["Bottom"] = None
    shoes_df = df_event[df_event["type_norm"].isin(SHOES_TYPES)]
    shoe_item = knn_recommend(shoes_df, shoes_df["type_norm"].iloc[0] if not shoes_df.empty else "", input_color_norm)
    if shoe_item is not None:
        outfit["Shoes"] = {
            "type": shoe_item["type"].capitalize(),
            "color": shoe_item["color"].capitalize(),
            "image_url": shoe_item.get("image_url", "")
        }
    else:
        outfit["Shoes"] = None

    accessories_df = df_event[df_event["type_norm"].isin(ACCESSORY_TYPES)].head(3)
    outfit["Accessories"] = [
        {
            "type": d["type"].capitalize(),
            "sub_type": d.get("sub_type", "").capitalize(),
            "color": d["color"].capitalize(),
            "image_url": d.get("image_url", "")
        }
        for _, d in accessories_df.iterrows()
    ]

   
    missing = []

    if "Top" not in outfit or not outfit["Top"]:
        missing.append("Top")

    if "Bottom" not in outfit or not outfit["Bottom"] or not outfit["Bottom"].get("image_url"):
        missing.append("Bottom")

    if "Shoes" not in outfit or not outfit["Shoes"]:
        missing.append("Shoes")

    if missing:
        return {
            "error": "not_found",
            "message": "You don't have this in your wardrobe.",
            "missing_items": missing
        }
    return outfit




    
