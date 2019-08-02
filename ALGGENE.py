import random
import numpy as np

k        = 15 + 1
nMax     = 5
paquetes = dict()
m        = 20
t0       = 2
tMax     = 20
x100Paro = 90



poblaciones = []
mutaciones  = []
costo       = []
mayores     = []
promedio    = []
menores     = []

def contenido_Paquetes(Cantidad_Paquetes, Tamaño_Maximo_x_Paquete):
    for unidad in range (1, Cantidad_Paquetes):
        paquetes[unidad] = random.randint(1, Tamaño_Maximo_x_Paquete)

def crear_Poblaciones(Cantidad_de_Poblacion_Inicial):
    for iteracion in range(t0):
        indices = list (paquetes.keys())
        random.shuffle(indices)
        poblaciones.append(indices)

def hacer_Cruza_Y_No_Repeticion_de_Indices():
    centro = len(poblaciones[0])//2
    for info in range (0, len(poblaciones)-1):
        for info2 in range (info+1, len(poblaciones)):
            seguir = True

            parte1_2 = poblaciones[info][0:centro] + poblaciones[info2][centro:len(poblaciones[info2])]
            parte2_1 = poblaciones[info2][0:centro] + poblaciones[info][centro:len(poblaciones[info])]

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
            mutaciones.append(parte1_2)
            mutaciones.append(parte2_1)

def hacer_Mutacion():
    posicion = 0
    for mut in mutaciones:
        repeticion = random.randrange(1,11)
        for rep in range(repeticion):
            valor1 = random.randrange(len(poblaciones[0]))
            valor2 = random.randrange(len(poblaciones[0]))
            while valor1 == valor2:
                valor2 = random.randrange(len(poblaciones[0]))
            x = mut[valor1]
            y = mut[valor2]
            mutaciones[posicion][valor1] = y
            mutaciones[posicion][valor2] = x
        posicion += 1

def agregar_Mutaciones_A_Poblaciones():
    for mut in mutaciones:
        poblaciones.append(mut)

def sumar_Paquetes():
    for fil in range (len(poblaciones)):
        suma = 0
        pack = 0
        aux  = []
        for col in range(len(poblaciones[0])):
            suma += paquetes.get(poblaciones[fil][col])
            if suma < m:
                pack += 1
            else:
                suma -= paquetes.get(poblaciones[fil][col])
        aux.append(pack)
        aux.append(suma)
        mutaciones.append(aux)
        mutaciones[fil].append(poblaciones[fil])
        costo.append(pack + suma)

def graficar_Menores_Promedio_Mayor():
    costos = np.array(costo)
    mayores.append(costos.max())
    promedio.append(costos.mean())
    menores.append(costos.min())
# INICIO
contenido_Paquetes(k, nMax)

crear_Poblaciones(t0)

DETENER = False
#iteraciones = 0
while DETENER == False:
    #iteraciones += 1
    hacer_Cruza_Y_No_Repeticion_de_Indices()

    hacer_Mutacion()

    agregar_Mutaciones_A_Poblaciones()

    mutaciones = []
    costo = []
    sumar_Paquetes()
    costo.sort(reverse = True)
    graficar_Menores_Promedio_Mayor()

    mutaciones.sort(reverse = True)
    mutaciones = mutaciones[:tMax]

    # --------------------- PODAR POBLACIONES ---------------------
    poblaciones = []
    for mut in mutaciones:
        poblaciones.append(mut[2])
    # --------------------- FIN DE LA PODA DE POBLACIONES ---------------------

    mutaciones = []

    num_Mayor = max(costo)
    if costo.count(num_Mayor) >= ((tMax*x100Paro) / 100):
        print(costo.count(num_Mayor), " >= ", ((tMax*x100Paro)/100))
        #print("cantidad de iteraciones dadas: ", iteraciones)
        DETENER = True

print(mayores)
print(promedio)
print(menores)
