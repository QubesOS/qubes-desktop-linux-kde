var biggestId = 0;
var tmpBiggestId = 0;

for (var i in activityIds) {
    var activity = activityById(activityIds[i]);
    if (activity.widgetIds.length > 0) {
        tmpBiggestId = Math.max.apply(null, activity.widgetIds);
        if (tmpBiggestId > biggestId) {
            biggestId = tmpBiggestId;
        }
    }
}

for (var i in panelIds) {
    var panel = panelById(panelIds[i]);
    if (panel.widgetIds.length > 0) {
        tmpBiggestId = Math.max.apply(null, panel.widgetIds);
        if (tmpBiggestId > biggestId) {
            biggestId = tmpBiggestId;
        }
    }
}

for (var i in panelIds) {
    var panel = panelById(panelIds[i]);
    for (var j in panel.widgetIds) {
        var widget = panel.widgetById(panel.widgetIds[j]);
        if (widget.type == "systemtray") {
	    widget.writeConfig('DefaultAppletsAdded', 'true')
            widget.currentConfigGroup = new Array('Applets', biggestId+1);
            widget.writeConfig('plugin', 'notifications');
            widget.currentConfigGroup = new Array('Applets', biggestId+2);
            widget.writeConfig('plugin', 'battery');
            widget.reloadConfig();
        }
    }
}
