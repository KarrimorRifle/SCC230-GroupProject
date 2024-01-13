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
-- passwords are 'JhonDoe123.' and 'JaneDoe123.' respectively
Values("Jhon","Doe","jhondoe@gmail.com", "$2b$12$IdHh.7xshmNM2kzFq9ei8eZkv1Qio3Ds2OVHvuGuymVl3yBcIdtSS" ),("Jane","Doe","janedoe@gmail.com","$2b$12$0tJQMTo/mbqHli7jO5qDGOewD39brx1Z3nkLgA0U3biwD3iug1wEO");