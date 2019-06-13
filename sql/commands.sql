
-- SQL QUERIES

CREATE EXTENSION pgcrypto;

-- create tables in the PostgreSQL database
CREATE TABLE unique_indexes (
    index numeric PRIMARY KEY
);

CREATE TABLE member (
    id numeric,
    password varchar(128) NOT NULL,
    leader boolean DEFAULT FALSE, --check if the member is an leader
    last_timestamp integer NOT NULL,
    upvotes_from_actions integer DEFAULT 0,
    downvotes_from_actions integer DEFAULT 0,
    upvotes integer DEFAULT 0,
    downvotes integer DEFAULT 0,
    active boolean DEFAULT TRUE,  --check if the member is not freezed
    PRIMARY KEY (id),
    FOREIGN KEY (id) REFERENCES unique_indexes(index)
);

CREATE TABLE action (
    id numeric,
    member_id numeric,
    project_id numeric,
    authority_id numeric,
    type boolean NOT NULL,  --check if the action is a support
    timestamp numeric NOT NULL,
    upvotes integer DEFAULT 0,
    downvotes integer DEFAULT 0,
    PRIMARY KEY (id),
    FOREIGN KEY (member_id) REFERENCES member(id),
    FOREIGN KEY (id) REFERENCES unique_indexes(index),
    FOREIGN KEY (project_id) REFERENCES unique_indexes(index),
    FOREIGN KEY (authority_id) REFERENCES unique_indexes(index)
);

CREATE TABLE votes (
    member_id numeric NOT NULL,
    action_id numeric NOT NULL,
    type boolean NOT NULL,  --check if the vote is an upvote
    timestamp numeric NOT NULL,
    PRIMARY KEY (member_id, action_id)
);
        

-- create functions in the PostgreSQL database

-- function TROLLS
CREATE OR REPLACE FUNCTION trolls()
RETURNS TABLE (troll_id numeric, downvotes integer, upvotes integer, act boolean) AS $X$
BEGIN
RETURN QUERY 
    SELECT id, downvotes_from_actions, upvotes_from_actions, active
    FROM member
    WHERE (downvotes_from_actions - upvotes_from_actions) > 0
    ORDER BY (downvotes_from_actions - upvotes_from_actions) DESC;
END; $X$
LANGUAGE PLPGSQL;


-- trigger INCREMENT GIVEN VOTES

CREATE OR REPLACE FUNCTION inc_votes_from_member() RETURNS TRIGGER AS $X$
DECLARE
up int := 0;
down int := 0;
mem_id int := NEW.member_id;
mem numeric;
BEGIN
    -- determine which needs to be increased
    IF NEW.type THEN
        up := 1;
    ELSE 
        down := 1;
    END IF;
    -- increment upvotes/downvotes
    UPDATE 
        member
        SET 
            upvotes = upvotes + up,
            downvotes = downvotes + down
        WHERE 
            id=mem_id;

    -- select member who is owner of the action
    SELECT member.id INTO mem
        FROM member JOIN action ON (member.id=action.member_id)
            WHERE action.id=NEW.action_id;

    -- increments upvotes_from_actions/downvotes_from_actions
    UPDATE
        member
        SET
            upvotes_from_actions = upvotes_from_actions + up,
            downvotes_from_actions = downvotes_from_actions + down
        WHERE
            id=mem;

    RETURN NEW;
END; $X$
LANGUAGE PLPGSQL;

CREATE TRIGGER vote AFTER INSERT ON votes FOR EACH ROW EXECUTE PROCEDURE inc_votes_from_member();

-- triggers ADD VALUE TO UNIQUE_INDEXES

--member
CREATE OR REPLACE FUNCTION add_unique() RETURNS TRIGGER AS $X$
BEGIN 
    INSERT INTO unique_indexes(index) VALUES(NEW.id);
    RETURN NEW;
END; $X$
LANGUAGE PLPGSQL;

--action
CREATE OR REPLACE FUNCTION add_unique_action() RETURNS TRIGGER AS $X$
DECLARE
auth numeric;
BEGIN
    INSERT INTO unique_indexes(index) VALUES(NEW.id);
    IF NEW.project_id NOT IN (SELECT * FROM unique_indexes) THEN
        INSERT INTO unique_indexes(index) VALUES(NEW.project_id);
    ELSE
        SELECT DISTINCT authority_id INTO auth FROM action WHERE project_id = NEW.project_id;
        NEW.authority_id = auth;
    END IF;
    IF NEW.authority_id NOT IN (SELECT * FROM unique_indexes) THEN
        INSERT INTO unique_indexes(index) VALUES(NEW.authority_id);
    END IF;
    RETURN NEW;
END; $X$
LANGUAGE PLPGSQL;

CREATE TRIGGER m_unique BEFORE INSERT ON member FOR EACH ROW EXECUTE PROCEDURE add_unique();
CREATE TRIGGER a_unique BEFORE INSERT ON action FOR EACH ROW EXECUTE PROCEDURE add_unique_action(); 

-- triggers INC up-/down- votes form actions
CREATE OR REPLACE FUNCTION inc_votes_action() RETURNS TRIGGER AS $X$
DECLARE
up int := 0;
down int := 0;
BEGIN
    -- determine which needs to be increased
    IF NEW.type THEN
        up := 1;
    ELSE
        down := 1;
    END IF; 
    -- increment up-/down- votes
    UPDATE 
        action
        SET
            upvotes = upvotes + up,
            downvotes = downvotes + down
        WHERE
            id = NEW.action_id;
    
    RETURN NEW;
END; $X$
LANGUAGE PLPGSQL;

CREATE TRIGGER vote_on_action AFTER INSERT ON votes FOR EACH ROW EXECUTE PROCEDURE inc_votes_action();

-- create user APP

CREATE USER app SUPERUSER LOGIN ENCRYPTED PASSWORD 'qwerty';