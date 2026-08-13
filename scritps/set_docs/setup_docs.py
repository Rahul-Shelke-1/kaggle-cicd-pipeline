import os
import re
from pathlib import Path

# Paths resolved relative to project root (2 levels up from scripts/docs/)
SCRIPT_DIR = Path(__file__).parent.resolve()
ROOT_DIR = SCRIPT_DIR.parent.parent
MKDOCS_YAML = ROOT_DIR / "mkdocs.yml"
DOCS_DIR = ROOT_DIR / "docs"


def extract_paths_with_yaml(yaml_path: Path) -> list[str]:
    """Extract file paths from nav using PyYAML if available."""
    import yaml

    with open(yaml_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    nav = data.get("nav", [])
    paths = []

    def recursive_extract(node):
        if isinstance(node, str):
            if node.endswith(".md"):
                paths.append(node)
        elif isinstance(node, list):
            for item in node:
                recursive_extract(item)
        elif isinstance(node, dict):
            for value in node.values():
                recursive_extract(value)

    recursive_extract(nav)
    return paths


def extract_paths_fallback(yaml_path: Path) -> list[str]:
    """Fallback regex parser to extract .md paths without third-party dependencies."""
    paths = []
    pattern = re.compile(r":\s*([^\s#]+\.md)")

    with open(yaml_path, "r", encoding="utf-8") as f:
        for line in f:
            match = pattern.search(line)
            if match:
                paths.append(match.group(1).strip("'\""))

    return paths


def get_nav_file_paths(yaml_path: Path) -> list[str]:
    """Dynamically gathers all target file paths defined in mkdocs.yml."""
    if not yaml_path.exists():
        raise FileNotFoundError(f"❌ Could not find mkdocs.yml at {yaml_path}")

    try:
        paths = extract_paths_with_yaml(yaml_path)
    except ImportError:
        print("ℹ️  PyYAML not installed. Falling back to regex extraction...")
        paths = extract_paths_fallback(yaml_path)

    return list(dict.fromkeys(paths))


def build_docs_structure():
    """Reads mkdocs.yml and creates missing directories and markdown files under docs/."""
    file_paths = get_nav_file_paths(MKDOCS_YAML)
    print(f"📄 Found {len(file_paths)} markdown files in {MKDOCS_YAML}\n")

    created_count = 0
    skipped_count = 0

    for relative_file in file_paths:
        target_file = DOCS_DIR / relative_file

        # Ensure directory exists
        target_file.parent.mkdir(parents=True, exist_ok=True)

        # Create file only if it doesn't already exist
        if not target_file.exists():
            heading_title = target_file.stem.replace("-", " ").replace("_", " ").title()
            
            with open(target_file, "w", encoding="utf-8") as f:
                f.write(f"# {heading_title}\n\n*Content coming soon...*\n")
            
            print(f"✅ Created : docs/{relative_file}")
            created_count += 1
        else:
            print(f"⏭️  Skipped : docs/{relative_file} (Already exists)")
            skipped_count += 1

    print(f"\n🎉 Finished! Created {created_count} new file(s), skipped {skipped_count} existing file(s).")


if __name__ == "__main__":
    build_docs_structure()