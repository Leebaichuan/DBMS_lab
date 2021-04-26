/*
* this is for DBMS lab1
* in this file, I am writing procedures for checking book status
* 设计一个存储过程,检查每本图书 status 是否正确,并返回 status 不正确的图书数
*/
use Library;
drop procedure if exists check_status;

/*
check the book status by searching Borrow record
a book's status is 0 iff there exists a Borrow record of 
that book where return_date is null
@param incorrect_num: the number of books with incorrect status
@param state: the returning status of this operation
	0: success
    1: failed due to sqlexceptions
*/
Delimiter //
create procedure check_status(out incorrect_num int, out state int )
begin
    # variable to indicate state
    declare s int default 0;
    # temporary book ID and status for checking
	declare temp_book_ID char(8);
    declare temp_book_status int;
    # if there exists a record for that book whose return date is null
    # then temp_not_avail is 1; else it is 0
    declare temp_not_avail int;
    
    # cursor declaration
    declare ct cursor for 
		select Book.ID, Book.status,
		# check whether there exists a record for that book whose return date is null
				if( exists(select * from Borrow 
						where Book.ID = Borrow.book_ID 
							and Borrow.return_date is null),1,0 ) as not_avail 
		from Book;

    # exception declaration
    declare continue handler for not found set s = 1;
    declare continue handler for sqlexception set s = 2;
    
    set incorrect_num = 0;
    open ct;
    repeat 
		fetch ct into temp_book_ID,temp_book_status,temp_not_avail;
        if s = 0 then
			# for each book, status and not_avail should be the same
			if temp_book_status <> temp_not_avail then
				set incorrect_num = incorrect_num + 1;
            end if;
        end if;
        until s = 1 or s = 2
    end repeat;
    
    # get state of operation
    if s = 2 then
		set state = 1;
	else
		set state = 0;
	end if;
    
    close ct;
end //
Delimiter ;

# for testing
set @incorrect_num = 0;
set @state = 0;
call check_status(@incorrect_num,@state);

select @incorrect_num,@state;