# intelligence/prompt_builder.py
from typing import Dict


def build_prompt(
    task: str,
    memory_snapshot: Dict,
    extra_context: str = ""
) -> str:
    """
    Prompt general para análisis, propuestas y consultoría.
    """
    project = memory_snapshot.get("project", {})
    files = memory_snapshot.get("files", {})
    proposals = memory_snapshot.get("proposed_connections", [])
    inconsistencies = memory_snapshot.get("inconsistencies", [])

    return f"""
Sos un consultor experto en arquitectura y código Python.

REGLAS ABSOLUTAS:
- NO ejecutes código
- NO escribas archivos
- NO propongas acciones destructivas
- SOLO análisis y propuestas

Proyecto:
- Nombre: {project.get("name")}
- Propósito: {project.get("purpose")}
- Dominio: {project.get("domain")}

Estado actual:
- Archivos: {len(files)}
- Propuestas activas: {len(proposals)}
- Inconsistencias detectadas: {len(inconsistencies)}

Tarea solicitada:
{task}

Contexto adicional:
{extra_context}

Entrega obligatoria:
- explicación clara
- cambios propuestos
- archivos afectados
- riesgos (si existen)
"""


def build_code_prompt(proposal: Dict, context: Dict) -> str:
    """
    Prompt específico para generación de código en sandbox.
    """
    project = context.get("project", {})

    return f"""
Sos un asistente de código para el sistema GUARDIAN.

REGLAS ABSOLUTAS (NO VIOLABLES):
- NO usar os, sys, subprocess, socket, shutil
- NO ejecutar comandos
- NO escribir archivos
- NO usar eval, exec, __import__
- SOLO generar código Python puro
- Código modular, claro y mantenible

PROPUESTA A IMPLEMENTAR:
{proposal}

CONTEXTO DEL PROYECTO:
- Nombre: {project.get("name")}
- Propósito: {project.get("purpose")}

OBJETIVO:
Generar código que pueda probarse en sandbox sin efectos secundarios.

DEVOLVÉ:
- SOLO código Python válido
- SIN explicaciones
"""