import json


class MentalStateComparisonTask:
    """
    Compara dos estados mentales exportados.
    """

    def compare(self, path_a: str, path_b: str):
        with open(path_a, "r", encoding="utf-8") as fa:
            a = json.load(fa)
        with open(path_b, "r", encoding="utf-8") as fb:
            b = json.load(fb)

        def keys(d):
            return set(d.keys())

        result = {
            "guardian_self_diff": list(
                keys(a.get("guardian_self", {})) ^ keys(b.get("guardian_self", {}))
            ),
            "concepts_diff": list(
                keys(a.get("cognitive_memory", {}).get("concepts", {})) ^
                keys(b.get("cognitive_memory", {}).get("concepts", {}))
            ),
            "error_patterns_diff": (
                len(a.get("cognitive_memory", {}).get("error_patterns", [])),
                len(b.get("cognitive_memory", {}).get("error_patterns", []))
            )
        }

        return result