# Qubes KDE Plasma Integration

This component makes the KDE Plasma desktop fit for use as the GUI domain of
[Qubes OS](https://www.qubes-os.org). It ships the KDE settings, menu and theme
tweaks that let Plasma host windows from many separate qubes and keep them
visually apart.

Its main pieces:

- **Colored window frames** (the `plasma-breeze-qubes` theme). Each qube has a
  label color, and `qubes-generate-color-palette` turns those labels into Breeze
  window-decoration color schemes, so a window's title bar shows the color of the
  qube it belongs to.
- **Qubes application menu** in place of the default Kickoff launcher, plus the
  matching panel layout, system tray and wallpaper.
- Default Plasma config for a fresh GUI-domain profile.

For how to install and use KDE as your Qubes desktop, see the
[KDE page in the Qubes OS docs](https://www.qubes-os.org/doc/kde/).
