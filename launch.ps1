./venv/Scripts/activate.ps1

# Get the current working directory
$current_dir = Get-Location

# Add the project's root directory to PYTHONPATH
$env:PYTHONPATH = "$current_dir" + ";" + $env:PYTHONPATH

python "./md_launcher/components/launcher/launch.py" "./config.json" *> $null