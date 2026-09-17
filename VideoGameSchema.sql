CREATE DATABASE IF NOT EXISTS videoGameDB;

USE videoGameDB;

CREATE USER IF NOT EXISTS 'gameDev'@'localhost' IDENTIFIED BY 'your_password_here';

GRANT 
	SELECT,
    INSERT,
    UPDATE,
    DELETE,
    CREATE,
    ALTER,
    DROP
ON videoGameDB.* TO 'gameDev'@'localhost';

FLUSH PRIVILEGES;

CREATE TABLE IF NOT EXISTS games (
	id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    release_date VARCHAR(255) NOT NULL,
    genre VARCHAR(255) NOT NULL,
    platforms VARCHAR(255) ,
    metacritic INT,
    rating FLOAT
	);

   USE videogamedb;
   SELECT * FROM games;