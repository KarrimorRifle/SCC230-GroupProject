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
    FOREIGN KEY (AccountID) REFERENCES accounts(AccountID),
    FOREIGN KEY (HubID) REFERENCES hubs(HubID)
);

INSERT INTO accounts_hubsRelation(`AccountID`,`HubID`,`PermissionLevel`)
Values("Accojk42VvlqdeBpOBc","Hubk23098jwij123msd",10);

CREATE TABLE `devices`(
    `DeviceID` varchar(100) NOT NULL PRIMARY KEY,
    `DeviceName` VARCHAR(255) NOT NULL,
    `DeviceType` VARCHAR(255) NOT NULL,
    `IpAddress` VARCHAR(255) NOT NULL UNIQUE,
    `HubID` varchar(100) NOT NULL,
    FOREIGN KEY (HubID) REFERENCES hubs(HubID)
);

INSERT INTO devices(`DeviceID`,`DeviceName`,`DeviceType`,`IpAddress`,`HubID`)
Values("Dev4t3rgd34df423gfs","Test Device","Test Device","1.1.1.1","Hubk23098jwij123msd");

CREATE TABLE `schedules`(
    `ScheduleID` varchar(100) NOT NULL PRIMARY KEY,
    `ScheduleName` VARCHAR(255) NOT NULL,
    `AuthorID` varchar(100) NOT NULL,
    `HubID` varchar(100),
    `IsActive` TINYINT UNSIGNED NOT NULL,
    `IsPublic` TINYINT UNSIGNED NOT NULL,
    `Rating` TINYINT UNSIGNED,
    FOREIGN KEY (HubID) REFERENCES hubs(HubID),
    FOREIGN KEY (AuthorID) REFERENCES accounts(AccountID)
);

INSERT INTO schedules(`ScheduleID`,`ScheduleName`,`AuthorID`,`HubID`,`IsActive`,`IsPublic`,`Rating`)
Values("Schk129jd2i23kd34jf","Test Schedule","Accojk42VvlqdeBpOBc","Hubk23098jwij123msd",0,0,0);

CREATE TABLE `triggers`(
    `TriggerID` VARCHAR(100) NOT NULL,
    `ScheduleID` varchar(100) NOT NULL,
    PRIMARY KEY (TriggerID, ScheduleID),
    FOREIGN KEY (ScheduleID) REFERENCES schedules(ScheduleID)
);

INSERT INTO triggers(`TriggerID`,`ScheduleID`)
Values("Trgk2190ej849dj345j","Schk129jd2i23kd34jf");

CREATE TABLE `trigger_data`(
    `DataID` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `DeviceID` varchar(100) NOT NULL,
    `TriggerID` varchar(100) NOT NULL,
    `Data` varchar(255) NOT NULL,
    `ListPos` INT UNSIGNED NOT NULL,
    FOREIGN KEY (DeviceID) REFERENCES devices(DeviceID),
    FOREIGN KEY (TriggerID) REFERENCES triggers(TriggerID)
);

ALTER TABLE trigger_data MODIFY ListPos INT DEFAULT 0;

INSERT INTO trigger_data(`TriggerID`,`DeviceID`,`Data`,`ListPos`)
Values("Trgk2190ej849dj345j","Dev4t3rgd34df423gfs", "var",0), ("Trgk2190ej849dj345j","Dev4t3rgd34df423gfs", "==",1), ("Trgk2190ej849dj345j","Dev4t3rgd34df423gfs", "4",2);

CREATE TABLE `function_blocks`( 
    `BlockID` varchar(100) NOT NULL PRIMARY KEY,
    `CommandType` VARCHAR(20) NOT NULL,
    `Num` INT NOT NULL, 
    `ScheduleID` varchar(100) NOT NULL,
    FOREIGN KEY (ScheduleID) REFERENCES schedules(ScheduleID)
    -- `num` referenced as foreign key, must be unique.
);

CREATE TABLE `function_block_params`(
    `ParamID` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `Value` VARCHAR(255) NOT NULL,
    `FunctionBlockID` varchar(100) NOT NULL,
    `ScheduleID` varchar(100) NOT NULL,
    `ListPos` INT UNSIGNED NOT NULL,
    FOREIGN KEY (ScheduleID) REFERENCES schedules(ScheduleID),
    FOREIGN KEY (FunctionBlockID) REFERENCES function_blocks(BlockID)
);

ALTER TABLE function_block_params MODIFY ListPos INT DEFAULT 0;

CREATE TABLE `function_block_links`(
    `LinkID` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `ParentID` varchar(100) NOT NULL,
    `Link` INT NOT NULL,
    `ScheduleID` varchar(100) NOT NULL,
    FOREIGN KEY (ScheduleID) REFERENCES schedules(ScheduleID), 
    FOREIGN KEY (ParentID) REFERENCES function_blocks(BlockID)
);

-- To reset DB delete the container and start up again
-- if any changes were made do the last line AND `docker-compose build`
