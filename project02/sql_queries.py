DDL_QUERY =  '''
CREATE TABLE IF NOT EXISTS equipment_type (
  id SERIAL PRIMARY KEY,
  name VARCHAR(45) NOT NULL,
  rental_value NUMERIC(13, 2) NOT NULL
);

CREATE TABLE IF NOT EXISTS location (
  id SERIAL PRIMARY KEY,
  street_address VARCHAR(100) NOT NULL,
  city VARCHAR(50) NOT NULL,
  state CHAR(2) NOT NULL,
  zipcode INT NOT NULL,
  CONSTRAINT zipcode_unique UNIQUE (zipcode)
);

CREATE TABLE IF NOT EXISTS equipment (
  id SERIAL PRIMARY KEY,
  name VARCHAR(45) NOT NULL,
  equipment_type_id INT NOT NULL,
  current_location_id INT NOT NULL,
  CONSTRAINT fk_equipment_equipment_type FOREIGN KEY (equipment_type_id)
    REFERENCES equipment_type (id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT fk_equipment_location FOREIGN KEY (current_location_id)
    REFERENCES location (id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS vehicle_type (
  id SERIAL PRIMARY KEY,
  name VARCHAR(45) NOT NULL,
  rental_value NUMERIC(13, 2) NOT NULL,
  CONSTRAINT id_unique UNIQUE (id)
);

CREATE TABLE IF NOT EXISTS insurance (
  id SERIAL PRIMARY KEY,
  name VARCHAR(45) NOT NULL,
  cost NUMERIC(13, 2) NOT NULL
);

CREATE TABLE IF NOT EXISTS vehicle (
  id SERIAL PRIMARY KEY,
  brand VARCHAR(45) NOT NULL,
  model VARCHAR(45) NOT NULL,
  model_year INT NOT NULL,
  mileage INT NOT NULL,
  color VARCHAR(45) NOT NULL,
  vehicle_type_id INT NOT NULL,
  current_location_id INT NOT NULL,
  CONSTRAINT fk_vehicle_vehicle_type FOREIGN KEY (vehicle_type_id)
    REFERENCES vehicle_type (id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT fk_vehicle_current_location FOREIGN KEY (current_location_id)
    REFERENCES location (id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS customer (
  id SERIAL PRIMARY KEY,
  first_name VARCHAR(45) NOT NULL,
  last_name VARCHAR(45) NOT NULL,
  dob DATE NOT NULL,
  driver_license_number VARCHAR(12) NOT NULL,
  email VARCHAR(255) NOT NULL,
  phone VARCHAR(12) NULL,
  CONSTRAINT driver_license_number_unique UNIQUE (driver_license_number),
  CONSTRAINT email_unique UNIQUE (email)
);

CREATE TABLE IF NOT EXISTS fuel_option (
  id SERIAL PRIMARY KEY,
  name VARCHAR(45) NOT NULL,
  description VARCHAR(255) NULL
);

CREATE TABLE IF NOT EXISTS rental (
  id SERIAL PRIMARY KEY,
  start_date DATE NOT NULL,
  end_date DATE NOT NULL,
  customer_id INT NOT NULL,
  vehicle_type_id INT NOT NULL,
  fuel_option_id INT NOT NULL,
  pickup_location_id INT NOT NULL,
  drop_off_location_id INT NOT NULL,
  CONSTRAINT fk_rental_customer
    FOREIGN KEY (customer_id)
    REFERENCES customer (id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT fk_rental_fuel_option
    FOREIGN KEY (fuel_option_id)
    REFERENCES fuel_option (id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT fk_rental_pickup_location
    FOREIGN KEY (pickup_location_id)
    REFERENCES location (id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT fk_rental_dropoff_location
    FOREIGN KEY (drop_off_location_id)
    REFERENCES location (id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT fk_rental_vehicle_type
    FOREIGN KEY (vehicle_type_id)
    REFERENCES vehicle_type (id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS rental_invoice (
  id SERIAL PRIMARY KEY,
  car_rent DECIMAL(13,2)  NOT NULL,
  equipment_rent_total DECIMAL(13,2)  NULL,
  insurance_cost_total DECIMAL(13,2)  NULL,
  tax_surcharges_and_fees DECIMAL(13,2)  NOT NULL,
  total_amount_payable DECIMAL(13,2)  NOT NULL,
  discount_amount DECIMAL(13,2)  NULL,
  net_amount_payable DECIMAL(13,2)  NOT NULL,
  rental_id INT NOT NULL,
  CONSTRAINT fk_rental_invoice_rental
    FOREIGN KEY (rental_id)
    REFERENCES rental (id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS vehicle_has_equiment (
  equipment_id INT NOT NULL,
  vehicle_id INT NOT NULL,
  start_date DATE NULL,
  end_date DATE NULL,
  PRIMARY KEY (equipment_id, vehicle_id),
  CONSTRAINT fk_equipment_has_vehicle_equipment
    FOREIGN KEY (equipment_id)
    REFERENCES equipment (id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT fk_equipment_has_vehicle_vehicle
    FOREIGN KEY (vehicle_id)
    REFERENCES vehicle (id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS rental_has_insurance (
  rental_id INT NOT NULL,
  insurance_id INT NOT NULL,
  PRIMARY KEY (rental_id, insurance_id),
  CONSTRAINT fk_rental_has_insurance_rental
    FOREIGN KEY (rental_id)
    REFERENCES rental (id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT fk_rental_has_insurance_insurance
    FOREIGN KEY (insurance_id)
    REFERENCES insurance (id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS rental_has_equipment_type (
  rental_id INT NOT NULL,
  equipment_type_id INT NOT NULL,
  PRIMARY KEY (rental_id, equipment_type_id),
  CONSTRAINT fk_rental_has_equipment_type_rental
    FOREIGN KEY (rental_id)
    REFERENCES rental (id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT fk_rental_has_equipment_type_equipment_type
    FOREIGN KEY (equipment_type_id)
    REFERENCES equipment_type (id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
);
 '''