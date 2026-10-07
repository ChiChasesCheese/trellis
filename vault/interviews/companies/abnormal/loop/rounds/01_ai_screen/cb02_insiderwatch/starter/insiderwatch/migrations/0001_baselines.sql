CREATE TABLE daily_totals (
    user TEXT NOT NULL,
    action TEXT NOT NULL,
    day TEXT NOT NULL,
    count INTEGER NOT NULL,
    total_bytes INTEGER NOT NULL,
    PRIMARY KEY (user, action, day)
);
CREATE TABLE user_activity (
    user TEXT PRIMARY KEY,
    first_day TEXT NOT NULL
);
CREATE TABLE login_countries (
    user TEXT NOT NULL,
    country TEXT NOT NULL,
    first_seen TEXT NOT NULL,
    PRIMARY KEY (user, country)
);
