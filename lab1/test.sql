/*
* this is for DBMS lab1
* in this file, I use the init testing data published by out TA
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

# the table recording the info of readers
create table Reader (
	ID			char(8),
    name		varchar(10),
    age			int,
    address		varchar(20),
    primary key(ID)
);

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

# 插入书籍
# ( I have pruned the book name of some books since its capacity is only 10 varchar)
insert into Book value('b1', '数据库系统实现', 'Ullman', 59.0, 1);
insert into Book value('b2', '数据库系统概念', 'Abraham', 59.0, 1);
insert into Book value('b3', 'C++ Primer', 'Stanley', 78.6, 1);
insert into Book value('b4', 'Redis设计与实现', '黄建宏', 79.0, 1);
insert into Book value('b5', '人类简史', 'Yuval', 68.00, 0);
insert into Book value('b6', '史记(公版)', '司马迁', 220.2, 1);
insert into Book value('b7', 'Oracle', 'Thomas', 43.1, 1);
insert into Book value('b8', '分布式数据库', '邵佩英', 30.0, 0);
insert into Book value('b9', 'Oracle运维', '张立杰', 51.9, 0);
insert into Book value('b10', '数理逻辑', '汪芳庭', 22.0, 0);
insert into Book value('b11', '三体', '刘慈欣', 23.0, 1);
insert into Book value('b12', 'Fluent py', 'Luciano', 354.2, 1);

# 插入读者
insert into Reader value('r1', '李林', 18, '中国科学技术大学东校区');
insert into Reader value('r2', 'Rose', 22, '中国科学技术大学北校区');
insert into Reader value('r3', '罗永平', 23, '中国科学技术大学西校区');
insert into Reader value('r4', 'Nora', 26, '中国科学技术大学北校区');
insert into Reader value('r5', '汤晨', 22, '先进科学技术研究院');

# 插入借书
# for reader r1
insert into Borrow value('b5','r1',  '2021-03-12', '2021-04-07');
insert into Borrow value('b6','r1',  '2021-03-08', '2021-03-19');
insert into Borrow value('b11','r1',  '2021-01-12', NULL);

# for reader r2
insert into Borrow value('b3', 'r2', '2021-02-22', NULL);
insert into Borrow value('b9', 'r2', '2021-02-22', '2021-04-10');
insert into Borrow value('b7', 'r2', '2021-04-11', NULL);

# for reader r3
insert into Borrow value('b1', 'r3', '2021-04-02', NULL);
insert into Borrow value('b2', 'r3', '2021-04-02', NULL);
insert into Borrow value('b4', 'r3', '2021-04-02', '2021-04-09');
insert into Borrow value('b7', 'r3', '2021-04-02', '2021-04-09');

# for reader r4
insert into Borrow value('b6', 'r4', '2021-03-31', NULL);
insert into Borrow value('b12', 'r4', '2021-03-31', NULL);

# for reader r5
insert into Borrow value('b4', 'r5', '2021-04-10', NULL);

select * from Book;
