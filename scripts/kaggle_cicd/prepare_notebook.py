import json
import uuid
from pathlib import Path
import nbformat


def prepare_notebook(notebook_path: Path) -> None:
    # 1. Read the notebook as a raw dictionary to safely inject IDs
    with open(notebook_path, "r", encoding="utf-8") as f:
        notebook_dict = json.load(f)

    # 2. Manually add a unique id to any cell missing one
    if "cells" in notebook_dict:
        for cell in notebook_dict["cells"]:
            if "id" not in cell:
                # Generate a short, clean, unique 8-character string ID
                cell["id"] = str(uuid.uuid4())[:8]

    # 3. Write it back to disk so nbformat reads the updated file
    with open(notebook_path, "w", encoding="utf-8") as f:
        json.dump(notebook_dict, f, indent=4)

    # 4. Now use nbformat safely just to verify validation and format consistency
    notebook = nbformat.read(notebook_path, as_version=4)

    # Ensure Jupyter kernel metadata exists.
    notebook.metadata.setdefault(
        "kernelspec",
        {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        },
    )

    # Validate after manual normalization
    nbformat.validate(notebook)

    # Write normalized notebook via nbformat standard engine
    nbformat.write(notebook, notebook_path)