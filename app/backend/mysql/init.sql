CREATE DATABASE database;
USE database;

CREATE TABLE `accounts`(
    `accountID` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `firstName` VARCHAR(255) NOT NULL,
    `surname` VARCHAR(255) NOT NULL,
    `email` VARCHAR(255) NOT NULL UNIQUE,
    `password` VARCHAR(255) NOT NULL,
    `sessionID` VARCHAR(255) NOT NULL,
    `sessionExp` DATETIME NOT NULL
);

CREATE TABLE `hubs`(
    `hubID` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `hubName` VARCHAR(255) NOT NULL
);

CREATE INDEX idx_hubs_hubName ON `hubs` (`hubName`);

CREATE TABLE `accounts_hubsRelation`(
    `accountID` BIGINT UNSIGNED NOT NULL,
    `hubID` BIGINT UNSIGNED NOT NULL,
    `permissionLevel` INT NOT NULL,
    CONSTRAINT UserHubRelation PRIMARY KEY (accountID, hubID),
    FOREIGN KEY (accountID) REFERENCES accounts(accountID),
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