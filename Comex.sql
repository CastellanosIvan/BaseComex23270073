DROP DATABASE IF EXISTS comex;
CREATE DATABASE comex;
USE comex;

CREATE TABLE Categoria (
  idcategoria INT PRIMARY KEY,
  nombre VARCHAR(45)
);

CREATE TABLE Articulos (
  codigo CHAR(13) PRIMARY KEY,
  nombre VARCHAR(100),
  precio FLOAT,
  costo FLOAT,
  existencia INT,
  unidad VARCHAR(45),
  idcategoria INT,
  CONSTRAINT agrupa FOREIGN KEY (idcategoria) REFERENCES Categoria(idcategoria)
);

CREATE TABLE Clientes (
  telefono CHAR(10) PRIMARY KEY,
  nombre VARCHAR(120),
  direccion VARCHAR(120),
  rfc CHAR(13),
  correo VARCHAR(150)
);

CREATE TABLE Ventas (
  ventas INT PRIMARY KEY,
  fecha DATE,
  importe FLOAT,
  iva FLOAT,
  total FLOAT,
  telefono CHAR(10),
  CONSTRAINT genera FOREIGN KEY (telefono) REFERENCES Clientes(telefono)
);

CREATE TABLE Detalle_Ventas (
  ventas INT,
  codigo CHAR(13),
  cantidad INT NOT NULL,
  precio FLOAT NOT NULL,
  importe FLOAT NOT NULL,
  CONSTRAINT incluye FOREIGN KEY (ventas) REFERENCES Ventas(ventas),
  CONSTRAINT es_vendido FOREIGN KEY (codigo) REFERENCES Articulos(codigo)
);