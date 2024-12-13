repo ?= adamwalford
app ?= office-lights
version ?= $$(cat ./src/${app}/VERSION)

.PHONY: build
build:
	docker build ./src/${app} -t ${repo}/${app}:${version}

.PHONY: push
push:
	docker push ${repo}/${app}:${version}

.PHONY: deploy-home
deploy-home:
	helm upgrade --install ./.deploy/home
