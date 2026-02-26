#!/usr/bin/env bash
set -euo pipefail

banner() {
  echo ""
  echo " _   _    _    ___ _____   _    _____ _____ ____ "
  echo "| | | |  / \\  |_ _|  ___| / \\  | ____| ____|  _ \\"
  echo "| |_| | / _ \\  | || |_   / _ \\ |  _| |  _| | |_) |"
  echo "|  _  |/ ___ \\ | ||  _| / ___ \\| |___| |___|  _ <"
  echo "|_| |_/_/   \\_\\___|_|  /_/   \\_\\_____|_____|_| \\_\\"
  echo ""
}

step() { echo "[*] $1"; }
ok() { echo "[OK] $1"; }
warn() { echo "[!!] $1"; }

banner
step "WSL Linux setup for EEG Workshop"

step "Updating packages..."
sudo apt-get update -y
sudo apt-get install -y git curl
ok "System packages ready."

step "Checking uv..."
if ! command -v uv >/dev/null 2>&1; then
  warn "uv not found. Installing..."
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ok "uv installed."
else
  ok "uv is installed."
fi

step "Choose where to save the repo"
warn "Avoid paths with Hebrew (or other non-ASCII) characters to prevent tool issues."
echo "[*] Suggested folder name: EEG_ANALYSIS"
read -r -p "Enter a full folder path to store the repo (default: $HOME/EEG_ANALYSIS): " baseDir
if [ -z "${baseDir}" ]; then baseDir="$HOME/EEG_ANALYSIS"; fi
if echo "$baseDir" | LC_ALL=C grep -q '[^ -~]'; then
  warn "The path contains non-ASCII characters. Please use only English letters, numbers, and standard symbols."
  exit 1
fi
mkdir -p "$baseDir"
cd "$baseDir"

step "Cloning repo..."
repoUrl="https://github.com/ngetter/EEG_workshop.git"
repoName="$(basename "$repoUrl" .git)"
if [ ! -d "$repoName" ]; then
  git clone "$repoUrl"
  ok "Repo cloned."
else
  ok "Repo already exists."
fi
cd "$repoName"
ok "Current directory set to $repoName"

step "Syncing environment from pyproject.toml..."
uv sync
uv pip install marimo jupyterlab
ok "Environment synced. marimo and jupyterlab ensured."

step "Choose notebook experience"
read -r -p "Init marimo or jupyter? [marimo/jupyter] (default: marimo): " choice
if [ -z "${choice}" ]; then choice="marimo"; fi
choice="$(echo "$choice" | tr '[:upper:]' '[:lower:]' | xargs)"

if [ "$choice" = "jupyter" ]; then
  ok "Launching JupyterLab..."
  uv run jupyter lab
else
  ok "Launching marimo..."
  uv run marimo edit sample.py
fi
