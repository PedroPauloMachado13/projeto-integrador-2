import mysql.connector

cnn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='projeto_integrador_2'
)

cursor = cnn.cursor()
cmd_insert_amostra = 'INSERT INTO amostras (id, obs, nome, link_foto) VALUES (%s, %s, %s, %s);'
cmd_insert_coleta = 'INSERT INTO amostra_coletas (amostra_id, latitude, longitude, nome_local, data_coleta, temperatura_fonte) VALUES (%s, %s, %s, %s, %s, %s);'
cmd_insert_medida = 'INSERT INTO amostra_medidas (amostra_id, ph, temperatura_externa, umidade_externa, ntu_turbidez, nivel, data_medida) VALUES (%s, %s, %s, %s, %s, %s, %s);'


# AMOSTRA 1
cursor.execute(cmd_insert_amostra, (1, "Balde para lavar pano de limpeza", "Amostra #1", 'link1'))
# AMOSTRA 2
cursor.execute(cmd_insert_amostra, (2, "Bom estado de uso", "Amostra #2", 'link2'))
# AMOSTRA 3
cursor.execute(cmd_insert_amostra, (3, "Rodeado de folhas caidas, grama e terra (mas aparentemente limpo)", "Amostra #3", 'link3'))
# AMOSTRA 4
cursor.execute(cmd_insert_amostra, (4, "Bastante utilizado, limpo", "Amostra #4", 'link4'))
# AMOSTRA 5
cursor.execute(cmd_insert_amostra, (5, "Água do lago, turva e aparentemente suja", "Amostra #5", 'link5'))
# AMOSTRA 6
cursor.execute(cmd_insert_amostra, (6, "Tanque atrás do restaurante universitário, para limpezas gerais e conexão de mangueira", "Amostra #6", 'link6'))
# AMOSTRA 7
cursor.execute(cmd_insert_amostra, (7, "Banheiro acessível ao lado do banheiro feminino, amostra recolhida da pia", "Amostra #7", 'link7'))

# DADOS DE COLETA AMOSTRA 1
cursor.execute(cmd_insert_coleta, (1, 22.41374, 45.44977, "Bloco B (B.1.1.1) (ao lado da mesa de sinuca)", "2025-12-02 10:41:00", 24.1))
# DADOS DE COLETA AMOSTRA 2
cursor.execute(cmd_insert_coleta, (2, 22.41382, 45.44950, "Bebedouro Bloco B (B.3.1.1)", "2025-12-02 10:46:00", 15.3))
# DADOS DE COLETA AMOSTRA 3
cursor.execute(cmd_insert_coleta, (3, 22.41277, 45.44862, "Torneira ao lado da BIM", "2025-12-02 10:57:00", 24.0))
# DADOS DE COLETA AMOSTRA 4
cursor.execute(cmd_insert_coleta, (4, 22.41203, 45.4464, "Bebedouro Bloco I (I.2.1.1)", "2025-12-02 11:02:00", 8.2))
# DADOS DE COLETA AMOSTRA 5
cursor.execute(cmd_insert_coleta, (5, 22.41180, 45.45096, "Lago", "2025-12-02 11:07:00", 26.9))
# DADOS DE COLETA AMOSTRA 6
cursor.execute(cmd_insert_coleta, (6, 22.41248, 45.45090, "Restaurante Universitário", "2025-12-02 11:12:00", 26.6))
# DADOS DE COLETA AMOSTRA 7
cursor.execute(cmd_insert_coleta, (7, 22.41340, 45.45045, "PRG", "2025-12-02 11:18:00", 25.3))

# MEDIDAS AMOSTRA 1
cursor.execute(cmd_insert_medida, (1, 7.4, 26.3, 67.5, 2563, "OK", "2025-12-02 14:53:00"))
# MEDIDAS AMOSTRA 2
cursor.execute(cmd_insert_medida, (2, 7.3, 25.9, 67.5, 1912, "OK", "2025-12-02 14:58:00"))
# MEDIDAS AMOSTRA 3
cursor.execute(cmd_insert_medida, (3, 7.33, 27.5, 69.2, 1821, "OK", "2025-12-02 15:03:00"))
# MEDIDAS AMOSTRA 4
cursor.execute(cmd_insert_medida, (4, 7.4, 28.1, 65.4, 1821, "OK", "2025-12-02 15:08:00"))
# MEDIDAS AMOSTRA 5
cursor.execute(cmd_insert_medida, (5, 6.74, 26.3, 65.3, 3000, "OK", "2025-12-02 15:13:00")) # Turbidade atingiu máx do sensor
# MEDIDAS AMOSTRA 6
cursor.execute(cmd_insert_medida, (6, 7.4, 27.0, 63.9, 1889, "OK", "2025-12-02 15:18:00"))
# MEDIDAS AMOSTRA 7
cursor.execute(cmd_insert_medida, (7, 7.06, 26.2, 64.8, 1912, "OK", "2025-12-02 15:23:00"))

cnn.commit()
cnn.close()