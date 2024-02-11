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

INSERT INTO accounts(FirstName, Surname, Email, `Password`)
-- passwords are 'JhonDoe123.' and 'JaneDoe123.' respectively
    Values("Jhon","Doe","jhondoe@gmail.com", "$2b$12$IdHh.7xshmNM2kzFq9ei8eZkv1Qio3Ds2OVHvuGuymVl3yBcIdtSS" ),("Jane","Doe","janedoe@gmail.com","$2b$12$0tJQMTo/mbqHli7jO5qDGOewD39brx1Z3nkLgA0U3biwD3iug1wEO");

CREATE TABLE `hubs`(
    `HubID` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `HubName` VARCHAR(255) NOT NULL
);

CREATE INDEX idx_hubs_hubName ON `hubs` (`hubName`);

CREATE TABLE `accounts_hubsRelation`(
    `AccountID` BIGINT NOT NULL,
    `HubID` BIGINT UNSIGNED NOT NULL,
    `PermissionLevel` INT NOT NULL,
    CONSTRAINT UserHubRelation PRIMARY KEY (AccountID, HubID),
    FOREIGN KEY (AccountID) REFERENCES accounts(AccountID),
    FOREIGN KEY (HubID) REFERENCES hubs(HubID)
);

CREATE TABLE `triggers`(
    `TriggerID` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `TriggerName` VARCHAR(255) NOT NULL,
    `EventListenerID` BIGINT NOT NULL 
);

CREATE TABLE `devices`(
    `DeviceID` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `DeviceName` VARCHAR(255) NOT NULL,
    `DeviceType` VARCHAR(255) NOT NULL,
    `IpAddress` VARCHAR(255) NOT NULL UNIQUE,
    `HubID` BIGINT UNSIGNED NOT NULL,
    FOREIGN KEY (HubID) REFERENCES hubs(HubID)
);

CREATE INDEX idx_devices_deviceName ON `devices` (`deviceName`);

CREATE TABLE `schedules`(
    `EventID` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `ScheduleName` VARCHAR(255) NOT NULL,
    `AuthorID` BIGINT UNSIGNED NOT NULL FOREIGN KEY REFERENCES accounts(AccountID),
    `HubID` BIGINT UNSIGNED,
    `TriggerID` BIGINT UNSIGNED NOT NULL,
    `IsActive` TINYINT UNSIGNED NOT NULL,
    `IsPublic` TINYINT UNSIGNED NOT NULL,
    `Rating` TINYINT UNSIGNED,
    FOREIGN KEY (HubID) REFERENCES hubs(HubID),
    FOREIGN KEY (TriggerID) REFERENCES triggers(TriggerID)
);

CREATE TABLE `function_block_params`(
    `ParamID` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `Value` VARCHAR(255) NOT NULL,
    `FunctionBlockID` BIGINT UNSIGNED NOT NULL FOREIGN KEY REFERENCES function_blocks(FunctionBlockID)
);

CREATE TABLE `function_block_links`(
    `LinkID` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `ParentID` BIGINT UNSIGNED NOT NULL FOREIGN KEY REFERENCES function_blocks(FunctionBlockID)
    `LinkedTo` INT NOT NULL FOREIGN KEY REFERENCES function_blocks(Num)
);

CREATE TABLE `function_blocks`( 
    `FunctionBlockID` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `CommandType` VARCHAR(20) NOT NULL,
    `Num` INT NOT NULL,
    `ScheduleID` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT FOREIGN KEY REFERENCES schedules(EventID)
);

-- To reset DB delete the container and start up again
-- if any changes were made do the last line AND `docker-compose build`