# Time Dilation Calculator

A Python special-relativity calculator with a dependency-free command line and an optional Tkinter desktop interface. Calculates the Lorentz factor and relates observer elapsed time to moving-clock proper time at constant relative speed.

## Run

Python 3.10 or later; no pip packages required:

```bash
python main.py --speed 80 --speed-unit '% of c' --time 10
python -m unittest discover -s tests -v
```

At 80% of light speed, gamma is approximately 1.6666667. Ten years of observer-frame time correspond to six years on the moving clock. To supply proper time instead:

```bash
python main.py --speed 80 --speed-unit '% of c' --time 6 --time-frame proper
```

Both commands describe the same interval. Use `--time-unit seconds` if the input is seconds; input and output use the same time unit, so no year-to-second convention is required.

## Desktop interface

```bash
python main.py --gui
```

The GUI accepts speed and observer elapsed years, then displays gamma and moving-clock proper years. Tkinter requires a graphical desktop and your Python distribution's Tk support; the CLI works without it. This replaces the earlier PySimpleGUI dependency. Importing the module does not open a window.

## Units and method

Supported speed units: `m/s`, `km/s`, `km/h`, and `% of c`. Percent means 80 for 80%, not 0.8. Uses `c = 299792458 m/s` and converts all speeds to m/s.

`beta = v/c`, `gamma = 1/sqrt((1-beta)*(1+beta))`, and `observer time = gamma * proper time`.

The factored expression reduces cancellation near light speed. Finite, nonnegative time and speeds strictly below c are required. Invalid units, NaN/infinity, negative inputs, and light/superluminal speeds produce clear errors. Finite-precision limitations still apply extremely close to c.

| Example | Expected result |
| --- | --- |
| Speed 0, observer time 10 years | gamma 1, proper time 10 years |
| Speed 60% of c, observer time 10 years | gamma 1.25, proper time 8 years |
| Speed 80% of c, proper time 6 years | gamma about 1.6666667, observer time 10 years |

## Scope and verification

The original implementation rejected decimal input with isnumeric(), lacked bounds checks, and labeled gamma ambiguously as a time. Calculation is now separated from interface code, units and clock frames are explicit, and examples are reproducible through the CLI.

Tests check reference values, conversion consistency, inverse time conversion, invalid boundaries, and import behavior. The desktop GUI requires a manual desktop smoke check; automated checks cover the calculation and CLI. This models a constant-velocity segment in flat spacetime, not gravitational time dilation or a complete accelerating round trip. It is a deterministic physics example, not an ML model.
