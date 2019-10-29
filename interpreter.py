from json_objects import *
from init import *
from functions import *
from show_results import *
import sys

def interpreter():
    conn = None
    obj = JSON_Obj()
    for line in sys.stdin:
        obj.read_obj(line)
        vals_dict = obj.get_values_as_dict() 
        if not program_end(obj):
            try:
                if (obj.check_key(0,'open')):
                    arg =  get_values_from_json_object(obj)
                    if (len(sys.argv)>1 and sys.argv[1]=='--init'):
                        conn = init(arg) 
                    else:
                        conn = psycopg2.connect(host='localhost',dbname=arg[0], user=arg[1], password=arg[2])
                    if conn == None:
                        print(ERROR_status("Wrong database name, login or password"))
                    else:
                        print(OK_status)
                elif(obj.check_key(0,'leader')):
                    add_member_do_action(vals_dict, obj, conn, lambda conn, vals_dict: update(conn.cursor(),'member','leader = TRUE','id = ' + str(d["member"])), OK_status)
                
                elif(obj.check_key(0,'support')):
                    add_member_do_action(vals_dict, obj, conn, lambda conn, vals_dict: insert(conn.cursor(), 'action(id, member_id, project_id, authority_id, type, timestamp)', d["action"], d["member"], d["project"], 0, "TRUE", d["timestamp"]),OK_status)
                
                elif(obj.check_key(0,'protest')):
                    add_member_do_action(vals_dict, obj, conn, lambda conn, vals_dict: insert(conn.cursor(), 'action(id, member_id, project_id, authority_id, type, timestamp)', d["action"], d["member"], d["project"], 0, "FALSE", d["timestamp"]),OK_status)
                
                elif(obj.check_key(0,'upvote')):
                    add_member_do_action(vals_dict, obj, conn, lambda conn, vals_dict: insert(conn.cursor(), 'votes(member_id, action_id, type, timestamp)', d["member"], d["action"], "TRUE", d["timestamp"]),OK_status)
                
                elif(obj.check_key(0,'downvote')):
                    add_member_do_action(vals_dict, obj, conn, lambda conn, vals_dict: insert(conn.cursor(), 'votes(member_id, action_id, type, timestamp)', d["member"], d["action"], "FALSE", d["timestamp"]),OK_status)
                
                elif(obj.check_key(0,'actions')):
                    add_member_do_action(vals_dict, obj,conn, actions, None)
                
                elif(obj.check_key(0,'projects')):
                    add_member_do_action(vals_dict, obj, conn, projects, None)
                
                elif(obj.check_key(0,'votes')):
                    add_member_do_action(vals_dict, obj, conn, votes, None)
                
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

def program_end(obj):
    return line == '' or line == '\n' or obj.get_current_Obj() == None

def get_values_from_json_object(obj):
    return list(obj.get_values_as_dict().values())

### add member if doesn't exists ###
### call function 'action' if conditions have been met ###
def add_member_do_action(vals_dict, obj, conn, action, status):
    if (not member_exists(conn.cursor(), vals_dict["member"])):
        add_member(conn, vals_dict)
    ### check last active of member
    # musy be less than 31536000 (365 days * 24 hours * 3600 seconds_in_hour)
    if (vals_dict["timestamp"] - member_last_timestamp(conn.cursor(), vals_dict["member"]) < 31536000): 
        ### if password is correct then do action
        if (is_password_correct(conn, vals_dict):
            action(conn, vals_dict)
            if status != None:
                print(status)
        else:
            print(ERROR_status('Wrong password! '))
    else:
        freeze_member(conn.cursor(), vals_dict["member"])
        print(ERROR_status("Member with id = " + str(vals_dict["member"]) + ' is freezed! ' ))

def add_member(conn, vals_dict):
    insert(conn.cursor(), 'member(id, password, leader, last_timestamp)', vals_dict["member"], 'crypt('+"'" + vals_dict["password"] + "', gen_salt('md5'))", 'FALSE', vals_dict["timestamp"])

def is_password_correct(conn, vals_dict):
    return member_password(conn.cursor(), vals_dict["member"], vals_dict["password"]) != None

def actions(conn, vals_dict):
    if member_leader(conn.cursor(), vals_dict["member"]):
        if "type" in vals_dict:
            print(show_actions_with_type(conn.cursor(), vals_dict["type"]))
        elif "project" in vals_dict:
            print(json_OK_object(show_actions_for_project(conn.cursor(), vals_dict["project"])))
        elif "authority" in vals_dict:
            print(json_OK_object(show_actions_for_authority(conn.cursor(), vals_dict["authority"])))
        else:
            print(json_OK_object(show_actions(conn.cursor())))
    else:
        print(ERROR_status("Member with id = "+str(vals_dict["member"])+" is not a leader!"))

def projects(conn, vals_dict):
    if member_leader(conn.cursor(), vals_dict["member"]):
        if "authority" in vals_dict:
            print(json_OK_object(show_projects_for_authority(conn.cursor(), vals_dict["authority"])))
        else:
            print(json_OK_object(show_projects(conn.cursor())))
    else:
        print(ERROR_status("Member with id = "+str(vals_dict["member"])+" is not a leader!"))

def votes(conn, vals_dict):
    if member_leader(conn.cursor(), vals_dict["member"]):
        if "action" in vals_dict:
            print(json_OK_object(show_votes_on_action(conn.cursor(), vals_dict["action"])))
        elif "project" in vals_dict:
            print(show_votes_on_project(conn.cursor(), vals_dict["project"]))
        else:
            print(json_OK_object(show_votes(conn.cursor())))
    else:
        print(ERROR_status("Member with id = "+str(vals_dict["member"])+" is not a leader!"))
