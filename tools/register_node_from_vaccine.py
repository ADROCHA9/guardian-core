import json
from memory import ProjectMemory

def register_from_file(root_path: str, node_profile_path: str):
    memory = ProjectMemory(root_path)
    memory.load()

    with open(node_profile_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    node = data["node_profile"]
    node_id = node["node_id"]

    memory.register_node(node_id, node)
    memory.register_consent({
        "timestamp": node["timestamp"],
        "node_id": node_id,
        "action": "vaccine_executed",
        "operator": node["consent"]["operator"],
        "scope": node["consent"]["scope"]
    })

    memory.log_event(
        event="node_registered",
        summary=f"Nodo registrado por vacuna manual: {node_id}"
    )