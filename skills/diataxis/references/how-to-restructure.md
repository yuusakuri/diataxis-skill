# Restructuring an existing docs tree

A docs tree is read while you rearrange it, and its links are held by search engines,
issue threads, and other people's bookmarks. So the aim is a sequence of small safe
moves, not a flag day.

## Order of work

1. **Audit before touching anything.**
   `python3 scripts/audit_docs.py docs/ --json > /tmp/audit.json`
   Record the starting state so you can show what changed.

2. **Create the four directories and an index, and stop.** Commit that alone. It
   changes nothing for readers and gives every later move a destination.

3. **Move the easy pages first.** Pages that are already one mode — an API reference, a
   single-task guide — just move. Each move is its own commit, so a bad call is one
   revert rather than an archaeology exercise.

4. **Split the mixed pages one at a time.** For each: create the new pages, move the
   material, leave the original as a stub linking to its parts if anything links to it.
   Splitting is where content gets silently lost; do one page per commit and re-read
   the diff.

5. **Re-run the audit.** The findings should have gone down. If a new one appeared, you
   moved something into the wrong mode.

## Keeping links alive

- Prefer redirects if the docs are published: most site generators have them, and a
  redirect costs a line.
- Where redirects are impossible, keep the old path as a one-line stub pointing to the
  new location. Delete stubs later, deliberately, not as part of the move.
- Grep the repository for links to a page *before* moving it — README files, code
  comments, and issue templates all link into docs and none of them are checked by a
  docs build.

## What not to do

- **Do not rename for tidiness mid-restructure.** Moving and renaming in one step makes
  the diff unreadable, and unreadable diffs are how content disappears.
- **Do not create empty mode directories to "complete the set."** An empty `tutorials/`
  advertises a tutorial that does not exist.
- **Do not restructure and rewrite at once.** Move first, commit, then improve the
  prose. Mixed commits cannot be reviewed.
- **Do not classify from filenames.** `setup.md` could be any of the four modes; you
  have to read it.

## When the tree is genuinely large

Work mode by mode rather than page by page: extract all the reference first, since it
is the easiest to recognise and often the biggest win, then how-to, then explanation.
Leave tutorials until last — they are the fewest and the most rewriting.
