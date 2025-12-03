CREATE TABLE amostras (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    obs VARCHAR(255) NOT NULL,
    link_foto VARCHAR(100)
);

CREATE TABLE amostra_coletas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    amostra_id INT,
    latitude VARCHAR(100) NOT NULL,
    longitude VARCHAR(50) NOT NULL,
    nome_local VARCHAR(50) NOT NULL,
    data_coleta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    temperatura_fonte DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (amostra_id) REFERENCES amostras(id)
);

CREATE TABLE amostra_medidas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    amostra_id INT,
    ph DECIMAL(10,2) NOT NULL,
    temperatura_externa DECIMAL(10,2) NOT NULL,
    umidade_externa DECIMAL(10,2) NOT NULL,
    ntu_turbidez DECIMAL(10,2) NOT NULL,
    nivel VARCHAR(10),
    data_medida TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (amostra_id) REFERENCES amostras(id)
);