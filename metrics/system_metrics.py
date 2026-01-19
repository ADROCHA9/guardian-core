# metrics/system_metrics.py

from typing import Dict
import time


def collect_metrics(memory) -> Dict:
    project = memory.get("project") or {}
    files = memory.get("files") or {}
    inconsistencies = memory.get("inconsistencies") or []
    proposals = memory.get("proposed_connections") or []

    guardian = memory._memory.get("guardian_self", {}) or {}
    identity = memory.get("identity", {}) or {}
    services = memory.get("services", {}) or {}
    root = memory.get("guardian_root", {}) or {}

    identity_verified = bool(identity.get("verified"))

    guardian_verified = (
        identity_verified
        and guardian.get("identity_propagated") is True
        and guardian.get("cognitive_core") == "active"
    )

    return {
        "timestamp": time.time(),

        # ---------------- GUARDIAN ----------------
        "guardian": {
            "status": guardian.get("status", "idle"),
            "mode": guardian.get("mode"),
            "last_decision": guardian.get("last_decision"),
            "skip_reason": guardian.get("last_skip_reason"),
            "last_cycle": guardian.get("last_cycle"),
            "identity_verified": guardian_verified,
            "cognitive_core": guardian.get("cognitive_core"),
            "services_active": [
                name for name, state in services.items()
                if state == "active"
            ],
        },

        # ---------------- PROYECTO ----------------
        "project": {
            "name": project.get("name"),
            "files_total": len(files),
            "inconsistencies": len(inconsistencies),
            "proposals_total": len(proposals),
            "prepared_evolutions": len(
                [p for p in proposals if p.get("status") == "prepared"]
            ),
        },

        # ---------------- SALUD ----------------
        "health": {
            "guardian": "verified" if guardian_verified else "unverified",
            "project": "stable" if not inconsistencies else "attention",
        },

        # ---------------- SEGURIDAD ----------------
        "security": {
            "identity": "verified" if identity_verified else "unverified",
            "root_protected": bool(root.get("protected")),
        }
    }