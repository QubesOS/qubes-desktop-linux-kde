install:
	install -D -m 0644 kfileplaces-bookmarks.xml $(DESTDIR)/etc/skel/.kde/share/apps/kfileplaces/bookmarks.xml
	install -D -m 0644 kickoffrc $(DESTDIR)/etc/skel/.kde/share/config/kickoffrc
	install -D -m 0644 kscreensaverrc $(DESTDIR)/etc/skel/.kde/share/config/kscreensaverrc
	install -D -m 0644 plasma-org.kde.plasma.desktop-appletsrc $(DESTDIR)/etc/skel/.config/plasma-org.kde.plasma.desktop-appletsrc
	install -D -m 0755 qubes-generate-color-palette $(DESTDIR)/usr/bin/qubes-generate-color-palette
	install -D -m 0644 qubes-generate-color-palette.desktop $(DESTDIR)/etc/xdg/autostart/qubes-generate-color-palette.desktop
	install -D -m 0644 11-qubes.js $(DESTDIR)/usr/share/plasma/shells/org.kde.plasma.desktop/contents/updates/11-qubes.js
	install -D -m 0644 qubes-systray.js $(DESTDIR)/usr/share/plasma/shells/org.kde.plasma.desktop/contents/updates/qubes-systray.js

	install -D -m 0644 applications/kde4/nepomukbackup.desktop $(DESTDIR)/usr/share/kde-settings/kde-profile/default/share/applications/kde4/nepomukbackup.desktop
	install -D -m 0644 applications/kde4/nepomukcontroller.desktop $(DESTDIR)/usr/share/kde-settings/kde-profile/default/share/applications/kde4/nepomukcontroller.desktop
	install -D -m 0644 applications/kde4/knetattach.desktop $(DESTDIR)/usr/share/kde-settings/kde-profile/default/share/applications/kde4/knetattach.desktop
	install -D -m 0644 applications/kde4/Help.desktop $(DESTDIR)/usr/share/kde-settings/kde-profile/default/share/applications/kde4/Help.desktop
	install -D -m 0644 applications/Thunar.desktop $(DESTDIR)/usr/share/kde-settings/kde-profile/default/share/applications/Thunar.desktop
	install -D -m 0644 applications/thunar-settings.desktop $(DESTDIR)/usr/share/kde-settings/kde-profile/default/share/applications/thunar-settings.desktop
	install -D -m 0644 applications/org.kde.klipper.desktop $(DESTDIR)/usr/share/kde-settings/kde-profile/default/share/applications/org.kde.klipper.desktop
	install -D -m 0644 applications/org.kde.knetattach.desktop $(DESTDIR)/usr/share/kde-settings/kde-profile/default/share/applications/org.kde.knetattach.desktop

	install -D -m 0644 autostart/nepomukcontroller.desktop $(DESTDIR)/usr/share/kde-settings/kde-profile/default/share/autostart/nepomukcontroller.desktop
	install -D -m 0644 autostart/nepomukserver.desktop $(DESTDIR)/usr/share/kde-settings/kde-profile/default/share/config/nepomukserverrc
	install -D -m 0644 autostart/org.kde.klipper.desktop $(DESTDIR)/usr/share/kde-settings/kde-profile/default/share/autostart/org.kde.klipper.desktop

	install -D -m 0644 kde4/services/kcm_nepomuk.desktop $(DESTDIR)/usr/share/kde-settings/kde-profile/default/share/kde4/services/kcm_nepomuk.desktop

	install -D -m 0644 config/klipperrc $(DESTDIR)/usr/share/kde-settings/kde-profile/default/share/config/klipperrc

	install -D -m 0644 plasmoidsetupscripts/template.js $(DESTDIR)/usr/share/plasma/look-and-feel/org.fedoraproject.fedora.desktop/contents/plasmoidsetupscripts/org.kde.plasma.kicker.js.qubes
	install -D -m 0644 plasmoidsetupscripts/template.js $(DESTDIR)/usr/share/plasma/look-and-feel/org.fedoraproject.fedora.desktop/contents/plasmoidsetupscripts/org.kde.plasma.kickerdash.js.qubes
	install -D -m 0644 plasmoidsetupscripts/template.js $(DESTDIR)/usr/share/plasma/look-and-feel/org.fedoraproject.fedora.desktop/contents/plasmoidsetupscripts/org.kde.plasma.kickoff.js.qubes

clean:
	rm -rf debian/changelog.*
	rm -rf pkgs
