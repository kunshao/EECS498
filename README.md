/* How to set up local MySQL database */

1. Download MySQL from: http://dev.mysql.com/downloads/mysql/
2. Follow the instruction and install MySQL on your computer
3. Start your MySQL server:
    Mac: System Preferences > MySQL > Start MySQL Server
    Windows: enter the command 
        >> "C:\Program Files\MySQL\MySQL Server 5.6\bin\mysqld" --console
    For more information about running the server for the first time on Windows, see 
    https://dev.mysql.com/doc/refman/5.5/en/windows-server-first-start.html
4. Create fquery_db database:
    run MySQL shell 
        >> mysql -u root -p
    then type in shell
        mysql> create database fquery_db


/* How to run server on localhost */
 
1. Change directory to EECS498
2. Run the following command
>> python manage.py syncdb

You should see tables being created in the database:

Creating tables ...
Creating table auth_permission
Creating table auth_group_permissions
Creating table auth_group
Creating table auth_user_groups
Creating table auth_user_user_permissions
Creating table auth_user
Creating table django_content_type
Creating table django_session
Creating table django_site
Creating table fqueryApp_status
Creating table fqueryApp_comment
Creating table fqueryApp_link
Creating table fqueryApp_photo
Creating table fqueryApp_note
Creating table fqueryApp_video
Creating table fqueryApp_post
Creating table fqueryApp_question
Creating table fqueryApp_questionoption

You just installed Django's auth system, which means you don't have any superusers defined.
Would you like to create one now? (yes/no): 

You could answer no, then you should see:

Installing custom SQL ...
Installing indexes ...
Installed 0 object(s) from 0 fixture(s)


3. Run the following command
>> python manage.py runserver

You should now see:

Validating models...

0 errors found
April 23, 2014 - 02:27:04
Django version 1.6.2, using settings 'fquery.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.

4. Use any web browser and go to localhost:8000

You should now see our website! Login and test it.

Please contact Kun Shao (kunshao@umich.edu) for any problem.
