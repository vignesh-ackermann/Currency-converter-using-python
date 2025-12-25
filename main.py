from fastapi import FastAPI, HTTPException
import requests

app = FastAPI(title="Currency Converter API")

BASE_API = "https://open.er-api.com/v6/latest/"


@app.get("/convert")
def convert_currency(from_currency: str, to_currency: str, amount: float):
    try:
        response = requests.get(BASE_API + from_currency.upper())
        response.raise_for_status()
        data = response.json()

        if data.get("result") != "success":
            raise HTTPException(status_code=400, detail="Invalid base currency")

        rates = data.get("rates", {})
        if to_currency.upper() not in rates:
            raise HTTPException(status_code=400, detail="Invalid target currency")

        rate = rates[to_currency.upper()]
        converted_amount = amount * rate

        return {
            "from": from_currency.upper(),
            "to": to_currency.upper(),
            "amount": amount,
            "rate": rate,
            "converted_amount": round(converted_amount, 2)
        }

    except requests.exceptions.RequestException:
        raise HTTPException(status_code=500, detail="External API error")
