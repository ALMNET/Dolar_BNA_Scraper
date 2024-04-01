CREATE TABLE `General`.Historico_Dolar_Nacion (
	ID_Trans INT auto_increment NOT NULL,
	CONSTRAINT Historico_Dolar_Nacion_PK PRIMARY KEY (ID_Trans),
	Fecha_Recepcion DATETIME NULL,
	Fecha_Creacion DATETIME NULL,
	Origen VARCHAR(20) NULL,
	Dolar_Venta FLOAT NULL,
	Dolar_Compra FLOAT NULL,
	Noticia_Relevante1 varchar(100) NULL,
	Noticia_Relevante2 varchar(100) NULL,
	Noticia_Relevante3 varchar(100) NULL
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_0900_ai_ci;
