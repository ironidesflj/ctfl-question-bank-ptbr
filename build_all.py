#!/usr/bin/env python3
"""Pipeline único: build_bank.py -> add_en.py -> check_alignment.py.
Substitui a execução manual em 3 passos."""
import subprocess
import sys

STEPS = ["build_bank.py", "add_en.py", "check_alignment.py"]

for script in STEPS:
    print(f"\n=== Executando {script} ===")
    sys.stdout.flush()
    result = subprocess.run([sys.executable, script])
    if result.returncode != 0:
        print(f"\nERRO: {script} falhou (exit {result.returncode}). Pipeline interrompido.", file=sys.stderr)
        sys.exit(result.returncode)

print("\n=== Pipeline completo: build + EN + alignment check OK ===")
