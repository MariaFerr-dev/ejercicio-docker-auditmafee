CREATE TABLE IF NOT EXISTS usuarios (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL
);

INSERT INTO usuarios (nombre)
VALUES ('Ana'), ('Carlos'), ('María')
ON DUPLICATE KEY UPDATE nombre = VALUES(nombre);
