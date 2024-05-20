import requests

# URL del archivo en Nextcloud (enlace público)
url_archivo = "https://drive.miteleferico.bo/s/ZG89gYjfsMwL7t4/download"

# Ruta de destino para guardar el archivo descargado localmente
ruta_destino_local = 'archivo.xlsx'
#ruta_destino_local = 'costo16horas.xlsx'

# Realizar solicitud GET para descargar el archivo
response = requests.get(url_archivo)

# Verificar si la solicitud fue exitosa (código de estado 200)
if response.status_code == 200:
    # Guardar el contenido del archivo en el archivo local
    with open(ruta_destino_local, 'wb') as archivo_local:
        archivo_local.write(response.content)
    print("El archivo se ha descargado correctamente.")
else:
    print(f"Error al descargar el archivo. Código de estado: {response.status_code}")
