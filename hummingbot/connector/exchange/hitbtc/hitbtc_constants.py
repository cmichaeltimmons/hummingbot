# A single source of truth for constant variables related to the exchange
from hummingbot.core.api_throttler.data_types import LinkedLimitWeightPair, RateLimit

DEFAULT_DOMAIN = "com"

REST_URL = "https://api.demo.hitbtc.{}/api/"

PUBLIC_API_VERSION = "2"
PRIVATE_API_VERSION = "2"

# Public API endpoints
SYMBOL_PATH_URL = "/public/symbol"

# Private API endpoints
USER_BALANCES = "/trading/balance"

# Rate Limit Type
MARKET_DATA = "MARKET_DATA"
ORDERS = "ORDERS"
OTHER = "OTHER"

# Rate Limit time intervals
ONE_SECOND = 1
ONE_MINUTE = 60

# Ask about no max request
# Also check on weights.
MAX_REQUEST = 5000

RATE_LIMITS = [
    # For Trading, the limit is 300 requests per second for one user;
    RateLimit(limit_id=ORDERS, limit=300, time_interval=ONE_SECOND),
    # For the Market data, the limit is 100 requests per second for one IP;
    RateLimit(limit_id=MARKET_DATA, limit=100, time_interval=ONE_SECOND),
    # For other requests, including Trading history, the limit is 10 requests per second for one user
    RateLimit(limit_id=OTHER, limit=10, time_interval=ONE_SECOND),
    # Weighted Limits
    RateLimit(limit_id=SYMBOL_PATH_URL, limit=MAX_REQUEST, time_interval=ONE_MINUTE,
              linked_limits=[LinkedLimitWeightPair(MARKET_DATA, 10)]),
    RateLimit(limit_id=USER_BALANCES, limit=MAX_REQUEST, time_interval=ONE_MINUTE,
              linked_limits=[LinkedLimitWeightPair(ORDERS, 10)])
]


class Constants:
    EXCHANGE_NAME = "hitbtc"
    REST_URL = "https://api.hitbtc.com/api/2"
    REST_URL_AUTH = "/api/2"
    WS_PRIVATE_URL = "wss://api.hitbtc.com/api/2/ws/trading"
    WS_PUBLIC_URL = "wss://api.hitbtc.com/api/2/ws/public"

    HBOT_BROKER_ID = "refzzz48"

    ACCOUNTS_PATH_URL = "/account"

    ENDPOINT = {
        # Public Endpoints
        "TICKER": "public/ticker",
        "TICKER_SINGLE": "public/ticker/{trading_pair}",
        "SYMBOL": "public/symbol",
        "ORDER_BOOK": "public/orderbook",
        "ORDER_CREATE": "order",
        "ORDER_DELETE": "order/{id}",
        "ORDER_STATUS": "order/{id}",
        "USER_ORDERS": "order",
        "USER_BALANCES": "trading/balance",
    }

    WS_SUB = {
        "TRADES": "Trades",
        "ORDERS": "Orderbook",
        "USER_ORDERS_TRADES": "Reports",

    }

    WS_METHODS = {
        "ORDERS_SNAPSHOT": "snapshotOrderbook",
        "ORDERS_UPDATE": "updateOrderbook",
        "TRADES_SNAPSHOT": "snapshotTrades",
        "TRADES_UPDATE": "updateTrades",
        "USER_BALANCE": "getTradingBalance",
        "USER_ORDERS": "activeOrders",
        "USER_TRADES": "report",
    }

    # Timeouts
    MESSAGE_TIMEOUT = 30.0
    PING_TIMEOUT = 10.0
    API_CALL_TIMEOUT = 10.0
    API_MAX_RETRIES = 4

    # Intervals
    # Only used when nothing is received from WS
    SHORT_POLL_INTERVAL = 5.0
    # One minute should be fine since we get trades, orders and balances via WS
    LONG_POLL_INTERVAL = 60.0
    UPDATE_ORDER_STATUS_INTERVAL = 60.0
    # 10 minute interval to update trading rules, these would likely never change whilst running.
    INTERVAL_TRADING_RULES = 600

    # Trading pair splitter regex
    TRADING_PAIR_SPLITTER = r"^(\w+)(BTC|BCH|DAI|DDRST|EOSDT|EOS|ETH|EURS|HIT|IDRT|PAX|BUSD|GUSD|TUSD|USDC|USDT|USD)$"
