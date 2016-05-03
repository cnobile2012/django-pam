#
# Development by Carl J. Nobile
#
include include.mk

PREFIX		= $(shell pwd)
BASE_DIR	= $(shell echo $${PWD\#\#*/})
PACKAGE_DIR	= $(BASE_DIR)-$(VERSION)
DOCS_DIR	= $(PREFIX)/docs
TODAY		= $(shell date +"%Y-%m-%d_%H%M")

#----------------------------------------------------------------------
all	: tar

#----------------------------------------------------------------------
.PHONY	: tar
tar	: clean
	@(cd ..; tar -czvf $(PACKAGE_DIR).tar.gz --exclude=".git" \
          --exclude="example_site/static" $(BASE_DIR))

.PHONY	: coverage
coverage: clobber
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
	python setup.py sdist upload -r pypi

.PHONY	: 
upload-test: clobber
	python setup.py sdist upload -r pypitest

#----------------------------------------------------------------------

.PHONY	: clean
clean	:
	$(shell cleanDirs.sh clean)

.PHONY	: clobber
clobber	: clean
	@rm -rf dist build *.egg-info
	@rm -rf $(DOCS_DIR)/htmlcov
	@rm -rf $(DOCS_DIR)/build
