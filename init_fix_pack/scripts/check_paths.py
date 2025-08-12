#!/usr/bin/env python3
import os

BASE = os.path.dirname(__file__)

paths = [
    os.path.join(BASE, "app", "agent", "templates", "outline.md.j2"),
    os.path.join(BASE, "app", "agent", "templates", "host_packets.md.j2"),
    os.path.join(BASE, "data", "prompts", "topic_engine.md"),
    os.path.join(BASE, "data", "prompts", "system.md"),
    os.path.join(BASE, "app", "main.py"),
]

print("Checking important paths...")
for p in paths:
    print(p, "=>", "OK" if os.path.exists(p) else "MISSING")
