<#
=====================================================================
 Make-TDSRMaster.ps1
 ---------------------------------------------------------------------
 Generates a SINGLE .txt "master source dump" of the TSDR repo, in the
 same format as your existing TDSR_Master_v2.txt:

     <TITLE> SOURCE DUMP
     Generated: MM/dd/yyyy HH:mm:ss
     =====================================================
     FILE: <relative\path\to\file>
     =====================================================
     <file contents>
     =====================================================
     FILE: <next file>
     ...

 This version INCLUDES netlify\functions\** and lib\** (the .mjs files
 that were missing from v2), plus html/css/js/sql/toml/json/md, etc.

 USAGE (run from the repo root, e.g. C:\...\star-dedication-registry):
     powershell -ExecutionPolicy Bypass -File .\Make-TDSRMaster.ps1
   or specify options:
     .\Make-TDSRMaster.ps1 -Root . -Output TDSR_Master_v3.txt -Title "TSDR MASTER"

 The output file is written to the repo root by default.
=====================================================================
#>

[CmdletBinding()]
param(
    # Repo root to scan (defaults to the folder you run the script from).
    [string]$Root = ".",

    # Output file name (written into $Root unless you give a full path).
    [string]$Output = "TDSR_Master_v3.txt",

    # Header title line.
    [string]$Title = "THE STAR DEDICATION REGISTRY MASTER"
)

$ErrorActionPreference = "Stop"

# --- resolve paths ----------------------------------------------------
$Root = (Resolve-Path -LiteralPath $Root).Path
if ([System.IO.Path]::IsPathRooted($Output)) {
    $OutPath = $Output
} else {
    $OutPath = Join-Path $Root $Output
}
$OutName = [System.IO.Path]::GetFileName($OutPath)

# --- what to INCLUDE --------------------------------------------------
# File extensions we treat as text and dump.
$IncludeExt = @(
    ".mjs", ".cjs", ".js", ".mts", ".ts",
    ".html", ".htm", ".css",
    ".sql", ".toml", ".json", ".md", ".txt",
    ".yml", ".yaml", ".xml", ".svg", ".csv"
)

# Files with NO/odd extension we still want (exact file names).
$IncludeNames = @(
    "_headers", ".gitignore", ".env.example",
    "robots.txt", "sitemap.xml", "netlify.toml", "package.json", "README.md"
)

# --- what to EXCLUDE --------------------------------------------------
# Directory names to skip entirely (any depth).
$ExcludeDirs = @(
    "node_modules", ".git", ".netlify", ".vscode", ".idea",
    "dist", "build", ".cache", "coverage", "_artifacts", ".DS_Store"
)

# Exact file names to skip.
$ExcludeNames = @(
    $OutName,                 # never include the dump itself
    "package-lock.json",      # huge + noise
    "yarn.lock", "pnpm-lock.yaml",
    "TDSR_Master_v1.txt", "TDSR_Master_v2.txt", "ZivoGift_FileIndex.txt"
)

# Skip anything bigger than this (bytes) to avoid accidental blobs.
$MaxBytes = 3MB

# --- gather files -----------------------------------------------------
Write-Host "Scanning: $Root" -ForegroundColor Cyan

$all = Get-ChildItem -LiteralPath $Root -Recurse -File -Force

$files = foreach ($f in $all) {
    # relative path with backslashes (matches your v2 format)
    $rel = $f.FullName.Substring($Root.Length).TrimStart('\','/')

    # exclude by directory segment
    $segs = $rel -split '[\\/]'
    $inBadDir = $false
    foreach ($s in $segs[0..($segs.Length-2)]) {
        if ($ExcludeDirs -contains $s) { $inBadDir = $true; break }
    }
    if ($inBadDir) { continue }

    # exclude by file name
    if ($ExcludeNames -contains $f.Name) { continue }

    # size guard
    if ($f.Length -gt $MaxBytes) {
        Write-Host "  skip (too big > $([math]::Round($MaxBytes/1MB,1))MB): $rel" -ForegroundColor DarkYellow
        continue
    }

    # include by extension OR by exact name
    $ext = $f.Extension.ToLowerInvariant()
    $keep = ($IncludeExt -contains $ext) -or ($IncludeNames -contains $f.Name)
    if (-not $keep) { continue }

    # emit an object we can sort
    [PSCustomObject]@{
        Rel  = ($rel -replace '/', '\')
        Full = $f.FullName
    }
}

# Deterministic order: sort by relative path (groups by folder).
$files = $files | Sort-Object Rel

if (-not $files -or $files.Count -eq 0) {
    Write-Warning "No matching files found under $Root. Nothing written."
    return
}

# --- build the dump ---------------------------------------------------
$sep = ('=' * 53)
$sb  = New-Object System.Text.StringBuilder

[void]$sb.AppendLine("$Title SOURCE DUMP")
[void]$sb.AppendLine("Generated: " + (Get-Date).ToString("MM/dd/yyyy HH:mm:ss"))

$count = 0
foreach ($item in $files) {
    $count++
    [void]$sb.AppendLine($sep)
    [void]$sb.AppendLine("FILE: " + $item.Rel)
    [void]$sb.AppendLine($sep)

    try {
        $content = Get-Content -LiteralPath $item.Full -Raw -ErrorAction Stop
    } catch {
        $content = "<< ERROR READING FILE: $($_.Exception.Message) >>"
    }
    if ($null -eq $content) { $content = "" }   # empty file

    [void]$sb.AppendLine($content)
    Write-Host ("  + " + $item.Rel) -ForegroundColor DarkGray
}

# --- write output (UTF-8, no BOM) ------------------------------------
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText($OutPath, $sb.ToString(), $utf8NoBom)

Write-Host ""
Write-Host "Done. $count files written to:" -ForegroundColor Green
Write-Host "  $OutPath" -ForegroundColor Green
Write-Host ("Size: {0:N0} KB" -f ([math]::Round((Get-Item $OutPath).Length / 1KB))) -ForegroundColor Green
