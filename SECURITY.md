# Security policy

## Reporting a vulnerability

Please do not open a public issue for security problems.

Report them privately through GitHub: go to the **Security** tab of this repo and click **Report a vulnerability** ([direct link](https://github.com/nicedreamzapp/Heat-N-Clean-Glass-Oven/security/advisories/new)). Only the maintainer sees the report.

Helpful details: what you found, which file and part it affects, which commit, and how it could lead to a fire, burn or electric shock if someone built the oven as drawn.

I aim to reply within 3 days and to ship a fix or a clear plan within 30 days, depending on severity. You will be credited in the advisory unless you ask not to be.

## Supported versions

Fixes go into the current design on `main`. The files to build from are listed in [CURRENT.md](CURRENT.md); older packages are not updated.

## What matters most here

The parts where a mistake could hurt someone:

- the controller settings and wiring in [Controller_Setup_Guide.md](Controller_Setup_Guide.md): the 870 F limit, the overheat alarm, the thermal fuse and the 6-hour timer on a 120V Kanthal heater
- the materials and sheet thickness in `FAB_PACKAGE_2026-10-16/`, which must hold up to 870 F continuous
- the insulation gap and outer mesh that keep the outside safe to touch, set in `Scripts/hnc_params.py`
