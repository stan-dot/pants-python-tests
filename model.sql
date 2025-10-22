CREATE TABLE todo (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'Primary Key',
    title VARCHAR(255) NOT NULL,
    description TEXT,
    completed BOOLEAN NOT NULL DEFAULT 0,
    create_time DATETIME COMMENT 'Create Time',
    name VARCHAR(255)
) COMMENT='';