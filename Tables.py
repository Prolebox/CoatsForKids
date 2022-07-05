
import sqlite3 as sql

def Create():

    con = sql.connect('CoatsDB')
    cur = con.cursor()

    #Create tables
    try:
        cur.executescript("""
            create table if not exists Boot (
                boot_type text check(boot_type in('Girls','Boys','Mens','Womens','Unisex')) not null,
                boot_size text check(boot_size in('Small','Medium','Large')) not null,
                boot_id integer primary key
            );
            create table if not exists Sock (
                sock_type text check(sock_type in('Female','Male')) not null,
                sock_size text check(sock_size in('Small','Medium','Large')) not null,
                sock_id integer primary key
            );
            create table if not exists Coat (
                coat_type text check(coat_type in('Girls','Boys','Men','Women')) not null,
                coat_size text check(coat_size in('Small','Medium','Large')) not null,
                coat_id integer primary key
            );
            create table if not exists Hat (
                hat_type text check(hat_type in('Male','Female')) not null,
                hat_id integer primary key
            );
            create table if not exists Glove (
                glove_type check(glove_type in ('Boys','Girls','Mens','Womens')) not null,
                glove_id integer primary key
            );

            create table if not exists Record (
                child_first text not null,
                child_last text not null,
                child_age int(2) not null,
                child_gender text check(child_gender in('Male','Female','Other')) not null,
                child_school text not null,
                parent_first text not null,
                parent_last text not null,
                parent_phone integer not null,
                parent_street text not null,
                parent_city text not null,
                parent_zip text not null,
                hat text,
                coat text,
                gloves text,
                socks text,
                boots text,
                record_id integer primary key
          );

        """)



    except:
        Print("An error has occured.")
        Quit()

#insert into Glove (glove_type, glove_id) values ('Boys', 1), ('Girls', 2);
#insert into Boot (boot_type, boot_size, boot_id) values ('Girls','Small',1),('Boys','Medium',2);


    con.close()
