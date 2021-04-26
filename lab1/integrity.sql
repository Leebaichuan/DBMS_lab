/*
* this is for DBMS lab1
* in this file, I am creating some examples to demonstrate 
* three integrities(entity,referential and user-defined)
*/
use Library;

/*
* test entity integrity
* entity integrity means the attributes that the primary key
* consists of cannot be null.
*/
#####################
# As I expected, there will be an error message showing 
# 		"Column 'reader_ID' cannot be null".
# because Borrow's primary key consists of book_ID and reader_ID
##################### 
#insert into Borrow value(1, null,'2019-09-12','2019-12-31');

/*
* test referential integrity
* referential integrity means that 
* for any non-null foreign key,
* there must be a unique key in the table that it references to
*/
##################### 
# As I expected, there will be an error message showing
# 	"Cannot delete or update a parent row: a foreign key constraint fails"
# because the foreign key book_ID of record ('6', '3','2019-09-12','2019-12-31')
# should follows referential integrity
##################### 
# delete from Book where ID = '6';
#####################
# also, since the foreign keys in Borrow are also primary keys,
# they cannot be null, so I can't create the example where foreign key is null
#####################

/*
* test user-defined integrity
* user-defined integrity means that 
* the constraint should satisfy some constraints made by users
*/

# I add a constraint that book's price should be non-negative
alter table Book
add constraint ck_book_price check(Book.price >= 0);

# ok
insert into Book value('9', 'par','Chen',0,0);
# error
insert into Book value('10', 'AI','Russell',-1,0);

alter table Book
drop constraint ck_book_price;

