/*==============================================================*/
/* DBMS name:      MySQL 5.0                                    */
/* Created on:     2021/5/18 19:22:18                           */
/*==============================================================*/


drop table if exists Account;

drop table if exists Check_Account;

drop table if exists Check_Record;

drop table if exists Client;

drop table if exists Client_gets_Loan;

drop table if exists Department;

drop table if exists Deposit_Account;

drop table if exists Deposit_Record;

drop table if exists Employee;

drop table if exists Employee_serves_client;

drop table if exists Loan;

drop table if exists Payment;

drop table if exists SubBank;

/*==============================================================*/
/* Table: Account                                               */
/*==============================================================*/
create table Account
(
   Account_ID           char(20) not null,
   Account_Remain       float(8),
   Account_RegDate      date,
   primary key (Account_ID)
);

alter table Account comment 'the entity of bank Account
it has two subclasses: Depo';

/*==============================================================*/
/* Table: Check_Account                                         */
/*==============================================================*/
create table Check_Account
(
   Account_ID           char(20) not null,
   Account_Remain       float(8),
   Account_RegDate      date,
   Check_Overdraft      float(8),
   primary key (Account_ID)
);

alter table Check_Account comment 'Entity: check account, which inherits Account';

/*==============================================================*/
/* Table: Check_Record                                          */
/*==============================================================*/
create table Check_Record
(
   Client_ID            char(20) not null,
   SubBank_Name         char(30) not null,
   Account_ID           char(20),
   CheckRecord_LastAccessTime date,
   primary key (Client_ID, SubBank_Name)
);

alter table Check_Record comment 'entity: the record of a check account
it should have t';

/*==============================================================*/
/* Table: Client                                                */
/*==============================================================*/
create table Client
(
   Client_ID            char(20) not null,
   Client_Name          char(30),
   Client_PhoneNum      char(20),
   Client_Addr          char(30),
   Client_Contact_Name  char(30),
   Client_Contact_PhoneNum char(20),
   Client_Contact_Email char(20),
   primary key (Client_ID)
);

alter table Client comment 'the Client of the bank system.
it has a unqiue ID.
                           -&';

/*==============================================================*/
/* Table: Client_gets_Loan                                      */
/*==============================================================*/
create table Client_gets_Loan
(
   Client_ID            char(20) not null,
   Loan_Num             char(20) not null,
   primary key (Client_ID, Loan_Num)
);

alter table Client_gets_Loan comment 'many-to-many relation
since a client can possess multi';

/*==============================================================*/
/* Table: Department                                            */
/*==============================================================*/
create table Department
(
   Depart_ID            char(20) not null,
   SubBank_Name         char(30),
   Depart_Name          char(30),
   Depart_Type          char(10),
   Depart_LeaderID      char(20),
   primary key (Depart_ID)
);

alter table Department comment 'the department in a branch bank.
it has a unique depar';

/*==============================================================*/
/* Table: Deposit_Account                                       */
/*==============================================================*/
create table Deposit_Account
(
   Account_ID           char(20) not null,
   Account_Remain       float(8),
   Account_RegDate      date,
   Deposit_InterestRate float,
   Deposit_CurrencyType char(20),
   primary key (Account_ID)
);

alter table Deposit_Account comment 'the deposit accound, which inherits Account
';

/*==============================================================*/
/* Table: Deposit_Record                                        */
/*==============================================================*/
create table Deposit_Record
(
   Client_ID            char(20) not null,
   SubBank_Name         char(30) not null,
   Account_ID           char(20) not null,
   DepositRecord_LastAccessDate date,
   primary key (Client_ID, SubBank_Name)
);

alter table Deposit_Record comment 'entity: the record of a deposit account
it should have';

/*==============================================================*/
/* Table: Employee                                              */
/*==============================================================*/
create table Employee
(
   Employee_ID          char(20) not null,
   Depart_ID            char(20),
   Employee_Name        char(30),
   Employee_PhoneNum    char(20),
   Employee_Addr        char(30),
   Employee_StartDate   date,
   primary key (Employee_ID)
);

alter table Employee comment 'the employee in the subBank
it has a unique ID number.';

/*==============================================================*/
/* Table: Employee_serves_client                                */
/*==============================================================*/
create table Employee_serves_client
(
   Client_ID            char(20) not null,
   Employee_ID          char(20) not null,
   Service_Type         longblob not null,
   primary key (Client_ID, Employee_ID)
);

alter table Employee_serves_client comment 'relation: employees are responsible for clients
it is ';

/*==============================================================*/
/* Table: Loan                                                  */
/*==============================================================*/
create table Loan
(
   Loan_Num             char(20) not null,
   SubBank_Name         char(30),
   Loan_money           float(8),
   primary key (Loan_Num)
);

alter table Loan comment 'Entity: Loan
it is possessed by clients.
it is i';

/*==============================================================*/
/* Table: Payment                                               */
/*==============================================================*/
create table Payment
(
   Loan_Num             char(20) not null,
   Pay_Date             date,
   Pay_Money            float(8),
   primary key (Loan_Num)
);

alter table Payment comment 'Entity: the payment of a loan,
since payment is depend';

/*==============================================================*/
/* Table: SubBank                                               */
/*==============================================================*/
create table SubBank
(
   SubBank_Name         char(30) not null,
   SubBank_City         char(30),
   SubBank_Asset        float(8),
   primary key (SubBank_Name)
);

alter table SubBank comment 'the entity of a subBank in a bank system.
 it has a un';

alter table Check_Account add constraint FK_CheckAccount_inherits_Account foreign key (Account_ID)
      references Account (Account_ID) on delete restrict on update restrict;

alter table Check_Record add constraint FK_CheckAccount_has_Record foreign key (Account_ID)
      references Check_Account (Account_ID) on delete restrict on update restrict;

alter table Check_Record add constraint FK_Client_possess_CheckRecord foreign key (Client_ID)
      references Client (Client_ID) on delete restrict on update restrict;

alter table Check_Record add constraint FK_SubBank_issues_CheckRecord foreign key (SubBank_Name)
      references SubBank (SubBank_Name) on delete restrict on update restrict;

alter table Client_gets_Loan add constraint FK_Client_gets_Loan foreign key (Client_ID)
      references Client (Client_ID) on delete restrict on update restrict;

alter table Client_gets_Loan add constraint FK_Client_gets_Loan2 foreign key (Loan_Num)
      references Loan (Loan_Num) on delete restrict on update restrict;

alter table Department add constraint FK_Department_belongs_to_SubBank foreign key (SubBank_Name)
      references SubBank (SubBank_Name) on delete restrict on update restrict;

alter table Deposit_Account add constraint FK_DepositAccount_inherits_Account foreign key (Account_ID)
      references Account (Account_ID) on delete restrict on update restrict;

alter table Deposit_Record add constraint FK_Client_possess_DepositRecord foreign key (Client_ID)
      references Client (Client_ID) on delete restrict on update restrict;

alter table Deposit_Record add constraint FK_DepositAccount_has_Record foreign key (Account_ID)
      references Deposit_Account (Account_ID) on delete restrict on update restrict;

alter table Deposit_Record add constraint FK_SubBank_issues_DepositRecord foreign key (SubBank_Name)
      references SubBank (SubBank_Name) on delete restrict on update restrict;

alter table Employee add constraint FK_Employee_works_in_Department foreign key (Depart_ID)
      references Department (Depart_ID) on delete restrict on update restrict;

alter table Employee_serves_client add constraint FK_Employee_serves_client foreign key (Client_ID)
      references Client (Client_ID) on delete restrict on update restrict;

alter table Employee_serves_client add constraint FK_Employee_serves_client2 foreign key (Employee_ID)
      references Employee (Employee_ID) on delete restrict on update restrict;

alter table Loan add constraint FK_SubBank_issues_Loan foreign key (SubBank_Name)
      references SubBank (SubBank_Name) on delete restrict on update restrict;

alter table Payment add constraint FK_Loan_consists_of_Payment foreign key (Loan_Num)
      references Loan (Loan_Num) on delete restrict on update restrict;

