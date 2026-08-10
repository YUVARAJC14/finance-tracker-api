# Finance Tracker Agent Notes

- This repo is currently a tiny Python script centered on [main.py](main.py); keep changes small and local unless the user asks for a larger refactor.
- Run the app with `python main.py` to verify behavior.
- Prefer the standard library and simple data structures first; do not introduce dependencies unless they clearly solve a new requirement.
- There is no test suite yet, so add one only when the feature set grows enough to justify it.
- Preserve the current Windows file encoding when editing [main.py](main.py); it is UTF-16LE in the workspace right now.
- The only existing ignore rule is [venv/](.gitignore), so avoid checking in virtual environments or other local runtime artifacts.