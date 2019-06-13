from json_objects import *
from init import *
from functions import *
from show_results import *
import sys

### add member if doesn't exists ###
### call function 'action' if conditions have been met ###
def add_member_do_action(d, obj, conn, action, status):

    ### add a member if doesn't exists
    if (not member_exists(conn.cursor(), d["member"])):
        insert(conn.cursor(), 'member(id, password, leader, last_timestamp)', d["member"], 'crypt('+"'" + d["password"] + "', gen_salt('md5'))", 'FALSE', d["timestamp"])
    
    ### check last active of member
    # if is less than 31536000 (365 days * 24 hours * 3600 seconds_in_hour)
    if (d["timestamp"] - member_last_timestamp(conn.cursor(), d["member"]) < 31536000): 
        ### if password is correct then do action
        if (member_password(conn.cursor(), d["member"],d["password"]) != None):
            action(conn, d)
            if status != None:
                print(status)
        else:
            print(ERROR_status('Wrong password! '))
    else:
        freeze(conn.cursor(), d["member"])
        print(ERROR_status("Member with id = " + str(d["member"]) + ' is freezed! ' ))


### procedures given as argument do add_member_do_action ###

def actions(conn, d):
    if member_leader(conn.cursor(), d["member"]):
        if "type" in d:
                    print(show_actions_with_type(conn.cursor(), d["type"]))
        elif "project" in d:
            print(json_OK_object(show_actions_for_project(conn.cursor(), d["project"])))
        elif "authority" in d:
            print(json_OK_object(show_actions_for_authority(conn.cursor(), d["authority"])))
        else:
            print(json_OK_object(show_actions(conn.cursor())))
    else:
        print(ERROR_status("Member with id = "+str(d["member"])+" is not a leader!"))

def projects(conn, d):
    if member_leader(conn.cursor(), d["member"]):
        if "authority" in d:
            print(json_OK_object(show_projects_for_authority(conn.cursor(), d["authority"])))
        else:
            print(json_OK_object(show_projects(conn.cursor())))
    else:
        print(ERROR_status("Member with id = "+str(d["member"])+" is not a leader!"))


def votes(conn, d):
    if member_leader(conn.cursor(), d["member"]):
        if "action" in d:
            print(json_OK_object(show_votes_on_action(conn.cursor(), d["action"])))
        elif "project" in d:
            print(show_votes_on_project(conn.cursor(), d["project"]))
        else:
            print(json_OK_object(show_votes(conn.cursor())))
    else:
        print(ERROR_status("Member with id = "+str(d["member"])+" is not a leader!"))


### the procedure interpreter reads objects from input ###

#obj must be initialized!
def interpreter(): # obj is an JSON_Object instance
    # connection to PostgreSQL
    conn = None

    # object JSON_Obj needed to read json objects from file
    obj = JSON_Obj()

    for line in sys.stdin:
        # read next JSON Object from stdin
        obj.read_obj(line)
        # read object which is a value of main key in JSON OBJECT
        d = obj.get_values_as_dict() # get a value from the json object - python dictionary
        # the end of the program is '\n'
        if line != '' and line != '\n' and obj.get_current_Obj() != None:
            try:
                if (obj.check_key(0,'open')):
                    arg = list(obj.get_values_as_dict().values()) #get bvalues from json object
                    if (len(sys.argv)>1 and sys.argv[1]=='--init'):
                        conn = init(arg) #open the DataBase and create tables
                    else:
                        conn = psycopg2.connect(host='localhost',dbname=arg[0], user=arg[1], password=arg[2])# connent to the PostgreSQL server
                    if conn == None:
                        print(ERROR_status("Wrong database name, login or password"))
                    else:
                        print(OK_status)
                elif(obj.check_key(0,'leader')):
                    add_member_do_action(d, obj, conn, lambda conn, d: update(conn.cursor(),'member','leader = TRUE','id = ' + str(d["member"])), OK_status)
                
                elif(obj.check_key(0,'support')):
                    add_member_do_action(d, obj, conn, lambda conn, d: insert(conn.cursor(), 'action(id, member_id, project_id, authority_id, type, timestamp)', d["action"], d["member"], d["project"], 0, "TRUE", d["timestamp"]),OK_status)
                
                elif(obj.check_key(0,'protest')):
                    add_member_do_action(d, obj, conn, lambda conn, d: insert(conn.cursor(), 'action(id, member_id, project_id, authority_id, type, timestamp)', d["action"], d["member"], d["project"], 0, "FALSE", d["timestamp"]),OK_status)
                
                elif(obj.check_key(0,'upvote')):
                    add_member_do_action(d, obj, conn, lambda conn, d: insert(conn.cursor(), 'votes(member_id, action_id, type, timestamp)', d["member"], d["action"], "TRUE", d["timestamp"]),OK_status)
                
                elif(obj.check_key(0,'downvote')):
                    add_member_do_action(d, obj, conn, lambda conn, d: insert(conn.cursor(), 'votes(member_id, action_id, type, timestamp)', d["member"], d["action"], "FALSE", d["timestamp"]),OK_status)
                
                elif(obj.check_key(0,'actions')):
                    add_member_do_action(d, obj,conn, actions, None)
                
                elif(obj.check_key(0,'projects')):
                    add_member_do_action(d, obj, conn, projects, None)
                
                elif(obj.check_key(0,'votes')):
                    add_member_do_action(d, obj, conn, votes, None)
                
                elif(obj.check_key(0,'trolls')):
                    print(json_OK_object(trolls(conn.cursor())))
                    
                else:
                    if(not obj.check_key(0,'open')):
                        print(ERROR_status('Function "'+list(obj.get_current_Obj())[0]+'" does not exist with parametr "--init"'))
            except (Exception) as error:
                print(ERROR_status(str(error)))
        else:
            break
    if conn != None:
        conn.commit()
        conn.close()