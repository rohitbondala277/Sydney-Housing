# Sydney Housing Price Predictor

A small end-to-end ML project that predicts the sale price of a property in Sydney CBD, Chatswood or Liverpool, then serves the model through a Flask web app.

I built this for SIT720 (Machine Learning) at Deakin University. The interesting part for me was that there was no ready-made dataset, so I collected the data myself.

## What's in here

| File | What it does |
|---|---|
| `8.1d.ipynb` | The full workflow: data cleaning, EDA, feature engineering, model comparison, error analysis |
| `app.py` | Flask app that loads the trained model and returns a price estimate |
| `templates/index.html` | The web form for entering property details |
| `housing_model_bundle.pkl` | Saved Random Forest model plus the lookup values the app needs |

## The data

105 sold properties, 35 per suburb, collected by hand from public listing sites. Each row has suburb, property type, bedrooms, bathrooms, parking, land size, internal area, distance to the CBD and distance to the nearest station.

Missing internal areas are filled using the median for that suburb and property type, and the app uses the same fallback so training and prediction stay consistent.

## Results

I compared three models with 5-fold cross validation:

| Model | CV R² | CV MAE |
|---|---|---|
| Linear Regression | 0.579 | $423k |
| Random Forest | **0.627** | $393k |
| Gradient Boosting | 0.623 | $392k |

Random Forest came out on top for R² and I picked it for the app. With only 105 rows the errors are still big, which is mostly a data size problem. The notebook walks through the five worst predictions one by one. The biggest misses were expensive Chatswood houses where the internal area was missing and had to be imputed, so the model never saw how big they really were.

I also ran a small experiment comparing the model against my own guesses and an LLM's guesses on the same properties. That comparison is in the last section of the notebook.

## Run it locally

```bash
git clone https://github.com/rohitbondala277/Sydney-Housing.git
cd Sydney-Housing
python -m venv venv
source venv/bin/activate      # on Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Then open http://localhost:5000.

## What I'd do next

- Collect more listings and more suburbs so the model has a fighting chance on expensive properties
- Containerise the app with Docker and deploy it to Azure App Service
- Add a simple CI check that loads the model and runs a test prediction

## Built with

Python, pandas, scikit-learn, matplotlib, seaborn, Flask, joblib
