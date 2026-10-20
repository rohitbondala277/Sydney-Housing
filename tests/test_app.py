"""Smoke tests for the Flask app. These run in CI before every deployment."""

import re
import sys
import warnings
from pathlib import Path

import joblib
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

import app as housing_app  # noqa: E402


@pytest.fixture()
def client():
    housing_app.app.config.update(TESTING=True)
    with housing_app.app.test_client() as c:
        yield c


def sample_house(**overrides):
    form = {
        "suburb": "Liverpool",
        "property_type": "House",
        "bedrooms": "4",
        "bathrooms": "2",
        "parking_spaces": "2",
        "distance_to_cbd_km": "31",
        "distance_to_station_km": "0.8",
        "land_size_sqm": "550",
        "internal_area_sqm": "220",
    }
    form.update(overrides)
    return form


def extract_price(html):
    match = re.search(r"\$([\d,]+)", html)
    assert match, "no predicted price found in the page"
    return int(match.group(1).replace(",", ""))


def test_model_loads_without_version_mismatch():
    from sklearn.exceptions import InconsistentVersionWarning

    with warnings.catch_warnings():
        warnings.simplefilter("error", InconsistentVersionWarning)
        bundle = joblib.load(REPO_ROOT / "housing_model_bundle.pkl")
    assert "model" in bundle


def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    body = res.get_json()
    assert body["status"] == "ok"
    assert body["model"] == "RandomForestRegressor"


def test_form_page_lists_suburbs(client):
    res = client.get("/")
    assert res.status_code == 200
    page = res.get_data(as_text=True)
    for suburb in ("Chatswood", "Liverpool", "Sydney CBD"):
        assert suburb in page


def test_prediction_is_plausible(client):
    res = client.post("/", data=sample_house())
    assert res.status_code == 200
    price = extract_price(res.get_data(as_text=True).split("Predicted sale price")[1])
    assert 200_000 < price < 20_000_000


def test_missing_floor_area_is_imputed(client):
    res = client.post("/", data=sample_house(internal_area_sqm="0"))
    assert res.status_code == 200
    assert "filled in estimate" in res.get_data(as_text=True)
