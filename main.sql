PRAGMA foreign_keys = OFF;

-- ----------------------------
-- Table structure for chat_history
-- ----------------------------
DROP TABLE IF EXISTS "main"."Chat_History";
CREATE TABLE "Chat_History" (
"ID"  INTEGER NOT NULL,
"User_ID"  INTEGER,
"Target_ID"  INTEGER,
"Target_Type"  TEXT,
"Data"  BLOB,
"Sent"  INTEGER,
PRIMARY KEY ("ID" ASC)
);

-- ----------------------------
-- Table structure for friends
-- ----------------------------
DROP TABLE IF EXISTS "main"."Friends";
CREATE TABLE "Friends" (
"Request_User_ID"  INTEGER NOT NULL,
"Receive_User_ID"  INTEGER NOT NULL,
"Accepted"  TEXT,
PRIMARY KEY ("Request_User_ID" ASC, "Receive_User_ID")
);

-- ----------------------------
-- Table structure for rooms
-- ----------------------------
DROP TABLE IF EXISTS "main"."Rooms";
CREATE TABLE "Rooms" (
"ID"  INTEGER NOT NULL,
"Room_Name"  TEXT,
PRIMARY KEY ("ID")
);

-- ----------------------------
-- Table structure for room_user
-- ----------------------------
DROP TABLE IF EXISTS "main"."Room_User";
CREATE TABLE "Room_User" (
"ID"  INTEGER NOT NULL,
"Room_ID"  INTEGER,
"User_ID"  INTEGER,
PRIMARY KEY ("ID")
);

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS "main"."Users";
CREATE TABLE "Users" (
"ID"  INTEGER NOT NULL,
"Username"  TEXT,
"Password"  TEXT,
"Nickname"  TEXT,
PRIMARY KEY ("ID" ASC)
);
