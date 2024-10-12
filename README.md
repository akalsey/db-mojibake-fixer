# db-mojibake-fixer
Uses ftfy library to fix mojibake in a MariaDB database

## Installation

No installation needed, but there are two libraries you'll need to install with pip. 

`pip install mariadb ftfy`

## Running

Takes three arguments, the DB table you want to act on, the column you want to fix, and the name of the primary key column for that table.

`python mojifix.py TABLE COLUMN PRIMARY_KEY`

Requires that you have your database connection credentials in environment variables. DATABASE_NAME, DATABASE_USER, and DATABASE_PASSWORD 
