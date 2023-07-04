/* replace the default kickoff with Qubes menu */
var panels = panels()
for (var i in panelIds) {
	var panel = panelById(panelIds[i])
	var widgetIds = panel.widgetIds
	for (id in widgetIds) {
		var widget = panel.widgetById(widgetIds[id])
		if (widget.type == 'org.kde.plasma.kickoff') {
			var qubesMenu = panel.addWidget('org.kde.plasma.quicklaunch')
			qubesMenu.index = widget.index
			qubesMenu.currentConfigGroup = ['General']
			qubesMenu.writeConfig('launcherUrls', ['file:///usr/share/applications/open-qubes-app-menu.desktop'])
			widget.remove()
		}
	}
}

/* wallpaper */
var desktop = desktops()[0];
desktop.wallpaperPlugin = "org.kde.image"
desktop.currentConfigGroup = Array('Wallpaper', 'org.kde.image', "General");
desktop.writeConfig('Image', 'file:///usr/share/wallpapers/Qubes_Steel');
