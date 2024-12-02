(function() {
    if (applet.readConfig("icon", "start-here-kde") == "start-here-kde" ||
        applet.readConfig("icon", "start-here-kde") == "start-here") {
        applet.currentConfigGroup = ["General"];
        applet.writeConfig("icon", "qubes-logo-icon");
    }
})();
