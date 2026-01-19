# environment/capability_profile.py
def build_capability_profile(mode: dict, hardware: dict) -> dict:
    capabilities = {
        "can_execute_real_changes": False,
        "can_manage_hardware": False,
        "can_format_system": False,
        "can_run_sandbox": True,
    }

    if mode["mode"] == "USER":
        capabilities.update({
            "can_execute_real_changes": True,   # con confirmación
            "can_manage_hardware": False,
            "can_format_system": False,
        })

    if mode["mode"] == "SYSTEM":
        capabilities.update({
            "can_execute_real_changes": True,
            "can_manage_hardware": True,
            "can_format_system": True,
        })

    if mode["mode"] == "FIRMWARE":
        capabilities.update({
            "can_execute_real_changes": True,
            "can_manage_hardware": True,
            "can_format_system": True,
            "can_run_sandbox": False,
        })

    return {
        "mode": mode,
        "hardware_limits": hardware,
        "capabilities": capabilities,
    }