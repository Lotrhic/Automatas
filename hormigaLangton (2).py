from copy import deepcopy
from random import randint
import json
import pygame

def generarMatriz(filas, cols):
    """
Función que genera una matriz con valores aleatorios entre 0 y 1
Entradas: El tamaño de la Matriz(número de filas y de columnas)
salida: la nueva matriz
"""
    M = []
    for f in range(filas):
        fila = []
        for c in range(cols):
            fila.append(randint(0, 1))
        M.append(fila)
    return M

def dibujarMatriz(M,hormigas, tam, window):
    """
Procedimiento que dibija la matriz y las hormigas en su respectiva ubicación
entradas: -la matriz
          -las hormigas
          -el tamaño de la ventana
colorea con rojo en la posición de cada hormiga
"""
    fila=len(M)
    cols=len(M[0])
    window.fill((0,0,0))
    for f in range(fila):
        for c in range(cols):
            if M[f][c]==0:
                pygame.draw.rect(window, (255,255,255),(c*tam, f*tam, tam, tam))
            for h in hormigas:
                if c == h[1] and f == h[0]:
                        pygame.draw.rect(window, (255,0,0),(c*tam, f*tam, tam, tam))

def mover_hormiga(hormigas,M,direccion):
    """
Funcion que realiza el movimiento de las hormigas en la dirección correspondiente
Entradas: -la(s) hormiga(s)
          -la matriz
          -la dirección actual de cada hormiga
Salidas:
         -Mover a las hormiga segun corresponda

"""
    i= 0
    for h in hormigas:
        movi= [[1,1],[0,1],[1,-1],[0,-1]]
        f = h[0]
        c = h[1]
        if M[f][c] == 0:
            M[f][c] = 1
            direccion[i] = (direccion[i] + 1) % 4
            h[movi[direccion[i]][0]] = (h[movi[direccion[i]][0]] + movi[direccion[i]][1])%100
        elif M[f][c] == 1:
            M[f][c] = 0
            direccion[i] = (direccion[i] - 1)% 4
            h[movi[direccion[i]][0]]= (h[movi[direccion[i]][0]] + movi[direccion[i]][1])%100
        i += 1
    return direccion
            
            
def Reiniciar(filas, cols):
    """
Reinicia la función
"""
    M=[]
    hormigas=[[filas//2,cols//2],[90,80],[10,10],[24,78]]
    direccion=[0,3,1,2]
    for f in range(filas):
        fila = []
        for c in range(cols):
            fila.append(0)
        M.append(fila)
    return (M,hormigas,direccion)

def Guardar(M,hormigas,direccion):
    with open('MatrisH.txt','w') as m, open('Hormigas.txt','w') as h,\
         open('Direcciones.txt','w') as d:
        json.dump(M,m)
        json.dump(hormigas,h)
        json.dump(direccion,d)

def Cargar():
    with open('MatrisH.txt','r') as m, open('Hormigas.txt','r') as h,\
         open('Direcciones.txt','r') as d:
        M= json.load(m)
        hormigas= json.load(h)
        direccion= json.load(d)
        return (M,hormigas,direccion)
def Hormiga_langton():
    """
Fun principal de la hormiga de langton
entradas: ninguna
salida: mostrar en acción la hormga de langton
"""
    pygame.init()
    filas=100
    cols=100
    tam=7
    window=pygame.display.set_mode((cols*tam, filas*tam))
    M=[[0 for c in range(cols)] for f in range(filas)]
    hormigas=[[filas//2,cols//2],[90,80],[10,10],[24,78]]
    direccion=[0,3,1,2]
    movi=0
    loop=True
    pausa=False
    while loop:
        pygame.time.delay(16)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                loop=False
            if event.type==pygame.KEYDOWN:
                keys=pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:
                    pausa= not pausa
                if keys[pygame.K_r]:
                    M=generarMatriz(filas, cols)
                if keys[pygame.K_DELETE]:
                    M,hormigas,direccion=Reiniciar(filas, cols)
                if keys[pygame.K_g]:
                    Guardar(M,hormigas,direccion)
                if keys[pygame.K_c]:
                    M,hormigas,direccion= Cargar()
            if event.type==pygame.MOUSEBUTTONDOWN:
                x,y=pygame.mouse.get_pos()
                fila=y//tam
                col=x//tam
                M[fila][col]=(M[fila][col]+1)%2


        dibujarMatriz(M,hormigas,tam,window)
        if not pausa:
            direccion= mover_hormiga(hormigas,M,direccion)
        pygame.display.update()

    pygame.quit()
Hormiga_langton()
