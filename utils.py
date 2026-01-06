import os
from supabase import create_client
from dotenv import load_dotenv      #access to environmental variables,cconnects to supabase,loads from .evn
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")

if not SUPABASE_URL or not SUPABASE_API_KEY:
    raise ValueError("Supabase URL or API key missing in .env")

supabase = create_client(SUPABASE_URL, SUPABASE_API_KEY)

def store_metadata_in_supabase(user_id, image_url, metadata):
    data = {
        "user_id": str(user_id).strip().lower(),
        "image_url": image_url,
        "type": (metadata.get("type", "") or "").strip().lower(),
        "color": (metadata.get("color", "") or "").strip().lower(),
        "event": (metadata.get("event", "") or "Casual").strip().lower(),
        "sub_type": (metadata.get("sub_type", "") or "").strip().lower()
    }
    response = supabase.table("Outfits").insert(data).execute()
    return response

def get_user_outfits(user_id): #fetches all outfits for the given user
    try:
        all_data = supabase.table("Outfits").select("*").execute().data or []
        matching = [
            item for item in all_data
            if str(item.get("user_id", "")).strip().lower() == str(user_id).strip().lower()
        ]
        cleaned = []
        for item in matching:
            cleaned.append({
                "user_id": item.get("user_id", "").strip().lower(),
                "type": (item.get("type", "") or "").strip().lower(),
                "color": (item.get("color", "") or "").strip().lower(),
                "event": (item.get("event", "Casual") or "Casual").strip().lower(),
                "image_url": item.get("image_url", ""),
                "sub_type": (item.get("sub_type", "") or "").strip().lower()
            })
        return cleaned
    except Exception as e:
        print(f"Supabase error: {e}")
        return []
