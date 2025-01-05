# Sampling-Theory-Studio
A desktop application illustrating signal sampling and recovery based on the Nyquist–Shannon theorem. Users can load and compose signals, sample at various frequencies, visualize original, sampled, and reconstructed signals in real-time, and explore different reconstruction methods while adding noise and investigating aliasing effects.

## Table of Contents
- [Demo](#demo)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Features](#features)
- [Contributors](#contributors)

## Demo
https://github.com/user-attachments/assets/736ee24c-a420-4012-9d03-9f1241f83d20

## Prerequisites

- Python 3.6 or higher

## Installation

1. **Clone the repository:**

   ``````
   git clone https://github.com/AhmedAmgadElsharkawy/Sampling-Theory-Studio.git
   ``````

2. **Install The Dependincies:**
    ``````
    pip install -r requirements.txt
    ``````

3. **Run The App:**

    ``````
    python main.py
    ``````

## Features

- **Load Signal:** Support loading pre-recorded signals from CSV files.  
- **Signal Mixer:** Compose custom signals by summing sinusoids with different frequencies, magnitudes, and phase shifts, with real-time generation.  
- **Export Signal:** Save composed signals to CSV files, allowing you to load and share them at any time.  
- **Signal Sampling:** Sample signals and display the sampling frequency in either actual or normalized form (0×fmax to 4×fmax).  
- **Signal-to-Noise Ratio (SNR):** Control the SNR to introduce noise into signals.  
- **Signal Reconstruction:** Provide five different signal reconstruction options: Whittaker–Shannon, Lanczos, Cubic Spline, Zero-Order Hold, and First-Order Hold.  




## Contributors
- **AhmedAmgadElsharkawy**: [GitHub Profile](https://github.com/AhmedAmgadElsharkawy)
- **AbdullahMahmoudHanafy**: [GitHub Profile](https://github.com/AbdullahMahmoudHanafy)
- **MohamadAhmedAli**: [GitHub Profile](https://github.com/MohamadAhmedAli)
- **RawanAhmed444**: [GitHub Profile](https://github.com/RawanAhmed444)
