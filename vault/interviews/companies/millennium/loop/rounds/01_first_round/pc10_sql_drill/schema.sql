-- pc10 SQL drill schema. sqlite3 syntax; window functions used by part4 need sqlite >= 3.25.

CREATE TABLE instruments (
    symbol   TEXT PRIMARY KEY,
    desk     TEXT NOT NULL,     -- 'EQUITY' | 'RATES' | 'FX'
    currency TEXT NOT NULL      -- the currency this instrument is priced in, e.g. 'USD'
);

CREATE TABLE trades (
    trade_id   INTEGER PRIMARY KEY,
    symbol     TEXT,            -- NULL for a cash adjustment entry that is not tied to any instrument
    trader     TEXT NOT NULL,
    trade_date TEXT NOT NULL,   -- 'YYYY-MM-DD'
    ts         TEXT NOT NULL,   -- 'YYYY-MM-DD HH:MM:SS', full timestamp of the trade
    qty        INTEGER NOT NULL,  -- positive = buy, negative = sell
    price      REAL NOT NULL,     -- in the instrument's own currency (instruments.currency)
    FOREIGN KEY (symbol) REFERENCES instruments(symbol)
);

CREATE TABLE fx_rates (
    currency     TEXT NOT NULL,   -- e.g. 'GBP'
    rate_date    TEXT NOT NULL,   -- 'YYYY-MM-DD'
    rate_to_usd  REAL NOT NULL,   -- 1 unit of currency = rate_to_usd USD
    PRIMARY KEY (currency, rate_date)
);
