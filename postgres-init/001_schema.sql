-- Initialize tables and seed data for crud_api_joint_trips
BEGIN;

DROP TABLE IF EXISTS expenseAllocations CASCADE;
DROP TABLE IF EXISTS notifications CASCADE;
DROP TABLE IF EXISTS expenses CASCADE;
DROP TABLE IF EXISTS tripMembers CASCADE;
DROP TABLE IF EXISTS tripBudgetCategories CASCADE;
DROP TABLE IF EXISTS trips CASCADE;
DROP TABLE IF EXISTS expenseTypes CASCADE;
DROP TABLE IF EXISTS currencies CASCADE;
DROP TABLE IF EXISTS users CASCADE;

CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    phone_number TEXT NOT NULL,
    avatar TEXT
);

CREATE TABLE currencies (
    id INTEGER PRIMARY KEY,
    code TEXT NOT NULL,
    name TEXT NOT NULL,
    symbol TEXT NOT NULL
);

CREATE TABLE expenseTypes (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    icon TEXT,
    color TEXT
);

CREATE TABLE trips (
    id INTEGER PRIMARY KEY,
    emoji TEXT NOT NULL,
    creator_id INTEGER REFERENCES users(id),
    title TEXT NOT NULL,
    country TEXT NOT NULL,
    startDate DATE NOT NULL,
    endDate DATE NOT NULL,
    currency_id INTEGER REFERENCES currencies(id),
    budget DOUBLE PRECISION NOT NULL,
    description TEXT
);

CREATE TABLE tripBudgetCategories (
    id INTEGER PRIMARY KEY,
    trip_id INTEGER REFERENCES trips(id),
    expense_type_id INTEGER REFERENCES expenseTypes(id),
    planned_amount DOUBLE PRECISION NOT NULL
);

CREATE TABLE tripMembers (
    id INTEGER PRIMARY KEY,
    trip_id INTEGER REFERENCES trips(id),
    member_id INTEGER REFERENCES users(id),
    status TEXT NOT NULL,
    role TEXT NOT NULL
);

CREATE TABLE expenses (
    id INTEGER PRIMARY KEY,
    trip_id INTEGER REFERENCES trips(id),
    user_id_pay INTEGER REFERENCES users(id),
    amount DOUBLE PRECISION NOT NULL,
    date DATE NOT NULL,
    type_of_expense INTEGER REFERENCES expenseTypes(id),
    description TEXT,
    currency_id INTEGER REFERENCES currencies(id)
);

CREATE TABLE expenseAllocations (
    id INTEGER PRIMARY KEY,
    expense_id INTEGER REFERENCES expenses(id),
    user_id INTEGER REFERENCES users(id),
    amount DOUBLE PRECISION NOT NULL,
    isPaid BOOLEAN NOT NULL
);

CREATE TABLE notifications (
    id INTEGER PRIMARY KEY,
    trip_id INTEGER REFERENCES trips(id),
    user_id INTEGER REFERENCES users(id),
    type TEXT NOT NULL,
    message TEXT NOT NULL,
    is_read BOOLEAN,
    created_at TIMESTAMPTZ NOT NULL
);

COMMIT;
