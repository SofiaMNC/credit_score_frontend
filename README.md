# Credit Scoring Web App - Front End

## Overview
This is the front end of the credit scoring web app. 
It presents the user with a dashboard, allowing easy browsing of relevant data for each anonymized client.
To achieve this, the dashboard make calls to a backend via a REST API.

## Requirements
pandas 1.0.1

plotly 4.12.0

requests 2.22.0

streamlit 0.71.0

## Usage
### Without Docker
To run the dashboard, please execute the following from the root directory:

```bash
pip3 install -r requirements.txt
streamlit run dashboard.py
```

When run locally, the dashboard is accessible here:
```
http://localhost:8501
```


### With Docker
To run the web app using Docker containers, please execute the following from the root directory:

```bash
docker build -t dashboard .
docker run -d --name dashboard -p 8501:8501 dashboard
```
