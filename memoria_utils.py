import json
from pathlib import Path

MEM_FILE = Path("memoria.json")


def ensure():
    if not MEM_FILE.exists():
        with MEM_FILE.open("w", encoding="utf-8") as f:
            json.dump({"memoria": []}, f)


def ler_memoria(limit=10):
    ensure()
    with MEM_FILE.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return data["memoria"][-limit:]


def salvar_memoria(item):
    ensure()
    with MEM_FILE.open("r", encoding="utf-8") as f:
        data = json.load(f)
    data["memoria"].append(item)
    with MEM_FILE.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
