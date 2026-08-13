from __future__ import annotations

import os
from pathlib import Path

import nbformat


def prepare_notebook(notebook_path: Path) -> None:
    notebook = nbformat.read(notebook_path, as_version=4)

    # Add missing cell IDs and normalize notebook structure.
    notebook = nbformat.normalize(notebook)

    # Ensure Jupyter kernel metadata exists.
    notebook.metadata.setdefault(
        "kernelspec",
        {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        },
    )

    # Validate after normalization.
    nbformat.validate(notebook)

    # Write normalized notebook.
    nbformat.write(notebook, notebook_path)


def main() -> None:
    notebook_path = Path(os.environ["NOTEBOOK"])

    if not notebook_path.exists():
        raise FileNotFoundError(
            f"Notebook not found: {notebook_path}"
        )

    prepare_notebook(notebook_path)


if __name__ == "__main__":
    main()