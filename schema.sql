-- Table: users
CREATE TABLE users (
	id INTEGER NOT NULL, 
	role VARCHAR(50), 
	full_name VARCHAR(255), 
	password VARCHAR(255), 
	PRIMARY KEY (id)
);

-- Table: parcel
CREATE TABLE parcel (
	upin_number VARCHAR NOT NULL, 
	woreda VARCHAR(100), 
	kebele VARCHAR(100), 
	house_number VARCHAR(50), 
	x_coordinate DECIMAL, 
	y_coordinate DECIMAL, 
	PRIMARY KEY (upin_number)
);

-- Table: verify_by_count
CREATE TABLE verify_by_count (
	court_verify_id INTEGER NOT NULL, 
	block_by_count VARCHAR(14), 
	court_title_number VARCHAR, 
	court_address_kebale VARCHAR, 
	court_address_worda VARCHAR, 
	court_address_house_number VARCHAR, 
	letter_number VARCHAR, 
	date_on_letter DATE, 
	karta_number VARCHAR, 
	registration_date DATE, 
	block_reason TEXT, 
	status VARCHAR(8), 
	PRIMARY KEY (court_verify_id)
);

-- Table: employees
CREATE TABLE employees (
	id INTEGER NOT NULL, 
	name VARCHAR, 
	PRIMARY KEY (id)
);

-- Table: announcement
CREATE TABLE announcement (
	announcement_number VARCHAR NOT NULL, 
	announcement_type VARCHAR(10), 
	announcement_status VARCHAR(18), 
	size VARCHAR, 
	asked_date DATE, 
	payed_amount DECIMAL, 
	karta_number VARCHAR, 
	now_date DATE, 
	last_payed_years VARCHAR, 
	total DECIMAL, 
	remaining_amount DECIMAL, 
	description TEXT, 
	PRIMARY KEY (announcement_number)
);

-- Table: file_holders
CREATE TABLE file_holders (
	id INTEGER NOT NULL, 
	file_id VARCHAR, 
	full_name VARCHAR(255), 
	gender VARCHAR(6), 
	wereda VARCHAR(100), 
	kebele VARCHAR(100), 
	house_number VARCHAR(50), 
	registration_date DATE, 
	phone_number VARCHAR(20), 
	user_id INTEGER, 
	created_at TIMESTAMP, 
	updated_at TIMESTAMP, 
	PRIMARY KEY (id), 
	UNIQUE (file_id), 
	FOREIGN KEY(user_id) REFERENCES users (id)
);

-- Table: verifying_bank_status
CREATE TABLE verifying_bank_status (
	bank_status_id INTEGER NOT NULL, 
	lender_organization VARCHAR(13), 
	borrower_organization VARCHAR, 
	employee_name VARCHAR, 
	address_kebale VARCHAR, 
	address_worda VARCHAR, 
	address_house_number VARCHAR, 
	received_letter_number VARCHAR, 
	letter_received_date DATE, 
	agreement_number VARCHAR, 
	karta_number VARCHAR, 
	loans_year INTEGER, 
	loans_amount DECIMAL, 
	loans_repayment_date DATE, 
	registration_date DATE, 
	loans_taker_organization VARCHAR, 
	loans_status VARCHAR(8), 
	PRIMARY KEY (bank_status_id), 
	FOREIGN KEY(employee_name) REFERENCES employees (name)
);

-- Table: archive_store
CREATE TABLE archive_store (
	id INTEGER NOT NULL, 
	file_id VARCHAR, 
	archive_code VARCHAR(100), 
	box_number VARCHAR(50), 
	row_number VARCHAR(50), 
	cover_number VARCHAR(50), 
	folder_number VARCHAR(50), 
	block_number VARCHAR(50), 
	parcel_code VARCHAR(100), 
	neighbor TEXT, 
	user_id INTEGER, 
	created_at TIMESTAMP, 
	updated_at TIMESTAMP, 
	PRIMARY KEY (id), 
	FOREIGN KEY(file_id) REFERENCES file_holders (file_id), 
	UNIQUE (archive_code), 
	FOREIGN KEY(parcel_code) REFERENCES parcel (upin_number), 
	FOREIGN KEY(user_id) REFERENCES users (id)
);

-- Table: parcel_possession
CREATE TABLE parcel_possession (
	id INTEGER NOT NULL, 
	file_id VARCHAR, 
	possession_structure VARCHAR(32), 
	possession_confirmation VARCHAR(12), 
	land_use VARCHAR(14), 
	how_obtained VARCHAR(15), 
	land_grade INTEGER, 
	carta_number VARCHAR(100), 
	serial_number VARCHAR(100), 
	book_number VARCHAR(100), 
	user_id INTEGER, 
	created_at TIMESTAMP, 
	updated_at TIMESTAMP, 
	PRIMARY KEY (id), 
	FOREIGN KEY(file_id) REFERENCES file_holders (file_id), 
	FOREIGN KEY(user_id) REFERENCES users (id)
);

-- Table: land_width
CREATE TABLE land_width (
	id INTEGER NOT NULL, 
	file_id VARCHAR, 
	width_by_document DECIMAL, 
	width_by_measurement DECIMAL, 
	width_difference DECIMAL, 
	employee_id INTEGER, 
	user_id INTEGER, 
	created_at TIMESTAMP, 
	updated_at TIMESTAMP, 
	PRIMARY KEY (id), 
	FOREIGN KEY(file_id) REFERENCES file_holders (file_id), 
	FOREIGN KEY(employee_id) REFERENCES employees (id), 
	FOREIGN KEY(user_id) REFERENCES users (id)
);

-- Table: available_documents
CREATE TABLE available_documents (
	id INTEGER NOT NULL, 
	file_id VARCHAR, 
	loan_and_restriction VARCHAR(3), 
	land_tax_payment VARCHAR(100), 
	tax_payment_amount DECIMAL, 
	tax_payment_start_year INTEGER, 
	user_id INTEGER, 
	created_at TIMESTAMP, 
	updated_at TIMESTAMP, 
	PRIMARY KEY (id), 
	FOREIGN KEY(file_id) REFERENCES file_holders (file_id), 
	FOREIGN KEY(user_id) REFERENCES users (id)
);

-- Table: archive_status
CREATE TABLE archive_status (
	id INTEGER NOT NULL, 
	file_id VARCHAR, 
	archive_level_status VARCHAR(100), 
	archive_in_out VARCHAR(100), 
	number_of_pages INTEGER, 
	missing_page VARCHAR(3), 
	missing_pages_by_number VARCHAR(100), 
	user_id INTEGER, 
	created_at TIMESTAMP, 
	updated_at TIMESTAMP, 
	PRIMARY KEY (id), 
	FOREIGN KEY(file_id) REFERENCES file_holders (file_id), 
	FOREIGN KEY(user_id) REFERENCES users (id)
);

-- Table: border_by_direction
CREATE TABLE border_by_direction (
	id INTEGER NOT NULL, 
	file_id VARCHAR, 
	direction_1 VARCHAR(5), 
	direction_2 VARCHAR(5), 
	direction_3 VARCHAR(5), 
	direction_4 VARCHAR(5), 
	user_id INTEGER, 
	created_at TIMESTAMP, 
	updated_at TIMESTAMP, 
	PRIMARY KEY (id), 
	FOREIGN KEY(file_id) REFERENCES file_holders (file_id), 
	FOREIGN KEY(user_id) REFERENCES users (id)
);

-- Table: land_share_holder
CREATE TABLE land_share_holder (
	id INTEGER NOT NULL, 
	full_name VARCHAR(255), 
	kebele VARCHAR(100), 
	woreda VARCHAR(100), 
	house_number VARCHAR(50), 
	phone_number VARCHAR(20), 
	file_id VARCHAR, 
	PRIMARY KEY (id), 
	FOREIGN KEY(file_id) REFERENCES file_holders (file_id)
);

-- Table: payment_registration
CREATE TABLE payment_registration (
	payment_id INTEGER NOT NULL, 
	file_id VARCHAR, 
	payment_type VARCHAR(18), 
	description TEXT, 
	payment_method VARCHAR(15), 
	amount DECIMAL, 
	receipt_number VARCHAR, 
	PRIMARY KEY (payment_id), 
	FOREIGN KEY(file_id) REFERENCES file_holders (file_id)
);

-- Table: tax
CREATE TABLE tax (
	tax_id INTEGER NOT NULL, 
	from_year INTEGER, 
	upto_year INTEGER, 
	receipt_number VARCHAR, 
	from_land DECIMAL, 
	from_house DECIMAL, 
	total_amount DECIMAL, 
	remaining_year INTEGER, 
	remaining_payment_amt DECIMAL, 
	file_id VARCHAR, 
	PRIMARY KEY (tax_id), 
	FOREIGN KEY(file_id) REFERENCES file_holders (file_id)
);

-- Table: receipt_evidence
CREATE TABLE receipt_evidence (
	document_number VARCHAR NOT NULL, 
	document_type VARCHAR(28), 
	number_of_pages INTEGER, 
	file_id VARCHAR, 
	PRIMARY KEY (document_number), 
	FOREIGN KEY(file_id) REFERENCES file_holders (file_id)
);

-- Table: letters
CREATE TABLE letters (
	letters_number VARCHAR NOT NULL, 
	the_letter_was_written_in DATE, 
	letter_arrival_date DATE, 
	number_of_pages INTEGER, 
	letters_type VARCHAR, 
	letter_is_about TEXT, 
	for_who_is_the_letter VARCHAR, 
	file_id VARCHAR, 
	short_description TEXT, 
	PRIMARY KEY (letters_number), 
	FOREIGN KEY(file_id) REFERENCES file_holders (file_id)
);

-- Table: house_information
CREATE TABLE house_information (
	id INTEGER NOT NULL, 
	file_id VARCHAR, 
	house_number VARCHAR, 
	how_old_is_the_house VARCHAR(18), 
	the_owner_of_the_house VARCHAR(46), 
	house_service VARCHAR(18), 
	the_content_situation VARCHAR(16), 
	house_status VARCHAR(26), 
	house_type VARCHAR(28), 
	have_service VARCHAR(3), 
	the_floor_is_made_of VARCHAR(7), 
	wall_made_of VARCHAR(15), 
	cornice_is_made_of VARCHAR(12), 
	roof_made_of VARCHAR(13), 
	kitchen VARCHAR(32), 
	water_supply VARCHAR(23), 
	private_showers_house VARCHAR(23), 
	defecating VARCHAR(20), 
	trash_disposal_method VARCHAR(35), 
	food_cooker VARCHAR(37), 
	PRIMARY KEY (id), 
	FOREIGN KEY(file_id) REFERENCES file_holders (file_id)
);

-- Table: lease_agreement
CREATE TABLE lease_agreement (
	id INTEGER NOT NULL, 
	lease_type VARCHAR(12), 
	lease_status VARCHAR(15), 
	lease_version VARCHAR(3), 
	agreement_number VARCHAR(100), 
	payment_type VARCHAR(19), 
	lease_agreement_giver VARCHAR(100), 
	lease_agreement_taker VARCHAR(255), 
	land_use VARCHAR(100), 
	land_use_id INTEGER, 
	file_id VARCHAR, 
	PRIMARY KEY (id), 
	FOREIGN KEY(land_use_id) REFERENCES parcel_possession (id), 
	FOREIGN KEY(file_id) REFERENCES file_holders (file_id)
);

-- Table: land_share_holder_organization
CREATE TABLE land_share_holder_organization (
	org_record_id INTEGER NOT NULL, 
	holder_id VARCHAR, 
	formed_year INTEGER, 
	organization_id VARCHAR, 
	group_members_number INTEGER, 
	land_asked_size DECIMAL, 
	asked_date DATE, 
	approve_date DATE, 
	allowed_land_size DECIMAL, 
	payed_amount DECIMAL, 
	receipt_number VARCHAR, 
	description TEXT, 
	PRIMARY KEY (org_record_id), 
	FOREIGN KEY(holder_id) REFERENCES land_share_holder (id)
);

-- Table: land_share_holders_investment
CREATE TABLE land_share_holders_investment (
	investment_id INTEGER NOT NULL, 
	holder_id VARCHAR, 
	investment_type VARCHAR, 
	capital DECIMAL, 
	organization_level VARCHAR, 
	accepted_status VARCHAR(6), 
	land_given_date DATE, 
	receipt_number VARCHAR, 
	PRIMARY KEY (investment_id), 
	FOREIGN KEY(holder_id) REFERENCES land_share_holder (id)
);

