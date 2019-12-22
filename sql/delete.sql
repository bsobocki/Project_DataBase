DROP EXTENSION IF EXISTS pgcrypto;
-- delete triggers
DROP TRIGGER IF EXISTS m_unique ON member;
DROP TRIGGER IF EXISTS a_unique ON action;
DROP TRIGGER IF EXISTS vote ON votes;
DROP TRIGGER IF EXISTS vote_on_action ON votes;
-- delete functions 
DROP FUNCTION IF EXISTS trolls();
DROP FUNCTION IF EXISTS inc_votes_action();
DROP FUNCTION IF EXISTS inc_votes_from_member();
DROP FUNCTION IF EXISTS add_unique();
DROP FUNCTION IF EXISTS add_unique_action();
-- delete tables
DROP TABLE IF EXISTS votes;
DROP TABLE IF EXISTS action;
DROP TABLE IF EXISTS member;
DROP TABLE IF EXISTS unique_indexes;
-- delete user app
DROP ROLE app;
