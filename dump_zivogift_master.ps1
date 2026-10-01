$RepoRoot = "C:\git\ZivoGift_Repo"
$OutputFile = Join-Path $RepoRoot "ZIVO_Master_v1.txt"

if (Test-Path $OutputFile) {
    Remove-Item $OutputFile -Force
}

$IncludeExtensions = @(
    ".html",
    ".css",
    ".js",
    ".json",
    ".sql",
    ".md",
    ".toml",
    ".yml",
    ".yaml"
)

$ExcludeFolders = @(
    "node_modules",
    ".git",
    "dist",
    "build",
    ".netlify",
    "coverage"
)

$Files = Get-ChildItem $RepoRoot -Recurse -File | Where-Object {

    $extOk = $IncludeExtensions -contains $_.Extension.ToLower()

    $folderOk = $true

    foreach ($folder in $ExcludeFolders) {
        if ($_.FullName -like "*\$folder\*") {
            $folderOk = $false
            break
        }
    }

    $extOk -and $folderOk
}

"ZIVOGIFT MASTER SOURCE DUMP" | Out-File $OutputFile -Encoding utf8
"Generated: $(Get-Date)" | Add-Content $OutputFile
"" | Add-Content $OutputFile

foreach ($file in $Files) {

    $relativePath = $file.FullName.Substring($RepoRoot.Length + 1)

    Add-Content $OutputFile ""
    Add-Content $OutputFile "====================================================="
    Add-Content $OutputFile "FILE: $relativePath"
    Add-Content $OutputFile "====================================================="
    Add-Content $OutputFile ""

    try {
        Get-Content $file.FullName -Raw -Encoding UTF8 | Add-Content $OutputFile
    }
    catch {
        Add-Content $OutputFile "ERROR READING FILE"
    }

    Add-Content $OutputFile ""
}

Write-Host ""
Write-Host "SUCCESS"
Write-Host "Created:"
Write-Host $OutputFile