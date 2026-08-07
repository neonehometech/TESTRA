-- TESTRA ecommerce foundation
create extension if not exists pgcrypto;

create table if not exists public.testra_products (
  id uuid primary key default gen_random_uuid(),
  sku text not null unique,
  name text not null,
  is_active boolean not null default true,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.testra_packages (
  id uuid primary key default gen_random_uuid(),
  product_id uuid not null references public.testra_products(id) on delete cascade,
  code text not null unique,
  label text not null,
  units integer not null check (units > 0),
  price_cents integer not null check (price_cents >= 0),
  is_active boolean not null default true,
  sort_order integer not null default 0,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.testra_orders (
  id uuid primary key default gen_random_uuid(),
  order_no text not null unique,
  customer_name text not null,
  phone text not null,
  email text,
  address1 text not null,
  city text not null,
  postcode text not null,
  state text not null,
  delivery_note text,
  currency text not null default 'MYR',
  subtotal_cents integer not null default 0,
  shipping_cents integer not null default 0,
  discount_cents integer not null default 0,
  total_cents integer not null default 0,
  payment_status text not null default 'pending' check (payment_status in ('pending','paid','failed','refunded','cancelled')),
  fulfilment_status text not null default 'new' check (fulfilment_status in ('new','processing','shipped','delivered','cancelled')),
  source text not null default 'website',
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.testra_order_items (
  id uuid primary key default gen_random_uuid(),
  order_id uuid not null references public.testra_orders(id) on delete cascade,
  package_id uuid references public.testra_packages(id),
  sku text not null,
  label text not null,
  units_per_package integer not null,
  quantity integer not null check (quantity > 0),
  unit_price_cents integer not null,
  line_total_cents integer not null,
  created_at timestamptz not null default now()
);

create table if not exists public.testra_payments (
  id uuid primary key default gen_random_uuid(),
  order_id uuid not null references public.testra_orders(id) on delete cascade,
  provider text,
  provider_payment_id text,
  amount_cents integer not null default 0,
  status text not null default 'pending',
  paid_at timestamptz,
  raw_payload jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.testra_shipments (
  id uuid primary key default gen_random_uuid(),
  order_id uuid not null unique references public.testra_orders(id) on delete cascade,
  provider text,
  courier text,
  tracking_no text,
  tracking_url text,
  awb_url text,
  shipment_status text not null default 'pending',
  provider_shipment_id text,
  pickup_at timestamptz,
  shipped_at timestamptz,
  delivered_at timestamptz,
  raw_payload jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.testra_order_events (
  id bigint generated always as identity primary key,
  order_id uuid not null references public.testra_orders(id) on delete cascade,
  event_type text not null,
  message text,
  payload jsonb,
  created_at timestamptz not null default now()
);

create table if not exists public.testra_checkout_drafts (
  id uuid primary key default gen_random_uuid(),
  session_id text not null unique,
  phone text,
  email text,
  package_code text,
  quantity integer,
  subtotal_cents integer,
  checkout_payload jsonb,
  converted_order_id uuid references public.testra_orders(id),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index if not exists testra_orders_phone_idx on public.testra_orders(phone);
create index if not exists testra_orders_created_at_idx on public.testra_orders(created_at desc);
create index if not exists testra_orders_payment_status_idx on public.testra_orders(payment_status);
create index if not exists testra_orders_fulfilment_status_idx on public.testra_orders(fulfilment_status);
create index if not exists testra_shipments_tracking_no_idx on public.testra_shipments(tracking_no);

alter table public.testra_products enable row level security;
alter table public.testra_packages enable row level security;
alter table public.testra_orders enable row level security;
alter table public.testra_order_items enable row level security;
alter table public.testra_payments enable row level security;
alter table public.testra_shipments enable row level security;
alter table public.testra_order_events enable row level security;
alter table public.testra_checkout_drafts enable row level security;

-- Product/package catalog may be read publicly. Order/payment/shipment tables are intentionally
-- server-only for now. Inserts will be performed by a verified Edge Function in the payment stage.
create policy if not exists "Public read active TESTRA products" on public.testra_products for select using (is_active = true);
create policy if not exists "Public read active TESTRA packages" on public.testra_packages for select using (is_active = true);

insert into public.testra_products (sku,name)
values ('TESTRA','TESTRA')
on conflict (sku) do nothing;

insert into public.testra_packages(product_id,code,label,units,price_cents,sort_order)
select p.id,v.code,v.label,v.units,v.price_cents,v.sort_order
from public.testra_products p
cross join (values
 ('TST-1','1 Botol',1,8900,1),
 ('TST-3','3 Botol · Popular',3,23900,2),
 ('TST-5','5 Botol · Best Value',5,36900,3)
) as v(code,label,units,price_cents,sort_order)
where p.sku='TESTRA'
on conflict (code) do update set label=excluded.label,units=excluded.units,price_cents=excluded.price_cents,sort_order=excluded.sort_order,updated_at=now();