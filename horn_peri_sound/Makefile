ifeq ($(USE_VLAB_VERSION),)
USE_VLAB_VERSION:=2.8
else ifeq ($(filter 2.8 2.9 3,$(USE_VLAB_VERSION)),)
$(error Error: Use proper USE_VLAB_VERSION=[2.8(default), 2.9, 3])
endif
export USE_VLAB_VERSION

# If running Conan, specify SW_MODULE_NAME and SW_MODEL_FILE
ifneq ($(filter build package update-lock,$(MAKECMDGOALS)),)
ifeq ($(SW_MODULE_NAME),)
$(error Set SW_MODULE_NAME and SW_MODEL_FILE)
endif
ifeq ($(SW_MODEL_FILE),)
$(error Set SW_MODULE_NAME and SW_MODEL_FILE)
endif
endif
ifeq ($(MAKECMDGOALS),)
ifeq ($(SW_MODULE_NAME),)
$(error Set SW_MODULE_NAME and SW_MODEL_FILE)
endif
ifeq ($(SW_MODEL_FILE),)
$(error Set SW_MODULE_NAME and SW_MODEL_FILE)
endif
endif

DEFAULT_CONAN_HOST_PROFILE := ubuntu-20.04-ghs-2022.1.4-rh850g4mh
DEFAULT_CONAN_BUILD_PROFILE := ubuntu-20.04-gcc-9.4

BUILD_TYPE ?= Release

CONAN_HOST_PROFILE ?= $(DEFAULT_CONAN_HOST_PROFILE)
CONAN_BUILD_PROFILE ?= $(DEFAULT_CONAN_BUILD_PROFILE)
CONAN_FLAGS += -pr:h $(CONAN_HOST_PROFILE) -pr:b $(CONAN_BUILD_PROFILE)
CONAN_FLAGS += \
	-o fnv4-veds/*:sw_modules=$(SW_MODULE_NAME) \
	-o fnv4-veds/*:sw_components=$(SW_COMPONENTS) \
	-o fnv4-veds/*:sw_model_file=$(SW_MODEL_FILE)
CONAN_FLAGS += --lockfile-partial

# Enable verbose output using `VERBOSE=1`
ifeq ($(VERBOSE),1)
export VERBOSE = 1
NINJA_FLAGS += -v
else
.SILENT:
endif

# Use latest version from remotes by default. Set UPDATE=0 to use the local cache.
ifneq ($(UPDATE),0)
CONAN_FLAGS += --update
endif

# Enable local conan cache directory for the test framework
ifeq ($(LOCAL_CONAN),1)
export CONAN_HOME=${CURDIR}/.conan2_local/.conan2
endif

.PHONY: all
all: configure build

.PHONY: configure
configure:
	poetry install
	poetry run conan config install git@github.ford.com:FNV4-FordOS/Zonal_Conan2_Config.git

.PHONY: build
build:
	poetry run conan install . --build=missing -s build_type=$(BUILD_TYPE) $(CONAN_FLAGS)

.PHONY: test
test:
	(. build/$(BUILD_TYPE)/generators/conanbuild.sh && run-ut-sim-docker build/$(BUILD_TYPE) ./scripts/run-rh850-sim $(BUILD_TYPE) '$(TEST_FILTER)' '$(COVERAGE)')

.PHONY: test-ide
test-ide:
	(. build/$(BUILD_TYPE)/generators/conanbuild.sh && run-ut-sim-docker build/$(BUILD_TYPE) ./scripts/run-rh850-sim $(BUILD_TYPE)-ide '$(TEST_FILTER)' '$(COVERAGE)')
.PHONY: run_tgt_docker
run_tgt_docker:
	(. build/$(BUILD_TYPE)/generators/conanbuild.sh && run-ut-sim-docker)
	
.PHONY: conan.lock update-lock
conan.lock update-lock:
	rm -f conan.lock && poetry run conan lock create . --update --build=missing -s build_type=$(BUILD_TYPE) $(CONAN_FLAGS)
	
.PHONY: clean
clean:
	rm -rf build
	rm -rf .conan2_local
	rm -rf scripts/coverage
clean_coverage:
	rm -rf scripts/coverage	
