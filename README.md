# autocorrect
Python fuzzy search and autocorrect implementation

This project provides a Python library to allow fuzzy search over a dictionary. It implements this with a prefix trie so as to search efficiently.

It is intended that this is used to create COM server so the Python implementation can communicate with AutoHotkey, to allow autocorrection of misspellings across Windows. The server/client COM setup works, but the Autohotkey front-end does not work well right now.

Future plans for this project:
1. Fix the AHK front end so that it efficiently replaces mistyped words with the better dictionary word
2. Implement a predictive model, based on at least the last two words written, to select the most likely word meant
3. As users type using this program to fix their errors, improve the model based on individual data
