# beetime 

**This is a fork, not ready for use!**

# Description
This add-on connects Anki to your Beeminder graphs.  Currently it supports syncing your time spent reviewing, number of cards reviewed and/or number of cards/notes added, with more metrics planned.  Discussion of features and bugs takes place over [on this thread on the Beeminder forum](http://forum.beeminder.com/t/announcing-beeminder-for-anki/2206).  The published version of this add-on can be found over on [AnkiWeb](https://ankiweb.net/shared/info/1728790823)

## Usage

1. Install the add-on (either build or use the latest release on GitHub)
2. Open add-on menu of Anki and configure the add-on
3. You're good to go!

## Building 

Although this version isn't available on AnkiWeb, you can use this add-on.

1. Run `pyuic5 resources/layout/config.ui > beetime/config_layout.py`
1. Run `cd beetime && zip -r ../beetime.ankiaddon * && cd ../`
2. Add the add-on using Anki menus.

## Contributing
Thanks!

Just two suggestions regarding commits: use a verb in the active tense and add a context cue to the front of the commit message.

## Notes
Edit the .ui file in Qt Creator and build it using `pyuic4`. `make ui` should take care of that.

- manifest.json [seems to be](https://www.reddit.com/r/Anki/comments/fbqwkx/anki_addon_manifest_documentation/fj63tse/?context=8&depth=9) only documented [here](https://github.com/ankitects/anki/blob/c966d88e4c003b043c22fca0cf71ea8d14b1cb97/qt/aqt/addons.py#L146-L167).
