-- pc10 seed data. Deterministic, hand-checkable, small enough to trace by eye.

INSERT INTO instruments (symbol, desk, currency) VALUES
    ('AAPL',   'EQUITY', 'USD'),
    ('MSFT',   'EQUITY', 'USD'),
    ('VOD',    'EQUITY', 'GBP'),
    ('BUND',   'RATES',  'EUR'),
    ('GILT',   'RATES',  'GBP'),
    ('EURUSD', 'FX',     'USD'),
    ('ORPHAN', 'EQUITY', 'USD');  -- never appears in trades: a listed instrument nobody has traded

INSERT INTO trades (trade_id, symbol, trader, trade_date, ts, qty, price) VALUES
    (1,  'AAPL',   'alice',  '2026-01-05', '2026-01-05 09:30:00', 100,     150.00),
    (2,  'AAPL',   'alice',  '2026-01-05', '2026-01-05 14:00:00', -50,     151.00),
    (3,  'AAPL',   'bob',    '2026-01-05', '2026-01-05 10:00:00', 200,     150.50),
    (4,  'AAPL',   'alice',  '2026-01-06', '2026-01-06 09:15:00', 100,     152.00),
    (5,  'MSFT',   'bob',    '2026-01-05', '2026-01-05 11:00:00', 300,     310.00),
    (6,  'VOD',    'garcia', '2026-01-05', '2026-01-05 08:00:00', 500,     100.00),
    (7,  'BUND',   'dan',    '2026-01-06', '2026-01-06 09:00:00', 1000,    98.50),
    (8,  'GILT',   'garcia', '2026-01-07', '2026-01-07 09:00:00', 200,     99.00),
    (9,  'EURUSD', 'dan',    '2026-01-06', '2026-01-06 10:00:00', 100000,  1.1000),
    (10, NULL,     'garcia', '2026-01-08', '2026-01-08 12:00:00', 1,       500.00),  -- cash adjustment, not tied to any instrument
    (11, 'AAPL',   'alice',  '2026-01-08', '2026-01-08 09:00:00', 10,      153.00),
    (12, 'AAPL',   'alice',  '2026-01-09', '2026-01-09 09:00:00', 10,      154.00),
    (13, 'AAPL',   'alice',  '2026-01-10', '2026-01-10 09:00:00', 10,      155.00),
    (14, 'MSFT',   'bob',    '2026-01-06', '2026-01-06 09:00:00', 50,      309.00),
    (15, 'MSFT',   'bob',    '2026-01-09', '2026-01-09 09:00:00', 20,      311.00);

INSERT INTO fx_rates (currency, rate_date, rate_to_usd) VALUES
    ('GBP', '2026-01-05', 1.2500),
    ('GBP', '2026-01-07', 1.2700),
    ('EUR', '2026-01-06', 1.0800);
