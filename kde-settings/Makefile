NAME := kde-settings
SPECFILE = $(firstword $(wildcard *.spec))

MAKEFILE_COMMON := ../Makefile.common

include $(MAKEFILE_COMMON)

verify-sources:
	@md5sum --quiet -c sources-4.9
