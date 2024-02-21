# -*- coding: utf-8 -*-

help: ## ** Show this help message
	@perl -nle'print $& if m{^[a-zA-Z_-]+:.*?## .*$$}' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-40s\033[0m %s\n", $$1, $$2}'


build-wf: ## ** Build Alfred Workflow release from source code
	python ./bin/s01_build_wf.py


refresh-code: ## ** Refresh Alfred Workflow source code
	python ./bin/s02_refresh_code.py
