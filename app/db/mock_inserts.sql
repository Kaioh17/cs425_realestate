-- Mock Input Data: 15 properties per type (75 total)
-- Properties start from ID 27 (after schema.sql test data ends at 25)
-- All properties have availability = TRUE

-- ============================================================================
-- APARTMENTS (property_id 27-41)
-- ============================================================================
INSERT INTO properties (description, type, location, state, city, price, availability, crime_rates) VALUES
-- Low crime rate apartments
('Luxury waterfront apartment with balcony', 'apartments', '100 Ocean Drive', 'FL', 'Miami', 1250000.00, TRUE, 'Low'),
('Modern studio in financial district', 'apartments', '250 Wall Street', 'NY', 'New York', 850000.00, TRUE, 'Low'),
('Spacious 2-bedroom with mountain views', 'apartments', '500 Mountain View Ave', 'CO', 'Denver', 650000.00, TRUE, 'Low'),
('Historic loft in arts district', 'apartments', '789 Arts Boulevard', 'TX', 'Austin', 720000.00, TRUE, 'Low'),
('High-rise apartment with city skyline views', 'apartments', '1200 Skyline Tower', 'CA', 'Los Angeles', 1100000.00, TRUE, 'Low'),
-- Medium crime rate apartments
('Cozy 1-bedroom near university', 'apartments', '456 College Ave', 'MA', 'Boston', 580000.00, TRUE, 'Medium'),
('Renovated 3-bedroom family apartment', 'apartments', '234 Family Street', 'GA', 'Atlanta', 420000.00, TRUE, 'Medium'),
('Modern apartment in up-and-coming neighborhood', 'apartments', '567 Growth Lane', 'NC', 'Charlotte', 380000.00, TRUE, 'Medium'),
('Affordable 2-bedroom with parking', 'apartments', '890 Park Place', 'AZ', 'Phoenix', 350000.00, TRUE, 'Medium'),
('Stylish apartment near downtown', 'apartments', '123 Downtown Plaza', 'WA', 'Seattle', 750000.00, TRUE, 'Medium'),
-- High crime rate apartments
('Budget-friendly studio apartment', 'apartments', '321 Budget Street', 'NV', 'Las Vegas', 280000.00, TRUE, 'High'),
('Compact 1-bedroom urban living', 'apartments', '654 Urban Way', 'OR', 'Portland', 450000.00, TRUE, 'High'),
('Affordable housing in city center', 'apartments', '987 Center Street', 'PA', 'Philadelphia', 320000.00, TRUE, 'High'),
('Basic apartment with utilities included', 'apartments', '147 Utility Road', 'MI', 'Detroit', 180000.00, TRUE, 'High'),
('Economical 2-bedroom apartment', 'apartments', '258 Economy Drive', 'IL', 'Rockford', 220000.00, TRUE, 'High');

-- Apartments child table data (property_id 27-41)
INSERT INTO apartments (property_id, num_rooms, sqr_footage, building_type, rental_price, nearby_schools) VALUES
(27, 2, 1200.0, 'Luxury High-rise', 3500.00, 'Miami Beach Elementary'),
(28, 1, 600.0, 'High-rise', 3200.00, 'Financial District Prep'),
(29, 2, 1100.0, 'Mid-rise', 2400.00, 'Mountain View Academy'),
(30, 2, 1000.0, 'Historic', 2200.00, 'Arts District School'),
(31, 3, 1500.0, 'Luxury High-rise', 4500.00, 'Skyline Elementary'),
(32, 1, 550.0, 'Mid-rise', 1800.00, 'Boston University Area'),
(33, 3, 1300.0, 'Mid-rise', 2800.00, 'Family Neighborhood School'),
(34, 2, 950.0, 'Low-rise', 2000.00, 'Growth District Elementary'),
(35, 2, 900.0, 'Low-rise', 1600.00, 'Park Place Academy'),
(36, 2, 1050.0, 'High-rise', 2800.00, 'Downtown Prep School'),
(37, 1, 500.0, 'Low-rise', 1200.00, 'Budget Street Elementary'),
(38, 1, 580.0, 'Mid-rise', 1500.00, 'Urban Way School'),
(39, 1, 520.0, 'Low-rise', 1100.00, 'Center Street Academy'),
(40, 1, 480.0, 'Low-rise', 900.00, 'Utility Road Elementary'),
(41, 2, 850.0, 'Low-rise', 1400.00, 'Economy Drive School');

-- ============================================================================
-- HOUSES (property_id 42-56)
-- ============================================================================
INSERT INTO properties (description, type, location, state, city, price, availability, crime_rates) VALUES
-- Low crime rate houses
('Luxury estate with pool and tennis court', 'houses', '1000 Estate Drive', 'CA', 'Beverly Hills', 8500000.00, TRUE, 'Low'),
('Modern 5-bedroom family home', 'houses', '2500 Suburban Lane', 'WA', 'Bellevue', 1200000.00, TRUE, 'Low'),
('Charming Victorian house with garden', 'houses', '567 Heritage Street', 'MA', 'Cambridge', 950000.00, TRUE, 'Low'),
('Spacious ranch-style home', 'houses', '890 Ranch Road', 'TX', 'Dallas', 650000.00, TRUE, 'Low'),
('Contemporary home with smart features', 'houses', '1234 Tech Avenue', 'CO', 'Boulder', 780000.00, TRUE, 'Low'),
-- Medium crime rate houses
('Family-friendly 4-bedroom home', 'houses', '3456 Family Circle', 'GA', 'Atlanta', 480000.00, TRUE, 'Medium'),
('Traditional 3-bedroom suburban home', 'houses', '4567 Suburb Street', 'NC', 'Raleigh', 420000.00, TRUE, 'Medium'),
('Updated 4-bedroom with finished basement', 'houses', '5678 Basement Blvd', 'AZ', 'Scottsdale', 550000.00, TRUE, 'Medium'),
('Cozy 3-bedroom starter home', 'houses', '6789 Starter Lane', 'FL', 'Tampa', 380000.00, TRUE, 'Medium'),
('Well-maintained 5-bedroom home', 'houses', '7890 Maintenance Way', 'NY', 'Buffalo', 520000.00, TRUE, 'Medium'),
-- High crime rate houses
('Affordable 3-bedroom fixer-upper', 'houses', '9012 Fixer Street', 'PA', 'Pittsburgh', 180000.00, TRUE, 'High'),
('Basic 2-bedroom house', 'houses', '1011 Basic Road', 'MI', 'Flint', 95000.00, TRUE, 'High'),
('Economical 3-bedroom home', 'houses', '1112 Economy Avenue', 'IL', 'Peoria', 150000.00, TRUE, 'High'),
('Renovation project 4-bedroom', 'houses', '1213 Project Drive', 'NV', 'Reno', 220000.00, TRUE, 'High'),
('Budget-friendly 3-bedroom house', 'houses', '1314 Budget Boulevard', 'OR', 'Eugene', 280000.00, TRUE, 'High');

-- Houses child table data (property_id 42-56)
INSERT INTO houses (property_id, num_rooms, sqr_footage, rental_price, houses_availability, nearby_schools) VALUES
(42, 6, 5000.0, 15000.00, TRUE, 'Beverly Hills Prep'),
(43, 5, 3500.0, 8500.00, TRUE, 'Bellevue High School'),
(44, 4, 2800.0, 6500.00, TRUE, 'Cambridge Academy'),
(45, 4, 2400.0, 4200.00, TRUE, 'Dallas Suburban School'),
(46, 5, 3200.0, 5800.00, TRUE, 'Boulder Tech School'),
(47, 4, 2200.0, 3800.00, TRUE, 'Family Circle Elementary'),
(48, 3, 1800.0, 2800.00, TRUE, 'Suburb Street Middle School'),
(49, 4, 2500.0, 4200.00, TRUE, 'Basement Blvd High'),
(50, 3, 1600.0, 2400.00, TRUE, 'Starter Lane Elementary'),
(51, 5, 3000.0, 4800.00, TRUE, 'Maintenance Way Academy'),
(52, 3, 1400.0, 1800.00, TRUE, 'Fixer Street School'),
(53, 2, 1100.0, 1200.00, TRUE, 'Basic Road Elementary'),
(54, 3, 1500.0, 1600.00, TRUE, 'Economy Avenue Middle'),
(55, 4, 2000.0, 2400.00, TRUE, 'Project Drive High'),
(56, 3, 1700.0, 2200.00, TRUE, 'Budget Boulevard Elementary');

-- ============================================================================
-- COMMERCIAL BUILDINGS (property_id 57-71)
-- ============================================================================
INSERT INTO properties (description, type, location, state, city, price, availability, crime_rates) VALUES
-- Low crime rate commercial
('Prime office space in business district', 'commercial_buildings', '500 Business Plaza', 'NY', 'New York', 5000000.00, TRUE, 'Low'),
('Modern retail storefront', 'commercial_buildings', '1200 Retail Row', 'CA', 'San Francisco', 3200000.00, TRUE, 'Low'),
('Medical office building', 'commercial_buildings', '800 Medical Center', 'TX', 'Houston', 2800000.00, TRUE, 'Low'),
('Professional services building', 'commercial_buildings', '600 Professional Way', 'WA', 'Seattle', 3500000.00, TRUE, 'Low'),
('Tech startup office space', 'commercial_buildings', '900 Innovation Hub', 'CO', 'Denver', 2400000.00, TRUE, 'Low'),
-- Medium crime rate commercial
('Shopping center anchor space', 'commercial_buildings', '1500 Shopping Mall', 'FL', 'Orlando', 1800000.00, TRUE, 'Medium'),
('Restaurant space with patio', 'commercial_buildings', '700 Restaurant Row', 'GA', 'Atlanta', 1200000.00, TRUE, 'Medium'),
('Warehouse with office space', 'commercial_buildings', '2000 Warehouse District', 'NC', 'Charlotte', 1500000.00, TRUE, 'Medium'),
('Fitness center facility', 'commercial_buildings', '1100 Fitness Avenue', 'AZ', 'Phoenix', 950000.00, TRUE, 'Medium'),
('Auto repair shop building', 'commercial_buildings', '800 Auto Row', 'MA', 'Worcester', 750000.00, TRUE, 'Medium'),
-- High crime rate commercial
('Budget retail space', 'commercial_buildings', '400 Budget Plaza', 'PA', 'Philadelphia', 450000.00, TRUE, 'High'),
('Small office building', 'commercial_buildings', '300 Office Complex', 'MI', 'Detroit', 380000.00, TRUE, 'High'),
('Warehouse facility', 'commercial_buildings', '500 Industrial Park', 'IL', 'Rockford', 420000.00, TRUE, 'High'),
('Storefront in urban area', 'commercial_buildings', '600 Urban Storefront', 'NV', 'Las Vegas', 550000.00, TRUE, 'High'),
('Basic commercial space', 'commercial_buildings', '350 Basic Business', 'OR', 'Portland', 480000.00, TRUE, 'High');

-- Commercial buildings child table data (property_id 57-71)
INSERT INTO commercial_buildings (property_id, sqr_footage, type_of_business, rental_price) VALUES
(57, 10000.0, 'Office Space', 25000.00),
(58, 3500.0, 'Retail & Shopping', 12000.00),
(59, 5000.0, 'Medical & Healthcare', 18000.00),
(60, 4500.0, 'Professional Services', 15000.00),
(61, 6000.0, 'Technology & Innovation', 20000.00),
(62, 8000.0, 'Retail & Shopping', 15000.00),
(63, 2500.0, 'Restaurant & Dining', 8000.00),
(64, 12000.0, 'Warehouse & Storage', 18000.00),
(65, 4000.0, 'Fitness & Recreation', 10000.00),
(66, 3000.0, 'Automotive Services', 6500.00),
(67, 2000.0, 'Retail & Shopping', 4500.00),
(68, 2500.0, 'Office Space', 5500.00),
(69, 5000.0, 'Warehouse & Storage', 8000.00),
(70, 1800.0, 'Retail & Shopping', 5000.00),
(71, 2200.0, 'General Business', 4800.00);

-- ============================================================================
-- VACATION HOMES (property_id 72-86)
-- ============================================================================
INSERT INTO properties (description, type, location, state, city, price, availability, crime_rates) VALUES
-- Low crime rate vacation homes
('Beachfront villa with private access', 'vacation_homes', '100 Beach Road', 'FL', 'Key West', 2500000.00, TRUE, 'Low'),
('Mountain cabin with hot tub', 'vacation_homes', '500 Mountain Trail', 'CO', 'Aspen', 1800000.00, TRUE, 'Low'),
('Lakeside retreat with dock', 'vacation_homes', '800 Lake Shore', 'CA', 'Lake Tahoe', 2200000.00, TRUE, 'Low'),
('Ski-in ski-out chalet', 'vacation_homes', '1200 Ski Slope', 'UT', 'Park City', 1900000.00, TRUE, 'Low'),
('Oceanfront cottage', 'vacation_homes', '600 Ocean View', 'CA', 'Malibu', 3200000.00, TRUE, 'Low'),
-- Medium crime rate vacation homes
('Countryside farmhouse', 'vacation_homes', '700 Farm Road', 'VT', 'Stowe', 650000.00, TRUE, 'Medium'),
('Riverside cabin', 'vacation_homes', '400 River Bend', 'OR', 'Bend', 580000.00, TRUE, 'Medium'),
('Desert retreat', 'vacation_homes', '900 Desert Oasis', 'AZ', 'Sedona', 750000.00, TRUE, 'Medium'),
('Forest hideaway', 'vacation_homes', '300 Forest Path', 'WA', 'Leavenworth', 620000.00, TRUE, 'Medium'),
('Hilltop getaway', 'vacation_homes', '550 Hilltop Drive', 'NC', 'Asheville', 680000.00, TRUE, 'Medium'),
-- High crime rate vacation homes
('Budget beach house', 'vacation_homes', '200 Budget Beach', 'SC', 'Myrtle Beach', 320000.00, TRUE, 'High'),
('Rustic cabin in woods', 'vacation_homes', '350 Woodland Trail', 'AR', 'Hot Springs', 280000.00, TRUE, 'High'),
('Simple lake house', 'vacation_homes', '450 Simple Lake', 'TN', 'Gatlinburg', 380000.00, TRUE, 'High'),
('Basic mountain cabin', 'vacation_homes', '250 Basic Mountain', 'WV', 'Snowshoe', 290000.00, TRUE, 'High'),
('Economical vacation home', 'vacation_homes', '380 Economy Escape', 'KY', 'Lexington', 350000.00, TRUE, 'High');

-- Vacation homes child table data (property_id 72-86)
INSERT INTO vacation_homes (property_id, num_rooms, sqr_footage) VALUES
(72, 4, 2800.0),
(73, 3, 2200.0),
(74, 5, 3200.0),
(75, 4, 2600.0),
(76, 6, 4000.0),
(77, 3, 1800.0),
(78, 2, 1400.0),
(79, 3, 2000.0),
(80, 2, 1600.0),
(81, 3, 1900.0),
(82, 2, 1200.0),
(83, 2, 1100.0),
(84, 3, 1700.0),
(85, 2, 1300.0),
(86, 3, 1500.0);

-- ============================================================================
-- LAND (property_id 87-101)
-- ============================================================================
INSERT INTO properties (description, type, location, state, city, price, availability, crime_rates) VALUES
-- Low crime rate land
('Prime development land in suburbs', 'land', '1000 Development Way', 'TX', 'Austin', 850000.00, TRUE, 'Low'),
('Waterfront building lot', 'land', '500 Waterfront Drive', 'FL', 'Naples', 1200000.00, TRUE, 'Low'),
('Mountain view acreage', 'land', '800 Mountain View', 'CO', 'Vail', 950000.00, TRUE, 'Low'),
('Suburban residential lot', 'land', '600 Suburban Plot', 'CA', 'Irvine', 750000.00, TRUE, 'Low'),
('Rural estate land', 'land', '1200 Estate Road', 'WA', 'Spokane', 680000.00, TRUE, 'Low'),
-- Medium crime rate land
('Commercial development site', 'land', '900 Commercial Site', 'GA', 'Savannah', 450000.00, TRUE, 'Medium'),
('Residential building lot', 'land', '700 Building Lot', 'NC', 'Wilmington', 380000.00, TRUE, 'Medium'),
('Agricultural acreage', 'land', '1500 Farm Land', 'AZ', 'Tucson', 320000.00, TRUE, 'Medium'),
('Mixed-use development land', 'land', '1100 Mixed Use', 'NY', 'Albany', 520000.00, TRUE, 'Medium'),
('Subdivision ready lot', 'land', '800 Subdivision Plot', 'MA', 'Springfield', 420000.00, TRUE, 'Medium'),
-- High crime rate land
('Affordable building lot', 'land', '400 Affordable Lot', 'PA', 'Allentown', 95000.00, TRUE, 'High'),
('Basic residential lot', 'land', '300 Basic Plot', 'MI', 'Grand Rapids', 75000.00, TRUE, 'High'),
('Economical development land', 'land', '500 Economy Land', 'IL', 'Springfield', 120000.00, TRUE, 'High'),
('Budget building site', 'land', '350 Budget Site', 'NV', 'Henderson', 150000.00, TRUE, 'High'),
('Simple vacant lot', 'land', '450 Simple Lot', 'OR', 'Salem', 180000.00, TRUE, 'High');

-- Land child table data (property_id 87-101)
INSERT INTO land (property_id, sqr_footage) VALUES
(87, 15000.0),
(88, 12000.0),
(89, 20000.0),
(90, 10000.0),
(91, 25000.0),
(92, 8000.0),
(93, 6000.0),
(94, 30000.0),
(95, 12000.0),
(96, 10000.0),
(97, 5000.0),
(98, 4000.0),
(99, 7000.0),
(100, 5500.0),
(101, 6500.0);

-- ============================================================================
-- AGENCIES (agency_id starts from 1)
-- ============================================================================
INSERT INTO agencies (agency_name, agency_email) VALUES
('Premier Realty Group', 'info@premierrealty.com'),
('Elite Properties Inc', 'contact@eliteproperties.com'),
('Metro Real Estate Solutions', 'hello@metrorealestate.com'),
('Coastal Living Realty', 'info@coastalliving.com'),
('Urban Development Partners', 'contact@urbandev.com'),
('Luxury Homes Agency', 'info@luxuryhomes.com'),
('Affordable Housing Solutions', 'contact@affordablehousing.com'),
('Commercial Real Estate Group', 'info@commercialrealestate.com');

-- ============================================================================
-- USERS (for agents - user_id starts from 6, since schema.sql has users 1-5)
-- ============================================================================
INSERT INTO users (role, first_name, last_name, email) VALUES
-- Agents for Premier Realty Group (agency_id 1)
('agent', 'Sarah', 'Johnson', 'sarah.johnson@premierrealty.com'), -- 6
('agent', 'Michael', 'Chen', 'michael.chen@premierrealty.com'), -- 7
-- Agents for Elite Properties Inc (agency_id 2)
('agent', 'Emily', 'Rodriguez', 'emily.rodriguez@eliteproperties.com'), -- 8
('agent', 'David', 'Thompson', 'david.thompson@eliteproperties.com'), -- 9
-- Agents for Metro Real Estate Solutions (agency_id 3)
('agent', 'Jessica', 'Williams', 'jessica.williams@metrorealestate.com'), -- 10
('agent', 'Robert', 'Martinez', 'robert.martinez@metrorealestate.com'), -- 11
-- Agents for Coastal Living Realty (agency_id 4)
('agent', 'Amanda', 'Davis', 'amanda.davis@coastalliving.com'), -- 12
('agent', 'James', 'Wilson', 'james.wilson@coastalliving.com'), -- 13
-- Agents for Urban Development Partners (agency_id 5)
('agent', 'Lisa', 'Anderson', 'lisa.anderson@urbandev.com'), -- 14
('agent', 'Christopher', 'Taylor', 'christopher.taylor@urbandev.com'), -- 15
-- Agents for Luxury Homes Agency (agency_id 6)
('agent', 'Jennifer', 'Brown', 'jennifer.brown@luxuryhomes.com'), -- 16
('agent', 'Daniel', 'Garcia', 'daniel.garcia@luxuryhomes.com'), -- 17
-- Agents for Affordable Housing Solutions (agency_id 7)
('agent', 'Patricia', 'Miller', 'patricia.miller@affordablehousing.com'), -- 18
('agent', 'Matthew', 'Moore', 'matthew.moore@affordablehousing.com'), -- 19
-- Agents for Commercial Real Estate Group (agency_id 8)
('agent', 'Linda', 'Jackson', 'linda.jackson@commercialrealestate.com'), -- 20
('agent', 'Mark', 'White', 'mark.white@commercialrealestate.com'); -- 21

-- ============================================================================
-- AGENTS_PROFILE (matching users 6-21 with agencies 1-8)
-- ============================================================================
INSERT INTO agents_profile (id, job_title, agency_id, contact_info) VALUES
-- Premier Realty Group (agency_id 1)
(6, 'Senior Real Estate Agent', 1, 'sarah.johnson@premierrealty.com'),
(7, 'Real Estate Agent', 1, 'michael.chen@premierrealty.com'),
-- Elite Properties Inc (agency_id 2)
(8, 'Senior Real Estate Agent', 2, 'emily.rodriguez@eliteproperties.com'),
(9, 'Real Estate Agent', 2, 'david.thompson@eliteproperties.com'),
-- Metro Real Estate Solutions (agency_id 3)
(10, 'Senior Real Estate Agent', 3, 'jessica.williams@metrorealestate.com'),
(11, 'Real Estate Agent', 3, 'robert.martinez@metrorealestate.com'),
-- Coastal Living Realty (agency_id 4)
(12, 'Senior Real Estate Agent', 4, 'amanda.davis@coastalliving.com'),
(13, 'Real Estate Agent', 4, 'james.wilson@coastalliving.com'),
-- Urban Development Partners (agency_id 5)
(14, 'Senior Real Estate Agent', 5, 'lisa.anderson@urbandev.com'),
(15, 'Real Estate Agent', 5, 'christopher.taylor@urbandev.com'),
-- Luxury Homes Agency (agency_id 6)
(16, 'Senior Real Estate Agent', 6, 'jennifer.brown@luxuryhomes.com'),
(17, 'Real Estate Agent', 6, 'daniel.garcia@luxuryhomes.com'),
-- Affordable Housing Solutions (agency_id 7)
(18, 'Senior Real Estate Agent', 7, 'patricia.miller@affordablehousing.com'),
(19, 'Real Estate Agent', 7, 'matthew.moore@affordablehousing.com'),
-- Commercial Real Estate Group (agency_id 8)
(20, 'Senior Real Estate Agent', 8, 'linda.jackson@commercialrealestate.com'),
(21, 'Real Estate Agent', 8, 'mark.white@commercialrealestate.com');

-- ============================================================================
-- AGENT_PROPERTY (linking all properties 27-101 to agencies)
-- ============================================================================
-- Properties distributed across agencies:
-- Agency 1 (Premier Realty): properties 27-35 (9 apartments)
-- Agency 2 (Elite Properties): properties 36-44 (9 properties: 5 apartments, 4 houses)
-- Agency 3 (Metro Real Estate): properties 45-53 (9 houses)
-- Agency 4 (Coastal Living): properties 54-62 (9 properties: 1 house, 8 commercial)
-- Agency 5 (Urban Development): properties 63-71 (9 commercial buildings)
-- Agency 6 (Luxury Homes): properties 72-80 (9 vacation homes)
-- Agency 7 (Affordable Housing): properties 81-89 (9 properties: 5 vacation homes, 4 land)
-- Agency 8 (Commercial Real Estate): properties 90-101 (12 land properties)

INSERT INTO agency_property (property_id, agency_id) VALUES
-- Agency 1: Premier Realty Group - Apartments 27-35
(27, 1), (28, 1), (29, 1), (30, 1), (31, 1), (32, 1), (33, 1), (34, 1), (35, 1),
-- Agency 2: Elite Properties Inc - Properties 36-44 (5 apartments, 4 houses)
(36, 2), (37, 2), (38, 2), (39, 2), (40, 2), (41, 2), (42, 2), (43, 2), (44, 2),
-- Agency 3: Metro Real Estate Solutions - Houses 45-53
(45, 3), (46, 3), (47, 3), (48, 3), (49, 3), (50, 3), (51, 3), (52, 3), (53, 3),
-- Agency 4: Coastal Living Realty - Properties 54-62 (1 house, 8 commercial)
(54, 4), (55, 4), (56, 4), (57, 4), (58, 4), (59, 4), (60, 4), (61, 4), (62, 4),
-- Agency 5: Urban Development Partners - Commercial 63-71
(63, 5), (64, 5), (65, 5), (66, 5), (67, 5), (68, 5), (69, 5), (70, 5), (71, 5),
-- Agency 6: Luxury Homes Agency - Vacation Homes 72-80
(72, 6), (73, 6), (74, 6), (75, 6), (76, 6), (77, 6), (78, 6), (79, 6), (80, 6),
-- Agency 7: Affordable Housing Solutions - Properties 81-89 (5 vacation homes, 4 land)
(81, 7), (82, 7), (83, 7), (84, 7), (85, 7), (86, 7), (87, 7), (88, 7), (89, 7),
-- Agency 8: Commercial Real Estate Group - Land 90-101
(90, 8), (91, 8), (92, 8), (93, 8), (94, 8), (95, 8), (96, 8), (97, 8), (98, 8), (99, 8), (100, 8), (101, 8);

-- ============================================================================
-- USERS (for renters - user_id starts from 22, since schema.sql has users 1-5 and mock_inserts has agents 6-21)
-- ============================================================================
INSERT INTO users (role, first_name, last_name, email) VALUES
('renter', 'Alex', 'Martinez', 'alex.martinez@email.com'), -- 22
('renter', 'Sophia', 'Lee', 'sophia.lee@email.com'), -- 23
('renter', 'Ryan', 'Anderson', 'ryan.anderson@email.com'), -- 24
('renter', 'Emma', 'Taylor', 'emma.taylor@email.com'), -- 25
('renter', 'Noah', 'Brown', 'noah.brown@email.com'), -- 26
('renter', 'Olivia', 'Garcia', 'olivia.garcia@email.com'), -- 27
('renter', 'Liam', 'Wilson', 'liam.wilson@email.com'), -- 28
('renter', 'Ava', 'Moore', 'ava.moore@email.com'), -- 29
('renter', 'Ethan', 'Jackson', 'ethan.jackson@email.com'), -- 30
('renter', 'Isabella', 'White', 'isabella.white@email.com'), -- 31
('renter', 'Mason', 'Harris', 'mason.harris@email.com'), -- 32
('renter', 'Mia', 'Clark', 'mia.clark@email.com'), -- 33
('renter', 'James', 'Lewis', 'james.lewis@email.com'), -- 34
('renter', 'Charlotte', 'Robinson', 'charlotte.robinson@email.com'), -- 35
('renter', 'Benjamin', 'Walker', 'benjamin.walker@email.com'); -- 36

-- ============================================================================
-- RENTERS_PROFILE (matching users 22-36)
-- ============================================================================
INSERT INTO renters_profile (id, move_in_date, preferred_location, budget) VALUES
(22, '2025-06-01', 'Miami, FL', 3500.00),
(23, '2025-07-15', 'New York, NY', 4500.00),
(24, '2025-08-01', 'Denver, CO', 2800.00),
(25, '2025-09-01', 'Austin, TX', 3200.00),
(26, '2025-10-01', 'Los Angeles, CA', 5000.00),
(27, '2025-11-01', 'Boston, MA', 3800.00),
(28, '2025-12-01', 'Atlanta, GA', 2500.00),
(29, '2026-01-01', 'Charlotte, NC', 2200.00),
(30, '2026-02-01', 'Phoenix, AZ', 2000.00),
(31, '2026-03-01', 'Seattle, WA', 4200.00),
(32, '2026-04-01', 'Las Vegas, NV', 1800.00),
(33, '2026-05-01', 'Portland, OR', 3000.00),
(34, '2026-06-01', 'Philadelphia, PA', 2400.00),
(35, '2026-07-01', 'Detroit, MI', 1500.00),
(36, '2026-08-01', 'Chicago, IL', 3500.00);

-- ============================================================================
-- RENTER_ADDRESSES (for renters 22-36)
-- ============================================================================
INSERT INTO renter_addresses (renter_id, street, city, state, zip) VALUES
(22, '123 Ocean Drive', 'Miami', 'FL', '33139'),
(23, '456 Broadway', 'New York', 'NY', '10013'),
(24, '789 Mountain View', 'Denver', 'CO', '80202'),
(25, '321 Music Lane', 'Austin', 'TX', '78701'),
(26, '654 Sunset Blvd', 'Los Angeles', 'CA', '90028'),
(27, '987 Beacon Street', 'Boston', 'MA', '02108'),
(28, '147 Peachtree Street', 'Atlanta', 'GA', '30309'),
(29, '258 Queen City Drive', 'Charlotte', 'NC', '28202'),
(30, '369 Desert Road', 'Phoenix', 'AZ', '85004'),
(31, '741 Space Needle Way', 'Seattle', 'WA', '98101'),
(32, '852 Strip Avenue', 'Las Vegas', 'NV', '89101'),
(33, '963 Rose Street', 'Portland', 'OR', '97204'),
(34, '159 Liberty Bell Lane', 'Philadelphia', 'PA', '19106'),
(35, '357 Motor City Drive', 'Detroit', 'MI', '48201'),
(36, '468 Lake Shore Drive', 'Chicago', 'IL', '60611');

-- ============================================================================
-- CREDIT_CARDS (for renters 22-36, using their addresses as billing addresses)
-- ============================================================================
-- Note: billing_address_id starts from 4 (schema.sql has addresses 1-3)
INSERT INTO credit_cards (renter_id, card_number, card_type, billing_address_id, expiration_month, expiration_year) VALUES
(22, '4111111111111111', 'visa', 4, 12, 2026), -- billing_address_id 4 (renter 22)
(23, '5555555555554444', 'mastercard', 5, 6, 2027), -- billing_address_id 5 (renter 23)
(24, '4111111111112222', 'visa', 6, 9, 2026), -- billing_address_id 6 (renter 24)
(25, '5555555555555555', 'mastercard', 7, 3, 2027), -- billing_address_id 7 (renter 25)
(26, '4111111111113333', 'visa', 8, 11, 2026), -- billing_address_id 8 (renter 26)
(27, '5555555555556666', 'mastercard', 9, 5, 2027), -- billing_address_id 9 (renter 27)
(28, '4111111111114444', 'visa', 10, 8, 2026), -- billing_address_id 10 (renter 28)
(29, '5555555555557777', 'mastercard', 11, 2, 2027), -- billing_address_id 11 (renter 29)
(30, '4111111111115555', 'visa', 12, 7, 2026), -- billing_address_id 12 (renter 30)
(31, '5555555555558888', 'mastercard', 13, 4, 2027), -- billing_address_id 13 (renter 31)
(32, '4111111111116666', 'visa', 14, 10, 2026), -- billing_address_id 14 (renter 32)
(33, '5555555555559999', 'mastercard', 15, 1, 2027), -- billing_address_id 15 (renter 33)
(34, '4111111111117777', 'visa', 16, 6, 2026), -- billing_address_id 16 (renter 34)
(35, '5555555555550000', 'mastercard', 17, 12, 2027), -- billing_address_id 17 (renter 35)
(36, '4111111111118888', 'visa', 18, 9, 2026); -- billing_address_id 18 (renter 36)

-- ============================================================================
-- AGENT_ASSIGNED (linking renters to agents)
-- ============================================================================
INSERT INTO agent_assigned (agent_id, renter_id) VALUES
-- Assigning renters to various agents across different agencies
(6, 22), (7, 23), -- Premier Realty Group
(8, 24), (9, 25), -- Elite Properties Inc
(10, 26), (11, 27), -- Metro Real Estate Solutions
(12, 28), (13, 29), -- Coastal Living Realty
(14, 30), (15, 31), -- Urban Development Partners
(16, 32), (17, 33), -- Luxury Homes Agency
(18, 34), (19, 35), -- Affordable Housing Solutions
(20, 36); -- Commercial Real Estate Group

-- ============================================================================
-- BOOKINGS (various bookings for renters 22-36 on properties 27-101)
-- ============================================================================
INSERT INTO bookings (renter_id, property_id, start_date, end_date, payment_card_id, price, booking_status) VALUES
-- Note: payment_card_id starts from 4 (schema.sql has credit_cards 1-3)
-- Renter 22 (Alex Martinez) - 3 bookings
(22, 27, '2025-06-01', '2026-06-01', 4, 42000.00, 'confirmed'), -- Apartment (1 year)
(22, 72, '2025-12-15', '2026-01-15', 4, 4500.00, 'pending'), -- Vacation home (1 month)
(22, 88, '2026-02-01', '2026-08-01', 4, 18000.00, 'confirmed'), -- Land lease (6 months)
-- Renter 23 (Sophia Lee) - 2 bookings
(23, 28, '2025-07-15', '2026-07-15', 5, 38400.00, 'confirmed'), -- Apartment (1 year)
(23, 57, '2026-01-01', '2026-12-31', 5, 300000.00, 'pending'), -- Commercial building (1 year)
-- Renter 24 (Ryan Anderson) - 2 bookings
(24, 29, '2025-08-01', '2026-02-01', 6, 14400.00, 'confirmed'), -- Apartment (6 months)
(24, 73, '2025-11-01', '2025-12-01', 6, 3500.00, 'confirmed'), -- Vacation home (1 month)
-- Renter 25 (Emma Taylor) - 3 bookings
(25, 30, '2025-09-01', '2026-09-01', 7, 26400.00, 'confirmed'), -- Apartment (1 year)
(25, 45, '2026-03-01', '2026-09-01', 7, 25200.00, 'pending'), -- House (6 months)
(25, 89, '2026-06-01', '2026-12-01', 7, 28500.00, 'confirmed'), -- Land lease (6 months)
-- Renter 26 (Noah Brown) - 2 bookings
(26, 31, '2025-10-01', '2026-10-01', 8, 54000.00, 'confirmed'), -- Apartment (1 year)
(26, 76, '2025-12-20', '2026-01-05', 8, 6000.00, 'confirmed'), -- Vacation home (2 weeks)
-- Renter 27 (Olivia Garcia) - 2 bookings
(27, 32, '2025-11-01', '2026-05-01', 9, 10800.00, 'confirmed'), -- Apartment (6 months)
(27, 47, '2026-01-01', '2026-07-01', 9, 22800.00, 'pending'), -- House (6 months)
-- Renter 28 (Liam Wilson) - 2 bookings
(28, 33, '2025-12-01', '2026-06-01', 10, 16800.00, 'confirmed'), -- Apartment (6 months)
(28, 48, '2026-02-01', '2026-08-01', 10, 16800.00, 'confirmed'), -- House (6 months)
-- Renter 29 (Ava Moore) - 1 booking
(29, 34, '2026-01-01', '2026-07-01', 11, 12000.00, 'confirmed'), -- Apartment (6 months)
-- Renter 30 (Ethan Jackson) - 2 bookings
(30, 35, '2026-02-01', '2026-08-01', 12, 9600.00, 'confirmed'), -- Apartment (6 months)
(30, 52, '2026-04-01', '2026-10-01', 12, 10800.00, 'pending'), -- House (6 months)
-- Renter 31 (Isabella White) - 2 bookings
(31, 36, '2026-03-01', '2027-03-01', 13, 33600.00, 'confirmed'), -- Apartment (1 year)
(31, 60, '2026-06-01', '2027-06-01', 13, 180000.00, 'pending'), -- Commercial building (1 year)
-- Renter 32 (Mason Harris) - 1 booking
(32, 37, '2026-04-01', '2026-10-01', 14, 7200.00, 'confirmed'), -- Apartment (6 months)
-- Renter 33 (Mia Clark) - 2 bookings
(33, 38, '2026-05-01', '2026-11-01', 15, 9000.00, 'confirmed'), -- Apartment (6 months)
(33, 63, '2026-07-01', '2027-01-01', 15, 48000.00, 'pending'), -- Commercial building (6 months)
-- Renter 34 (James Lewis) - 1 booking
(34, 39, '2026-06-01', '2026-12-01', 16, 6600.00, 'confirmed'), -- Apartment (6 months)
-- Renter 35 (Charlotte Robinson) - 1 booking
(35, 40, '2026-07-01', '2027-01-01', 17, 5400.00, 'confirmed'), -- Apartment (6 months)
-- Renter 36 (Benjamin Walker) - 2 bookings
(36, 41, '2026-08-01', '2027-02-01', 18, 8400.00, 'confirmed'), -- Apartment (6 months)
(36, 90, '2026-09-01', '2027-03-01', 18, 51000.00, 'pending'); -- Land lease (6 months)

-- ============================================================================
-- PROPERTY_UPDATE_LOG (tracking property updates by agents)
-- ============================================================================
INSERT INTO property_update_log (property_id, agent_id) VALUES
-- Various property updates by different agents
(27, 6), (28, 6), (29, 7), (30, 7), (31, 6),
(36, 8), (37, 8), (38, 9), (39, 9), (40, 8),
(42, 8), (43, 9), (44, 8), (45, 10), (46, 10),
(54, 12), (55, 12), (56, 13), (57, 12), (58, 13),
(63, 14), (64, 14), (65, 15), (66, 15), (67, 14),
(72, 16), (73, 16), (74, 17), (75, 17), (76, 16),
(81, 18), (82, 18), (83, 19), (84, 19), (85, 18),
(90, 20), (91, 20), (92, 21), (93, 21), (94, 20);

