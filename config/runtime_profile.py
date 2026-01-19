# ==========================================
# PERFIL DE EJECUCIÓN GLOBAL
# ==========================================

# Modos posibles: "desktop", "server"
RUNTIME_PROFILE = "server"


# ==========================================
# PERFIL SERVER – EVOLUCIÓN DE LARGO PLAZO
# ==========================================

SERVER_PROFILE = {

    # --------------------------------------------------
    # ⏱️ CICLO COGNITIVO
    # --------------------------------------------------

    # Intervalo base del loop cognitivo (segundos)
    # Más bajo = más ciclos, más reflexión
    "base_interval": 4,

    # Forzar pensamiento aunque no haya estímulos externos
    # Evita estancamiento cognitivo
    "force_think_interval": 20,


    # --------------------------------------------------
    # 📚 APRENDIZAJE
    # --------------------------------------------------

    # Aprendizaje pasivo continuo (Python, patrones, errores)
    # Se ejecuta aunque no haya interacción humana
    "passive_learning_interval": 45,

    # Permitir sesiones largas de aprendizaje profundo
    "allow_long_sessions": True,

    # Intensidad semántica (leída por varias tareas)
    # Valores esperados: "low", "normal", "high", "intense"
    "learning_intensity": "intense",

    # Modo de aprendizaje global
    "learning_mode": "aggressive",


    # --------------------------------------------------
    # 🧪 TESTS Y EXPLORACIÓN
    # --------------------------------------------------

    # Permite tests más complejos y costosos
    "enable_deep_tests": True,

    # Número máximo de micro-tests por ciclo
    "max_micro_tests_per_cycle": 5,

    # Permitir generación de hipótesis internas
    "enable_hypothesis_generation": True,

    # Permitir exploración conceptual autónoma
    "enable_concept_exploration": True,


    # --------------------------------------------------
    # 🧹 LIMPIEZA Y CALIDAD COGNITIVA
    # --------------------------------------------------

    # Forzar limpieza cognitiva periódica
    "force_cognitive_cleanup": True,

    # No conservar ideas no usadas mucho tiempo
    "discard_stale_ideas": True,

    # Ventana máxima de ideas crudas (segundos)
    "raw_idea_ttl": 3600,   # 1 hora

    # Priorizar patrones útiles sobre cantidad
    "pattern_quality_over_quantity": True,


    # --------------------------------------------------
    # 🧯 AUTORREGULACIÓN DE RECURSOS
    # --------------------------------------------------

    # RAM mínima libre antes de bajar intensidad (MB)
    "min_free_ram_mb": 128,

    # Permitir usar swap si es necesario (ya existe en el sistema)
    "allow_swap_usage": True,

    # Nivel de estrés permitido antes de regular
    # Valores: "low", "medium", "high"
    "allowed_load_pressure": "high",


    # --------------------------------------------------
    # 🌱 CONTEXTO DE EJECUCIÓN
    # --------------------------------------------------

    # Entorno semántico
    "environment": "stable",

    # Guardian no está en supervivencia
    "memory_mode": "growth",

    # Permitir evolución continua sin pausa humana
    "autonomous_continuous_operation": True,

    # Horizonte temporal (informativo para tareas de planificación)
    "planning_horizon": "long_term",
}
