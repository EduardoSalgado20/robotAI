# Importar las bibliotecas necesarias
import tensorflow as tf
from tensorflow import keras
import numpy as np
import machine
from machine import Pin
from machine import I2C
import network
import esp32
import esp
import urequests as requests
import ujson as json
import utime as time
from time import sleep
from machine import reset
import cv2

# Configuración de la red Wi-Fi
SSID = 'nombre_de_red' # Comprar modem o  router
PASSWORD = 'contraseña_de_red'

# Dirección IP de la Raspberry Pi 4B
RASPBERRY_PI_IP = '192.168.1.100' #Ejemplo

# Cargar el modelo de IA preentrenado para reconocimiento de objetos
modelo = keras.models.load_model('modelo_objetos.h5') # aun no se ha creado

# Definir las clases de objetos que se pueden reconocer
clases_objetos = ['perro', 'gato', 'automóvil', 'bicicleta'] # solo es un ejemplo

# Inicializar la conexión Wi-Fi
sta_if = network.WLAN(network.STA_IF) # Establecer el modo de conexión Wi-Fi
sta_if.active(True)     # Activar la conexión Wi-Fi
sta_if.connect(SSID, PASSWORD) # Conectar a la red Wi-Fi
while not sta_if.isconnected(): # Esperar a que se establezca la conexión Wi-Fi
    pass

print('Conexión Wi-Fi establecida')

# Configuración de la cámara ESP32-CAM
i2c = I2C(sda=Pin(14), scl=Pin(15), freq=100000)
cam = esp32.CAM(sda=Pin(14), scl=Pin(15), freq=100000, i2c=i2c)

# Función para capturar y procesar imágenes de la cámara
def capturar_imagen():
    img = cam.capture()
    img = img.resize(224, 224)  # Ajustar el tamaño de la imagen
    img = img.to_grayscale()  # Convertir la imagen a escala de grises
    img = img.invert()  # Invertir los colores de la imagen
    img = img.to_bytes()  # Convertir la imagen a bytes
    return img

# Función para preprocesar la imagen antes de pasarla al modelo
def preprocesar_imagen(imagen):
    imagen = tf.image.resize(imagen, (224, 224))  # Ajustar el tamaño de la imagen
    imagen = imagen / 255.0  # Normalizar los valores de píxeles
    imagen = tf.expand_dims(imagen, axis=0)  # Agregar una dimensión adicional para el lote
    return imagen

def reconocer_objeto(imagen):
    # Realizar la predicción del objeto en la imagen
    prediccion = modelo.predict(imagen)
    indice_clase = np.argmax(prediccion)
    objeto_reconocido = clases_objetos[indice_clase]
    return objeto_reconocido
# Cargar el modelo de reconocimiento de objetos
modelo = tf.keras.models.load_model(MODELO_RECONOCIMIENTO)
# Función para mover los motores hacia adelante

def mover_adelante():
    # Código para mover los motores hacia adelante
    # Utiliza los pines PIN_MOTOR_1, PIN_MOTOR_2, PIN_MOTOR_3, PIN_MOTOR_4

# Función para detener los motores
def detener():
    # Código para detener los motores
    # Utiliza los pines PIN_MOTOR_1, PIN_MOTOR_2, PIN_MOTOR_3, PIN_MOTOR_4

# Bucle principal del programa
while True:
    try:
        # Capturar una imagen con la cámara
        imagen = capturar_imagen()
        # Preprocesar la imagen
        imagen = preprocesar_imagen(imagen)
        # Realizar el reconocimiento de objetos en la imagen
        objeto = reconocer_objeto(imagen)
        #si se detecta el objeto deseado, mover los motores hacia el objetivo
        if objeto == 'objeto_deseado':
            mover_adelante()
            url = 'http://' + RASPBERRY_PI_IP + '/mover_robot'
            resp = requests.get(url)
        # Imprimir el resultado del reconocimiento
        print("Objeto reconocido:", objeto)
            if resp.status_code == 200:
                mover_adelante()
            else:
                print('Error al enviar la petición a la Raspberry Pi 4B')
        
        # Mostrar el flujo de video en una ventana
        cv2.imshow('Flujo de Video', imagen)
        cv2.waitKey(1)
        # Esperar un tiempo antes de tomar la siguiente imagen
        time.sleep(1)
        
    except KeyboardInterrupt:
        detener()
        break
# Cerrar la ventana de visualización
cv2.destroyAllWindows()