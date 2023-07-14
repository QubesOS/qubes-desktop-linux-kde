/* replace the default kickoff with Qubes menu */
var panels = panels()
for (var i in panelIds) {
	var panel = panelById(panelIds[i])
	var widgetIds = panel.widgetIds
	var menuLauncherId = -1
	for (id in widgetIds) {
		var widget = panel.widgetById(widgetIds[id])
		if (widget.type == 'org.kde.plasma.kickoff') {
			var qubesMenu = panel.addWidget('org.kde.plasma.quicklaunch')
			qubesMenu.index = widget.index
			qubesMenu.currentConfigGroup = ['General']
			qubesMenu.writeConfig('launcherUrls', ['file:///usr/share/applications/open-qubes-app-menu.desktop'])
			menuLauncherId = qubesMenu.id
			widget.remove()
		} else if (widget.type == 'org.kde.plasma.quicklaunch') {
			// move existing one too, to fix after earlier broken version
			menuLauncherId = widget.id
		}
	}
	// move the menu launcher as the first applet
	if (menuLauncherId != -1) {
		panel.currentConfigGroup = ['General']
		var order = panel.readConfig("AppletOrder").split(";")
		if (!order)
			order = panel.widgetIds
		// remove from the list (likely its end) and add it at the beginning
		order = order.filter(function(x) { return x != menuLauncherId })
		order.unshift(menuLauncherId)
		panel.writeConfig("AppletOrder", order.join(";"))
	}
}

/* wallpaper */
var desktop = desktops()[0];
desktop.wallpaperPlugin = "org.kde.image"
desktop.currentConfigGroup = Array('Wallpaper', 'org.kde.image', "General");
desktop.writeConfig('Image', 'file:///usr/share/wallpapers/Qubes_Steel');
