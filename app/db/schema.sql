-- psql -U postgres -h localhost
-- To create database:
-- CREATE DATABASE realestate;
-- To delete database:
-- DROP DATABASE realestate;
-- To delete all tables:
--  DROP SCHEMA public CASCADE;
--  CREATE SCHEMA public;

--  To delete properties table and all child tables --
--  (recommended - drops all dependent tables automatically)
--  DROP TABLE IF EXISTS <table_name> CASCADE;
-- DROP VIEW IF EXISTS view_name;

-- to create tables:
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  role VARCHAR(20) NOT NULL, CHECK (role IN  ('agent', 'renter')),
  first_name varchar(25) NOT NULL,
  last_name varchar(25) NOT NULL,
  email varchar(255) UNIQUE,
  created_at timestamp DEFAULT now(),
  updated_at timestamp DEFAULT now()  -- Added updated_at column
);

CREATE TABLE  agencies(
  id serial primary key,
  agency_name varchar(255) not null UNIQUE,
  agency_email varchar(255) not null UNIQUE,
  created_at timestamp DEFAULT now(),
  updated_at timestamp DEFAULT now()
);

CREATE TABLE renters_profile (
  id SERIAL PRIMARY KEY,
  move_in_date timestamp,
  preferred_location varchar(255),
  budget float,
  created_at timestamp DEFAULT now(),
  updated_at timestamp DEFAULT now(),  -- Added updated_at column
  FOREIGN KEY (id) REFERENCES users(id)
);

CREATE TABLE agents_profile (
  id SERIAL PRIMARY KEY,
  job_title varchar,
  agency_id int NOT NULL,
  contact_info varchar NOT NULL,
  created_at timestamp DEFAULT now(),
  updated_at timestamp DEFAULT now(),  -- Added updated_at column
  FOREIGN KEY (id) REFERENCES users(id) ON DELETE CASCADE,
  FOREIGN KEY (agency_id) REFERENCES agencies(id) ON DELETE CASCADE

);



CREATE TABLE renter_addresses (
  id SERIAL PRIMARY KEY,
  renter_id int NOT NULL,
  street varchar(255) NOT NULL,
  city varchar(255) NOT NULL,
  state varchar(255) NOT NULL,
  zip varchar(20) NOT NULL,
  created_at timestamp DEFAULT now(),
  updated_at timestamp DEFAULT now(),  -- Added updated_at column
  FOREIGN KEY (renter_id) REFERENCES renters_profile(id) ON DELETE CASCADE
);

CREATE TABLE credit_cards (
  id SERIAL PRIMARY KEY,
  renter_id int NOT NULL,
  card_number varchar(20) NOT NULL, 
  card_type varchar(20) NOT NULL, CHECK(card_type IN ('visa', 'mastercard')),
  billing_address_id int NOT NULL,
  expiration_month int NOT NULL,
  expiration_year int NOT NULL,
  created_at timestamp DEFAULT now(),
  updated_at timestamp DEFAULT now(),  -- Added updated_at column
  FOREIGN KEY (renter_id) REFERENCES renters_profile(id) ON DELETE CASCADE,
  FOREIGN KEY (billing_address_id) REFERENCES renter_addresses(id) ON DELETE CASCADE
);

CREATE TABLE agent_assigned (
  agent_id int DEFAULT 1,
  renter_id int DEFAULT 2,
  created_at timestamp DEFAULT now(),
  updated_at timestamp DEFAULT now(),  -- Added updated_at column
  PRIMARY KEY (agent_id, renter_id),
  FOREIGN KEY (agent_id) REFERENCES agents_profile(id) ON DELETE SET DEFAULT,
  FOREIGN key (renter_id) REFERENCES renters_profile(id) ON DELETE SET DEFAULT
);

CREATE TABLE properties (
  id SERIAL PRIMARY KEY,
  description text NOT NULL,
  type varchar(50) NOT NULL,
  location varchar(255) NOT NULL,
  state varchar(25) NOT NULL,
  city varchar(25) NOT NULL,
  price NUMERIC(10, 2) NOT NULL,
  availability boolean NOT NULL,
  crime_rates varchar(20) NOT NULL,
  created_at timestamp DEFAULT now(),
  updated_at timestamp DEFAULT now()  -- Added updated_at column
);

CREATE TABLE apartments (
  property_id int PRIMARY KEY,
  num_rooms int NOT NULL,
  sqr_footage float NOT NULL,
  building_type varchar(25) NOT NULL,
  rental_price NUMERIC(10, 2) NOT NULL, 
  nearby_schools varchar,
  created_at timestamp DEFAULT now(),
  updated_at timestamp DEFAULT now(),  -- Added updated_at column
  FOREIGN KEY (property_id) REFERENCES properties(id) ON DELETE CASCADE
);

CREATE TABLE houses (
  property_id int PRIMARY KEY,
  num_rooms int NOT NULL,
  sqr_footage float NOT NULL,
  rental_price NUMERIC(10, 2) NOT NULL,
  houses_availability boolean NOT NULL,
  nearby_schools varchar NOT NULL,
  created_at timestamp DEFAULT now(),
  updated_at timestamp DEFAULT now(),  -- Added updated_at column
  FOREIGN KEY (property_id) REFERENCES properties(id) ON DELETE CASCADE
);

CREATE TABLE commercial_buildings (
  property_id int PRIMARY KEY, 
  sqr_footage float NOT NULL,
  type_of_business varchar(225) NOT NULL,
  rental_price NUMERIC(10, 2) NOT NULL,
  created_at timestamp DEFAULT now(),
  updated_at timestamp DEFAULT now(),  -- Added updated_at column
  FOREIGN KEY (property_id) REFERENCES properties(id) ON DELETE CASCADE
);

CREATE TABLE vacation_homes (
  property_id int PRIMARY KEY,
  num_rooms int NOT NULL,
  sqr_footage float NOT NULL,
  created_at timestamp DEFAULT now(),
  updated_at timestamp DEFAULT now(),  -- Added updated_at column
  FOREIGN KEY (property_id) REFERENCES properties(id) ON DELETE CASCADE
);

CREATE TABLE land (
  property_id int PRIMARY KEY, 
  sqr_footage float NOT NULL,
  created_at timestamp DEFAULT now(),
  updated_at timestamp DEFAULT now(),  -- Added updated_at column
  FOREIGN KEY (property_id) REFERENCES properties(id) ON DELETE CASCADE
);

CREATE TABLE bookings (
  id SERIAL PRIMARY KEY,
  renter_id int DEFAULT 2,
  property_id int DEFAULT 1,
  start_date date NOT NULL,
  end_date date NOT NULL,
  payment_card_id int DEFAULT 0,
  price NUMERIC(10, 2) NOT NULL,
  booking_date timestamp DEFAULT now(),
  booking_status varchar(20) DEFAULT 'pending', CHECK (booking_status IN ('pending', 'confirmed', 'canceled')),
  created_at timestamp DEFAULT now(),
  updated_at timestamp DEFAULT now(),  -- Added updated_at column
  FOREIGN KEY (renter_id) REFERENCES renters_profile(id) ON DELETE SET DEFAULT,
  FOREIGN KEY (payment_card_id) REFERENCES credit_cards(id) ON DELETE SET DEFAULT,
  FOREIGN KEY (property_id) REFERENCES properties(id) ON DELETE SET DEFAULT
);

create table agency_property(
    property_id int NOT NULL,
    agency_id int NOT NULL,
    created_at timestamp DEFAULT now(),
    updated_at timestamp DEFAULT now(),
    FOREIGN KEY (agency_id) REFERENCES agencies(id) ON DELETE CASCADE,
    FOREIGN KEY (property_id) REFERENCES properties(id) ON DELETE CASCADE
    
);
--keeps track of who updated what
create table property_update_log(
    property_id int Not NULL,
    agent_id int NOT Null,
    logged_at timestamp DEFAULT now(),
    foreign key (agent_id) references agents_profile(id) on delete cascade,
    foreign key (property_id) references properties(id) on delete cascade
);




-- We switched to view so total_points is always up-to-data and automatically calculating from bookings avoiding redundancy. 
CREATE OR REPLACE VIEW renter_reward_view AS (select renter_id, sum(price *10) as total_points from bookings group by renter_id);
-- COMMENT ON COLUMN reward_program.total_points IS 'derived from price total bookings(sum(price)*100) per renter';

--TEST DATA

-- Delete on cascade constraint if needed
-- alter table credit_cards add constraint credit_cards_billing_address_id_fkey foreign key (b
-- illing_address_id) references renter_addresses (id) on delete cascade; -- if needed
-- deleted placeholders

-- Users table placeholder for deleted accounts
INSERT INTO users (role, first_name, last_name, email) 
VALUES 
    ('agent', 'Default', 'Deleted', 'agentdeleted@gmail.com'), --1
    ('renter', 'Default', 'Deleted', 'renterdeleted@gmail.com'); --2

-- Renters profile placeholder
INSERT INTO renters_profile (id, move_in_date, preferred_location, budget) 
VALUES 
    (2, '1970-01-01', 'N/A', 0.00);

-- Agencies placeholder for deleted accounts
INSERT INTO agencies (agency_name, agency_email) 
VALUES 
    ('Deleted Agency', 'deleted@domain.com'); -- 1

-- Agents profile placeholder
INSERT INTO agents_profile (id, job_title, agency_id, contact_info) 
VALUES 
    (1, 'Deleted', 1, 'deleted@domain.com');

--Properties Place holder
INSERT INTO properties (description, type, location, state, city, price, availability, crime_rates) 
VALUES ('Deleted property placeholder', 'N/A', 'N/A', 'N/A', 'N/A', 0.00, FALSE, 'N/A'); --1

INSERT INTO renter_addresses 
(renter_id, street, city, state, zip, created_at) 
VALUES 
(2, 'N/A', 'N/A', 'N/A', '00000', now()); --1

--Credit Cards placeholder
INSERT INTO credit_cards 
(renter_id, card_number, card_type, billing_address_id, expiration_month, expiration_year, created_at) 
VALUES 
(2, '0000-0000-0000-0000', 'visa', 1, 0, 1970, now());

INSERT INTO users (role, first_name, last_name, email) VALUES ('agent','Add','Name', 'admintest@gmail.com'), -- 3
                                                              ('renter','Renter','Name', 'rentertest@gmail.com'), --4
                                                              ('renter','John','Smith', 'johnsmith@gmail.com'); --5
INSERT INTO renters_profile (id, move_in_date, preferred_location, budget) VALUES 
(4, '2025-09-01', 'Chicago, IL', 2500.00),
(5, '2025-10-15', 'Naperville, IL', 3000.00);
-- Agency for test agent
INSERT INTO agencies (agency_name, agency_email) 
VALUES 
    ('DreamHomes Realty', 'info@dreamhomes.com'); -- 2
INSERT INTO agents_profile (id, job_title, agency_id, contact_info) VALUES (3, 'Real Estate Agent', 2, 'test@dreamhomes.com');                                                                        
INSERT INTO  renter_addresses (renter_id, street, city, state, zip) VALUES 
(4, '123 State Street', 'Chicago', 'IL', '60616'),
(5, '456 Oak Avenue', 'Naperville', 'IL', '60540');
INSERT INTO credit_cards (renter_id, card_number, card_type, billing_address_id, expiration_month, expiration_year) VALUES 
(4, '15056415105421', 'visa', 1, 12, 2026),
(5, '98765432109876', 'mastercard', 2, 6, 2027);
INSERT INTO agent_assigned (agent_id, renter_id) VALUES (3, 4), (3, 5);
-- Properties: 5 apartments (1-5), 5 houses (6-10), 5 commercial buildings (11-15), 5 vacation homes (16-20), 5 land (21-25)
INSERT INTO properties (description, type, location, state, city, price, availability, crime_rates) VALUES
-- Apartments (property_id 1-5)
('Modern 2-bedroom downtown apartment', 'apartments', '2344 Main St', 'IL', 'Chicago', 1222200.00, TRUE, 'Low'),
('Luxury 1-bedroom studio with city views', 'apartments', '5678 Lake Shore Dr', 'IL', 'Chicago', 850000.00, TRUE, 'Low'),
('Spacious 3-bedroom apartment near parks', 'apartments', '1234 Oak Ave', 'IL', 'Evanston', 950000.00, TRUE, 'Low'),
('Cozy 1-bedroom apartment in historic building', 'apartments', '7890 Elm St', 'IL', 'Chicago', 650000.00, FALSE, 'Medium'),
('Modern 4-bedroom penthouse with balcony', 'apartments', '4567 Michigan Ave', 'IL', 'Chicago', 1850000.00, TRUE, 'Low'),
-- Houses (property_id 6-10)
('Suburban 3-bedroom family home', 'houses', '4534 Elm Rd', 'IL', 'Naperville', 350000.00, TRUE, 'Medium'),
('Charming 4-bedroom Victorian house', 'houses', '2345 Maple Dr', 'IL', 'Oak Park', 425000.00, TRUE, 'Low'),
('Modern 5-bedroom new construction', 'houses', '6789 Pine St', 'IL', 'Schaumburg', 550000.00, TRUE, 'Low'),
('Classic 3-bedroom ranch style home', 'houses', '3456 Cedar Ln', 'IL', 'Aurora', 280000.00, FALSE, 'Medium'),
('Luxury 6-bedroom estate with pool', 'houses', '8901 River Rd', 'IL', 'Winnetka', 1200000.00, TRUE, 'Low'),
-- Commercial Buildings (property_id 11-15)
('Prime retail space in downtown', 'commercial_buildings', '4875 Prairie St', 'IL', 'Chicago', 122200.00, TRUE, 'High'),
('Office building with parking garage', 'commercial_buildings', '1234 Business Blvd', 'IL', 'Chicago', 2500000.00, TRUE, 'Medium'),
('Restaurant space in busy district', 'commercial_buildings', '5678 Commerce Ave', 'IL', 'Chicago', 850000.00, TRUE, 'Medium'),
('Warehouse facility with loading docks', 'commercial_buildings', '9012 Industrial Way', 'IL', 'Elk Grove', 1800000.00, TRUE, 'Low'),
('Medical office building near hospital', 'commercial_buildings', '3456 Health Dr', 'IL', 'Chicago', 2100000.00, FALSE, 'Low'),
-- Vacation Homes (property_id 16-20)
('Perfect vacation home with backyard pool', 'vacation_homes', '123 Canem St', 'IL', 'Chicago', 2200.00, FALSE, 'High'),
('Lakeside cabin with private dock', 'vacation_homes', '789 Lake View Dr', 'IL', 'Lake Forest', 450000.00, TRUE, 'Low'),
('Mountain retreat with scenic views', 'vacation_homes', '2345 Hilltop Rd', 'IL', 'Galena', 380000.00, TRUE, 'Low'),
('Beachfront cottage near the shore', 'vacation_homes', '5678 Shoreline Ave', 'IL', 'Waukegan', 520000.00, TRUE, 'Medium'),
('Rustic log cabin in the woods', 'vacation_homes', '9012 Forest Trail', 'IL', 'Barrington', 320000.00, FALSE, 'Low'),
-- Land (property_id 21-25)
('Bare land with dying weeds', 'land', '123 Main St', 'IL', 'Chicago', 222300.00, TRUE, 'Low'),
('Prime development lot in suburbs', 'land', '4567 Development Way', 'IL', 'Naperville', 150000.00, TRUE, 'Low'),
('Wooded acreage for building', 'land', '7890 Timber Ln', 'IL', 'Crystal Lake', 95000.00, TRUE, 'Low'),
('Corner lot in residential area', 'land', '2345 Corner St', 'IL', 'Schaumburg', 180000.00, FALSE, 'Medium'),
('Large rural parcel with road access', 'land', '5678 Country Rd', 'IL', 'Joliet', 125000.00, TRUE, 'Low');

-- Apartments data (property_id 1-5)
INSERT INTO apartments (property_id, num_rooms, sqr_footage, building_type, rental_price, nearby_schools) VALUES
(1, 2, 950.5, 'High-rise', 2200.00, 'South Loop Elementary'),
(2, 1, 650.0, 'High-rise', 1800.00, 'Lincoln Park Elementary'),
(3, 3, 1200.0, 'Mid-rise', 2800.00, 'Evanston Central School'),
(4, 1, 550.0, 'Historic', 1500.00, 'Old Town Academy'),
(5, 4, 1800.0, 'Luxury High-rise', 4500.00, 'Magnificent Mile Prep');

-- Houses data (property_id 6-10)
INSERT INTO houses (property_id, num_rooms, sqr_footage, rental_price, houses_availability, nearby_schools) VALUES
(6, 3, 1800.0, 2500.00, TRUE, 'Naperville Central High'),
(7, 4, 2200.0, 3200.00, TRUE, 'Oak Park Elementary'),
(8, 5, 2800.0, 4200.00, TRUE, 'Schaumburg High School'),
(9, 3, 1600.0, 2200.00, FALSE, 'Aurora Middle School'),
(10, 6, 3500.0, 6500.00, TRUE, 'Winnetka Academy');

-- Commercial Buildings data (property_id 11-15)
INSERT INTO commercial_buildings (property_id, sqr_footage, type_of_business, rental_price) VALUES
(11, 1456.21, 'Retail & Shopping', 2023.23),
(12, 5000.0, 'Office Space', 8500.00),
(13, 2500.0, 'Restaurant & Dining', 4500.00),
(14, 8000.0, 'Warehouse & Storage', 12000.00),
(15, 3500.0, 'Medical & Healthcare', 6500.00);

-- Vacation Homes data (property_id 16-20)
INSERT INTO vacation_homes (property_id, num_rooms, sqr_footage) VALUES
(16, 3, 1500.0),
(17, 4, 2000.0),
(18, 3, 1800.0),
(19, 5, 2400.0),
(20, 2, 1200.0);

-- Land data (property_id 21-25)
INSERT INTO land (property_id, sqr_footage) VALUES
(21, 1456.21),
(22, 2000.0),
(23, 5000.0),
(24, 3000.0),
(25, 10000.0);


-- Bookings: 3 for renter_id = 5, 8 for renter_id = 4
INSERT INTO bookings (renter_id, property_id, start_date, end_date, payment_card_id, price, booking_status) VALUES 
-- Bookings for renter_id = 5 (3 bookings)
(5, 6, '2025-12-01', '2026-06-01', 2, 15000.00, 'confirmed'), -- House rental (6 months)
(5, 17, '2025-11-15', '2025-12-15', 2, 4500.00, 'pending'), -- Vacation home (1 month)
(5, 2, '2026-01-01', '2026-12-31', 2, 21600.00, 'confirmed'), -- Apartment rental (1 year)
-- Bookings for renter_id = 4 (8 bookings)
(4, 1, '2025-11-08', '2026-11-08', 1, 26400.00, 'confirmed'), -- Apartment (1 year)
(4, 7, '2025-12-01', '2026-03-01', 1, 9600.00, 'confirmed'), -- House (3 months)
(4, 3, '2026-02-01', '2026-08-01', 1, 16800.00, 'pending'), -- Apartment (6 months)
(4, 8, '2026-04-15', '2026-07-15', 1, 12600.00, 'confirmed'), -- House (3 months)
(4, 18, '2025-12-20', '2026-01-05', 1, 3200.00, 'confirmed'), -- Vacation home (2 weeks)
(4, 12, '2026-01-01', '2026-12-31', 1, 102000.00, 'pending'), -- Commercial building (1 year)
(4, 9, '2026-05-01', '2026-11-01', 1, 13200.00, 'confirmed'), -- House (6 months)
(4, 19, '2026-06-01', '2026-06-15', 1, 2400.00, 'pending'); -- Vacation home (2 weeks)

-- Agent-Property links for properties 1-25
-- All properties assigned to DreamHomes Realty (agency_id 2)
INSERT INTO agency_property (property_id, agency_id) VALUES
-- Apartments (property_id 1-5)
(1, 2), (2, 2), (3, 2), (4, 2), (5, 2),
-- Houses (property_id 6-10)
(6, 2), (7, 2), (8, 2), (9, 2), (10, 2),
-- Commercial Buildings (property_id 11-15)
(11, 2), (12, 2), (13, 2), (14, 2), (15, 2),
-- Vacation Homes (property_id 16-20)
(16, 2), (17, 2), (18, 2), (19, 2), (20, 2),
-- Land (property_id 21-25)
(21, 2), (22, 2), (23, 2), (24, 2), (25, 2);

