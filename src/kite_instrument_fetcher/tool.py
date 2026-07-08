from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Optional
import requests
import os


class KiteInstrumentFetcherInput(BaseModel):
    exchange: str = Field(description="Exchange name e.g. NSE, BSE, NFO")


class KiteInstrumentFetcher(BaseTool):
    name: str = "Kite Instrument Fetcher"
    description: str = "Fetches the list of tradable instruments for a given exchange from Zerodha Kite Connect API."
    args_schema: type[BaseModel] = KiteInstrumentFetcherInput

    def _run(self, exchange: str) -> str:
        api_key = os.environ.get("KITE_API_KEY")
        access_token = os.environ.get("KITE_ACCESS_TOKEN")

        if not api_key or not access_token:
            return "Error: KITE_API_KEY and KITE_ACCESS_TOKEN environment variables are required."

        headers = {
            "X-Kite-Version": "3",
            "Authorization": f"token {api_key}:{access_token}"
        }

        url = f"https://api.kite.trade/instruments/{exchange}"
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            return f"Error fetching instruments: {response.status_code} - {response.text}"

        lines = response.text.strip().split("\n")
        # Return first 50 instruments to avoid overflow
        preview = "\n".join(lines[:51])
        return f"Instruments for {exchange} (showing first 50):\n{preview}"