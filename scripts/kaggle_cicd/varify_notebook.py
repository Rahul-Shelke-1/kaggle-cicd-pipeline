import json
import uuid
from pathlib import Path
import nbformat


def prepare_notebook(notebook_path: Path) -> None:
    # 1. Read the notebook as a raw dictionary
    with open(notebook_path, "r", encoding="utf-8") as f:
        notebook_dict = json.load(f)

    # 2. Inject cell IDs if missing
    if "cells" in notebook_dict:
        for cell in notebook_dict["cells"]:
            if "id" not in cell:
                cell["id"] = str(uuid.uuid4())[:8]

    # 3. Ensure the metadata block and kernelspec are explicitly structured in the dictionary
    if "metadata" not in notebook_dict:
        notebook_dict["metadata"] = {}
        
    notebook_dict["metadata"]["kernelspec"] = {
        "display_name": "Python 3",
        "language": "python",
        "name": "python3",
    }
    
    if "language_info" not in notebook_dict["metadata"]:
        notebook_dict["metadata"]["language_info"] = {"name": "python"}

    # 4. Save the fully updated dictionary back to disk
    with open(notebook_path, "w", encoding="utf-8") as f:
        json.dump(notebook_dict, f, indent=4)

    # 5. Read back via nbformat solely for final schema validation
    notebook = nbformat.read(notebook_path, as_version=4)
    nbformat.validate(notebook)
    
    # Final clean save ensuring nbformat structural compliance
    nbformat.write(notebook, notebook_path)