-- ============================================================
-- ZivoGift — DEPLOY STATE PROBE  (READ-ONLY, changes nothing)
-- Run this FIRST in the Supabase SQL Editor.
-- It tells you what is already in your live database, so you
-- know which consolidated files still need to be applied.
-- ============================================================

-- 1) Which tables exist?
select table_name
from information_schema.tables
where table_schema = 'public'
order by table_name;

-- 2) Which columns exist on the main order tables?
--    (Later files mostly ADD columns to these.)
select table_name, column_name, data_type
from information_schema.columns
where table_schema = 'public'
  and table_name in ('orders','order_items','products','addons','profiles')
order by table_name, ordinal_position;

-- 3) Which functions exist?
select routine_name
from information_schema.routines
where routine_schema = 'public'
order by routine_name;

-- 4) Which indexes exist?
select tablename, indexname
from pg_indexes
where schemaname = 'public'
order by tablename, indexname;

-- 5) Which RLS policies exist?
select tablename, policyname
from pg_policies
where schemaname = 'public'
order by tablename, policyname;

-- 6) Catalogue sanity — is the add-on wording already fixed?
select id, name, description, price, active
from public.addons
order by id;
