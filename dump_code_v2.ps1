param(
    [string]$RepoPath = "C:\git\ZivoGift_Repo",
    [string]$OutFile  = "C:\git\ZivoGift_AllCode_v2.txt"
)

# ---- file types to collect (v2: now includes HTML/CSS/TOML/SQL) ----
$extensions = @(
    "*.html","*.htm","*.css",          # <-- NEW: were missing in v1
    "*.toml","*.sql",                  # <-- NEW: netlify.toml + supabase schema
    "*.js","*.jsx","*.ts","*.tsx","*.mjs","*.cjs",
    "*.json","*.xml","*.yml","*.yaml",
    "*.py","*.cpp","*.h","*.c","*.java","*.robot",
    "*.md","*.txt","*.sh","*.cfg","*.ini",
    ".env.example"
)

# ---- folders to skip ----
$excludeDirs = '\\(\.git|node_modules|build|dist|bin|obj|\.venv|venv|__pycache__|\.netlify|\.idea|\.vs|coverage)\\'

# ---- individual files to skip (huge + zero review value) ----
$excludeFiles = '(package-lock\.json|yarn\.lock|pnpm-lock\.yaml)$'

# ---- SAFETY: never include real secret files ----
$secretFiles = '(^\.env$|^\.env\.local$|^\.env\.production$|\.pem$|\.key$)'

if (-not (Test-Path $RepoPath)) {
    Write-Host "ERROR: Path not found -> $RepoPath" -ForegroundColor Red
    exit 1
}
$RepoPath = (Resolve-Path $RepoPath).Path

$files = Get-ChildItem -Path $RepoPath -Recurse -File -Include $extensions -ErrorAction SilentlyContinue |
         Where-Object {
            $_.FullName -notmatch $excludeDirs -and
            $_.Name     -notmatch $excludeFiles -and
            $_.Name     -notmatch $secretFiles
         } |
         Sort-Object FullName

if (-not $files -or $files.Count -eq 0) {
    Write-Host "No matching source files found under $RepoPath" -ForegroundColor Yellow
    exit 1
}

$sb = New-Object System.Text.StringBuilder
[void]$sb.AppendLine("PROJECT CODE DUMP (v2)")
[void]$sb.AppendLine("Repo    : $RepoPath")
[void]$sb.AppendLine("Created : $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')")
[void]$sb.AppendLine("Files   : $($files.Count)")
[void]$sb.AppendLine("")
[void]$sb.AppendLine("---------- FILE LIST ----------")
foreach ($f in $files) {
    [void]$sb.AppendLine($f.FullName.Substring($RepoPath.Length).TrimStart('\'))
}
[void]$sb.AppendLine("---------- END FILE LIST ----------")

foreach ($f in $files) {
    $rel = $f.FullName.Substring($RepoPath.Length).TrimStart('\')
    [void]$sb.AppendLine("")
    [void]$sb.AppendLine("===================================================")
    [void]$sb.AppendLine("===== FILE: $rel")
    [void]$sb.AppendLine("===================================================")
    try {
        [void]$sb.AppendLine((Get-Content -LiteralPath $f.FullName -Raw -ErrorAction Stop))
    } catch {
        [void]$sb.AppendLine("[could not read: $($_.Exception.Message)]")
    }
}

$sb.ToString() | Out-File -FilePath $OutFile -Encoding utf8

$sizeMB = [math]::Round((Get-Item $OutFile).Length / 1MB, 2)
Write-Host ""
Write-Host "DONE." -ForegroundColor Green
Write-Host "  Files collected : $($files.Count)"
Write-Host "  Output file     : $OutFile"
Write-Host "  Size            : $sizeMB MB"
Write-Host ""
Write-Host "Excluded: package-lock.json, node_modules, .git, .env files" -ForegroundColor DarkGray

# Quick sanity check: did HTML actually get picked up?
$htmlCount = ($files | Where-Object { $_.Extension -in '.html','.htm' }).Count
Write-Host "  HTML files      : $htmlCount" -ForegroundColor Cyan
if ($htmlCount -eq 0) {
    Write-Host "  WARNING: no HTML found - check your repo path!" -ForegroundColor Yellow
}
