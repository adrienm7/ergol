all:
	@powershell -Command "Get-ChildItem -Recurse -Path keymaps -Include *.toml, *.yaml | ForEach-Object { kalamine build $($_.FullName) --out $($_.FullName -replace '\.toml$$|\.yaml$$', '.json') }"

watch:
	@powershell -NoExit -Command "& { \
		$watcher = New-Object System.IO.FileSystemWatcher; \
		$watcher.Path = 'keymaps'; \
		$watcher.Filter = '*.*'; \
		$watcher.IncludeSubdirectories = $true; \
		$watcher.EnableRaisingEvents = $true; \
		Register-ObjectEvent $watcher Changed -SourceIdentifier FileChanged -Action { \
			if ($_.FullPath -match '\\.toml$$|\\.yaml$$') { \
				kalamine build $($_.FullPath) --out $($_.FullPath -replace '\\.toml$$|\\.yaml$$', '.json'); \
			} \
		}; \
		Write-Host 'Watching for changes in keymaps directory. Press Ctrl+C to exit...'; \
		while ($true) { Start-Sleep -Seconds 1; } \
	}"

dev:
	pipx install kalamine

clean:
	@powershell -Command "Remove-Item -Recurse -Force dist\*"

install:
	@echo "Installer script for Windows."
	@kalamine install keymaps\ergol.toml

uninstall:
	@echo "Uninstaller script for Windows."
	@kalamine remove fr\ergol
