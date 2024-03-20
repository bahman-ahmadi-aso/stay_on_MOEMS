# MOEMS
A multi-objective optimization for smart grid
This system optimizes the energy management of a microgrid, considering various energy sources and storage units. It aims to minimize the cost and environmental impact while ensuring the reliability of the microgrid.

## Features
- Optimization of grid energy import/export to reduce costs and CO2 emissions.
- Management of Energy Storage Systems (ESS) to optimize charging and discharging schedules.
- Integration of renewable energy sources (e.g., PV panels) into the microgrid's energy mix.
- Electric Vehicle (EV) and electric bus (eBUS) charging management, including smart charging capabilities.
- Flexibility to accommodate different time resolutions and forecasting intervals.

## Setup Instructions
1. Ensure Python 3.5 or higher is installed on your system.
2. Install the required Python packages listed in `requirements.txt`.
3. Adjust the `main.py` parameters according to your microgrid's specifications.
4. Run `main.py` to perform the optimization.

## Dependencies
- Python 3.5+
- NumPy
- Pyomo  6.7.0
- Ipopt 3.12.12


Refer to `requirements.txt` for a complete list of dependencies.

replace solver "Ipopt 3.12.12" by your solver of choice.
## Usage
Run the following command in the terminal:
```bash
python main.py
