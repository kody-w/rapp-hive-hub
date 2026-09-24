# RAPP Hive Hub

The RAPP instance of Hive Hub: a hub for finding Hives and starting RAPP Work organizations. It is
a tree of markdown cards, one fact per file: one card per Hive protocol, one per Hive, one per
organization and one per starter, plus twelve starter templates under `starters/`.
`tools/build.py`, a byte-identical copy of the generic Hive Hub's builder, turns the cards into
views: a JSON API, a static site and a list of chants. Nothing in the hub runs. You join a Hive
with your own Brainstem, and the hub never writes into a Hive or keeps a record of who joined.

## Who curates it

The maintainers of the kody-w/rapp-hive-hub repository. A curator adds, moves or retires a card
with one signed commit. Moving card files is how the hub is reorganized.

## Submit a card

1. Write one card file. Copy a card under `cards/` and change its fields; the builder refuses
   fields it does not know.
2. Pin exact bytes. A spec or an agent is a URL at a full commit id, with its SHA-256. A Hive
   card carries the Hive id, its first commit and the founder's key fingerprint. A starter card
   names a template folder under `starters/` that obeys the Hive file rules, with a README.md.
3. Run `python tools/build.py` and fix whatever it refuses.
4. Send the card file (and any starter folder) to a curator by any channel, for example a pull
   request. A curator reviews it and adds it with a signed commit.

Every card is public. Never put a password, a token or a private Hive's name in one. A private
Hive can leave its address out and say in its channel how to ask.

## Where it fits

In the experimental RAPP/1 organism map, this hub is RAPP Work starters plus the discovery part
of the Hive Mind, the network across sovereign Hives (candidate). Transport carries; signatures
decide: a card, a chant or a URL is a locator, never authority.

```text
6  You            talk to your Brainstem; confirm every exact plan
5  Brainstem      your own AI (in force); its Hive agent (experimental) creates or joins a Hive
4  Your device    your copy of each Hive, one key per device per Hive; references
3  Hive           rapp-hive/1 Private Hive (in force) or hive-md folder Hive (experimental)
                  <-- across: the Hive Mind (this hub)
2  Organization   canonical rapp-work/1: one owner, one world, one policy, one release scope,
                  exactly one Hive (specified: no estate has activated it, G16; it cannot
                  bind a folder Hive yet, G10)
1  Estate         an owner's signed registry and protocol pins   (in force)
0  RAPP/1         bytes and identity   (in force)
```

An organization card here is a plan (specified), and its starter is a Hive template
(experimental). `rapp-hive/2` is frozen as a research record. The map is
[ECOSYSTEM.md](https://github.com/kody-w/rapp-work/blob/experimental/rapp-work-constitution/ECOSYSTEM.md)
with the draft [CONSTITUTION.md](https://github.com/kody-w/rapp-work/blob/experimental/rapp-work-constitution/CONSTITUTION.md),
on kody-w/rapp-work branch experimental/rapp-work-constitution, and the
[Hive folder convention](https://github.com/kody-w/rapp-model-hive/blob/experimental/hive-md/HIVE-MD.md)
on kody-w/rapp-model-hive branch experimental/hive-md.

## Join a Hive

1. Dial a chant from `views/chants.txt`, or open a card.
2. Check the card's sha256 against `views/api/v2/index.json`.
3. Give the card to your Brainstem. Its Hive agent joins with the card's address, hive, root and
   founder: it clones the Hive, verifies the root and the founder fingerprint, writes one
   SSH-signed request file, and sends it the way the card's channel says.

## Start from a starter

1. Pull the starter's template down read-only: as a reference (the Hive agent's `reference`), with
   `npx degit`, or as a ZIP.
2. Your Brainstem's Hive agent creates a new Hive, fills its `hive:` id, and brings each room in
   by signed copy. The starter's README.md says exactly how.
3. People join that new Hive by request, like any Hive.
