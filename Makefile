default: help

VERSION := $(shell cat version)
REL := $(shell cat rel)

SUBDIRS_STAGE1 := kde-filesystem
SUBDIRS_STAGE2 := kde-settings kdelibs
SUBDIRS_STAGE3 := kdebase-workspace kdebase-runtime kdebase oxygen-icon-theme qubes-kde-dom0 qubes-menus
SUBDIRS_STAGE4 := kdemultimedia
SUBDIRS:= $(SUBDIRS_STAGE1) $(SUBDIRS_STAGE2) $(SUBDIRS_STAGE3) $(SUBDIRS_STAGE4)

.PHONY: verify-sources get-sources clean-sources clean

all: get-sources verify-sources prep rpms srpms

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

prep%:
	@for dir in $($(subst prep,SUBDIRS_STAGE,$@)); do \
		$(MAKE) -C $$dir prep || exit 1;\
	done

prep: get-sources verify-sources prep1 prep2 prep3 prep4

rpms_stage_completed%:
	@for dir in $($(subst rpms_stage_completed,SUBDIRS_STAGE,$@)); do \
		$(MAKE) -C $$dir rpms || exit 1;\
	done
	@touch $@

rpms: get-sources verify-sources rpms_stage_completed1 rpms_stage_completed2 rpms_stage_completed3 rpms_stage_completed4
	rpm --addsign rpm/*/*$(VERSION)-$(REL)*.rpm

srpms: get-sources
	@for dir in $(SUBDIRS); do \
		$(MAKE) -s -C $$dir srpm || exit 1;\
	done

clean:
	-@for dir in $(SUBDIRS); do \
		$(MAKE) -C $$dir clean ;\
	done
	-rm -f rpms_stage_completed*

mrproper: clean
	-@for dir in $(SUBDIRS); do \
		$(MAKE) -C $$dir clean-sources ;\
	done
	-rm -fr rpm/* srpm/*

update-repo:
	ln -f rpm/x86_64/*$(VERSION)*.rpm ../yum/r1/dom0/rpm/
	ln -f rpm/noarch/kde-filesystem-*$(VERSION)*.rpm ../yum/r1/dom0/rpm/
	ln -f rpm/noarch/kde-settings-*$(VERSION)*.rpm ../yum/r1/dom0/rpm/
	ln -f rpm/noarch/kdebase-runtime-flags-*$(VERSION)*.rpm ../yum/r1/dom0/rpm/
	ln -f rpm/noarch/qubes-kde-dom0-*$(VERSION)*.rpm ../yum/r1/dom0/rpm/
	ln -f rpm/noarch/qubes-menus-*.rpm ../yum/r1/dom0/rpm/

update-repo-testing:
	ln -f rpm/x86_64/*$(VERSION)*.rpm ../yum/r1-testing/dom0/rpm/
	ln -f rpm/noarch/kde-filesystem-*$(VERSION)*.rpm ../yum/r1-testing/dom0/rpm/
	ln -f rpm/noarch/kde-settings-*$(VERSION)*.rpm ../yum/r1-testing/dom0/rpm/
	ln -f rpm/noarch/kdebase-runtime-flags-*$(VERSION)*.rpm ../yum/r1-testing/dom0/rpm/
	ln -f rpm/noarch/qubes-kde-dom0-*$(VERSION)*.rpm ../yum/r1-testing/dom0/rpm/
	ln -f rpm/noarch/qubes-menus-*.rpm ../yum/r1-testing/dom0/rpm/

update-repo-installer:
	ln -f rpm/x86_64/*$(VERSION)*.rpm ../installer/yum/qubes-dom0/rpm/
	ln -f rpm/noarch/kde-filesystem-*$(VERSION)*.rpm ../installer/yum/qubes-dom0/rpm/
	ln -f rpm/noarch/kde-settings-*$(VERSION)*.rpm  ../installer/yum/qubes-dom0/rpm/
	ln -f rpm/noarch/kdebase-runtime-flags-*$(VERSION)*.rpm   ../installer/yum/qubes-dom0/rpm/
	ln -f rpm/noarch/qubes-kde-dom0-*$(VERSION)*.rpm   ../installer/yum/qubes-dom0/rpm/
	ln -f rpm/noarch/qubes-menus-*.rpm   ../installer/yum/qubes-dom0/rpm/
	ln -f rpm/noarch/oxygen-icon-theme-*$(VERSION)*.rpm   ../installer/yum/qubes-dom0/rpm/

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


	@echo

