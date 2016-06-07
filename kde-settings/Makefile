NAME := kde-settings
SPECFILE = $(firstword $(wildcard *.spec))

MAKEFILE_COMMON := ../Makefile.common

verify-sources:
	@sha512sum --quiet -c sources-23

export NAME SPECFILE

%: force
	@$(MAKE) -f $(MAKEFILE_COMMON) $@
force: ;
