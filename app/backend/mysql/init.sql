USE DB;

CREATE TABLE accounts(
    `AccountID` varchar(100) NOT NULL,
    `FirstName` varchar(100) NOT NULL,
    `Surname` varchar(100) NOT NULL,
    `Email` varchar(100) NOT NULL,
    `Password` VARCHAR(100) NOT NULL,
    `SessionID` VARCHAR(100),
    `SessionExp` DATETIME,
    PRIMARY KEY (AccountID)
);

INSERT INTO accounts(AccountID, FirstName, Surname, Email, `Password`)
-- passwords are 'JhonDoe123.' and 'JaneDoe123.' respectively
Values("Accojk42VvlqdeBpOBc","Jhon","Doe","jhondoe@gmail.com", "$2b$12$IdHh.7xshmNM2kzFq9ei8eZkv1Qio3Ds2OVHvuGuymVl3yBcIdtSS" ),("Acc89kaE64Aize3NX2j","Jane","Doe","janedoe@gmail.com","$2b$12$0tJQMTo/mbqHli7jO5qDGOewD39brx1Z3nkLgA0U3biwD3iug1wEO");

CREATE TABLE `hubs`(
    `HubID` varchar(100) NOT NULL PRIMARY KEY,
    `HubName` VARCHAR(255) NOT NULL
);

INSERT INTO hubs(`HubID`,`HubName`)
Values("Hubk23098jwij123msd","Test Hub");

CREATE INDEX idx_hubs_hubName ON `hubs` (`hubName`);

CREATE TABLE `accounts_hubsRelation`(
    `AccountID` varchar(100) NOT NULL,
    `HubID` varchar(100) NOT NULL,
    `PermissionLevel` INT NOT NULL,
    CONSTRAINT UserHubRelation PRIMARY KEY (AccountID, HubID),
    FOREIGN KEY (AccountID) REFERENCES accounts(AccountID) ON DELETE CASCADE,
    FOREIGN KEY (HubID) REFERENCES hubs(HubID) ON DELETE CASCADE
);

INSERT INTO accounts_hubsRelation(`AccountID`,`HubID`,`PermissionLevel`)
Values("Acc89kaE64Aize3NX2j","Hubk23098jwij123msd",5);

CREATE TABLE `hub_inviteTokens`(
    `TokenID` INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `HubID` VARCHAR(100) NOT NULL,
    `Token` VARCHAR(50) NOT NULL,
    `Expiry` INT NOT NULL,
    FOREIGN KEY (HubID) REFERENCES hubs(HubID) ON DELETE CASCADE
);

INSERT INTO hub_inviteTokens(`HubID`, `Token`, `Expiry`)
VALUES ("Hubk23098jwij123msd", "testToken", 2147483647);

CREATE TABLE `devices`(
    `DeviceID` varchar(100) NOT NULL PRIMARY KEY,
    `DeviceName` VARCHAR(255) NOT NULL,
    `Key` VARCHAR(255) NOT NULL,
    `IpAddress` VARCHAR(255) NOT NULL UNIQUE,
    `Version` FLOAT,
    `Company` VARCHAR(255) NOT NULL DEFAULT "Tuya",
    `HubID` varchar(100) NOT NULL,
    FOREIGN KEY (HubID) REFERENCES hubs(HubID) ON DELETE CASCADE
);

CREATE TABLE `device_vars`(
    `VarID` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `DeviceID` varchar(100) NOT NULL,
    `VarName` VARCHAR(255) NOT NULL,
    `VarType` VARCHAR(255) NOT NULL,
    `Writeable` TINYINT UNSIGNED NOT NULL DEFAULT 0,
    FOREIGN KEY (DeviceID) REFERENCES devices(DeviceID) ON DELETE CASCADE
);

INSERT INTO devices(`DeviceID`,`DeviceName`,`Key`,`IpAddress`,`Version`,`Company`,`HubID`)
VALUES("Dev4t3rgd34df423gfsaeft","Test Device","12345678","192.168.0.1",1.0,"NotTuya","Hubk23098jwij123msd");

CREATE TABLE `schedules`(
    `ScheduleID` varchar(100) NOT NULL PRIMARY KEY,
    `ScheduleName` VARCHAR(255) NOT NULL,
    `Description` VARCHAR(1020) NOT NULL DEFAULT "No Description",
    `AuthorID` varchar(100) NOT NULL,
    `CopyFrom` varchar(100),
    `HubID` varchar(100),
    `IsActive` TINYINT UNSIGNED NOT NULL DEFAULT 0,
    `IsPublic` TINYINT UNSIGNED NOT NULL DEFAULT 0,
    `Rating` TINYINT UNSIGNED DEFAULT 0,
    `NumRated` INT UNSIGNED DEFAULT 0,
    `IsDraft` TINYINT UNSIGNED NOT NULL DEFAULT 1,
    FOREIGN KEY (HubID) REFERENCES hubs(HubID) ON DELETE CASCADE,
    FOREIGN KEY (AuthorID) REFERENCES accounts(AccountID) ON DELETE CASCADE,
    FOREIGN KEY (CopyFrom) REFERENCES accounts(AccountID) ON DELETE SET NULL
);

INSERT INTO schedules(`ScheduleID`,`ScheduleName`,`AuthorID`,`HubID`,`IsActive`,`IsPublic`)
Values("Schk129jd2i23kd34jf","Test Schedule","Accojk42VvlqdeBpOBc","Hubk23098jwij123msd",0,0);

INSERT INTO schedules(`ScheduleID`,`ScheduleName`,`AuthorID`,`HubID`,`IsActive`,`IsPublic`)
Values("Schk129jd2i23kd34af","Test Schedule","Acc89kaE64Aize3NX2j","Hubk23098jwij123msd",0,1);

CREATE TABLE `triggers`(
    `TriggerID` VARCHAR(100) NOT NULL,
    `ScheduleID` varchar(100) NOT NULL,
    PRIMARY KEY (TriggerID, ScheduleID),
    FOREIGN KEY (ScheduleID) REFERENCES schedules(ScheduleID) ON DELETE CASCADE
);

INSERT INTO triggers(`TriggerID`,`ScheduleID`)
Values("Trgk2190ej849dj345j","Schk129jd2i23kd34jf");

CREATE TABLE `trigger_data`(
    `DataID` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `TriggerID` varchar(100) NOT NULL,
    `Data` varchar(255) NOT NULL,
    `ListPos` INT UNSIGNED NOT NULL DEFAULT 0,
    FOREIGN KEY (TriggerID) REFERENCES triggers(TriggerID) ON DELETE CASCADE
);

INSERT INTO trigger_data(`TriggerID`,`Data`,`ListPos`)
Values("Trgk2190ej849dj345j", "var",0), ("Trgk2190ej849dj345j", "==",1), ("Trgk2190ej849dj345j", "4",2);

CREATE TABLE `function_blocks`( 
    `BlockID` varchar(100) NOT NULL PRIMARY KEY,
    `CommandType` VARCHAR(20) NOT NULL,
    `Num` INT NOT NULL, 
    `ScheduleID` varchar(100) NOT NULL,
    FOREIGN KEY (ScheduleID) REFERENCES schedules(ScheduleID) ON DELETE CASCADE
    -- `num` referenced as foreign key, must be unique.
);

CREATE TABLE `function_block_params`(
    `ParamID` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `Value` VARCHAR(255) NOT NULL,
    `FunctionBlockID` varchar(100) NOT NULL,
    `ScheduleID` varchar(100) NOT NULL,
    `ListPos` INT UNSIGNED NOT NULL,
    FOREIGN KEY (ScheduleID) REFERENCES schedules(ScheduleID) ON DELETE CASCADE,
    FOREIGN KEY (FunctionBlockID) REFERENCES function_blocks(BlockID) ON DELETE CASCADE
);

ALTER TABLE function_block_params MODIFY ListPos INT DEFAULT 0;

CREATE TABLE `function_block_links`(
    `LinkID` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `ParentID` varchar(100) NOT NULL,
    `Link` INT NOT NULL,
    `ScheduleID` varchar(100) NOT NULL,
    FOREIGN KEY (ScheduleID) REFERENCES schedules(ScheduleID) ON DELETE CASCADE, 
    FOREIGN KEY (ParentID) REFERENCES function_blocks(BlockID) ON DELETE CASCADE
);

CREATE TABLE `error_log`(
    `LogID` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `Error` VARCHAR(255) NOT NULL,
    `Time` VARCHAR(100) NOT NULL DEFAULT "0000-00-00 00:00:00"
);

-- To reset DB delete the container and start up again
-- if any changes were made do the last line AND `docker-compose build`
