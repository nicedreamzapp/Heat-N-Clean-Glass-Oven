# Contributing

Thanks for taking a look. This is an open-hardware oven design, so feedback from people who work
with sheet metal, heaters or PID controllers is as useful as code.

## Reporting a problem

Open an [issue](https://github.com/nicedreamzapp/Heat-N-Clean-Glass-Oven/issues/new/choose). The
things that make it quick to look into:

- the part number and name from [PARTS_LIST.md](PARTS_LIST.md) (for example `05 top cap`)
- which file you looked at (a STEP file in `FAB_PACKAGE_2026-10-16/`, a `viewer-*.html` page, or a
  script in `Scripts/`)
- what is wrong: a dimension, a clash between parts, something a shop cannot make, or a controller
  setting
- for a script error, your Python version and the full traceback

Anything about temperatures, wiring or the safety limits in
[Controller_Setup_Guide.md](Controller_Setup_Guide.md), please say so at the top of the issue.

## Running it locally

```bash
# View the parts in a browser (the viewers load files by relative path)
python3 -m http.server        # then open http://localhost:8000/viewer-thickness.html

# Regenerate the STL/GLB meshes
python3 -m venv .venv-cad && .venv-cad/bin/pip install build123d trimesh numpy
.venv-cad/bin/python Scripts/export_all_parts.py
```

[CURRENT.md](CURRENT.md) lists the only files to build from. Some scripts read files from
`Factory Files/`, which is not in the repo.

## Tests

There are no automated tests. After changing CAD code, check that every STEP file in the fab package
loads as one solid:

```bash
.venv-cad/bin/python Scripts/verify_steps.py FAB_PACKAGE_2026-10-16
```

Then look at the changed parts in the viewers and confirm nothing that mates with the ceramic or the
glass has moved.

## Pull requests

Small and focused is easiest to review. Include a render or screenshot of any geometry change. For
big changes, open an issue first so we can talk it through.

Please follow the [code of conduct](CODE_OF_CONDUCT.md).
