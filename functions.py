def freeze_member(cursor, member):
    cursor.execute('UPDATE member SET active = FALSE WHERE id =' + str(member))

def insert_test_values(cursor):
    cursor.execute(open('sql/test.sql').read())

def trolls(cursor):
    cursor.execute(open('sql/trolls.sql').read())
    records = cursor.fetchall()
    for i in range(0,len(records)):
        records[i] = list(records[i])
        records[i][0] = int(records[i][0])
    return records

def insert(cursor, table, *vals):
    s = 'INSERT INTO ' + table + ' VALUES('
    for i in range(0,len(vals)):
        s += str(vals[i]) 
        if(i!=len(vals)-1):
            s += ', '
    s += ');'
    cursor.execute(s)

def update(cursor, table, set, where):
    s = 'UPDATE ' + str(table) + ' SET '+ str(set) + ' WHERE ' + str(where)
    cursor.execute(s)

def get_val(cursor, q):
    cursor.execute(q)
    l = cursor.fetchone()
    if l == None :
        return None
    if len(l) > 0:
        return l[0]
    return None

def member_exists(cursor, member):
    q1 = '(SELECT id FROM member)'
    q = 'SELECT (' + str(member) + ' IN ' + q1 + ');'
    return get_val(cursor, q)

def member_password(cursor, member, password):
    q = 'SELECT id FROM member WHERE id = ' + str(member) + " AND password = crypt('" + password +"', password)" 
    return get_val(cursor, q)

def member_last_timestamp(cursor, member):
    q = 'SELECT last_timestamp FROM member WHERE id = ' + str(member)
    return get_val(cursor, q)

def member_leader(cursor, member):
    q = 'SELECT leader FROM member WHERE id = ' + str(member)
    return get_val(cursor, q)
