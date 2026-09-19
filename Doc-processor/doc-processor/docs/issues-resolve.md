The .venv was copied or moved from another directory. Windows launchers contain absolute paths, so it still points to the old location.
Rebuild it from uv.lock using the working user-level uv installation:$uv = 

$uv = "$env:APPDATA\Python\Python313\Scripts\uv.exe"

& $uv venv --clear
& $uv sync
& $uv run fastapi dev


$env:Path += ";$env:APPDATA\Python\Python313\Scripts"
uv --version


## run the fast api for dev
uv run fastapi dev
