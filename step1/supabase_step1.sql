-- medengine-STEP1: its own private backup table, so Step 1 progress never overwrites STUDY progress.
-- Run once in the Supabase SQL editor (same project as STUDY). Safe to run again.
-- Sign-in, comments and pings stay shared with STUDY; Step 1 topic threads use the prefix s1u: and never meet STUDY's u: threads.
-- STEP1 never writes to med_profiles, so the STUDY leaderboard is untouched.

create table if not exists public.med_backups_step1 (
  id uuid primary key default auth.uid() references auth.users (id) on delete cascade,
  state jsonb not null default '{}'::jsonb,
  updated_at timestamptz not null default now()
);

alter table public.med_backups_step1 enable row level security;

drop policy if exists "backup own" on public.med_backups_step1;
create policy "backup own" on public.med_backups_step1 for all to authenticated
  using (id = auth.uid()) with check (id = auth.uid());

revoke all on public.med_backups_step1 from anon;
grant select, insert, update, delete on public.med_backups_step1 to authenticated;
