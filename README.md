# Sydney Housing Price Predictor

An end-to-end machine learning project that predicts the sale price of residential properties in Sydney CBD, Chatswood and Liverpool, and serves the trained model through a Flask web application.

Developed as part of SIT720 Machine Learning at Deakin University. No suitable public dataset existed, so the training data was collected manually from public property listings.

![Flask app showing a predicted sale price](docs/app-screenshot.png)

## Repository contents

| File | Purpose |
|---|---|
| `housing_price_model.ipynb` | Full workflow: data cleaning, exploratory analysis, feature engineering, model comparison and error analysis |
| `app.py` | Flask application that loads the trained model and returns a price estimate |
| `templates/index.html` | Web form for entering property details |
| `housing_model_bundle.pkl` | Trained Random Forest model plus the lookup values used for imputation |

## Data

105 sold properties (35 per suburb) collected from public listing sites, sold between March and August 2026. Features include suburb, property type, bedrooms, bathrooms, parking spaces, land size, internal floor area, distance to the CBD and distance to the nearest station.

Missing internal floor areas are imputed using the median for the same suburb and property type. The web app applies the same fallback, so training and inference stay consistent.

## Results

Three models were compared using 5-fold cross validation:

| Model | CV R² | CV MAE |
|---|---|---|
| Linear Regression | 0.579 | $423k |
| Random Forest | **0.627** | $393k |
| Gradient Boosting | 0.623 | $392k |

Random Forest achieved the highest R² and is the model used in the app. Error remains high given the small dataset. Analysis of the five largest prediction errors showed the biggest misses were high-value Chatswood houses with imputed floor areas, which points to data coverage rather than model choice as the main limitation.

The notebook also compares the model against human and LLM price estimates on a held-out set of properties.

## Running locally

```bash
git clone https://github.com/rohitbondala277/Sydney-Housing.git
cd Sydney-Housing
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Then open http://localhost:5000.

## Next steps

- Expand the dataset to more listings and suburbs to improve accuracy on high-value properties
- Containerise the app with Docker and deploy it to Azure
- Add a CI pipeline that loads the model and runs a test prediction on every push

## Tech stack

Python, pandas, scikit-learn, matplotlib, seaborn, Flask, joblib

## License

Released under the [MIT License](LICENSE).
