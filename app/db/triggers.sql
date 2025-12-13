--Triggers to update updated at columns
create function update_updated_at_column()
returns trigger as 
$$
begin
  new.updated_at = now();
  return new;
end;
$$ language plpgsql;

create trigger updateDate
  before update
  on properties
  for each row
  execute function update_updated_at_column();

create trigger updateDate
  before update
  on users
  for each row
  execute function update_updated_at_column();

create trigger updateDate
  before update
  on renters_profile
  for each row
  execute function update_updated_at_column();

create trigger updateDate
  before update
  on agents_profile
  for each row
  execute function update_updated_at_column();

create trigger updateDate
  before update
  on renter_addresses
  for each row
  execute function update_updated_at_column();

create trigger updateDate
  before update
  on credit_cards
  for each row
  execute function update_updated_at_column();

create trigger updateDate
  before update
  on apartments
  for each row
  execute function update_updated_at_column();

create trigger updateDate
  before update
  on houses
  for each row
  execute function update_updated_at_column();

create trigger updateDate
  before update
  on commercial_buildings
  for each row
  execute function update_updated_at_column();

create trigger updateDate
  before update
  on vacation_homes
  for each row
  execute function update_updated_at_column();

create trigger updateDate
  before update
  on land
  for each row
  execute function update_updated_at_column();

create trigger updateDate
  before update
  on bookings
  for each row
  execute function update_updated_at_column();

create trigger updateDate
  before update
  on agencies
  for each row
  execute function update_updated_at_column();

create trigger updateDate
  before update
  on agency_property
  for each row
  execute function update_updated_at_column();

