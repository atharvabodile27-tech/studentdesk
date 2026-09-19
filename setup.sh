#!/usr/bin/env bash
# ===================================================================
# setup.sh — ek command me pura local environment ready
#
#   bash setup.sh          # venv + dependencies + tests
#   bash setup.sh --run    # upar wala + app bhi chala do
# ===================================================================
set -e

cd "$(dirname "$0")"

echo "=========================================="
echo "  StudentDesk — Local Setup"
echo "=========================================="

# ---- 1. Python check ----
if command -v python3 >/dev/null 2>&1; then PY=python3; elif command -v python >/dev/null 2>&1; then PY=python; else
  echo "❌ Python nahi mila. Pehle install karo: https://www.python.org/downloads/"; exit 1
fi
echo "✅ Python: $($PY --version)"

# ---- 2. Virtual environment ----
if [ ! -d "venv" ]; then
  echo "📦 Virtual environment bana raha hoon..."
  $PY -m venv venv
else
  echo "✅ venv already maujood hai"
fi

# shellcheck disable=SC1091
source venv/bin/activate 2>/dev/null || . venv/Scripts/activate
echo "✅ venv activated: $(which python)"

# ---- 3. Dependencies ----
echo "📥 Dependencies install kar raha hoon..."
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt
pip install --quiet -r requirements-dev.txt
echo "✅ Dependencies installed"

# ---- 4. Tests ----
echo ""
echo "🧪 Tests chala raha hoon..."
if pytest -q; then
  echo "✅ Saare tests PASS"
else
  echo "❌ Kuch tests FAIL hue — upar output dekho"
  exit 1
fi

# ---- 5. Optional: app run ----
if [ "$1" == "--run" ]; then
  echo ""
  echo "🚀 App start kar raha hoon..."
  echo "   👉 http://localhost:5000"
  echo "   👉 login: admin / admin123"
  echo "   Band karne ke liye: Ctrl+C"
  echo ""
  python run.py
else
  echo ""
  echo "=========================================="
  echo "  ✅ SETUP COMPLETE"
  echo "=========================================="
  echo ""
  echo "  App chalane ke liye:"
  echo "    source venv/bin/activate"
  echo "    python run.py"
  echo ""
  echo "  Ya directly:"
  echo "    bash setup.sh --run"
  echo ""
  echo "  👉 http://localhost:5000   (admin / admin123)"
  echo "=========================================="
fi
