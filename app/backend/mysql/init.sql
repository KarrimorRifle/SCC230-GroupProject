USE DB;

CREATE TABLE accounts(
    `AccountID` BIGINT not null AUTO_INCREMENT,
    `FirstName` varchar(100) NOT NULL,
    `Surname` varchar(100) NOT NULL,
    `Email` varchar(100) NOT NULL,
    `Password` VARCHAR(100) NOT NULL,
    `SessionID` VARCHAR(100),
    `SessionExp` DATETIME,
    PRIMARY KEY (AccountID)
);

CREATE TABLE `hubs`(
    `hubID` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `hubName` VARCHAR(255) NOT NULL
);

CREATE INDEX idx_hubs_hubName ON `hubs` (`hubName`);

CREATE TABLE `accounts_hubsRelation`(
    `accountID` BIGINT NOT NULL,
    `hubID` BIGINT UNSIGNED NOT NULL,
    `permissionLevel` INT NOT NULL,
    CONSTRAINT UserHubRelation PRIMARY KEY (accountID, hubID),
    FOREIGN KEY (accountID) REFERENCES accounts(AccountID),
    FOREIGN KEY (hubID) REFERENCES hubs(hubID)
);

CREATE TABLE `triggers`(
    `triggerID` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `triggerName` VARCHAR(255) NOT NULL,
    `eventListenerID` BIGINT NOT NULL 
);

CREATE TABLE `devices`(
    `deviceID` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `deviceName` VARCHAR(255) NOT NULL,
    `deviceType` VARCHAR(255) NOT NULL,
    `ipAddress` VARCHAR(255) NOT NULL UNIQUE,
    `hubID` BIGINT UNSIGNED NOT NULL,
    FOREIGN KEY (hubID) REFERENCES hubs(hubID)
);

CREATE INDEX idx_devices_deviceName ON `devices` (`deviceName`);

CREATE TABLE `schedules`(
    `eventID` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `scheduleName` VARCHAR(255) NOT NULL,
    `hubID` BIGINT UNSIGNED NOT NULL,
    `deviceInstructions` JSON NOT NULL,
    `triggerID` BIGINT UNSIGNED NOT NULL,
    FOREIGN KEY (hubID) REFERENCES hubs(hubID),
    FOREIGN KEY (triggerID) REFERENCES triggers(triggerID)
);

-- To reset DB delete the container and start up again
-- if any changes were made do the last line AND `docker-compose build`

INSERT INTO accounts(FirstName, Surname, Email, `Password`)
-- passwords are 'JhonDoe123.' and 'JaneDoe123.' respectively
Values("Jhon","Doe","jhondoe@gmail.com", "$2b$12$IdHh.7xshmNM2kzFq9ei8eZkv1Qio3Ds2OVHvuGuymVl3yBcIdtSS" ),("Jane","Doe","janedoe@gmail.com","$2b$12$0tJQMTo/mbqHli7jO5qDGOewD39brx1Z3nkLgA0U3biwD3iug1wEO");