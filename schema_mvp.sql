-- LocA MVP - PostgreSQL schema (simplifié)
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  full_name TEXT,
  role TEXT CHECK (role IN ('owner','tenant','agency_admin')) NOT NULL,
  agency_id INTEGER,
  created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE agencies (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE properties (
  id SERIAL PRIMARY KEY,
  owner_id INTEGER REFERENCES users(id),
  agency_id INTEGER REFERENCES agencies(id),
  name TEXT,
  address TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE units (
  id SERIAL PRIMARY KEY,
  property_id INTEGER REFERENCES properties(id),
  label TEXT NOT NULL,
  bedrooms INTEGER,
  surface_m2 NUMERIC
);

CREATE TABLE leases (
  id SERIAL PRIMARY KEY,
  unit_id INTEGER REFERENCES units(id),
  tenant_id INTEGER REFERENCES users(id),
  start_date DATE NOT NULL,
  end_date DATE,
  monthly_rent NUMERIC NOT NULL,
  indexation_enabled BOOLEAN DEFAULT TRUE,
  status TEXT CHECK (status IN ('active','terminated','pending')) DEFAULT 'active'
);

CREATE TABLE payments (
  id SERIAL PRIMARY KEY,
  lease_id INTEGER REFERENCES leases(id),
  due_date DATE NOT NULL,
  amount NUMERIC NOT NULL,
  paid_at TIMESTAMP,
  method TEXT,
  status TEXT CHECK (status IN ('due','paid','overdue','failed')) DEFAULT 'due'
);

CREATE TABLE tickets (
  id SERIAL PRIMARY KEY,
  lease_id INTEGER REFERENCES leases(id),
  creator_id INTEGER REFERENCES users(id),
  title TEXT NOT NULL,
  description TEXT,
  status TEXT CHECK (status IN ('open','in_progress','resolved','closed')) DEFAULT 'open',
  assignee_id INTEGER REFERENCES users(id),
  created_at TIMESTAMP DEFAULT now(),
  updated_at TIMESTAMP DEFAULT now()
);

CREATE TABLE ticket_messages (
  id SERIAL PRIMARY KEY,
  ticket_id INTEGER REFERENCES tickets(id),
  author_id INTEGER REFERENCES users(id),
  body TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE documents (
  id SERIAL PRIMARY KEY,
  lease_id INTEGER REFERENCES leases(id),
  uploader_id INTEGER REFERENCES users(id),
  doc_type TEXT CHECK (doc_type IN ('lease_pdf','inventory','peb','certificate','receipt')),
  filename TEXT NOT NULL,
  storage_url TEXT,
  created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE rent_invoices (
  id SERIAL PRIMARY KEY,
  lease_id INTEGER REFERENCES leases(id),
  period_ym CHAR(7) NOT NULL, -- 'YYYY-MM'
  amount_due NUMERIC NOT NULL,
  reference TEXT NOT NULL, -- BE structured or RF
  status TEXT CHECK (status IN ('due','pending_bank','paid','overdue')) DEFAULT 'due',
  created_at TIMESTAMP DEFAULT now(),
  paid_at TIMESTAMP,
  tx_id TEXT
);

CREATE UNIQUE INDEX rent_invoices_lease_period_uidx ON rent_invoices(lease_id, period_ym);


CREATE TABLE reminder_rules (
  id SERIAL PRIMARY KEY,
  agency_id INTEGER REFERENCES agencies(id),
  days_before INTEGER[] DEFAULT ARRAY[3,1], -- J-3, J-1
  days_after INTEGER[] DEFAULT ARRAY[1,3,10], -- J+1, J+3, J+10
  hours INTEGER DEFAULT 9, -- 9h locales
  channel TEXT[] DEFAULT ARRAY['email','push'] -- 'sms' optionnel
);

CREATE TABLE reminder_logs (
  id SERIAL PRIMARY KEY,
  invoice_id INTEGER REFERENCES rent_invoices(id),
  sent_at TIMESTAMP DEFAULT now(),
  channel TEXT CHECK (channel IN ('email','sms','push')),
  to_target TEXT,
  locale TEXT DEFAULT 'fr',
  template_key TEXT,
  status TEXT DEFAULT 'queued',
  provider_msg_id TEXT,
  details TEXT
);
