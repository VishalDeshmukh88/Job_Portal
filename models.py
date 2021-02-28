"""
Author: Vishal Deshmukh
Program: Cretae database and create table in it.
"""
import sqlite3
conn = sqlite3.connect('database.db')
print("Opened database successfully");

conn.execute('CREATE TABLE students (email TEXT, password TEXT, name TEXT, phone INTGER,address TEXT,skills TEXT,Education TEXT,Certifications TEXT)')
print("Table created successfully");
conn.close()