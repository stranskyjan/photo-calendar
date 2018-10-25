######################################################################
# Makefile for PhotoCalendar project
# Run 'make help' for more info
######################################################################

######################################################################
# settable variables
######################################################################
PYTHON=python
PREFIX=
USER=
SPHINX_BUILD_COMMAND=sphinx-build
SPHINX_BUILD_DIR=build/doc

######################################################################
# auxiliary functions and variables
######################################################################
define run_example
	@echo $1
	@cd $1 
	@echo "  python"
	$(PYTHON) $1.py
	@echo "  shell"
	sh $1.sh
	@cd ..
endef

_PYTHON_HELP="    PYTHON ... sets python executable (e.g. PYTHON='python3'). Defaults is 'python'"
INSTALLCMD=$(PYTHON) setup.py install

######################################################################
# targets
######################################################################
.PHONY: doc examples

help:
	@echo
	@echo "PhotoCalendar makefile"
	@echo
	@echo "targets:"
	@echo "  install"
	@echo "    runs 'python setup.py install' to installs the application"
	@echo "    options:"
	@echo "    USER=1 ... adds '--user' switch to the install command"
	@echo "    PREFIX=/your/prefix ... adds '--prefix=/your/prefix' to the install commands"
	@echo $(_PYTHON_HELP)
	@echo "  test"
	@echo "    run tests"
	@echo $(_PYTHON_HELP)
	@echo "  doc"
	@echo "    create Sphinx HTML documentation"
	@echo "    options:"
	@echo "      SPHINX_BUILD_COMMAND ... sphinx build command (default is 'sphinx-build')"
	@echo "      SPHINX_BUILD_DIR     ... target directory (default is 'build/doc')"
	@echo "  examples"
	@echo "    buld all examples (takes some time)"
	@echo "  clean"
	@echo "    cleans intermediate and auxiliary files"
	@echo "  dist"
	@echo "    creates distribution for PyPI by 'pythonX setup.py sdist bdist_wheel' command"


install:
ifneq ($(USER),)
	$(INSTALLCMD) --user
else ifneq ($(PREFIX),)
	$(INSTALLCMD) --prefix $(PREFIX)
else
	$(INSTALLCMD)
endif


test:
	$(PYTHON) tests


doc:
	$(SPHINX_BUILD_COMMAND) -b html -a -E doc $(SPHINX_BUILD_DIR)/html


.ONESHELL:
examples:
	@cd examples
	$(call run_example, example1)
	$(call run_example, custom-template)
	$(call run_example, templates)


clean:
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
	find . -type f -name '*.pyc' -delete
	find . -type d -name __pycache__ -delete


dist:
	make clean
	python2 setup.py sdist bdist_wheel
	python3 setup.py sdist bdist_wheel
