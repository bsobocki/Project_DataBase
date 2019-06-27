# Project_DataBase
Project from DataBase Course from the Institute of Computer Science.

## Table Of Contents
- [Program Designed To Manage a Political Party](#Program-Designed-To-Manage-a-Political-Party)  
  
## Program Designed To Manage a Political Party  

The program was created for the political party in need of a system of managing it, to keep a register of government and self-government activities that it supports or protects against.  
The party is managed by the Team of Leaders who are its members.  
Member can propose actions and vote for or against them.  
You become a party member through active participation in her life. After one year of inactivity, understood as the lack of calls to the program functions authorized by a given person, the party member's righst are lost, and such account is permanently frozen (the member can not perform any action, but all information about him is further stored and reported). This rule applies to all party members, including leaders.
  
  
## How To Run
### The Necessary Components
 To run the program you need :
* Python3.x (to interpret all files \*.py),
* PostgreSQL (DataBase)
* psycopg2 (to create, connect and manage to the DataBase)
  
  
  
## Before You Run  
To run the program a new database and the superuser that can create users must be created. You can connect with the database by the created user using _{ "open" : {"database":"<the_name_of_the_database>", "login":"<the_name_of_the_user", "password":"<the_users_password>"}}_ 
  
  
  
## Run In Linux
The start of the program follows by running the python interpreter using the 'python3' command  with the 'app.py' parameter   
```
~$ python3 app.py
```
Now you can enter new commands. For example:
```
~$ python3 app.py
  > { "open" : { "database":"student", "login":"init", "password":"qwerty" }}
  { "status":"OK" }
  ```
    
    
### Running From `delete.sh`, `init.sh`, `run.sh`  
  
`delete.sh` - delete all data from the database  
`init.sh` - run the program with the _--init_ parameter  
`run.sh` - run the program without _--init_  
  
  ***An Example :***  
    
  ![](https://github.com/bsobocki/Project_DataBase/blob/master/files/run_example.png)

## Functions

After running the program with parameter _**--init**_ (for example via _init.sh_) a new user with login _`app`_ and password `qwerty` will be created. You must open a database using the _`init`_ user with password _`qwerty`_  

Function description:  
> * ***name***  
      description  
      _example_  
      _`a list of function's arguments types`_
  * ***open*** 
    * connect to the database  
    _{"open" : {"database":"party", "login":"app", "password":"qwerty" }}_  
    _`string  string  string`_  
 * ***leader***  
    * create leaders in the party    
    _{"leader" : {"timestamp":42, "password":"aaa", "member":1}}_    
    _`long_integer  integer  string  integer`_  
 * ***support***  
    * create a support action for the project (if the project exists in the database you don't have to give the authority of this project)  
    _{ "support": { "timestamp":1557475701, "password":"123", "member":3, "action":600, "project":5000}}_  
    _`long_integer  string  integer  integer  integer`_    
  * ***protest***  
    * create a protest action for the project (if the project exists in the database you don't have to give the authority of this project)  
    _{ "protest": { "timestamp":1557475701, "password":"123", "member":3, "action":600, "project":6000, "authority":7}}_  
    _`long_integer  string  integer  integer  integer  integer`_  
  * ***upvote***  
    * add a new up-vote on action  
    _{ "upvote": { "timestamp": 1557475702, "password": "ako", "member": 3, "action":7}}_   
    _`long_integer  string  integer  integer_  
  * ***downvote***  
    * add a new down-vote on action  
    _{ "downvote": { "timestamp": 1557475702, "password": "aa", "member": 1, "action":7}}_  
    _`long_integer  string  integer  integer  integer`_  
  * ***actions***  
    * write all actions \[optionally actions of the project or of the authority\]  
    returns: `[<action> <type> <project> <authority> <upvotes> <downvotes>]`  
    _{ "actions": {"timestamp":415124352435, "member":123, "password":"idontknowwahtishouldwritehere"}}_  
    _{ "actions": {"timestamp"122344352:, "member":42, "password":"future", "project":111}}_  
    _{ "actions": {"timestamp":89746104548901, "member":44, "password":"youdontknowmebutiknowyou", "authority":4444}}_  
    _`long_integer  integer  string  [integer]`_  
  * ***projects***  
    * write all projects \[optionally projects of the authority\]  
    returns: `[<project> <authority>]`  
    _{ "projects": {"timestamp":415124352435, "member":123, "password":"idontknowwahtishuoldwritehere"}}_  
    _{ "projects": {"timestamp":89746104548901, "member":44, "password":"youdontknowmebutiknowyou", "authority":4444}}_  
    _`long_integer  integer string  [integer]`_  
  * ***votes***  
    * write all members with their votes \[optionally votes on the action or the project or all projects of the authority\]  
    returns: `[<member> <upvotes> <downvotes>]`  
    _{ "votes": {"timestamp":415252435, "member":123, "password":"idontknowwahtishuoldwritehere"}}_  
    _{ "votes": {"timestamp":122344352, "member":42, "password":"future", "action":111}}_  
    _{ "votes": {"timestamp":897469041, "member":44, "password":"youdontknowmebutiknowyou", "project":4444}}_  
    _`long_integer  integer  integer  string  [integer]`_
  * ***trolls***
    * write all members whose propose actions having a bigger sum of all down-votes than up-votes  
    returns: `[<member> <upvotes> <downvotes> <active>]`  
    _{ "trolls": {"timestamp" : 1557477060}}_  
    _`long_integer`_

## A Bit About The Rules  

**For *all functions*:**  
  * if the member hasn't been active for over a year the member id will be frozen
  * if _\<member>_ is the Party member _\<password>_ must be the member's password  
  * if the member with id = _\<member>_ does not exist, a new member will be created with _\<password>_  
  * if the member id is _frozen_, the error will be shown  

**For _support_ and _protest_:**  
  * if _\<project>_ does exist in the data base then the authority will be skiped otherwise _\<authority>_ must be given to create a new project  
  
**For _upvote_ and _downvote_:**  
  * if _\<action>_ does not exist in the database the error will be shown  
  * you can vote only once for a given action
  
**For _trolls_, _actions_ and _projets_:**  
  * the member must be a lider
