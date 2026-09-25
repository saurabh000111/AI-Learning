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


#############====== python env setup

# Delete the old environment
Remove-Item -LiteralPath .venv -Recurse -Force


# Create a new environment
py -3.13 -m venv .venv

# Activate it
.\.venv\Scripts\Activate.ps1

# Install dependencies
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# Start FastAPI without uv
python -m uvicorn doc_processor.main:app --reload --app-dir src