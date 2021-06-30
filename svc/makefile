# Makefile used for building and pushing docker images to dockerhub 
###
### Settings commom for all docker images and services
### 
USER = nicklasxyz
IMAGE_VERSION = latest

###
### Directories specific to certain services
###
# Directory containing dependencies and a dockerfile for 
# creating a base image used by the landingpage
LANDINGPAGE_DEPENDENCIES_DIR = static/landingpage
LANDINGPAGE_DEPENDENCIES_NAME = landingpage-dep
# Base image tag
LANDINGPAGE_DEPENDENCIES_TAG = $(USER)/$(LANDINGPAGE_DEPENDENCIES_NAME):$(IMAGE_VERSION)

# Directory containing files for the 'nxyz-landingpage'
LANDINGPAGE_SVC_DIR = static/landingpage
LANDINGPAGE_SVC_NAME = nxyz-landingpage
# Specify the 'nxyz-landingpage' image tag
LANDINGPAGE_SVC_TAG = $(USER)/$(LANDINGPAGE_SVC_NAME):$(IMAGE_VERSION)

# Build landingpage base image
build-landingpage-dep:
	$(eval $@_DIR := $(LANDINGPAGE_DEPENDENCIES_DIR))
	$(eval $@_TAG := $(LANDINGPAGE_DEPENDENCIES_TAG))
	@echo ""; echo "--> Compiling files and building Docker image. Running target: '$@'"
	$(eval $@_TMP := $(shell mktemp -d))
	@echo ""; echo "--> Creating temporary build directory '$($@_TMP)'"
	@echo ""; echo "--> Copying files in directory '$($@_DIR)' to directory '$($@_TMP)'"
	cp -r $($@_DIR)/* $($@_TMP)
	ls -la $($@_TMP)
	@echo ""; echo "--> Building docker image: '$($@_TAG)'"
	sudo docker build --file $($@_TMP)/Dockerfile.base --tag $($@_TAG) $($@_TMP)
	@echo ""; echo "--> Removing temporary directory '$($@_TMP)/*'"
	rm -rf $($@_TMP)

# Production build: landingpage
build-nxyz-landingpage:
	$(eval $@_SVC := $(LANDINGPAGE_SVC_DIR))
	$(eval $@_TAG := $(LANDINGPAGE_SVC_TAG))
	@echo ""; echo "--> Compiling files and building Docker image. Running target: '$@'"
	$(eval $@_TMP := $(shell mktemp -d))
	@echo ""; echo "--> Creating temporary build directory '$($@_TMP)'"
	@echo ""; echo "--> Copying all files in directory '$($@_SVC)' to directory '$($@_TMP)'"
	cp -r $($@_SVC)/* $($@_TMP)
	ls -la $($@_TMP)
	@echo ""; echo "--> Building docker image: '$($@_TAG)'"
	sudo docker build --file $($@_TMP)/Dockerfile.prod --tag $($@_TAG) $($@_TMP)
	@echo ""; echo "--> Removing temporary directory '$($@_TMP)/*'"
	rm -rf $($@_TMP)

build-all: build-landingpage-dep build-nxyz-landingpage

push-nxyz-landingpage:
	$(eval $@_TAG := $(LANDINGPAGE_SVC_TAG))
	@echo ""; echo "--> Pushing docker image: '$($@_TAG)'"
	sudo docker push $($@_TAG)

push-all: push-nxyz-landingpage
