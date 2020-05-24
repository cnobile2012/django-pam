#
# Development by Carl J. Nobile
#
include include.mk

PREFIX		= $(shell pwd)
BASE_DIR	= $(shell echo $${PWD\#\#*/})
TEST_TAG	=
PACKAGE_DIR	= $(BASE_DIR)-$(VERSION)$(TEST_TAG)
DOCS_DIR	= $(PREFIX)/docs
TODAY		= $(shell date +"%Y-%m-%d_%H%M")
RM_REGEX	= '(^.*.pyc$$)|(^.*.wsgic$$)|(^.*~$$)|(.*\#$$)|(^.*,cover$$)'
RM_CMD		= find $(PREFIX) -regextype posix-egrep -regex $(RM_REGEX) \
                  -exec rm {} \;
PIP_ARGS	=

#----------------------------------------------------------------------
all	: tar

#----------------------------------------------------------------------
.PHONY	: tar
tar	: clean
	@(cd ..; tar -czvf $(PACKAGE_DIR).tar.gz --exclude=".git" \
          --exclude="example_site/static" $(BASE_DIR))

.PHONY	: tests
tests	: clobber
	coverage erase
	coverage run ./manage.py test
	coverage report
	coverage html

.PHONY	: sphinx
sphinx	: clean
	(cd $(DOCS_DIR); make html)

.PHONY	: build
build	: clean
	python setup.py sdist

.PHONY	: upload
upload	: clobber
	python setup.py sdist
	python setup.py bdist_wheel --universal
	twine upload --repository pypi dist/*

.PHONY	: upload-test
# To add a pre-release candidate such as 'rc0' to a test package name because
# pypi doesn't allow more than one package with a given name do this:
#
# make upload-test TEST_TAG=rc1
#
# The tagball would then be names django-pam-2.0.0rc1.tar.gz
#
upload-test: clobber
	python setup.py sdist -- $(TEST_TAG)
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
