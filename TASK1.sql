BEGIN TRANSACTION;
DROP TABLE IF EXISTS `Sports`;
CREATE TABLE IF NOT EXISTS `Sports` (
	`StudentID`	INTEGER,
	`Contact`	TEXT,
	`Cost`	REAL,
	PRIMARY KEY(`StudentID`),
	FOREIGN KEY(`StudentID`) REFERENCES `Registration`(`StudentID`)
);
DROP TABLE IF EXISTS `Registration`;
CREATE TABLE IF NOT EXISTS `Registration` (
	`StudentID`	INTEGER,
	`Type`	TEXT,
	`Venue`	TEXT,
	`Session`	TEXT,
	PRIMARY KEY(`StudentID`),
	FOREIGN KEY(`StudentID`) REFERENCES `Registration`(`StudentID`)
);
DROP TABLE IF EXISTS `Cultural`;
CREATE TABLE IF NOT EXISTS `Cultural` (
	`StudentID`	INTEGER,
	`Race`	TEXT,
	PRIMARY KEY(`StudentID`),
	FOREIGN KEY(`StudentID`) REFERENCES `Registration`(`StudentID`)
);
DROP TABLE IF EXISTS `Arts`;
CREATE TABLE IF NOT EXISTS `Arts` (
	`StudentID`	INTEGER,
	`Performance`	TEXT,
	FOREIGN KEY(`Performance`) REFERENCES `Registration`(`StudentID`),
	PRIMARY KEY(`StudentID`)
);
COMMIT;
