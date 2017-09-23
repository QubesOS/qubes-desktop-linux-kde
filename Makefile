default: help

SUBDIRS:= kde-baseapps kde-settings qubes-kde-dom0

.PHONY: verify-sources get-sources clean-sources clean

all: get-sources verify-sources rpms

verify-sources get-sources clean-sources:
	@for dir in $(SUBDIRS); do \
		$(MAKE) -s -C $$dir $@ || exit 1;\
	done

# Even though we're serializing the builds here, I don't think we're losing
# any CPU on multi cores, because the build process should still be using
# as many cores as are available (-j). Hopefully... -- joanna
#
# Ok, one problem is with the kdebase-workspace package that
# cannot be built with SMP flag -- most likely a bug  in dependencies -- joanna

rpms: get-sources verify-sources
	@for dir in $(SUBDIRS); do \
		$(MAKE) -C $$dir rpms || exit 1;\
	done

srpms: get-sources verify-sources
	@for dir in $(SUBDIRS); do \
		$(MAKE) -s -C $$dir srpm || exit 1;\
	done

clean:
	-@for dir in $(SUBDIRS); do \
		$(MAKE) -C $$dir clean ;\
	done

mrproper: clean
	-@for dir in $(SUBDIRS); do \
		$(MAKE) -C $$dir clean-sources ;\
	done
	-rm -fr rpm/* srpm/* pkgs/*

update-repo-%:
	@for dir in $(SUBDIRS); do \
	    $(MAKE) -s -C $$dir $@ || exit 1;\
	done

help:
	@echo "Usage: make <target>"
	@echo
	@echo "get-sources     Download all the KDE sources"
	@echo "verify-sources  Verify the KDE sources tarballs"
	@echo "rpms            Build all rpms"
	@echo "srpms           Create all srpms"
	@echo "all             get-sources verify-sources rpms srpms"
	@echo


	@echo

