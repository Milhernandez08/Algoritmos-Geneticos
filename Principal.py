import os, sys
import cv2 as cv
import numpy as np
import random
import pylab as pl
import matplotlib.pyplot as plt

from PyQt5.QtWidgets import QApplication, QDialog, QFileDialog, QProgressBar
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtCore import Qt
from PyQt5.Qt import QMovie
from openpyxl import Workbook
from datetime import datetime

form_class = uic.loadUiType("Diseño.ui")[0]

class Principal(QtWidgets.QMainWindow, form_class):
    def __init__(self):
        super(Principal, self).__init__()
        # ======================= VARIABLES GLOBALES ===========================
        global k, nMax, paquetes, m, tMax, t0, x100Paro
        # ======================= VENTANA1 PRINCIPAL ===========================
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        # ======================= SOQUEKETS DE CONECCIONES =====================
        self.connectActions()

    # ======================= CONECCIONES WIDGETS ============================
    def connectActions(self):
        self.btnEjecutar.clicked.connect(self.inicio)

    # ======================= ARRAYS ============================
    poblaciones = []
    mutaciones  = []
    costo       = []
    mayores     = []
    promedio    = []
    menores     = []
    # ======================= FUNCIONES ============================
    def inicio(self):
        ############ CARACTERISTAS DE LOS PAQUETES ############
        self.k = int(self.numPaq.text()) + 1
        self.nMax = int(self.tamMaxPaq.text())
        self.paquetes = dict()
        ############ CARACTERISTAS DEL CONTENEDOR DE PAQUETES ############
        self.m = int(self.tamContenedor.text())

        ############ CARACTERISTAS DE LA POBLACION ############
        self.tMax = int(self.tamMaxPob.text())
        self.t0 = int(self.tamInicialPob.text())

        ############ CARACTERISTAS DEL PORCENTAJE DE PARO ############
        self.x100Paro = int(self.porcentajeMin.text())

        ############ INICIO ############
        self.contenido_Paquetes(self.k, self.nMax)

        self.crear_Poblaciones(self.t0)

        DETENER = False
        #iteraciones = 0
        while DETENER == False:
            #iteraciones += 1
            self.hacer_Cruza_Y_No_Repeticion_de_Indices()

            self.hacer_Mutacion()

            self.agregar_Mutaciones_A_Poblaciones()

            self.mutaciones = []
            self.costo = []
            self.sumar_Paquetes()
            self.costo.sort(reverse = True)
            self.graficar_Menores_Promedio_Mayor()

            self.mutaciones.sort(reverse = True)
            self.mutaciones = self.mutaciones[:self.tMax]
            print("\n\n", self.paquetes, "\n", self.mutaciones, "\n\n")
            # --------------------- COLOCAR LA GRAFICA DE LOS PAQUETES ----------------------
            wb = Workbook() 
            #iteracion = 1  
             
            ruta = 'Mejores.xlsx'
            
            hoja = wb.active
            hoja.title = "Fecha-Valor"
            
            for fil in range(len(self.mutaciones)):
                muta = self.mutaciones[fil]
                if fil < int((self.tMax * self.x100Paro)/100):
                    for col in range (muta[0]):
                        
                        loc = muta[2][col]
                        hoja.cell(column=col+2, row=fil+2, value=self.paquetes.get(loc))
                    
            wb.save(filename = ruta)
                                                       
            #iteracion += 1
            # --------------------- FIN COLOCAR LA GRAFICA DE LOS PAQUETES ----------------------
            # --------------------- PODAR POBLACIONES ---------------------
            self.poblaciones = []
            for mut in self.mutaciones:
                self.poblaciones.append(mut[2])
            # --------------------- FIN DE LA PODA DE POBLACIONES ---------------------

            self.mutaciones = []
            num_Mayor = max(self.costo)
            if self.costo.count(num_Mayor) >= ((self.tMax*self.x100Paro) / 100):
                print(self.costo.count(num_Mayor), " >= ", ((self.tMax*self.x100Paro)/100))
                #print("cantidad de iteraciones dadas: ", iteraciones)
                DETENER = True

        print(self.mayores)
        print(self.promedio)
        print(self.menores)

    def contenido_Paquetes(self, Cantidad_Paquetes, Tamaño_Maximo_x_Paquete):
        for unidad in range (1, Cantidad_Paquetes):
            self.paquetes[unidad] = random.randint(1, Tamaño_Maximo_x_Paquete)

    def crear_Poblaciones(self, Cantidad_de_Poblacion_Inicial):
        for iteracion in range(self.t0):
            indices = list (self.paquetes.keys())
            random.shuffle(indices)
            self.poblaciones.append(indices)

    def hacer_Cruza_Y_No_Repeticion_de_Indices(self):
        centro = len(self.poblaciones[0])//2
        for info in range (0, len(self.poblaciones)-1):
            for info2 in range (info+1, len(self.poblaciones)):
                seguir = True

                parte1_2 = self.poblaciones[info][0:centro] + self.poblaciones[info2][centro:len(self.poblaciones[info2])]
                parte2_1 = self.poblaciones[info2][0:centro] + self.poblaciones[info][centro:len(self.poblaciones[info])]

                while seguir:
                    valor1 = 0
                    valor2 = 0
                    p1     = 0
                    p2     = 0

                    for i in parte1_2:
                        if parte1_2.count(i) > 1:
                            valor1 = i
                            p1 = parte1_2.index(i)
                            break

                    for v in parte2_1:
                        if parte2_1.count(v) > 1:
                            valor2 = v
                            p2 = parte2_1.index(v)
                            break

                    if valor1 != 0:
                        parte1_2[p1] = valor2
                        parte2_1[p2] = valor1
                    else:
                        seguir = False
                self.mutaciones.append(parte1_2)
                self.mutaciones.append(parte2_1)

    def hacer_Mutacion(self):
        posicion = 0
        for mut in self.mutaciones:
            repeticion = random.randrange(1,11)
            for rep in range(repeticion):
                valor1 = random.randrange(len(self.poblaciones[0]))
                valor2 = random.randrange(len(self.poblaciones[0]))
                while valor1 == valor2:
                    valor2 = random.randrange(len(self.poblaciones[0]))
                x = mut[valor1]
                y = mut[valor2]
                self.mutaciones[posicion][valor1] = y
                self.mutaciones[posicion][valor2] = x
            posicion += 1

    def agregar_Mutaciones_A_Poblaciones(self):
        for mut in self.mutaciones:
            self.poblaciones.append(mut)

    def sumar_Paquetes(self):
        for fil in range (len(self.poblaciones)):
            suma = 0
            pack = 0
            aux  = []
            for col in range(len(self.poblaciones[0])):
                suma += self.paquetes.get(self.poblaciones[fil][col])
                if suma <= self.m:
                    pack += 1
                    print("\nvalor de suma ", suma, "\tcantidad de paquetes ", pack, "\t de la fila ", fil, "\tvalor paquete ", self.paquetes.get(self.poblaciones[fil][col]), "\tposicion ", self.poblaciones[fil][col])
                else:
                    suma -= self.paquetes.get(self.poblaciones[fil][col])
                    break # -------- EL ERROR DE LAS SUMAS EN LA GRAFICA DE ECXEL FUE QUE NO HABIA INGRESADO EL BREAK --------
            aux.append(pack)
            print("Paquete ", pack, "\tdatos fila ", self.poblaciones[fil], "\tfila ", fil)
            aux.append(suma)
            self.mutaciones.append(aux)
            self.mutaciones[fil].append(self.poblaciones[fil].copy())
            self.mutaciones[fil].append(fil)
            self.costo.append(pack + suma)

    def graficar_Menores_Promedio_Mayor(self):
        self.costos = np.array(self.costo)
        self.mayores.append(self.costos.max())
        self.promedio.append(self.costos.mean())
        self.menores.append(self.costos.min())

        #plt = plt.subplots()

        plt.ylabel('Costos')
        plt.xlabel('Iteraciones')
        plt.grid()

        plt.ion() # decimos de forma explícita que sea interactivo
        plt.plot(self.mayores, color="blue", marker='o' ,linewidth=2.5, linestyle=":", label="maximo")
        plt.plot(self.promedio, color="red", marker='*' ,linewidth=2.5, linestyle="-", label="media")
        plt.plot(self.menores, color="green", marker='x' ,linewidth=2.5, linestyle="--", label="minimo")

        plt.pause(0.5) # esto pausará el gráfico
        plt.cla() # esto limpia la info                        


    def limpiarDatos(self):
        self.numPaq.setText("")
        self.porcentajeMin.setText("")
        self.tamContenedor.setText("")
        self.tamInicialPob.setText("")
        self.tamMaxPob.setText("")
        self.tamMaxPaq.setText("")
# ======================= MAIN ============================
app = QtWidgets.QApplication(sys.argv)
main = Principal()
main.show()
sys.exit(app.exec_())
