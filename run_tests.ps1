$env:TESTING = "True"
$env:PYTHONPATH = "$env:PYTHONPATH;$(Get-Location)"
pytest $args
