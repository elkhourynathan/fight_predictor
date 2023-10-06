# UFC Fight Predictor Web Application

## Overview

The UFC Fight Predictor is a web application that utilizes a custom-trained machine learning model to offer probability predictions for UFC fight outcomes. 

## Features

- **Fighter Selection**: Select two UFC fighters from a list of available fighters.
- **Prediction**: Click the "Predict" button to receive a probability prediction for each fighter's chance of winning.
- **User-Friendly Interface**: An intuitive and user-friendly interface makes it easy for anyone to use.
- **Responsive Design**: The application is responsive, adapting to various screen sizes, including mobile devices.
- **Custom Trained Model**: The predictions are generated using a custom-trained machine learning model tailored to UFC fight data.

## How It Works

The UFC Fight Predictor leverages historical UFC fight data and fighter statistics to generate probabilistic predictions for upcoming bouts. The custom-trained machine learning model takes into account various factors such as fighter records, fighting styles, and past performance to estimate the likelihood of each fighter winning.

## Usage

1. Visit the [UFC Fight Predictor](https://ufc-fight-pred-00326a93d210.herokuapp.com/) website.
2. Select two UFC fighters from the available list.
3. Click the "Predict" button.
4. Receive probability predictions for each fighter's chance of winning the upcoming fight.

## Installation

If you want to run the UFC Fight Predictor locally, follow these steps:

1. Clone the repository:

3. Navigate to the frontend directory, install packages and run
```
    cd frontend
    npm i
    npm start
```

2. Navigate to the backend directory, install packages and run
```
    cd backend
    python -m venv venv # optional
    source venv/bin/activate #optional

    pip install -r requirements.txt

    gunicorn backend.app:app
```
3. Access application from 'http://localhost:8000'
