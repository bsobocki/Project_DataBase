-- insert data to test
INSERT INTO member(id, password, last_timestamp) VALUES (1, 'aa', 111);
INSERT INTO member(id, password, last_timestamp) VALUES (4, 'aa', 111);
INSERT INTO member(id, password, last_timestamp) VALUES (10, 'aa', 111);
INSERT INTO action(id, member_id, project_id, authority_id, type, timestamp) VALUES(2, 1, 6, 111, FALSE, 4332);
INSERT INTO action(id, member_id, project_id, authority_id, type, timestamp) VALUES(7, 4, 6, 111, TRUE, 4332);
INSERT INTO votes(member_id, action_id, type, timestamp) VALUES (3,2,FALSE,111);
INSERT INTO votes(member_id, action_id, type, timestamp) VALUES (3,7,TRUE,111);
INSERT INTO votes(member_id, action_id, type, timestamp) VALUES (12,2,TRUE,111);
INSERT INTO votes(member_id, action_id, type, timestamp) VALUES (1,7,FALSE,111);
INSERT INTO votes(member_id, action_id, type, timestamp) VALUES (1,2,TRUE,111);
INSERT INTO votes(member_id, action_id, type, timestamp) VALUES (4,7,FALSE,111);
INSERT INTO votes(member_id, action_id, type, timestamp) VALUES (4,2,FALSE,111);
INSERT INTO votes(member_id, action_id, type, timestamp) VALUES (10,2,TRUE,111);