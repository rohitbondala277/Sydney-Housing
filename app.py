"""
Sydney Housing Price Prediction App
SIT720 8.1 Distinction Task

Loads the trained Random Forest model from housing_model_bundle.pkl
(created in the accompanying notebook) and predicts a sale price
for a property based on user entered features.

Run with: python app.py
Then open http://localhost:5000 in a browser.
"""

import pandas as pd
import joblib
from flask import Flask, render_template, request

app = Flask(__name__)

bundle = joblib.load("housing_model_bundle.pkl")
model = bundle["model"]
feature_columns = bundle["feature_columns"]
suburb_type_medians = bundle["suburb_type_medians"]
suburb_medians = bundle["suburb_medians"]
global_median_area = bundle["global_median_area"]
suburbs = bundle["suburbs"]
property_types = bundle["property_types"]


def impute_internal_area(suburb, property_type):
    """Same group-median fallback logic used during training in the notebook."""
    key = (suburb, property_type)
    if key in suburb_type_medians and pd.notna(suburb_type_medians[key]):
        return suburb_type_medians[key]
    if suburb in suburb_medians and pd.notna(suburb_medians[suburb]):
        return suburb_medians[suburb]
    return global_median_area


def build_feature_row(suburb, property_type, bedrooms, bathrooms, parking_spaces,
                       land_size_sqm, internal_area_sqm, distance_to_cbd_km,
                       distance_to_station_km):
    has_land = 1 if land_size_sqm and land_size_sqm > 0 else 0
    bed_bath_ratio = bedrooms / (bathrooms + 1)

    area_was_imputed = not internal_area_sqm or internal_area_sqm <= 0
    if area_was_imputed:
        internal_area_sqm = impute_internal_area(suburb, property_type)

    row = {
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "parking_spaces": parking_spaces,
        "internal_area_sqm": internal_area_sqm,
        "distance_to_cbd_km": distance_to_cbd_km,
        "distance_to_station_km": distance_to_station_km,
        "has_land": has_land,
        "bed_bath_ratio": bed_bath_ratio,
    }

    for s in suburbs:
        row[f"suburb_{s}"] = 1 if s == suburb else 0
    for pt in property_types:
        row[f"property_type_{pt}"] = 1 if pt == property_type else 0

    row_df = pd.DataFrame([row])
    for col in feature_columns:
        if col not in row_df.columns:
            row_df[col] = 0
    row_df = row_df[feature_columns]
    return row_df, internal_area_sqm, area_was_imputed


@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    area_note = None

    form_values = {
        "suburb": suburbs[0],
        "property_type": property_types[0],
        "bedrooms": 2,
        "bathrooms": 1,
        "parking_spaces": 1,
        "distance_to_cbd_km": 8.0,
        "distance_to_station_km": 0.5,
        "land_size_sqm": 0,
        "internal_area_sqm": 0,
    }

    if request.method == "POST":
        suburb = request.form.get("suburb")
        property_type = request.form.get("property_type")
        bedrooms = int(request.form.get("bedrooms", 0))
        bathrooms = int(request.form.get("bathrooms", 0))
        parking_spaces = int(request.form.get("parking_spaces", 0))
        distance_to_cbd_km = float(request.form.get("distance_to_cbd_km", 0))
        distance_to_station_km = float(request.form.get("distance_to_station_km", 0))
        land_size_sqm = float(request.form.get("land_size_sqm", 0) or 0)
        internal_area_sqm = float(request.form.get("internal_area_sqm", 0) or 0)

        form_values.update({
            "suburb": suburb, "property_type": property_type,
            "bedrooms": bedrooms, "bathrooms": bathrooms, "parking_spaces": parking_spaces,
            "distance_to_cbd_km": distance_to_cbd_km, "distance_to_station_km": distance_to_station_km,
            "land_size_sqm": land_size_sqm, "internal_area_sqm": internal_area_sqm,
        })

        row_df, area_used, area_was_imputed = build_feature_row(
            suburb, property_type, bedrooms, bathrooms, parking_spaces,
            land_size_sqm, internal_area_sqm, distance_to_cbd_km, distance_to_station_km
        )

        predicted_price = model.predict(row_df)[0]
        prediction = f"${predicted_price:,.0f}"

        if area_was_imputed:
            area_note = (
                f"Internal area wasn't entered, so the model used a filled in estimate of "
                f"{area_used:.0f} sqm based on similar {property_type.lower()} properties in {suburb}."
            )

    return render_template(
        "index.html",
        suburbs=suburbs,
        property_types=property_types,
        form_values=form_values,
        prediction=prediction,
        area_note=area_note,
    )


if __name__ == "__main__":
    app.run(debug=True)
