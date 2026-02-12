import json
from pathlib import Path

HISTORY_FILE = Path("storage/history.json")
HISTORY_FILE.parent.mkdir(exist_ok=True)

def load_history():
    if not HISTORY_FILE.exists():
        return {}
    try:
        return json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}

def save_query(user_id: int, query: str):
    data = load_history()
    user_id_str = str(user_id)
    
    if user_id_str not in data:
        data[user_id_str] = []
    
    if query in data[user_id_str]:
        data[user_id_str].remove(query)
    
    data[user_id_str].insert(0, query)
    
    data[user_id_str] = data[user_id_str][:10]
    
    HISTORY_FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

def get_user_history(user_id: int):
    data = load_history()
    return data.get(str(user_id), [])