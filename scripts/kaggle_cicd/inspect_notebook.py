import json
import os

notebook = os.environ["NOTEBOOK"]

with open(notebook, encoding="utf-8") as f:
    nb = json.load(f)

print("Notebook:", notebook)
print("Kernel metadata:")
print(json.dumps(
    nb.get("metadata", {}).get("kernelspec", {}),
    indent=2
))

print("Language metadata:")
print(json.dumps(
    nb.get("metadata", {}).get("language_info", {}),
    indent=2
))

print("Cell count:", len(nb.get("cells", [])))

missing_ids = [
    i for i, cell in enumerate(nb.get("cells", []))
    if "id" not in cell
]

print("Cells missing IDs:", missing_ids)