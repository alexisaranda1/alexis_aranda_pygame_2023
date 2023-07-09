


def crear_bandera(ruta:str,bool:str):
    
    with open(f"{ruta}.txt","w") as archivo:
                    archivo.write(bool)



def leer_bandera(ruta:str,)->list:
    lista_bandera = []

    archivo = open(f"{ruta}.txt","r")
    for linea in archivo:
        # print(linea)
        lista_bandera.append(linea)
    
    archivo.close() 

    return lista_bandera