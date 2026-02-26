$ErrorActionPreference = "Stop"

function Write-Header([string]$msg) {
  Write-Host ""
  Write-Host "==============================================================="
  Write-Host $msg
  Write-Host "==============================================================="
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
Write-Header "EEG Workshop: Windows 11 Native Setup"
Write-Warn "This script is Windows-only and does not use WSL."

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
Write-Warn "GitHub Desktop check may pause on first winget use while source agreements are processed."
$setupGithubDesktop = Read-Host "Do you want to check/install GitHub Desktop? [y/N]"
if (-not [string]::IsNullOrWhiteSpace($setupGithubDesktop) -and $setupGithubDesktop.ToLower().Trim() -eq "y") {
  Write-Step "Checking GitHub Desktop..."
  if (-not (Get-Command winget -ErrorAction SilentlyContinue)) {
    Write-Warn "winget not found. Skipping GitHub Desktop setup."
  } else {
    $ghd = winget list --id GitHub.GitHubDesktop -e --accept-source-agreements --disable-interactivity 2>$null | Select-String "GitHub Desktop"
    if (-not $ghd) {
      Write-Warn "GitHub Desktop not found. Installing..."
      winget install --id GitHub.GitHubDesktop -e --source winget --accept-package-agreements --accept-source-agreements --disable-interactivity
      Write-Ok "GitHub Desktop installed."
    } else {
      Write-Ok "GitHub Desktop is installed."
    }
  }
} else {
  Write-Step "Skipping GitHub Desktop setup by user choice."
}

# 3. Choose repo location + clone
Write-Step "Choose where to save the repo"
Write-Warn "Avoid paths with Hebrew (or other non-ASCII) characters to prevent tool issues."
Write-Step "Suggested folder name: EEG_ANALYSIS"
$baseDir = Read-Host "Enter a full folder path to store the repo (default: C:\EEG_ANALYSIS)"
if ([string]::IsNullOrWhiteSpace($baseDir)) {
  $baseDir = "C:\EEG_ANALYSIS"
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
  uv run marimo edit sample.py
}
