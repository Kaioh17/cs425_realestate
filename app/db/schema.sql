
--  To delete all tables --
--  DROP SCHEMA public CASCADE;
--  CREATE SCHEMA public;

CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  role VARCHAR(20) NOT NULL, CHECK (role IN  ('agent', 'renter')),
  first_name varchar(25) NOT NULL,
  last_name varchar(25) NOT NULL,
  email varchar(255) UNIQUE,
  created_at timestamp DEFAULT now()
  
);

CREATE TABLE renters_profile (
  id SERIAL PRIMARY KEY,
  move_in_date timestamp,
  preferred_location varchar(255),
  budget float,
  created_at timestamp DEFAULT now(),
  FOREIGN KEY (id) REFERENCES users(id)
);

CREATE TABLE agents_profile (
  id SERIAL PRIMARY KEY,
  job_title varchar,
  agency varchar NOT NULL,
  contact_info varchar NOT NULL,
  created_at timestamp DEFAULT now(),
  FOREIGN KEY (id) REFERENCES users(id) ON DELETE CASCADE

);
CREATE TABLE renter_addresses (
  id SERIAL PRIMARY KEY,
  renter_id int NOT NULL,
  street varchar(255) NOT NULL,
  city varchar(255) NOT NULL,
  state varchar(255) NOT NULL,
  zip varchar(20) NOT NULL,
  created_at timestamp DEFAULT now(),

  FOREIGN KEY (renter_id) REFERENCES renters_profile(id) ON DELETE CASCADE
);

-- CREATE TABLE payment_methods (
--   card_number varchar PRIMARY KEY,
--   renter_id SERIAL NOT NULL,
--   address varchar NOT NULL,
--   expiry_date varchar NOT NULL,
--   type varchar NOT NULL,
--   at timestamp DEFAULT now()
--   FOREIGN KEY (renter_id) REFERENCES renters_profile(id)
-- );
-- WE CHANGED THIS PAYMENT METHOD TO CREDIT_CARDS, WITH BETTER FIELDS TO HANDLE DATA

CREATE TABLE credit_cards (
  id SERIAL PRIMARY KEY,
  renter_id int NOT NULL,
  card_number varchar(20) NOT NULL, 
  card_type varchar(20) NOT NULL, CHECK(card_type IN ('visa', 'mastercard')),   -- e.g. ,visa, Master card
  billing_address_id int NOT NULL,
  expiration_month int NOT NULL,
  expiration_year int NOT NULL,
  created_at timestamp DEFAULT now(),
  FOREIGN KEY (renter_id) REFERENCES renters_profile(id) ON DELETE CASCADE,
  FOREIGN KEY (billing_address_id) REFERENCES renter_addresses(id) ON DELETE CASCADE
);


CREATE TABLE agent_assigned (
  agent_id int DEFAULT 1,
  renter_id int DEFAULT 2,
  created_at timestamp DEFAULT now(),
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
  created_at timestamp DEFAULT now()
);

CREATE TABLE apartments (
  property_id int PRIMARY KEY,
  num_rooms int NOT NULL,
  sqr_footage float NOT NULL,
  building_type varchar(25)NOT NULL,
  rental_price NUMERIC(10, 2) NOT NULL,
  nearby_schools varchar,
  created_at timestamp DEFAULT now(),
  FOREIGN KEY (property_id) REFERENCES properties(id) ON DELETE CASCADE
);

CREATE TABLE houses (
  property_id int PRIMARY KEY,
  num_rooms int NOT NULL,
  sqr_footage float NOT NULL,
  -- building_type varchar(25) NOT NULL,
  price float NOT NULL,
  rental_price NUMERIC(10, 2) NOT NULL,
  houses_availability boolean NOT NULL,
  nearby_schools varchar NOT NULL,
  created_at timestamp DEFAULT now(),
  FOREIGN KEY (property_id) REFERENCES properties(id) ON DELETE CASCADE
);

-- do you think we should create a seperate table for nearby schools? To hold the description and use a multi valued attribute? 
--  so _schools(property_id, school_name, school_address) or simply a foreign key. 

CREATE TABLE commercial_buildings (
  property_id int PRIMARY KEY, 
  sqr_footage float NOT NULL,
  -- building_type varchar NOT NULL,
  type_of_business varchar(225) NOT NULL,
  rental_price NUMERIC(10, 2) NOT NULL,
  FOREIGN KEY (property_id) REFERENCES properties(id) ON DELETE CASCADE
);

CREATE TABLE vacation_homes (
  property_id int PRIMARY KEY,
  num_rooms int NOT NULL,
  sqr_footage float NOT NULL,
  -- building_type varchar NOT NULL,
  FOREIGN KEY (property_id) REFERENCES properties(id) ON DELETE CASCADE
);

CREATE TABLE land (
  property_id int PRIMARY KEY, 
  sqr_footage float NOT NULL,
  created_at timestamp DEFAULT now(),

  FOREIGN KEY (property_id) REFERENCES properties(id) ON DELETE CASCADE
);
--can we buy a house in a real estate 
CREATE TABLE bookings (
  id SERIAL PRIMARY KEY,
  renter_id int DEFAULT 2,
  property_id int DEFAULT 1,
  start_date date NOT NULL, --start rent period
  end_date date NOT NULL, --start rent period
  payment_card_id int DEFAULT 0,
  price NUMERIC(10, 2) NOT NULL,
  booking_date timestamp DEFAULT now(),
  booking_status varchar(20) DEFAULT 'pending', CHECK (booking_status IN ('pending', 'confirmed', 'canceled')), -- 'pending', 'confirmed', 'cancelled'
  FOREIGN KEY (renter_id) REFERENCES renters_profile(id) ON DELETE SET DEFAULT,
  FOREIGN KEY (payment_card_id) REFERENCES credit_cards(id) ON DELETE SET DEFAULT,
  FOREIGN KEY (property_id) REFERENCES properties(id) ON DELETE SET DEFAULT
);

CREATE TABLE reward_program (
  renter_id int PRIMARY KEY,
  total_points NUMERIC NOT NULL,-- derived from price total bookings(sum(price)*100) per renter   -- total_points NUMERIC GENERATED ALWAYS AS((SELECT COALESCE(SUM(b.price), 0)*100
  --                                         FROM bookings b WHERE b.renter_id = renter_id))STORED 
  created_at timestamp DEFAULT now(),
  updated_at timestamp NULL, 
  FOREIGN KEY (renter_id) REFERENCES renters_profile(id) ON DELETE CASCADE
);   

COMMENT ON COLUMN reward_program.total_points IS 'derived from price total bookings(sum(price)*100) per renter';

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

-- Agents profile placeholder
INSERT INTO agents_profile (id, job_title, agency, contact_info) 
VALUES 
    (1, 'Deleted', 'Deleted Account', 'deleted@domain.com');

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
                                                              ('renter','Renter','Name', 'rentertest@gmail.com') ; --4
INSERT INTO renters_profile (id, move_in_date, preferred_location, budget) VALUES (4, '2025-09-01', 'Chicago, IL', 2500.00);
INSERT INTO agents_profile (id, job_title, agency, contact_info) VALUES (3, 'Real Estate Agent', 'DreamHomes Realty', 'test@dreamhomes.com');                                                                        
INSERT INTO  renter_addresses (renter_id, street, city, state, zip) VALUES (4, '123 State Street', 'Chicago', 'IL', '60616');
INSERT INTO credit_cards (renter_id, card_number, card_type, billing_address_id, expiration_month, expiration_year) VALUES (4, '15056415105421', 'visa', 1, 12, 2026);
INSERT INTO agent_assigned (agent_id, renter_id) VALUES (3, 4);
INSERT INTO properties (description, type, location, state, city, price, availability, crime_rates)  VALUES
                      ('Modern 2-bedroom downtown apartment', 'apartments', '2344 Main St', 'IL', 'Chicago', 2200.00, TRUE, 'Low'),
                      ('Baren land With dying weeds', 'Land', '123 Main St', 'IL', 'Chicago', 2200.00, TRUE, 'Low'),
                      ('Modern 4-bedroom downtown apartment', 'commercial buildings', '4875 Prarie St', 'IL', 'Chicago', 2200.00, TRUE, 'High'),
                      ('Perfect vacations home with a backyard pool', 'vacation homes', '123 Canem St', 'IL', 'Chicago', 2200.00, FALSE, 'High'),
                      ('Suburban 3-bedroom family home', 'houses', '4534 Elm Rd', 'IL', 'Naperville', 350000.00, TRUE, 'Medium');




INSERT INTO apartments (property_id, num_rooms, sqr_footage, building_type, rental_price, nearby_schools) VALUES (1, 2, 950.5, 'High-rise', 2200.00, 'South Loop Elementary');

INSERT INTO houses (property_id, num_rooms, sqr_footage, price, rental_price, houses_availability, nearby_schools) VALUES (5, 3, 1800.0, 350000.00, 2500.00, TRUE, 'Naperville Central High');


INSERT INTO land (property_id, sqr_footage) VALUES (2, 1456.21);

INSERT INTO commercial_buildings (property_id, sqr_footage, type_of_business, rental_price) VALUES (3, 1456.21, 'robbery & lacerny', 2023.23);


INSERT INTO bookings (renter_id, property_id, start_date, end_date, payment_card_id, price, booking_status) VALUES (4, 1, '2025-11-08', '2026-11-08', 1, 2200.00, 'confirmed');

INSERT INTO reward_program (renter_id, total_points) SELECT renter_id, SUM(price) * 100 FROM bookings WHERE renter_id = 4 GROUP BY renter_id;

