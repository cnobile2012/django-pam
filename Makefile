#
# Development by Carl J. Nobile
#
include include.mk

TODAY		= $(shell date +"%Y-%m-%dT%H:%M:%S.%N%:z")
PREFIX		= $(shell pwd)
BASE_DIR	= $(shell basename $(PREFIX))
TEST_TAG	=
PACKAGE_DIR	= $(BASE_DIR)-$(VERSION)$(TEST_TAG)
DOCS_DIR	= $(PREFIX)/docs
RM_REGEX	= '(^.*.pyc$$)|(^.*.wsgic$$)|(^.*~$$)|(.*\#$$)|(^.*,cover$$)'
RM_CMD		= find $(PREFIX) -regextype posix-egrep -regex $(RM_REGEX) \
                  -exec rm {} \;
PIP_ARGS	= # Pass variables for pip install.
TEST_PATH	= # The path to run tests on.

#----------------------------------------------------------------------
all	: help

#----------------------------------------------------------------------
.PHONY: help
help    :
        @LC_ALL=C $(MAKE) -pRrq -f $(firstword $(MAKEFILE_LIST)) : \
                2>/dev/null | awk -v RS= \
                -F: '/(^|\n)# Files(\n|$$)/,/(^|\n)# Finished Make data \
                     base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | grep \
                -E -v -e '^[^[:alnum:]]' -e '^$@$$'

.PHONY	: tar
tar	: clobber
	@(cd ..; tar -czvf $(PACKAGE_DIR).tar.gz --exclude=".git" \
          --exclude="__pycache__" --exclude="example_site/static" $(BASE_DIR))

# Run all tests
# $ make tests
#
# Run all tests in a specific test file.
# $ make tests TEST_PATH=tests.test_bases.py
#
# Run all tests in a specific test file and class.
# $ make tests TEST_PATH=tests.test_bases.py.TestBases
#
# Run just one test in a specific test file and class.
# $ make tests TEST_PATH=tests.test_bases.py.TestBases.test_version
.PHONY	: tests
tests	: clobber
	@$(VIRTUAL_ENV)/bin/coverage erase
	@$(VIRTUAL_ENV)/bin/coverage run ./manage.py test $(TEST_PATH)
	@$(VIRTUAL_ENV)/bin/coverage report
	@$(VIRTUAL_ENV)/bin/coverage html
	@echo $(TODAY)

.PHONY	: flake8
flake8	:
#       Error on syntax errors or undefined names.
	flake8 . --select=E9,F7,F63,F82 --show-source
#       Warn on everything else.
	flake8 . --exit-zero

.PHONY	: sphinx
sphinx	: clean
	(cd $(DOCS_DIR); make html)

# To add a pre-release candidate such as 'rc1' to a test package name an
# environment variable needs to be set that setup.py can read.
#
# make build TEST_TAG=rc1
# make upload-test TEST_TAG=rc1
#
# The tarball would then be named dcolumn-2.0.0rc1.tar.gz
#
.PHONY	: build
build	: export PR_TAG=$(TEST_TAG)
build	: clean
	python setup.py sdist

# https://pypi.org
.PHONY	: upload
upload	: clobber
	python setup.py sdist
	python setup.py bdist_wheel --universal
	twine upload --repository pypi dist/*

# https://test.pypi.org
.PHONY	: upload-test
upload-test: clobber build
	python setup.py bdist_wheel --universal
	twine upload --repository testpypi dist/*

.PHONY  : install-dev
install-dev:
	pip install $(PIP_ARGS) -r requirements/development.txt

#----------------------------------------------------------------------

.PHONY	: clean
clean	:
	$(shell $(RM_CMD))

.PHONY	: clobber
clobber	: clean
	@rm -rf dist build *.egg-info
	@rm -rf $(DOCS_DIR)/htmlcov
	@rm -rf $(DOCS_DIR)/build
