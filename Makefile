EXODUS_VERSION ?=
DATE=$(shell LC_ALL=C date "+%a %b %d %Y")
GIT_EMAIL=$(shell git config user.email)
GIT_USERNAME=$(shell git config user.name)

.PHONY: help build download version_update commit
.DEFAULT_GOAL := help

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[0-9a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

build: ## Build RPM package
	@cp exodus.svg ~/rpmbuild/SOURCES/
	@cp exodus-linux-x64-$(EXODUS_VERSION).zip ~/rpmbuild/SOURCES/
	@rpmbuild -ba exodus.spec

download: ## Download Exodus release zip
	@curl -sL -o "exodus-linux-x64-$(EXODUS_VERSION).zip" \
		"https://downloads.exodus.com/releases/exodus-linux-x64-$(EXODUS_VERSION).zip"

version_update: ## Update Exodus version in exodus.spec
	@awk --include=inplace \
	  -v version="$(EXODUS_VERSION)" \
	  -v date="$(DATE)" \
	  -v git_email="$(GIT_EMAIL)" \
	  -v git_username="$(GIT_USERNAME)" \
	  -f update_specfile.awk exodus.spec

commit: ## Commit spec update to git (create version_update branch)
	git checkout -B version_update
	git add exodus.spec
	git commit -m "Update Exodus to version $(EXODUS_VERSION)"
