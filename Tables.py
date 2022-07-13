import sqlite3 as sql

def Create():

    con = sql.connect('CoatsDB')
    cur = con.cursor()

    #Create tables
    try:
        cur.executescript("""
            create table if not exists Schools (
                school_name text not null,
                school_id integer primary key
            );
            create table if not exists Boots (
                boot_type text not null,
                boot_size text not null,
                boot_id integer primary key
            );
            create table if not exists Socks (
                sock_type text check(sock_type in('Female','Male')) not null,
                sock_size text check(sock_size in('Small','Medium','Large')) not null,
                sock_id integer primary key
            );
            create table if not exists Coats (
                coat_type text check(coat_type in('Girls','Boys','Men','Women')) not null,
                coat_size text check(coat_size in('Small','Medium','Large')) not null,
                coat_id integer primary key
            );
            create table if not exists Hats (
                hat_type text check(hat_type in('Male','Female')) not null,
                hat_id integer primary key
            );
            create table if not exists Gloves (
                glove_type check(glove_type in ('Boys','Girls','Mens','Womens')) not null,
                glove_id integer primary key
            );

            create table if not exists Records (
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
        print('ERROR: Failure creating database tables')
        quit()

    con.commit()
    con.close()
