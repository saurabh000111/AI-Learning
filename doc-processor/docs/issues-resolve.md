.venv\Scripts\activate.ps1

pip install -r requirements.txt

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




# python venv setup
## Deactivate the current environment and delete the folder:
deactivate
Remove-Item -Recurse -Force .venv

## Run the venv command again, but this time add the prompt flag:
python -m venv --prompt doc-processor .venv

## Activate it normally. Your terminal will now show (doc-processor) again.
.\.venv\Scripts\activate


## to run test 
uv run python tests/test_password.py

## to print folder structure
tree src /F