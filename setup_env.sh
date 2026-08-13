#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "🚀 Setting up local environment with uv..."

# 1. Install 'uv' if it's not available on PATH
if ! command -v uv &> /dev/null; then
    echo "📦 'uv' not found. Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    
    # Source path for immediate use in current session
    export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"
else
    echo "✅ 'uv' is already installed."
fi

# 2. Create virtual environment (.venv) if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "🛠️ Creating virtual environment using uv..."
    uv venv .venv --python 3.11
else
    echo "✅ Virtual environment '.venv' already exists."
fi

# 3. Activate environment and install dependencies
echo "⚡ Activating virtual environment and syncing dependencies..."

# Detect OS for proper activation script path
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source .venv/Scripts/activate
else
    source .venv/bin/activate
fi

# 4. Install essential packages (PyYAML, MkDocs Material) via uv
echo "📥 Installing MkDocs & documentation dependencies..."
uv pip install pyyaml mkdocs mkdocs-material

echo ""
echo "🎉 Setup complete! To activate your environment manually, run:"
echo "   source .venv/bin/activate  # (On Linux/macOS)"
echo "   .venv\\Scripts\\activate     # (On Windows)"