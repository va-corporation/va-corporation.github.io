-- VA Corporation client cabinet — Supabase schema.
-- Run once in Supabase → SQL Editor → New query → paste → Run.
-- Admin = the owner's account(s) listed in public.admins (add your e-mail at the bottom).

create table if not exists public.admins (email text primary key);

create or replace function public.is_admin() returns boolean
language sql stable security definer set search_path = public as $$
  select exists (select 1 from public.admins where email = auth.jwt() ->> 'email');
$$;

-- Client profile (one per auth user)
create table if not exists public.profiles (
  id uuid primary key references auth.users on delete cascade,
  name text, company text, phone text, messenger text, lang text default 'en',
  created_at timestamptz default now()
);

-- Projects with stages: brief → prototype → development → launch → support
create table if not exists public.projects (
  id uuid primary key default gen_random_uuid(),
  client_id uuid not null references auth.users on delete cascade,
  title text not null,
  service text,                       -- key from the price list, e.g. 'support-agent'
  brief text,
  stage text not null default 'brief' check (stage in ('brief','prototype','development','launch','support','done','cancelled')),
  progress int not null default 0 check (progress between 0 and 100),
  deadline date,
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

-- Quotes and invoices (50/50 by our terms; no escrow)
create table if not exists public.invoices (
  id uuid primary key default gen_random_uuid(),
  project_id uuid not null references public.projects on delete cascade,
  client_id uuid not null references auth.users on delete cascade,
  kind text not null default 'invoice' check (kind in ('quote','invoice')),
  title text not null,
  amount_eur numeric(10,2) not null,
  vat_note text default '+ VAT',
  status text not null default 'sent' check (status in ('draft','sent','accepted','paid','overdue','cancelled')),
  due_date date,
  pay_url text,
  created_at timestamptz default now()
);

-- Messages per project
create table if not exists public.messages (
  id uuid primary key default gen_random_uuid(),
  project_id uuid not null references public.projects on delete cascade,
  author_id uuid not null references auth.users on delete cascade,
  from_team boolean not null default false,
  body text not null check (length(body) between 1 and 5000),
  file_path text,                     -- object in storage bucket 'files'
  created_at timestamptz default now()
);

alter table public.profiles enable row level security;
alter table public.projects enable row level security;
alter table public.invoices enable row level security;
alter table public.messages enable row level security;
alter table public.admins   enable row level security;

-- profiles: own row, admin sees all
create policy "profiles own read"   on public.profiles for select using (id = auth.uid() or public.is_admin());
create policy "profiles own insert" on public.profiles for insert with check (id = auth.uid());
create policy "profiles own update" on public.profiles for update using (id = auth.uid());

-- projects: client reads own and creates briefs; only admin changes stage/progress
create policy "projects read"   on public.projects for select using (client_id = auth.uid() or public.is_admin());
create policy "projects create" on public.projects for insert with check (client_id = auth.uid() and stage = 'brief' and progress = 0);
create policy "projects admin"  on public.projects for update using (public.is_admin());
create policy "projects admin del" on public.projects for delete using (public.is_admin());

-- invoices: client reads own; client may only accept a quote; admin manages all
create policy "invoices read"  on public.invoices for select using (client_id = auth.uid() or public.is_admin());
create policy "invoices admin ins" on public.invoices for insert with check (public.is_admin());
create policy "invoices admin upd" on public.invoices for update using (public.is_admin());
create policy "invoices client accept" on public.invoices for update
  using (client_id = auth.uid() and kind = 'quote' and status = 'sent')
  with check (client_id = auth.uid() and status = 'accepted');

-- messages: participants of the project
create policy "messages read" on public.messages for select using (
  public.is_admin() or exists (select 1 from public.projects p where p.id = project_id and p.client_id = auth.uid()));
create policy "messages write" on public.messages for insert with check (
  author_id = auth.uid() and (
    (public.is_admin() and from_team) or
    (not from_team and exists (select 1 from public.projects p where p.id = project_id and p.client_id = auth.uid()))));

create policy "admins self read" on public.admins for select using (email = auth.jwt() ->> 'email');

-- Files: private bucket, path = <client uid>/<project id>/<file>
insert into storage.buckets (id, name, public) values ('files', 'files', false) on conflict do nothing;
create policy "files read"   on storage.objects for select using (bucket_id = 'files' and ((storage.foldername(name))[1] = auth.uid()::text or public.is_admin()));
create policy "files upload" on storage.objects for insert with check (bucket_id = 'files' and ((storage.foldername(name))[1] = auth.uid()::text or public.is_admin()));

-- expose tables to the Data API (needed when "Grant API access to new tables automatically" is off)
grant usage on schema public to anon, authenticated;
grant select, insert, update, delete on public.profiles, public.projects, public.invoices, public.messages to authenticated;
grant select on public.admins to authenticated;
grant execute on function public.is_admin() to authenticated;

-- keep updated_at fresh
create or replace function public.touch() returns trigger language plpgsql as $$ begin new.updated_at = now(); return new; end $$;
drop trigger if exists projects_touch on public.projects;
create trigger projects_touch before update on public.projects for each row execute function public.touch();

-- >>> Put the owner's login e-mail here, then Run:
insert into public.admins (email) values ('benzogamesltd@gmail.com') on conflict do nothing;
