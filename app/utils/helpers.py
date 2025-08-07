"""Funções auxiliares (exemplo: logs, formatação, etc.)."""

import datetime

def log_event(event):
    print(f"[{datetime.datetime.now()}] {event}")
