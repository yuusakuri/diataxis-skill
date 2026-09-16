# How to configure a project

Create `widget.toml` in the project root:

```toml
[widget]
mode = "strict"
```

Run `widget check` to confirm the file is read. A project without the file uses
the defaults, which is fine for a first run.
