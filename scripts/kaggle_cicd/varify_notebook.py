import json
import os

notebook = os.environ["NOTEBOOK"]

with open(notebook, encoding="utf-8") as f:
    nb = json.load(f)

kernelspec = nb.get("metadata", {}).get("kernelspec", {})

print("Notebook kernelspec:")
print(kernelspec)

assert kernelspec.get("name"), ("Notebook does not contain a Jupyter kernel name")

print(f"✓ Kernel detected: {kernelspec['name']}")