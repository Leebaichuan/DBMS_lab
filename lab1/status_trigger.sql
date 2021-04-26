/*
* this is for DBMS lab1
* in this file, I am writing procedures for status trigger
* 
* 设计触发器,实现:当一本书被借出时,自动将 Book 表中相应图书的 status 修改为
* 1;当某本书被归还时,自动将 status 改为 0。
*/
use Library;
drop trigger if exists borrow_trigger;
drop trigger if exists return_trigger;

/*
change the book status after the insertion to Borrow.
a new Borrow record with return_date = null 
means that the book is borrowed, and its status becomes 1;
*/
Delimiter //
create trigger borrow_trigger after insert on Borrow for each row
begin
    # the book is borrowed
    if new.return_date is null then
		update Book set Book.status = 1 
        where Book.ID = new.book_ID;
    end if;
end //
Delimiter ;

/*
change the book status after the update to Borrow.
an updated Borrow record that changes return_date from null to non-null means 
that the book is returned, and its status becomes 0;
*/
Delimiter //
create trigger return_trigger after update on Borrow for each row
begin
    # the book is borrowed
    if old.return_date is null and new.return_date is not null then
		update Book set Book.status = 0 
        where Book.ID = new.book_ID;
    end if;
end //
Delimiter ;

# testing data
insert into Borrow value('b9', 'r5', '2021-04-12', null);
# book b9's status will be 1
select * from Book;
update Borrow set return_date = '2021-05-11' 
where Borrow.book_ID = 'b9' and Borrow.reader_ID = 'r5';
# book b9's status will be 0
select * from Book;