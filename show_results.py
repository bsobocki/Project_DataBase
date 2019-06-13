# the start and the end of the queries

start_action = '''SELECT DISTINCT id, member_id, project_id, authority_id, upvotes, downvotes
                FROM action'''
where = '''
                WHERE '''

start_project = '''SELECT DISTINCT project_id, authority_id
                FROM action '''

end = '''
                ORDER BY '''

def return_value(cur, q):
    cur.execute(q)
    return cur.fetchall()

# functions returns queries

def show_actions(cur):
    query = start_action
    query += end + '''id;'''
    return return_value(cur, query)

def show_actions_with_type(cur, type):
    query = start_action + where
    if not type:
        query += '''NOT '''
    query += '''type'''
    query += end + '''id;'''
    return return_value(cur, query)

def show_actions_for_project(cur, project):
    query = start_action + where
    query += '''project_id = ''' + str(project)
    query += end + '''id;'''
    return return_value(cur, query)

def show_actions_for_authority(cur, authority):
    query = start_action + where
    query += ''' authority_id = ''' + str(authority)
    query += end + '''id;'''
    return return_value(cur, query)

def show_projects(cur):
    query = start_project
    query += end + '''project_id;'''
    return return_value(cur, query)

def show_projects_for_authority(cur, authority):
    query = start_project + where
    query += '''authority_id = ''' + str(authority)
    query += end + '''project_id;'''
    return return_value(cur, query )

def show_votes(cur):
    query = '''SELECT id, upvotes, downvotes FROM member ORDER BY id;'''
    return return_value(cur, query)

def show_votes_on_action(cur, action):
    return return_value(cur, '''
    SELECT member.id, COUNT (up.action_id) AS upvotes, COUNT (down.action_id) AS downvotes
    FROM 
    member
    LEFT JOIN (SELECT * FROM votes WHERE type AND action_id = '''+str(action)+''') AS up ON (member.id = up.member_id), 
    member as mem
    LEFT JOIN (SELECT * FROM votes WHERE NOT type AND action_id = '''+str(action)+''') AS down ON (mem.id = down.member_id )
    WHERE member.id = mem.id
    GROUP BY member.id;''')

def show_votes_on_project(cur, project):
    return return_value(cur, '''
    SELECT member.id, COUNT (up.action_id) AS upvotes, COUNT (down.action_id) AS downvotes
    FROM 
    member
    LEFT JOIN 

    (SELECT votes.* 
        FROM votes 
        JOIN action ON (action.id=votes.action_id) 
        WHERE votes.type AND project_id = '''+str(project)+''') 
    AS up ON (member.id = up.member_id), 

    member as mem
    LEFT JOIN 

    (SELECT votes.* 
        FROM votes 
        JOIN action ON (action.id=votes.action_id) 
        WHERE NOT votes.type AND project_id = '''+str(project)+''') 
    AS down ON (mem.id = down.member_id )

    WHERE member.id = mem.id
    GROUP BY member.id;''')