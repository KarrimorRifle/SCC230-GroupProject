CREATE DATABASE Accounts;
USE Accounts

CREATE TABLE accounts(
    AccountID int not null AUTO_INCREMENT,
    FirstName varchar(100) NOT NULL,
    Surname varchar(100) NOT NULL,
    Email varchar(100) NOT NULL,
    Pass VARCHAR(100) NOT NULL,
    PRIMARY KEY (AccountID)
);

INSERT INTO accounts(FirstName, Surname, Email, Pass)
Values("Jhon","Doe","jhondoe@gmail.com", SHA2("JaneDoe123.",256) ),("Jane","Doe","janedoe@gmail.com",SHA2("JhonDoe123.",256));