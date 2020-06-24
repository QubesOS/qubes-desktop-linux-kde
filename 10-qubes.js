var panels = panels()
for (var i in panelIds) {
	var panel = panelById(panelIds[i])
	var widgetIds = panel.widgetIds
	for (id in widgetIds) {
		var widget = panel.widgetById(widgetIds[id])
		if (widget.type == 'launcher') {
			var simpleMenu = panel.addWidget('simplelauncher')
			simpleMenu.index = widget.index + 1
			simpleMenu.writeConfig('icon', 'start-here-qubes')
			widget.remove()
		}
	}
}

/* wallpaper */
var activity = activities()[0];
activity.currentConfigGroup = new Array('Wallpaper', 'image');
activity.writeConfig('wallpaper', '/usr/share/wallpapers/Qubes_Steel');
activity.writeConfig('wallpaperposition', '2');
