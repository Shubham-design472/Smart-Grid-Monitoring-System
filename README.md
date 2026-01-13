# Smart Grid Cyber-Physical Monitoring System

A real-time "Mission Control" dashboard for the IEEE 14-bus smart grid. This project uses **Django** and **Vis.js** to visualize the grid topology and a **Hidden Markov Model (HMM)** to detect False Data Injection (FDI) attacks.

## Features
- **Real-time Monitoring:** Live visualization of grid nodes (Generators/Loads).
- **Attack Detection:** HMM-based engine detects anomalies with ~89% accuracy.
- **Digital Twin:** Dynamic color-changing nodes (Red = Attack, Orange = Warning).

## Tech Stack
- Python, Django
- JavaScript (Vis.js, Chart.js)
- Pandas, HMM (hmmlearn)
