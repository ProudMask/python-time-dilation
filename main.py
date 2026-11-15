"""Special-relativistic time dilation with explicit units and clock frames."""
import argparse
import json
import math

C_M_PER_S = 299792458.0
SPEED_UNITS = ('m/s', 'km/s', 'km/h', '% of c')


def finite_number(value, name):
    if isinstance(value, bool):
        raise ValueError(f'{name} must be a finite number')
    try:
        result = float(value)
    except (ValueError, TypeError) as exc:
        raise ValueError(f'{name} must be a finite number') from exc
    if not math.isfinite(result):
        raise ValueError(f'{name} must be a finite number')
    return result


def speed_m_per_s(speed, unit):
    value = finite_number(speed, 'Speed')
    if unit not in SPEED_UNITS:
        raise ValueError(f'Unknown speed unit: {unit}')
    if value < 0:
        raise ValueError('Speed must be nonnegative')
    # Reject a 100% input before conversion/rounding can conceal the boundary.
    if unit == '% of c' and value >= 100:
        raise ValueError('Speed must be strictly below the speed of light')
    converted = value * {'m/s': 1.0, 'km/s': 1000.0, 'km/h': 1 / 3.6, '% of c': C_M_PER_S / 100}[unit]
    if not math.isfinite(converted) or converted >= C_M_PER_S:
        raise ValueError('Speed must be strictly below the speed of light')
    return converted


def calculate(speed, speed_unit, elapsed_time, time_frame='observer', time_unit='years'):
    velocity = speed_m_per_s(speed, speed_unit)
    elapsed = finite_number(elapsed_time, 'Elapsed time')
    if elapsed < 0:
        raise ValueError('Elapsed time must be nonnegative')
    if time_frame not in {'observer', 'proper'} or time_unit not in {'years', 'seconds'}:
        raise ValueError('Choose observer/proper time and years/seconds')
    beta = velocity / C_M_PER_S
    if beta >= 1:
        raise ValueError('Speed is too close to light speed for float precision')
    gamma = 1 / math.sqrt((1 - beta) * (1 + beta))
    observer = elapsed if time_frame == 'observer' else elapsed * gamma
    proper = elapsed / gamma if time_frame == 'observer' else elapsed
    if not all(math.isfinite(value) for value in (gamma, observer, proper)):
        raise ValueError('Result exceeds floating-point range')
    return {'speed_m_per_s': velocity, 'fraction_of_c': beta, 'lorentz_factor': gamma, 'time_unit': time_unit, 'observer_elapsed_time': observer, 'proper_elapsed_time': proper}


def launch_gui():
    # Lazy import keeps the CLI usable on systems without a graphical toolkit.
    import tkinter as tk
    from tkinter import ttk
    root = tk.Tk()
    root.title('Time Dilation Calculator')
    panel = ttk.Frame(root, padding=20)
    panel.grid()
    speed = tk.StringVar(value='80')
    unit = tk.StringVar(value='% of c')
    time = tk.StringVar(value='10')
    result = tk.StringVar(value='Enter speed and observer time, then calculate.')
    ttk.Label(panel, text='Speed').grid(row=0, column=0, sticky='w')
    ttk.Entry(panel, textvariable=speed).grid(row=0, column=1)
    ttk.Combobox(panel, textvariable=unit, values=SPEED_UNITS, state='readonly').grid(row=0, column=2)
    ttk.Label(panel, text='Observer elapsed time (years)').grid(row=1, column=0, sticky='w')
    ttk.Entry(panel, textvariable=time).grid(row=1, column=1)

    def update():
        try:
            report = calculate(speed.get(), unit.get(), time.get())
            result.set(f'Lorentz factor: {report["lorentz_factor"]:.8g}\nMoving-clock proper time: {report["proper_elapsed_time"]:.8g} years')
        except ValueError as exc:
            result.set(str(exc))

    ttk.Button(panel, text='Calculate', command=update).grid(row=2, column=0, columnspan=3, pady=12)
    ttk.Label(panel, textvariable=result, wraplength=500).grid(row=3, column=0, columnspan=3)
    root.mainloop()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--gui', action='store_true', help='Open the optional Tkinter desktop interface')
    parser.add_argument('--speed', type=float)
    parser.add_argument('--speed-unit', choices=SPEED_UNITS, default='% of c')
    parser.add_argument('--time', type=float)
    parser.add_argument('--time-frame', choices=['observer', 'proper'], default='observer')
    parser.add_argument('--time-unit', choices=['years', 'seconds'], default='years')
    args = parser.parse_args()
    if args.gui:
        if args.speed is not None or args.time is not None:
            parser.error('--gui cannot be combined with --speed or --time')
        try:
            launch_gui()
        except ImportError:
            parser.exit(1, 'Tkinter is unavailable; install your Python distribution\'s Tk support or use the CLI.\n')
        return
    if args.speed is None or args.time is None:
        parser.error('--speed and --time are required unless using --gui')
    try:
        report = calculate(args.speed, args.speed_unit, args.time, args.time_frame, args.time_unit)
    except ValueError as exc:
        parser.error(str(exc))
    print(json.dumps(report, indent=2, allow_nan=False))


if __name__ == '__main__':
    main()
