# Orbisol

Orbisol is a Python-based application designed to track space debris, aiming to enhance the safety of the orbital environment. This project utilizes technologies such as Pygame and OpenGL to visualize orbital paths and debris movement in real-time, providing insights and analytics to mitigate potential hazards in space.

## Features

- Real-time visualization of space debris orbits.
- Analytical tools to assess potential collision paths.
- User-friendly interface for monitoring and interaction.
- Extensible framework for integrating additional datasets.

## Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.8 or newer
- Pip (Python package installer)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/Orbisol.git
   cd Orbisol
   ```

2. Install the required Python packages:
    ```bash
    pip install -r requirements.txt

3. To set up the virtual environment and install dependencies:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    pip install -e
    ```


### Usage
To run the application, execute:
    ```
    python src/app.py
    ```


## Directory Structure
- `assets/`: Static files like images used in the application.
- `bin/`: Contains executable scripts.
- `data/`: Data files and datasets related to space debris.
- `lib/`: Library code for core functionalities.
- `src/`: Source files of the application.
- `tests/`: Test suite for the application.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
This project relies on James Cranch's Python Octrees library for efficient rendering: (https://github.com/jcranch/octrees)

Thank you to ACM@CMU for hosting CMUHacks 2023, and for selecting Orbisol as the winner!

And special thanks to Jose Cestero, Mihail Alexandrov, and Arturo Paras for helping to make this project a reality.