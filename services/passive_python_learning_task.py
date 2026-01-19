import inspect
import time
from datetime import datetime
from typing import List, Dict, Any

import math
import itertools
import functools
import collections
import inspect as inspect_mod
import ast
import types
import os
import sys
import pathlib
import threading
import multiprocessing
import asyncio
import subprocess
import signal
import logging
import argparse
import json
import csv
import sqlite3
import dataclasses
import typing
import socket
import http.client
import urllib.parse
import timeit
import cProfile


from config.runtime_profile import RUNTIME_PROFILE, SERVER_PROFILE


class PassivePythonLearningTask:
    """
    Aprendizaje pasivo REAL y profundo de Python.
    Diseñado para evolución a largo plazo (1+ año).
    """

    INTERVAL_DESKTOP = 180

    BUILTINS = [
        len, sum, min, max, any, all, enumerate, zip, sorted, reversed,
        isinstance, issubclass, getattr, setattr, hasattr, callable
    ]

    TYPES = [
        list, dict, set, tuple, frozenset,
        int, float, str, bool, bytes
    ]

    ADVANCED_TYPES = [
        dataclasses.dataclass,
        typing.NamedTuple,
        typing.TypedDict
    ]

    MODULES = [
        # Core
        math, itertools, functools, collections, inspect_mod, ast, types,
        # Sistema
        os, sys, pathlib, subprocess, signal, logging, argparse,
        # Concurrencia
        threading, multiprocessing, asyncio,
        # Datos
        json, csv, sqlite3, dataclasses, typing,
        # Red
        socket, http.client, urllib.parse,
        # Performance
        timeit, cProfile,
        # GUI
  
    ]

    EXCEPTIONS = [
        Exception, ValueError, TypeError, IndexError,
        KeyError, AttributeError, RuntimeError
    ]

    def __init__(self, memory):
        self.memory = memory

    # =================================================
    # CONTROL DE EJECUCIÓN
    # =================================================
    def should_run(self) -> bool:
        guardian = self.memory._memory.setdefault("guardian_self", {})
        now = time.time()

        last = guardian.get("last_passive_learning")
        if not last:
            return True

        try:
            last_ts = float(last)
        except Exception:
            return True

        if RUNTIME_PROFILE == "server":
            return (now - last_ts) >= SERVER_PROFILE["passive_learning_interval"]

        return (now - last_ts) >= self.INTERVAL_DESKTOP

    # =================================================
    # APRENDIZAJE REAL
    # =================================================
    def run(self) -> List[Dict[str, Any]]:
        learned: List[Dict[str, Any]] = []

        snapshot = self.memory._memory
        guardian = snapshot.setdefault("guardian_self", {})
        cognitive = snapshot.setdefault("cognitive_memory", {})
        python_knowledge = cognitive.setdefault("python_knowledge", {})

        today = datetime.utcnow().date().isoformat()
        daily = cognitive.setdefault("python_daily", {})
        daily.setdefault(today, 0)

        for obj in self.BUILTINS:
            learned += self._learn_object(obj, "builtin", python_knowledge, daily, today)

        for obj in self.TYPES:
            learned += self._learn_object(obj, "type", python_knowledge, daily, today)

        for obj in self.ADVANCED_TYPES:
            learned += self._learn_object(obj, "advanced_type", python_knowledge, daily, today)

        for mod in self.MODULES:
            learned += self._learn_module(mod, python_knowledge, daily, today)

        for exc in self.EXCEPTIONS:
            learned += self._learn_object(exc, "exception", python_knowledge, daily, today)

        guardian["last_passive_learning"] = str(time.time())

        if learned:
            self.memory.log_event(
                event="python_passive_learning",
                summary=f"{len(learned)} nuevos conceptos Python"
            )

        self.memory._persist()
        return learned

    # =================================================
    # HELPERS
    # =================================================
    def _learn_object(self, obj, category, python_knowledge, daily, today):
        name = getattr(obj, "__name__", str(obj))
        bucket = python_knowledge.setdefault(category, [])

        if any(e["name"] == name for e in bucket):
            return []

        item = {
            "name": name,
            "category": category,
            "type": type(obj).__name__,
            "doc": inspect.getdoc(obj) or ""
        }

        bucket.append(item)
        daily[today] += 1
        return [item]

    def _learn_module(self, module, python_knowledge, daily, today):
        name = module.__name__
        bucket = python_knowledge.setdefault("module", [])

        if any(e["name"] == name for e in bucket):
            return []

        item = {
            "name": name,
            "type": "module",
            "doc": inspect.getdoc(module) or ""
        }

        bucket.append(item)
        daily[today] += 1
        return [item]
