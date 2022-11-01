from decimal import Decimal
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple

from bidict import bidict

from hummingbot.connector.constants import s_decimal_NaN
from hummingbot.connector.exchange.hitbtc import hitbtc_constants as CONSTANTS, hitbtc_web_utils as web_utils
from hummingbot.connector.exchange.hitbtc.hitbtc_auth import HitbtcAuth
from hummingbot.connector.exchange.hitbtc.hitbtc_utils import translate_asset
from hummingbot.connector.exchange_py_base import ExchangePyBase
from hummingbot.connector.trading_rule import TradingRule
from hummingbot.connector.utils import combine_to_hb_trading_pair
from hummingbot.core.data_type.common import OrderType, TradeType
from hummingbot.core.data_type.in_flight_order import InFlightOrder, OrderUpdate, TradeUpdate
from hummingbot.core.data_type.order_book_tracker_data_source import OrderBookTrackerDataSource
from hummingbot.core.data_type.trade_fee import TradeFeeBase
from hummingbot.core.data_type.user_stream_tracker_data_source import UserStreamTrackerDataSource
from hummingbot.core.web_assistant.connections.data_types import RESTMethod
from hummingbot.core.web_assistant.web_assistants_factory import WebAssistantsFactory

if TYPE_CHECKING:
    from hummingbot.client.config.config_helpers import ClientConfigAdapter


class HitbtcExchange(ExchangePyBase):

    web_utils = web_utils

    def __init__(self,
                 client_config_map: "ClientConfigAdapter",
                 hitbtc_api_key: str,
                 hitbtc_api_secret: str,
                 trading_pairs: Optional[List[str]] = None,
                 trading_required: bool = True,
                 domain: str = CONSTANTS.DEFAULT_DOMAIN,
                 ):
        self.api_key = hitbtc_api_key
        self.secret_key = hitbtc_api_secret
        self._domain = domain
        self._trading_required = trading_required
        self._trading_pairs = trading_pairs
        super().__init__(client_config_map)

    @property
    def authenticator(self):
        return HitbtcAuth(
            api_key=self.api_key,
            secret_key=self.secret_key,
            time_provider=self._time_synchronizer)

    @property
    def name(self) -> str:
        return "hitbtc"

    @property
    def rate_limits_rules(self):
        return CONSTANTS.RATE_LIMITS

    @property
    def domain(self):
        return self._domain

    @property
    def client_order_id_max_length(self):
        return {}

    @property
    def client_order_id_prefix(self):
        return {}

    @property
    def trading_rules_request_path(self):
        return {}

    @property
    def trading_pairs_request_path(self):
        return CONSTANTS.SYMBOL_PATH_URL

    @property
    def check_network_request_path(self):
        return {}

    @property
    def trading_pairs(self):
        return {}

    @property
    def is_cancel_request_in_exchange_synchronous(self) -> bool:
        return {}

    @property
    def is_trading_required(self) -> bool:
        return {}

    def supported_order_types(self):
        return {}

    async def get_all_pairs_prices(self) -> List[Dict[str, str]]:
        return {}

    # Ask about this
    def _is_request_exception_related_to_time_synchronizer(self, request_exception: Exception):
        return False

    def _create_web_assistants_factory(self) -> WebAssistantsFactory:
        return web_utils.build_api_factory(
            throttler=self._throttler,
            domain=self._domain,
            auth=self._auth
        )

    def _create_order_book_data_source(self) -> OrderBookTrackerDataSource:
        return {}

    def _create_user_stream_data_source(self) -> UserStreamTrackerDataSource:
        return {}

    def _get_fee(self,
                 base_currency: str,
                 quote_currency: str,
                 order_type: OrderType,
                 order_side: TradeType,
                 amount: Decimal,
                 price: Decimal = s_decimal_NaN,
                 is_maker: Optional[bool] = None) -> TradeFeeBase:
        return {}

    async def _place_order(self,
                           order_id: str,
                           trading_pair: str,
                           amount: Decimal,
                           trade_type: TradeType,
                           order_type: OrderType,
                           price: Decimal,
                           **kwargs) -> Tuple[str, float]:
        return {}

    async def _place_cancel(self, order_id: str, tracked_order: InFlightOrder):
        return {}

    async def _format_trading_rules(self, exchange_info_dict: Dict[str, Any]) -> List[TradingRule]:
        return {}

    async def _status_polling_loop_fetch_updates(self):
        return {}

    async def _update_trading_fees(self):
        {}

    async def _user_stream_event_listener(self):
        {}

    async def _update_order_fills_from_trades(self):
        return {}

    async def _all_trade_updates_for_order(self, order: InFlightOrder) -> List[TradeUpdate]:
        return {}

    async def _request_order_status(self, tracked_order: InFlightOrder) -> OrderUpdate:
        return {}

    async def _update_balances(self):
        account_info = await self._api_request(path_url=CONSTANTS.USER_BALANCES, method=RESTMethod.GET, is_auth_required=True)
        local_asset_names = set(self._account_balances.keys())
        remote_asset_names = set()
        for account in account_info:
            asset_name = translate_asset(account["currency"])
            self._account_available_balances[asset_name] = Decimal(str(account["available"]))
            self._account_balances[asset_name] = Decimal(str(account["reserved"])) + Decimal(str(account["available"]))
            remote_asset_names.add(asset_name)

        asset_names_to_remove = local_asset_names.difference(remote_asset_names)
        for asset_name in asset_names_to_remove:
            del self._account_available_balances[asset_name]
            del self._account_balances[asset_name]

    def _initialize_trading_pair_symbols_from_exchange_info(self, exchange_info: Dict[str, Any]):
        mapping = bidict()
        for symbol_data in exchange_info:
            base = translate_asset(symbol_data['baseCurrency'])
            qoute = translate_asset(symbol_data['quoteCurrency'])
            mapping[symbol_data["id"]] = combine_to_hb_trading_pair(base=base, quote=qoute)
        return mapping

    async def _get_last_traded_price(self, trading_pair: str) -> float:
        return {}
