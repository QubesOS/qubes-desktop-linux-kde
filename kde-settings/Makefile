NAME := kde-settings
SPECFILE = $(firstword $(wildcard *.spec))

MAKEFILE_COMMON := ../Makefile.common

verify-sources:
	@md5sum --quiet -c sources-23

export NAME SPECFILE

%: force
	@$(MAKE) -f $(MAKEFILE_COMMON) $@
force: ;
