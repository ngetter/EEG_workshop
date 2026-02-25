$ErrorActionPreference = "Stop"

function Write-Header([string]$msg) {
  Write-Host ""
  Write-Host "╔══════════════════════════════════════════════════════════════╗"
  Write-Host "║ $msg"
  Write-Host "╚══════════════════════════════════════════════════════════════╝"
}

function Write-Banner {
  Write-Host " _   _    _    ___ _____   _    _____ _____ ____ "
  Write-Host "| | | |  / \\  |_ _|  ___| / \\  | ____| ____|  _ \\"
  Write-Host "| |_| | / _ \\  | || |_   / _ \\ |  _| |  _| | |_) |"
  Write-Host "|  _  |/ ___ \\ | ||  _| / ___ \\| |___| |___|  _ <"
  Write-Host "|_| |_/_/   \\_\\___|_|  /_/   \\_\\_____|_____|_| \\_\\"
}

function Write-Step([string]$msg) {
  Write-Host "[*] $msg"
}

function Write-Ok([string]$msg) {
  Write-Host "[OK] $msg"
}

function Write-Warn([string]$msg) {
  Write-Host "[!!] $msg"
}

Write-Banner
Write-Header "EEG Workshop: Windows 11 Environment Setup"
Write-Warn "Recommendation: Use WSL for a smoother Python/science stack on Windows."
$useWindows = Read-Host "Continue with native Windows setup? [y/N]"
if ([string]::IsNullOrWhiteSpace($useWindows) -or $useWindows.ToLower().Trim() -ne "y") {
  Write-Step "Installing/launching WSL (Ubuntu) and running Linux setup..."
  wsl --install
  Write-Step "Checking if WSL is ready..."
  $wslReady = $true
  try {
    wsl -d Ubuntu -- bash -lc "echo WSL_READY" | Out-Null
  } catch {
    $wslReady = $false
  }
  if (-not $wslReady) {
    Write-Warn "WSL needs a reboot or first-run setup. Please reboot, then rerun this script."
    Write-Ok "Exiting Windows setup."
    exit 0
  }

  $linuxScript = @'
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
  uv run marimo tutorial
fi
'@

  # Run the Linux setup script inside Ubuntu
  wsl -d Ubuntu -- bash -lc "$linuxScript"
  Write-Ok "WSL setup complete. Exiting Windows setup."
  exit 0
}

# 1. Git
Write-Step "Checking Git..."
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
  Write-Warn "Git not found. Installing Git for Windows..."
  winget install --id Git.Git -e --source winget
  Write-Ok "Git installed."
} else {
  Write-Ok "Git is installed."
}

# 2. GitHub Desktop
Write-Step "Checking GitHub Desktop..."
$ghd = winget list --id GitHub.GitHubDesktop -e 2>$null | Select-String "GitHub Desktop"
if (-not $ghd) {
  Write-Warn "GitHub Desktop not found. Installing..."
  winget install --id GitHub.GitHubDesktop -e --source winget
  Write-Ok "GitHub Desktop installed."
} else {
  Write-Ok "GitHub Desktop is installed."
}

# 3. Choose repo location + clone
Write-Step "Choose where to save the repo"
Write-Warn "Avoid paths with Hebrew (or other non-ASCII) characters to prevent tool issues."
Write-Step "Suggested folder name: EEG_ANALYSIS"
$baseDir = Read-Host "Enter a full folder path to store the repo (default: C:\\EEG_ANALYSIS)"
if ([string]::IsNullOrWhiteSpace($baseDir)) {
  $baseDir = "C:\\EEG_ANALYSIS"
}
if ($baseDir -match "[^\x00-\x7F]") {
  Write-Warn "The path contains non-ASCII characters. Please use only English letters, numbers, and standard symbols."
  exit 1
}
if (-not (Test-Path $baseDir)) {
  Write-Step "Creating folder: $baseDir"
  New-Item -ItemType Directory -Path $baseDir | Out-Null
}
Set-Location $baseDir

Write-Step "Cloning repo..."
$repoUrl = "https://github.com/ngetter/EEG_workshop.git"
$repoName = [System.IO.Path]::GetFileNameWithoutExtension($repoUrl.TrimEnd("/"))
if (-not (Test-Path $repoName)) {
  git clone $repoUrl
  Write-Ok "Repo cloned."
} else {
  Write-Ok "Repo already exists."
}
Set-Location $repoName
Write-Ok "Current directory set to $repoName"

# 4. uv
Write-Step "Checking uv..."
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
  Write-Warn "uv not found. Installing..."
  irm https://astral.sh/uv/install.ps1 | iex
  Write-Ok "uv installed."
} else {
  Write-Ok "uv is installed."
}

# 5. Sync environment
Write-Step "Syncing environment from pyproject.toml..."
uv sync
uv pip install marimo jupyterlab
Write-Ok "Environment synced. marimo and jupyterlab ensured."

# 6. Launch choice
Write-Step "Choose notebook experience"
$choice = Read-Host "Init marimo or jupyter? [marimo/jupyter] (default: marimo)"
if ([string]::IsNullOrWhiteSpace($choice)) { $choice = "marimo" }
$choice = $choice.ToLower().Trim()

if ($choice -eq "jupyter") {
  Write-Ok "Launching JupyterLab..."
  uv run jupyter lab
} else {
  Write-Ok "Launching marimo..."
  uv run marimo tutorial
}
