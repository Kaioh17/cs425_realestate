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

