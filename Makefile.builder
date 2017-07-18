RPM_SPEC_FILES.dom0 = \
    kde-baseapps/kde-baseapps.spec \
    kde-settings/kde-settings.spec \
    qubes-kde-dom0/qubes-kde-dom0.spec

ifeq ($(shell expr $(subst fc,,$(DIST)) \<= 22),1)
    RPM_SPEC_FILES.dom0 += plastik-for-qubes/kde-style-plastik-for-qubes.spec
else
    RPM_SPEC_FILES.dom0 += plasma-breeze-qubes/plasma-breeze-qubes.spec
endif

RPM_SPEC_FILES := $(RPM_SPEC_FILES.$(PACKAGE_SET))
