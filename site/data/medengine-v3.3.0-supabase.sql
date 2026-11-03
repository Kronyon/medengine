-- medengine v3.3.0 secure cloud schema. Run once in Supabase: SQL Editor, New query, Run.
-- Safe to run again. Every row now belongs to a signed-in user (auth.uid()), and the
-- anonymous key on its own can read or write nothing.

-- 1. Retire the v3.2.0 tables. Their policies let anyone read, edit and delete every row.
do $$
begin
  if to_regclass('public.med_profiles') is not null and not exists (
    select 1 from information_schema.columns where table_schema = 'public' and table_name = 'med_profiles' and column_name = 'id') then
    alter table public.med_profiles rename to med_profiles_v32;
  end if;
  if to_regclass('public.med_comments') is not null and not exists (
    select 1 from information_schema.columns where table_schema = 'public' and table_name = 'med_comments' and column_name = 'author_id') then
    alter table public.med_comments rename to med_comments_v32;
  end if;
  if to_regclass('public.med_pings') is not null and not exists (
    select 1 from information_schema.columns where table_schema = 'public' and table_name = 'med_pings' and column_name = 'from_id') then
    alter table public.med_pings rename to med_pings_v32;
  end if;
  if to_regclass('public.med_profiles_v32') is not null then
    execute 'drop policy if exists "med_profiles_all" on public.med_profiles_v32';
    execute 'alter table public.med_profiles_v32 enable row level security';
    execute 'revoke all on public.med_profiles_v32 from anon, authenticated';
  end if;
  if to_regclass('public.med_comments_v32') is not null then
    execute 'drop policy if exists "med_comments_all" on public.med_comments_v32';
    execute 'alter table public.med_comments_v32 enable row level security';
    execute 'revoke all on public.med_comments_v32 from anon, authenticated';
  end if;
  if to_regclass('public.med_pings_v32') is not null then
    execute 'drop policy if exists "med_pings_all" on public.med_pings_v32';
    execute 'alter table public.med_pings_v32 enable row level security';
    execute 'revoke all on public.med_pings_v32 from anon, authenticated';
  end if;
end $$;

-- 2. Tables. Leaderboard numbers only in profiles; your full progress lives in a private backup row.
create table if not exists public.med_profiles (
  id uuid primary key default auth.uid() references auth.users (id) on delete cascade,
  handle text not null unique check (handle ~ '^[a-z0-9_]{3,20}$'),
  name text not null default '' check (char_length(name) <= 40),
  avatar text not null default '🩺' check (char_length(avatar) <= 16),
  year text not null default '' check (char_length(year) <= 30),
  sys text not null default '' check (char_length(sys) <= 20),
  overall_pct int not null default 0 check (overall_pct between 0 and 100),
  total_done int not null default 0 check (total_done >= 0),
  streak int not null default 0 check (streak >= 0),
  sys_stats_json jsonb not null default '{}'::jsonb,
  week_stats_json jsonb not null default '{}'::jsonb,
  paper_stats_json jsonb not null default '{}'::jsonb,
  cond_top_json jsonb not null default '{}'::jsonb,
  updated_at timestamptz not null default now()
);

create table if not exists public.med_backups (
  id uuid primary key default auth.uid() references auth.users (id) on delete cascade,
  state jsonb not null default '{}'::jsonb,
  updated_at timestamptz not null default now()
);

create table if not exists public.med_comments (
  id text primary key check (char_length(id) <= 64),
  author_id uuid not null default auth.uid() references auth.users (id) on delete cascade,
  thread_id text not null check (char_length(thread_id) <= 64),
  cond_id int not null default 0,
  author_handle text not null default '' check (char_length(author_handle) <= 20),
  author_name text not null default '' check (char_length(author_name) <= 40),
  author_avatar text not null default '🩺' check (char_length(author_avatar) <= 16),
  author_sys text not null default '' check (char_length(author_sys) <= 20),
  category text not null default 'tip' check (category in ('tip', 'trap', 'guideline', 'help')),
  body text not null check (char_length(body) between 1 and 1500),
  created_at timestamptz not null default now()
);
create index if not exists med_comments_thread on public.med_comments (thread_id);

create table if not exists public.med_votes (
  comment_id text not null references public.med_comments (id) on delete cascade,
  voter_id uuid not null default auth.uid() references auth.users (id) on delete cascade,
  primary key (comment_id, voter_id)
);

create table if not exists public.med_pings (
  id text primary key check (char_length(id) <= 64),
  from_id uuid not null default auth.uid() references auth.users (id) on delete cascade,
  to_id uuid not null references auth.users (id) on delete cascade,
  from_handle text not null default '' check (char_length(from_handle) <= 20),
  from_name text not null default '' check (char_length(from_name) <= 40),
  from_avatar text not null default '🩺' check (char_length(from_avatar) <= 16),
  to_handle text not null default '' check (char_length(to_handle) <= 20),
  thread_id text not null default 'u:0' check (char_length(thread_id) <= 64),
  cond_id int not null default 0,
  q_idx text not null default '' check (char_length(q_idx) <= 40),
  title text not null default '' check (char_length(title) <= 120),
  note text not null default '' check (char_length(note) <= 500),
  is_read boolean not null default false,
  created_at timestamptz not null default now()
);
create index if not exists med_pings_to on public.med_pings (to_id);

-- 3. Row level security: signed-in users read the leaderboard and comments; you write only your own rows.
alter table public.med_profiles enable row level security;
alter table public.med_backups enable row level security;
alter table public.med_comments enable row level security;
alter table public.med_votes enable row level security;
alter table public.med_pings enable row level security;

drop policy if exists "profiles read" on public.med_profiles;
drop policy if exists "profiles insert own" on public.med_profiles;
drop policy if exists "profiles update own" on public.med_profiles;
drop policy if exists "profiles delete own" on public.med_profiles;
create policy "profiles read" on public.med_profiles for select to authenticated using (true);
create policy "profiles insert own" on public.med_profiles for insert to authenticated with check (id = auth.uid());
create policy "profiles update own" on public.med_profiles for update to authenticated using (id = auth.uid()) with check (id = auth.uid());
create policy "profiles delete own" on public.med_profiles for delete to authenticated using (id = auth.uid());

drop policy if exists "backup own" on public.med_backups;
create policy "backup own" on public.med_backups for all to authenticated using (id = auth.uid()) with check (id = auth.uid());

drop policy if exists "comments read" on public.med_comments;
drop policy if exists "comments insert own" on public.med_comments;
drop policy if exists "comments update own" on public.med_comments;
drop policy if exists "comments delete own" on public.med_comments;
create policy "comments read" on public.med_comments for select to authenticated using (true);
create policy "comments insert own" on public.med_comments for insert to authenticated with check (author_id = auth.uid());
create policy "comments update own" on public.med_comments for update to authenticated using (author_id = auth.uid()) with check (author_id = auth.uid());
create policy "comments delete own" on public.med_comments for delete to authenticated using (author_id = auth.uid());

drop policy if exists "votes read" on public.med_votes;
drop policy if exists "votes insert own" on public.med_votes;
drop policy if exists "votes delete own" on public.med_votes;
create policy "votes read" on public.med_votes for select to authenticated using (true);
create policy "votes insert own" on public.med_votes for insert to authenticated with check (voter_id = auth.uid());
create policy "votes delete own" on public.med_votes for delete to authenticated using (voter_id = auth.uid());

drop policy if exists "pings read own" on public.med_pings;
drop policy if exists "pings send" on public.med_pings;
drop policy if exists "pings mark read" on public.med_pings;
drop policy if exists "pings delete own" on public.med_pings;
create policy "pings read own" on public.med_pings for select to authenticated using (from_id = auth.uid() or to_id = auth.uid());
create policy "pings send" on public.med_pings for insert to authenticated with check (from_id = auth.uid());
create policy "pings mark read" on public.med_pings for update to authenticated using (to_id = auth.uid()) with check (to_id = auth.uid());
create policy "pings delete own" on public.med_pings for delete to authenticated using (from_id = auth.uid() or to_id = auth.uid());

-- 4. Privileges: the anonymous key gets nothing; a recipient can only flip is_read on a ping.
revoke all on public.med_profiles, public.med_backups, public.med_comments, public.med_votes, public.med_pings from anon;
grant select, insert, update, delete on public.med_profiles, public.med_backups, public.med_comments, public.med_votes to authenticated;
grant select, insert, delete on public.med_pings to authenticated;
revoke update on public.med_pings from authenticated;
grant update (is_read) on public.med_pings to authenticated;
