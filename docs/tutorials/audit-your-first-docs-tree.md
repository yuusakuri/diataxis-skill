# Audit your first docs tree

In this tutorial you will run the auditor on a sample docs tree and read its
findings. It takes about five minutes. By the end you will have seen the tool
report a real problem and will know what its output means.

You need Python 3.9 or later. Nothing else.

## 1. Get the repository

```bash
git clone https://github.com/yuusakuri/diataxis-skill
cd diataxis-skill
```

## 2. Audit a tree that is already correct

The repository ships sample trees for testing. Start with the tidy one:

```bash
python3 skills/diataxis/scripts/audit_docs.py tests/fixtures/clean
```

You should see:

```
Diátaxis audit: tests/fixtures/clean

4 pages, modes present: explanation, how-to, reference, tutorial

No findings. Every page sits in a mode and none of them are visibly doing two
jobs at once.
```

Four pages, one per mode, each doing one job. A correct tree is quiet.

## 3. Audit a tree with a problem

```bash
python3 skills/diataxis/scripts/audit_docs.py tests/fixtures/mixed
```

This time you get findings. One of them reads:

```
[warning] reference/cli.md
  reference page carrying 6 action signals. Reference is for looking things up
  mid-task; step-by-step instruction belongs in a how-to guide. A reader
  scanning for a parameter has to read past a procedure to find it.
  evidence: line 6, line 7, line 8, line 9, +2 more
```

## 4. Check the evidence yourself

Open the file it named and look at the lines it cited:

```bash
sed -n '6,12p' tests/fixtures/mixed/reference/cli.md
```

You will see install steps sitting inside a reference page. That is the problem
the tool found: someone looking up an option has to read past a procedure.

## What you did

You ran the auditor on a correct tree and on a broken one, and confirmed one
finding against the source. That is the whole loop.

Next:

- [Install the skill](../how-to/install-the-skill.md) so an agent can use it.
- [Run the auditor in CI](../how-to/run-the-auditor-in-ci.md) to catch this on
  every pull request.
- [Why Diátaxis](../explanation/why-diataxis.md) if you want the reasoning.
