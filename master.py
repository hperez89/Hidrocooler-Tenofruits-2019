#!/usr/bin/python3
import time
import os
#import pymysql
import RPi.GPIO as GPIO
import pigpio

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
""" ############### RASPBERRY 1 MOTORES ################ """
GPIO.setup(4, GPIO.OUT)     #motor cadena M1
GPIO.setup(17, GPIO.OUT)    #motor cadena M2
GPIO.setup(18, GPIO.OUT)    #motor cadena M3
GPIO.setup(27, GPIO.OUT)    #motor cadena entrada hidro M4
GPIO.setup(22, GPIO.OUT)    #motor cadena dentro hidro M5
GPIO.setup(23, GPIO.OUT)    #motor salida hidro M6
GPIO.setup(24, GPIO.OUT)    #motor giro atras M7
GPIO.setup(10, GPIO.OUT)    #motor cadena giro M7
GPIO.setup(9, GPIO.OUT)     #motor cadena N9
GPIO.setup(25, GPIO.OUT)    #motor cadena M10
GPIO.setup(11, GPIO.OUT)    #motor cadena M11
GPIO.setup(6, GPIO.OUT)     #motor cadena M12
GPIO.setup(12, GPIO.OUT)    #motor giro adelandte M7


""" #### funcion lectora de sensores #### """
sensores = pigpio.pi('192.168.0.96')

"""sensores[4] => sensor motor 1                        sensores[17] => sensor motor 2
sensores[18] => sensor motor 3                          sensores[27] => sensor entrada hidro S4
sensores[22] => sensor salida hidro S5 salida ducha     sensores[23] => sensor entrada giro S6
sensores[24] => sensor no girado S7                     sensores[10] => Sensor girado S8
sensores[9] => presencia de bins S9                     sensores[25] => Sensor motor 9 S10
sensores[11] => Sensor motor 10 S11                     sensores[8] => Sensor motor 11 S12       sensores[7] => Sensor motor 12 S13
sensores[5] => boton partir                             sensores[6] => boton parar               sensores[12] => boton pausa"""
def parartodos():
    GPIO.output(4, False)   #M1
    GPIO.output(17, False)  #M2
    GPIO.output(18, False)  #M3
    GPIO.output(27, False)  #M4
    GPIO.output(22, False)  #M5
    GPIO.output(23, False)  #M6
    GPIO.output(24, False)  #M7
    GPIO.output(10, False)  #M7_cadena
    GPIO.output(9, False)   #M9
    GPIO.output(25, False)  #M10
    GPIO.output(11, False)  #M11
    GPIO.output(6, False)   #M12
    GPIO.output(12, False)  #M7_INVERTIR
    GPIO.output(10, False)
def iniciar_cadenas():
    time.sleep(2)
    GPIO.output(6, True)    #M12
    time.sleep(2)
    GPIO.output(11, True)   #M11
    time.sleep(2)
    GPIO.output(25, True)   #M10
    time.sleep(2)
    GPIO.output(9, True)    #M9
    time.sleep(2)
    GPIO.output(23, True)   #M6
    time.sleep(2)
    GPIO.output(22, True)   #M5
    time.sleep(2)
    GPIO.output(27, True)   #M4
    time.sleep(2)
    GPIO.output(18, True)   #M3
    time.sleep(2)
    GPIO.output(17, True)   #M2
    time.sleep(2)
    GPIO.output(4, True)    #M1
    GPIO.output(10, True) #cadena giro
""" ############### ciclo master ################ """
parartodos()
estado = "parado"  ## iniciado / parado / pausa
estado_anterior = ""
girando = 0
anteriorbt1 = anteriorbt2 = anteriorbt3 = anteriorSPG= 0
contador = 0
contadorGIRO = 0
print("")
print("============================================================")
print("============== SISTEMA HIDROCOOLER SPSI 2019 ===============")
print("============================================================")
print("")
while(True):
    ##print("estado = "+estado)
    if(sensores.read(5) == 0 and anteriorbt1 == 1 and estado != "iniciado"):
        estado_anterior = estado
        print("iniciando motores...")
        iniciar_cadenas()
        estado = "iniciado"
    if(sensores.read(6) == 0 and anteriorbt2 == 1 and estado != "parado"):
        estado_anterior = estado
        estado = "parado"
        print("parando motores...")
        parartodos()
    """ ########################## INICIO Rutinas ################################## """
    """print("         sensor giro: "+str(sensores.read(10)))"""

    if(estado == "iniciado"):
        """ verificar sensores """
        if(sensores.read(17) == 1 and sensores.read(4) == 1):
            GPIO.output(4, False)
        else:
            GPIO.output(4, True)
        if(sensores.read(18) == 1 and sensores.read(17) == 1):
            GPIO.output(17, False)
        else:
            GPIO.output(17, True)
        if(sensores.read(27) == 1 and sensores.read(18) == 1):
            GPIO.output(18, False)
        else:
            GPIO.output(18, True)
        if(sensores.read(11) == 1 and sensores.read(25) == 1):
            GPIO.output(9, False)
        else:
            GPIO.output(9, True)
        if(sensores.read(8) == 1 and sensores.read(11) == 1):
            GPIO.output(25, False)
        else:
            GPIO.output(25, True)
        if(sensores.read(7) == 1 and sensores.read(8) == 1):
            GPIO.output(11, False)
        else:
            GPIO.output(11, True)
        if(sensores.read(7) == 1):
            GPIO.output(6, False)
        else:
            GPIO.output(6, True)
        if(sensores.read(27) == 1 and sensores.read(22) == 1 and sensores.read(23) == 1):
            GPIO.output(27, False)
        else:
            GPIO.output(27, True)
        if(sensores.read(9) == 1 and sensores.read(10) == 1 and sensores.read(25) == 1):
            GPIO.output(10, False)
        if(sensores.read(9) == 1 and sensores.read(10) == 1 and sensores.read(25) == 0):
            GPIO.output(10, True)
        """ verificar giro """

        if(sensores.read(24) == 1 and sensores.read(9) == 1 and girando == 0):
            GPIO.output(10, False)
            GPIO.output(12, True)
            girando = 1
            print("              ACTIVA GIRAR")
        if(sensores.read(23) == 1 and sensores.read(24) == 1 and sensores.read(9) == 0 and girando == 0):  ##activa cadena entrada bins al giro
            GPIO.output(12, False)
            GPIO.output(10, True)
        if((sensores.read(23) == 1 and (girando == 1 or girando == -1)) or (sensores.read(24) == 0 and sensores.read(10) == 0)):
            GPIO.output(23, False)
        if(sensores.read(9) == 0 and sensores.read(24) == 1):
            GPIO.output(23, True)
        if(sensores.read(22) == 1 and sensores.read(23) == 1):
            GPIO.output(22, False)
        else:
            GPIO.output(22, True)
        if(sensores.read(9) == 0 and sensores.read(10) == 1 and girando == 0):
            ##devolver giro
            time.sleep(2)
            GPIO.output(24, True)
            time.sleep(0.2)
            GPIO.output(10, False)
            girando = -1
            print("              DEVOLVIENDO DEL GIRO")
        if(sensores.read(24) == 1 and girando == -1):
            GPIO.output(10, True)
            GPIO.output(24, False)
            GPIO.output(12, False)
            girando = 0
            print("              PARANDO GIRO DE VUELTA")
        if(sensores.read(10) == 1 and girando == 1):
            GPIO.output(12, False)
            GPIO.output(24, False)
            GPIO.output(10, True)
            GPIO.output(9, True)
            girando = 0
            print("              PARANDO GIRO")

    ##########################  FIN Rutinas  ##################################
    anteriorbt1 = sensores.read(5)
    anteriorbt2 = sensores.read(6)
    anteriorbt3 = sensores.read(12)
    time.sleep(0.1)

