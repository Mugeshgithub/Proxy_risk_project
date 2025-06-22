# Proxy Risk Project

This project analyzes proxy service risks using Python and provides interactive visualizations via a Streamlit dashboard.

## Features
- Loads and analyzes proxy risk data (fraud scores, countries, ISPs)
- Generates interactive charts with Plotly
- Streamlit dashboard for easy exploration
- GitHub-ready codebase (large datasets excluded)

## Setup
1. Clone the repository:
   ```sh
   git clone https://github.com/Mugeshgithub/Proxy_risk_project.git
   cd Proxy_risk_project
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
   Or manually:
   ```sh
   pip install pandas plotly streamlit kaleido
   ```
3. Place your dataset (e.g., `PROXYSCOPEW.csv`) in the project folder (not tracked by git).

## Usage
To launch the dashboard:
```sh
streamlit run app.py
```

## Notes
- The main dataset is not included in the repository due to GitHub file size limits. Please contact the project owner for access.
- All analysis code and dashboard logic are included.

## License
MIT 