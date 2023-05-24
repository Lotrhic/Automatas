from random import randint
from copy import deepcopy
import pygame
import json


"""Falta hacer el diccionario con todos los numero y a cada numero se le asigna un color rgb 
como se muestra en el video: https://www.youtube.com/watch?v=Mt7RVipjkxc&list=PLVPrxFlaWQgBm
Cb4eKww4t9S-NKqgvTsj&index=2&t=3818s en el minuto 11"""

def Guardar(M):
    archivo= open('Ciclo.txt','w')
    json.dump(M,archivo)
    archivo.close()
def Cargar():
    archivo= open('Ciclo.txt','r')
    M= json.load(archivo)
    archivo.close()
    return M
def generarMatriz(filas, cols):
    M = []
    for f in range(filas):
        fila = []
        for c in range(cols):
###########################################################Cambio          
            fila.append(randint(0, 15))
###########################################################Cambio       
        M.append(fila)
    return M

def generarMatrizMuerta(filas, cols):
    M=[]
    for f in range(filas):
        fila = []
        for c in range(cols):
            fila.append(0)
        M.append(fila)
    return M
def vecinos(M, fila, col):
    v = []
    filas=len(M)
    cols=len(M[0])

    for f in range(fila - 1, fila + 2):
        for c in range(col - 1, col + 2):
            if f != fila or c != col:
                v.append(M[f%filas][c%cols])
    return v


def nuevaGeneracion(M):
    M2=deepcopy(M)
    filas=len(M)
    cols=len(M[0])
    for f in range(filas):
        for c in range(cols):
            vecino= vecinos(M,f,c)
            if (M[f][c] + 1)%16 in vecino:
                M2[f][c]= (M2[f][c] + 1)%16
    del M
    return M2



def dibujarMatriz(M, tam, window):
    colores=[(255,0,0),(255,100,0),(255,180,0),(255,255,0),(100,255,0),
             (0,255,0),(0,255,100),(0,255,180),(0,255,255),(0,100,255),
             (0,0,255),(100,0,255),(180,0,255),(255,0,255),(255,0,180),
             (255,0,100)]
    #Una lista tambien sirve
    fila=len(M)
    cols=len(M[0])
    window.fill((0,0,0))
    for f in range(fila):
        for c in range(cols):
            pygame.draw.rect(window, colores[M[f][c]],(c*tam, f*tam, tam, tam))
    
def Ciclico():
    pygame.init()
    filas=100
    cols=100
    tam=7
    window=pygame.display.set_mode((cols*tam, filas*tam))
    M=generarMatriz(filas, cols)
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
                    M=generarMatrizMuerta(filas, cols)
                if keys[pygame.K_g]:
                    Guardar(M)
                if keys[pygame.K_c]:
                    M= Cargar()
            if event.type==pygame.MOUSEBUTTONDOWN:
                x,y=pygame.mouse.get_pos()
                fila=y//tam
                col=x//tam
                M[fila][col]=(M[fila][col]+1)%2


        dibujarMatriz(M,tam,window)
        if not pausa:
            M=nuevaGeneracion(M)
        pygame.display.update()

    pygame.quit()
Ciclico()
