/*
* this is for DBMS lab1
* in this file, I am initializing the data in the database
*/

create database if not exists Library;
use Library;
# to avoid creating an existing table
# Note that we must drop Borrow first
# 	since Borrow's foreign key has referenced
# 	Book and Reader's primary key
drop table if exists Borrow;
drop table if exists Book;
drop table if exists Reader;


# the table recording the info of books
create table Book (
	ID 			char(8),
    name 		varchar(10),
    author		varchar(10),
    price		float,
    status		int default 0,
    primary key(ID)
);

# insert some testing data(CS textbook) into Book
insert into Book value('1', 'math_logic','WangFT',1.1,0);
insert into Book value('2', 'DB Concept','Abraham',2.2,0);
insert into Book value('3', 'CLRS','MIT',3.3,0);
insert into Book value('4', 'ARCH','Patterson',4.4,0);
insert into Book value('5', 'COD','Patterson',5.5,0);
insert into Book value('6', 'compiler','MIT',6.6,0);

# the table recording the info of readers
create table Reader (
	ID			char(8),
    name		varchar(10),
    age			int,
    address		varchar(20),
    primary key(ID)
);

# insert some testing data into Reader
insert into Reader value('1', 'Eddie',20,'Shenzhen');
insert into Reader value('2', 'John',20,'Hefei');
insert into Reader value('3', 'Kate',19,'Guangzhou');
insert into Reader value('4', 'Li',30,'Xi''an');


# the table recording the info of borrowing books
create table Borrow (
	book_ID			char(8),
    reader_ID		char(8),
    borrow_date		date,
    return_date		date,
    primary key(book_ID,reader_ID),
    FOREIGN KEY(book_ID) references Book(ID),
    FOREIGN KEY(reader_ID) references Reader(ID)
);

# insert some testing data into Borrow
# for reader 1
insert into Borrow value('2', '1','2019-09-12','2019-09-13');
insert into Borrow value('4', '1','2019-09-12','2019-12-05');
# for reader 2
insert into Borrow value('3', '2','2020-03-08','2020-04-08');
insert into Borrow value('5', '2','2019-09-12','2019-12-05');
insert into Borrow value('3', '1','2020-06-07','2020-06-08');
# for reader 3
insert into Borrow value('2', '3','2019-09-12','2019-12-31');
insert into Borrow value('3', '3','2019-09-12','2019-12-31');
insert into Borrow value('4', '3','2019-09-12','2019-12-31');
insert into Borrow value('5', '3','2019-09-12','2019-12-31');
insert into Borrow value('6', '3','2019-09-12','2019-12-31');
# reader 4 hasn't borrowed any book.

select * from Book;
select * from Reader;
select * from Borrow;