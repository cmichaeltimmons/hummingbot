from decimal import Decimal

from pydantic import Field, SecretStr

from hummingbot.client.config.config_data_types import BaseConnectorConfigMap, ClientFieldData
from hummingbot.core.data_type.trade_fee import TradeFeeSchema

CENTRALIZED = True
EXAMPLE_PAIR = "BTC-USD"

# Todo determine what to set buy_percent_fee_deducted_from_returns to
DEFAULT_FEES = TradeFeeSchema(
    maker_percent_fee_decimal=Decimal("0.001"),
    taker_percent_fee_decimal=Decimal("0.0025")
)


class HitbtcConfigMap(BaseConnectorConfigMap):
    connector: str = Field(default="hitbtc", client_data=None)
    hitbtc_api_key: SecretStr = Field(
        default=...,
        client_data=ClientFieldData(
            prompt=lambda cm: "Enter your HitBTC API key",
            is_secure=True,
            is_connect_key=True,
            prompt_on_new=True,
        )
    )
    hitbtc_api_secret: SecretStr = Field(
        default=...,
        client_data=ClientFieldData(
            prompt=lambda cm: "Enter your HitBTC secret key",
            is_secure=True,
            is_connect_key=True,
            prompt_on_new=True,
        )
    )

    class Config:
        title = "hitbtc"


def translate_asset(asset_name: str) -> str:
    asset_replacements = [
        ("USD", "USDT"),
    ]
    for asset_replacement in asset_replacements:
        for inv in [0, 1]:
            if asset_name == asset_replacement[inv]:
                return asset_replacement[(0 if inv else 1)]
    return asset_name


KEYS = HitbtcConfigMap.construct()
