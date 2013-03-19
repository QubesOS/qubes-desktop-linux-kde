ifeq ($(PACKAGE_SET),dom0)
RPM_SPEC_FILES := kde-baseapps/kde-baseapps.spec \
		kde-settings/kde-settings.spec \
		plastik-for-qubes/kde-style-plastik-for-qubes.spec \
		qubes-kde-dom0/qubes-kde-dom0.spec \
		qubes-menus/qubes-menus.spec
endif
