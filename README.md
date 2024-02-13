# System Analyzer Dashboard 📈 📊

The easiest way to analyze the efficiency of a server is by using various plots.

The idea:
1. User provides input server path where profile files stored.
2. The `System Analyzer Dashboard ` constructs a data frame form profile files, which helps to create various plots and these plots tell us the performance of server. 

## Overview 
This Python-based system analyzer dashboard application allows users to view server performance through various informative plots.

## Features
- **Interactive Visualization**: Explore server performance through engaging graph plots you can directly interact with to zoom, filter, and customize your view.
- **Platform Agnostic:** Monitor the health of a wide range of servers
- **Data Export:** Easily download graphs.

## Environment Setup
<p align="center">
  <img alt="" src="https://img.shields.io/pypi/pyversions/plotai.svg"/>
  <img alt="" src="https://img.shields.io/badge/web_framework-Stramlit-blue"/>
  <img alt="" src="https://img.shields.io/badge/graph_library-Plotly-blue"/>
  <img alt="" src="https://img.shields.io/badge/License-Apache_2.0-blue.svg"/>
</p>

- Python 3.x
- Streamlit web framework
- plotly library (for interactive graphs)
- Other dependencies (specified in requirements.txt)

## Installation
1. Clone this repository to your local machine.
2. Create a virtual environment: `python3 -m venv venv`
3. Activate the virtual environment: `source venv/bin/activate` (Linux/macOS) or `venv\Scripts\activate` (Windows).
4. Install the required dependencies: `pip install -r requirements.txt`

## Usage

1. Start the application: `streamlit run system_analyzer.py`.
2. see the application on **`http://localhost:8501`**

## How to Use
- Upload a profile file location and name of server to start.
- Choose the server.
- Explore the graphs and know the status of server.
- Click the ``camera`` icon to download the graph for further report.

## Contributing
Contributions are welcome! Please create a pull request or open an issue for any improvements or bug fixes.

## License
This project is licensed under the Apache 2.0 License. See the [LICENSE](./licence/LICENSE) file for details.

