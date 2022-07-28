#!python3.10
#Ethan Suhr 2022
import sqlite3 as sql

def Create():

    con = sql.connect('CoatsDB')
    cur = con.cursor()

    #('Hat','Coat','Gloves','Boots','Socks')
    #Create tables
    try:
        cur.executescript("""
            create table if not exists Schools (
                School_Name text not null,
                School_Id integer primary key
            );
            create table if not exists Boots (
                Boots_Type text not null,
                Boots_Size text not null,
                Boots_Id integer primary key
            );
            create table if not exists Socks (
                Socks_Type text not null,
                Socks_Id integer primary key
            );
            create table if not exists Coat (
                Coat_Type text not null,
                Coat_Size text not null,
                Coat_Id integer primary key
            );
            create table if not exists Hat (
                Hat_Type text not null,
                Hat_Id integer primary key
            );
            create table if not exists Gloves (
                Gloves_Type text not null,
                Gloves_Size text not null,
                Gloves_Id integer primary key
            );

            create table if not exists Boots_Inventory (
                Boots_Type text not null,
                Boots_Size text not null,
                Boots_Id integer primary key
            );
            create table if not exists Socks_Inventory (
                Socks_Type text not null,
                Socks_Id integer primary key
            );
            create table if not exists Coats_Inventory (
                Coat_Type text not null,
                Coat_Size text not null,
                Coat_Id integer primary key
            );
            create table if not exists Hats_Inventory (
                Hat_Type text not null,
                Hat_Id integer primary key
            );
            create table if not exists Gloves_Inventory (
                Gloves_Type text not null,
                Gloves_Size text not null,
                Gloves_Id integer primary key
            );

            create table if not exists Records (
                Child_First text not null,
                Child_Lasts text not null,
                Child_Age int(2) not null,
                Child_Gender text check(child_gender in('Male','Female','Other')) not null,
                Child_School text not null,
                Parent_First text not null,
                Parent_Last text not null,
                Parent_Phone integer not null,
                Parent_Street text not null,
                Parent_City text not null,
                Parent_Zip text not null,
                Hat text,
                Coat text,
                Gloves text,
                Socks text,
                Boots text,
                Record_Id integer primary key
            );
        """)
    except:
        print('ERROR: Failure creating database tables')
        quit()

    con.commit()
    con.close()
