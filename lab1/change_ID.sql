/*
* this is for DBMS lab1
* in this file, I am writing procedures for changing book ID
*
* 设计一个存储过程,实现对 Book 表的 ID 的修改(本题要求不得使用外键定义时的
* on update cascade 选项,因为该选项不是所有 DBMS 都支持)。
*/
use Library;
drop procedure if exists change_ID;

/*
change the book ID in Book record and Borrow record
@param orig_ID: the original book ID
@param new_ID: the new book ID 
@param state: the returning status of this operation
	0: success
	1: orig_ID is not found in Book, failure
	2: new_ID is found is Book, failure
	3: other sqlexceptions, failure

For referential integrity, firstly add the new record in Book,
then update the old record in Borrow 
and later delete the old record in Book, 

*/
Delimiter //
create procedure change_ID(in orig_ID char(8), in new_ID char(8),out state int )
begin
	# declare statement should be put at the beginning of begin
    # variable to indicate state
    declare s int default 0;
    # variables to update the record
	declare temp_book_ID,book_name,book_author varchar(10);
	declare book_price float;
	declare book_status int;
    
    # exception declaration
    declare continue handler for sqlexception set s = 3;
    
    #------------------------------------------------------------
    start transaction;
    
    # see whether new_ID has been found in Book before the change
    select ID from Book where ID = new_ID into temp_book_ID;
    
	# get the variables in the record containing orig_ID
	select name from Book where ID = orig_ID into book_name;
	select author from Book where ID = orig_ID into book_author;
	select price from Book where ID = orig_ID into book_price;
	select status from Book where ID = orig_ID into book_status;

    # orig_ID is in Book and new_ID is not in Book
    if orig_ID <> new_ID then
    
		# insert the updated record into Book
		insert into Book value(new_ID, book_name, 
				book_author, book_price, book_status);
		
		# update the old record in Borrow
		update Borrow set book_ID = new_ID
		where book_ID = orig_ID;
        
		# delete the old record from Book
		delete from Book where ID = orig_ID; 
	end if;
    
    # ---------------------------------------
    # self-defined exceptions:
    
    # orig_ID is not in Book before change
	if book_name is null then
		set s = 1;
	end if;
    # --------------------------------------
    
    # new_ID is in book before change
    if temp_book_ID is not null then
		set s = 2;
	end if;
    
    # ----------------------------------------------------
    # deal with the exceptions
    set state = s;
    if s = 0 then
		commit;
	else
		rollback;
	end if;
end //
Delimiter ;

# testing data
# b1 -> c1, should be successful
set @state = -1;
set @orig_ID = 'b1';
set @new_ID = 'c1';
call change_ID(@orig_ID, @new_ID, @state);
# c1 -> c2, should be successful
set @state = -1;
set @orig_ID = 'c1';
set @new_ID = 'c2';
call change_ID(@orig_ID, @new_ID, @state);
# c3 -> c4, should be failed since c3 is not in Book
set @state = -1;
set @orig_ID = 'c3';
set @new_ID = 'c4';
call change_ID(@orig_ID, @new_ID, @state);
# b2 -> c2, should be failed since c2 is in Book
set @state = -1;
set @orig_ID = 'b2';
set @new_ID = 'c2';
call change_ID(@orig_ID, @new_ID, @state);
# at last, Ullman's 数据库系统实现 will be c2 in Book;

select * from Book;