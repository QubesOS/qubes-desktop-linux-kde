default: help
SUBDIRS := kde-filesystem kde-settings kdelibs kdebase-workspace kdebase-runtime kdebase oxygen-icon-theme kdemultimedia qubes-kde-dom0

.PHONY: verify-sources get-sources clean-sources clean

# TODO: there should really be a more elegant way for coding this
# instead od repeating the for loop in each target... Anybody?

all: get-sources verify-sources prep rpms srpms

verify-sources:
	@for dir in $(SUBDIRS); do \
		$(MAKE) -s -C $$dir verify-sources || exit 1;\
	done

get-sources:
	@for dir in $(SUBDIRS); do \
		$(MAKE) -s -C $$dir get-sources || exit 1;\
	done

clean-sources:
	@for dir in $(SUBDIRS); do \
		$(MAKE) -s -C $$dir rm-sources || exit 1;\
	done

# Even though we're serializing the builds here, I don't think we're losing
# any CPU on multi cores, because the build process should still be using
# as many cores as are available (-j). Hopefully... -- joanna
#
# Ok, one problem is with the kdebase-workspace package that
# cannot be built with SMP flag -- most likely a bug  in dependencies -- joanna

prep: get-sources
	@for dir in $(SUBDIRS); do \
		$(MAKE) -C $$dir prep || exit 1;\
	done

rpms: get-sources
	@for dir in $(SUBDIRS); do \
		$(MAKE) -C $$dir rpms || exit 1;\
	done
	rpm --addsign rpm/*/*.rpm

srpms: get-sources
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
	-rm -fr rpm/* srpm/*

update-repo:
	ln -f rpm/x86_64/*.rpm ../yum/r1/dom0/rpm/
	ln -f rpm/noarch/kde-filesystem-*.rpm ../yum/r1/dom0/rpm/
	ln -f rpm/noarch/kde-settings-*.rpm ../yum/r1/dom0/rpm/
	ln -f rpm/noarch/qubes-kde-dom0-*.rpm ../yum/r1/dom0/rpm/

update-repo-testing:
	ln -f rpm/x86_64/*.rpm ../yum/r1-testing/dom0/rpm/
	ln -f rpm/noarch/kde-filesystem-*.rpm ../yum/r1-testing/dom0/rpm/
	ln -f rpm/noarch/kde-settings-*.rpm ../yum/r1-testing/dom0/rpm/
	ln -f rpm/noarch/qubes-kde-dom0-*.rpm ../yum/r1-testing/dom0/rpm/



help:
	@echo "Usage: make <target>"
	@echo
	@echo "get-sources     Download all the KDE sources"
	@echo "verify-sources  Verify the KDE sources tarballs"
	@echo "prep            Prep all rpms (useful for checking build requirements)"
	@echo "rpms            Build all rpms"
	@echo "srpms           Create all srpms"
	@echo "all             get-sources verify-sources rpms srpms"
	@echo
	@echo "update-repo     copy newly generated rpms to qubes yum repo"
	@echo "update-repo-testing -- same, but to -testing repo"
	@echo

