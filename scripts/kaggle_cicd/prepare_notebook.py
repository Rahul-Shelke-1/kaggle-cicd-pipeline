import json
import uuid
from pathlib import Path

import nbformat


def prepare_notebook(notebook_path: Path) -> None:
    with notebook_path.open("r", encoding="utf-8") as f:
        notebook_dict = json.load(f)

    # ------------------------------------------------------------------
    # Ensure every cell has an ID
    # ------------------------------------------------------------------
    for cell in notebook_dict.get("cells", []):
        if "id" not in cell:
            cell["id"] = uuid.uuid4().hex[:8]

    # ------------------------------------------------------------------
    # Ensure notebook metadata exists
    # ------------------------------------------------------------------
    metadata = notebook_dict.setdefault("metadata", {})

    # ------------------------------------------------------------------
    # Force a valid Jupyter Python kernel
    # ------------------------------------------------------------------
    metadata["kernelspec"] = {
        "display_name": "Python 3",
        "language": "python",
        "name": "python3",
    }

    metadata["language_info"] = {
        "name": "python",
    }

    # ------------------------------------------------------------------
    # Write raw JSON
    # ------------------------------------------------------------------
    with notebook_path.open("w", encoding="utf-8") as f:
        json.dump(
            notebook_dict,
            f,
            indent=4,
            ensure_ascii=False,
        )

    # ------------------------------------------------------------------
    # Final nbformat validation + normalization
    # ------------------------------------------------------------------
    notebook = nbformat.read(notebook_path, as_version=4)

    nbformat.validate(notebook)

    # Verify the thing Papermill actually needs
    kernel_name = notebook.metadata.get("kernelspec", {}).get("name")

    if kernel_name != "python3":
        raise ValueError(
            f"Invalid notebook kernel: {kernel_name!r}"
        )

    nbformat.write(notebook, notebook_path)

    print(f"Notebook normalized successfully: {notebook_path}")
    print(f"Kernel: {kernel_name}")