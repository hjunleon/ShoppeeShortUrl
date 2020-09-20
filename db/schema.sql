DROP TABLE IF EXISTS `short_url_db`.`urls_tab`;

CREATE TABLE `short_url_db`.`urls_tab` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `url` VARCHAR(2083) NOT NULL,
    `short_key` VARCHAR(32) NOT NULL,
    `hashed_url` BINARY(20) NOT NULL,
    `ctime` INT UNSIGNED NOT NULL,
    PRIMARY KEY (`id`)
) collate='utf8mb4_bin' ENGINE=InnoDB;
 
CREATE UNIQUE INDEX idx_short_key ON `short_url_db`.`urls_tab` (short_key);
CREATE INDEX idx_hashed_url ON `short_url_db`.`urls_tab` (hashed_url);
