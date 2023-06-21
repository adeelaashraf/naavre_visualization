# Makefile

update_env:
	@echo "Updating version in .env and package.json"
	@version=$$(date +'%Y.%m.%d'); \
	echo "APP_VERSION=$$version" > .env; \
	node -e "const fs = require('fs'); \
	const packageJson = JSON.parse(fs.readFileSync('package.json')); \
	packageJson.version = '$$version'; \
	fs.writeFileSync('package.json', JSON.stringify(packageJson, null, 2));"

run_python:
	python3 python_scripts/input_to_json.py

update_version: update_env run_python