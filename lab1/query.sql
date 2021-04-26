/*
* this is for DBMS lab1
* in this file, I am writing MYSQL queries
*/
use Library;

# 1.检索读者 Rose 的读者号和地址
select ID as reader_ID, address as reader_address
from Reader
where name = 'Rose';

# 2.检索读者 Rose 所借阅读书(包括已还和未还图书)的图书名和借期
select Book.name as book_name, Borrow.borrow_date as borrow_date
from Book, Reader, Borrow
where Reader.name = 'Rose' and Reader.ID = Borrow.reader_ID 
	and Borrow.book_ID = Book.ID;

# 3.检索未借阅图书的读者姓名
select Reader.name as reader_name
from Reader
# there is no borrow record where that reader gets involved 
where not exists(
	select * 
    from Borrow
    where Borrow.reader_ID = Reader.ID
);

# 4.检索 Ullman 所写的书的书名和单价
select Book.name as book_name, Book.price as book_price
from Book
where Book.author = 'Ullman';

# 5.检索读者“李林”借阅未还的图书的图书号和书名
select Book.ID as book_ID, Book.name as book_name
from Reader, Book, Borrow
where Reader.name = '李林' and Reader.ID = Borrow.reader_ID
	and Borrow.return_date is null
    and Book.ID = Borrow.book_ID;

# 6.检索借阅图书数目超过3本的读者姓名 
select Reader.name as reader_name
from Reader
# 返回借阅书目
# 这里用distinct book_ID, 因为<book_ID,reader_ID> 是Borrow的主键
# 因此不会出现一个人多次借同一本书的情况
where( select count(distinct book_ID)
		from Borrow
        where Borrow.reader_ID = Reader.ID
        group by Borrow.reader_ID
	) > 3;

# 7. 检索没有借阅读者“李林”所借的任何一本书的读者姓名和读者号
# 创建一个李林借过的书的视图
drop view if exists LiLin_Book_ID;

create view LiLin_Book_ID as
select Book.ID as book_ID
from Borrow,Reader,Book
where Reader.name = '李林' and Reader.ID = Borrow.reader_ID 
		and Book.ID = Borrow.book_ID;

select Reader.name as reader_name, Reader.ID as reader_ID
from Reader
# 不存在这个读者借过的且李林借过的书
where not exists(
	select *
    from Borrow
    where Borrow.reader_ID = Reader.ID
		and exists(
			select * 
            from LiLin_Book_ID
            where LiLin_Book_ID.book_ID = Borrow.book_ID)
);
drop view if exists LiLin_Book_ID;

# 8. 检索书名中包含“Oracle”的图书书名及图书号
select Book.name as book_name, Book.ID as book_ID
from Book
where Book.name like '%Oracle%';

# 9.创建一个读者借书信息的视图,该视图包含读者号、姓名、所借图书号、图书名
# 和借期;并使用该视图查询最近一年所有读者的读者号以及所借阅的不同图书数
# Borrow_info即为所需的视图
drop view if exists Borrow_info;

# create the view to record the basic info
create view Borrow_info as 
select 	Reader.ID as reader_ID, Reader.name as reader_name,
		Borrow.book_ID as book_ID, Book.name as book_name, Borrow.borrow_date as borrow_date
from Reader, Borrow, Book
where Reader.ID = Borrow.reader_ID and Book.ID = Borrow.book_ID;

# get the borrow info of the recent year
select reader_ID, count(book_ID)
from Borrow_info
where timestampdiff(year,borrow_date,now()) < 1  
group by reader_ID;

drop view if exists Borrow_info;