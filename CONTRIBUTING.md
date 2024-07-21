# Contributing to Binary
## Development
Binary is developed using GTK4, Libadwaita and Python3 using PyGObject. I recommend using [GNOME Builder from Flathub](https://flathub.org/apps/org.gnome.Builder) for development, as it automatically manages building Binary, testing it in a Flatpak and contains the runtimes and build dependencies needed.

Every time a new string is added, it's recommended to run the update_translations.sh script. This automatically updates potfiles to accomodate for new strings, as well as for other ones moving on to different lines of code. Credit to Gregor Niehl and TheEvilSkeleton for this script.

**Note:** the version in the Builder runtime terminal does not properly detect the translate="no" property, you should use meson on your host system or using a container instead.

## Translations
<a href="https://hosted.weblate.org/engage/binary/">
<img src="https://hosted.weblate.org/widget/binary/287x66-black.png" alt="Translation status" />
</a>

Binary uses [Weblate](https://hosted.weblate.org/engage/binary/) for translations, which provides a graphical UI for translations without needing to manually edit code. If unsure, use that as it's generally easier for everyone. More experienced users who prefer to do so can also manually edit potfiles, but please be mindful of other people's work when doing this.

Remember to add your name as a translation to "translator-credits" in main.py for credit!
