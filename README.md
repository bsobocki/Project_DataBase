# Project_DataBase
Project from DataBase Course from the Institute of Computer Science.

##   Program designed to manage a political party  

The program was created for the political party in need of a system of managing it, to keep a register of government and self-government activities that it supports or protects against.  
The party is managed by the Team of Leaders who are its members.  
Member can propose actions and vote for or against them.  
You become a party member through active participation in her life. After one year of inactivity, understood as the lack of calls to the program functions authorized by a given person, the party member's righst are lost, and such account is permanently frozen (the member can not perform any action, but all information about him is further stored and reported). This rule applies to all party members, including leaders.
  
  
## How to Run
### The Necessary Components
 To run the program you need :
* Python3.x (to interpret all files \*.py),
* PostgreSQL (DataBase)
* psycopg2 (to create, connect and manage to the DataBase)
  
  
  
## Before you run  
To run the program a new database and the superuser that can create users must be created. You can connect with the database by the created user using _{ "open" : {"database":"<the_name_of_the_database>", "login":"<the_name_of_the_user", "password":"<the_users_password>"}}_ 
  
  
  
## Run in Linux
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
Function description:  
***\<name>***  
\<example>  
`<type_of_the_first_argument type_of_the_second_argument ...>`
 * after running the program with parameter _**--init**_ (for example via _init.sh_) a new user with login _`app`_ and password `qwerty` will be created. You must open a database using the _`init`_ user with password _`qwerty`_
 * ***open*** 
    * connects to the database  
    _{"open" : {"database":"party", "login":"app", "password":"qwerty" }}_  
    _`string  string  string`_
 * ***leader***
    * create leaders in the party
    _{"leader" : {"timestamp":42, "password":"aaa", "member":1}}  
    _`long_integer  integer  string  integer`_
