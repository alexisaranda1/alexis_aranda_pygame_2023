import sqlite3

lista = []

with sqlite3.connect("mi_base_de_datos.db") as conexion:
    try:
        # CREAR TABLA--------------------------
        # sentencia = '''
        #             create table Ranking
        #             (
        #                 nombre text,
        #                 score integer
                        
        #             ) 
        #    
        #          '''
        # conexion.execute(sentencia)
        
        # INSERTAR-----------------------------

        # nombre = "Leo M"
        # score = 16000


        # sentencia = '''
        #             insert into Ranking (nombre, score) values(?,?)
        #             '''
        # conexion.execute(sentencia,(nombre,score))

        # SELECT-------------------

        # sentencia = '''
        #             select * from Ranking limit 2
        #             '''
        sentencia = '''
                    select * from Ranking order by score desc limit 3
                    '''
        cursor = conexion.execute(sentencia)
        for fila in cursor:
            # print(fila)

            lista.append(fila)


        print("Tabla creada")
    except Exception as e:
        print(f"Error en Base de datos {e}")
print(lista)