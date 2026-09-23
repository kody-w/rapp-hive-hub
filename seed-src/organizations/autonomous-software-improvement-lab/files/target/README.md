# Practice Shelf — a deliberately imperfect practice target

Practice Shelf is a tiny command-line bookmark keeper written for this seed:
one Python file (standard library only, Python 3.10+), one test file, no
network, no dependencies. People add, list, remove, export and import web
links, and the shelf lives in one JSON file under their home directory.

It exists so you can run one complete improvement generation — baseline,
eight strategist reports, tally, integration, independent verification and
review — on something harmless before you point the kit at your own software.

## The flaws are deliberate practice material

**This program and its tests contain several deliberate flaws of different
kinds.** They are practice material, not accidents, and they are not marked
in the code: finding them is the strategists' job. Different strategy lenses
should find different flaws. Do not use Practice Shelf to keep anything you
care about.

The answer key is `ANSWER-KEY.md`, next to this file in the seed. Keep it
**out of the practice repository** so strategists cannot read it, and open it
only after the tally is drafted, to see what the loop found and what it
missed.

## Warning: as shipped, the tests write into your real home directory

`test_shelf.py` writes `~/.practice-shelf/shelf.json` in the home directory of
whoever runs it. That is one of the deliberate flaws, and the case's
`hermetic-tests` task fixes it before the baseline. Until then, run the suite
only through the kit's `baseline` command (which gives every verify command a
throwaway home) or give it a throwaway home yourself:

```sh
mkdir -p .throwaway-home
HOME="$PWD/.throwaway-home" python3 -B -m unittest -v test_shelf
```

On Windows the home directory comes from `USERPROFILE`; the kit sets both.
If you already ran the suite with your real home, delete `~/.practice-shelf`.

## Use it

```sh
python3 shelf.py add https://example.org/reading --title "Reading list" --tag later
python3 shelf.py list --tag later
python3 shelf.py export --format csv
python3 shelf.py remove 1
```

`PRACTICE_SHELF_HOME` points the shelf at another directory.

## Set it up as a practice project

Copy only these three files into a new directory, make it a git repository,
and commit them as the starting point:

```sh
mkdir -p practice/practice-shelf
cp shelf.py test_shelf.py README.md practice/practice-shelf/
cd practice/practice-shelf
git init -b main
git add shelf.py test_shelf.py README.md
git commit -m "Practice Shelf as shipped"
```

Then follow the seed's top-level README to configure the kit and run a
generation. Everything stays on your machine.
