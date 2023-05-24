from random import randint
from copy import deepcopy
import json
import pygame


def generarMatriz(filas, cols):
    M = []
    for f in range(filas):
        fila = []
        for c in range(cols):
            i= randint(1,100)
            if i < 60:
                fila.append(0)
            else:
                fila.append(randint(1,2))
        M.append(fila)
    return M

def dibujarMatriz(M, tam, window):
    color=[(255,255,255),(255,0,0),(0,0,255)]
    fila=len(M)
    cols=len(M[0])
    window.fill((0,0,0))
    for f in range(fila):
        for c in range(cols):
            pygame.draw.rect(window,color[M[f][c]],(c*tam, f*tam, tam, tam))


def avance(M):
    for f in range(len(M)):
        for c in range(len(M[0])):
            if M[f][c] == 1 and M[f][(c+1)%100] == 0:
                M[f][(c+1)%100] = 1
                M[f][c] = 0
            elif M[f][c] == 2 and M[(f+1)%100][c] == 0:
                M[(f+1)%100][c] = 2
                M[f][c] = 0
    return M
def avance_R(M):
    M2= deepcopy(M)
    for f in range(len(M)):
            for c in range(len(M[0])):
                if M[f][c] == 1 and M[f][(c+1)%len(M[0])] == 0:
                    M2[f][(c+1)%len(M[0])] = 1
                    M2[f][c] = 0
    return M2
def avance_V(M):
    M2= deepcopy(M)
    for f in range(len(M)):
            for c in range(len(M[0])):
                if M[f][c] == 2 and M[(f+1)%len(M)][c] == 0:
                    M2[(f+1)%len(M)][c] = 2
                    M2[f][c] = 0
    return M2

def Reiniciar(filas, cols):
    """
Genera una matriz en ceros
Entradas: número de filas y columnas
salida: la matriz solo en ceros
"""
    M=[]
    for f in range(filas):
        fila = []
        for c in range(cols):
            fila.append(0)
        M.append(fila)
    return M

def Guardar(M):
    archivo= open('modeloTrafico.txt','w')
    json.dump(M,archivo)
    archivo.close

def Cargar():
    archivo= open('modeloTrafico.txt','r')
    M= json.load(archivo)
    archivo.close
    return M

def main():
    pygame.init()
    filas=100
    cols=150
    tam=5
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
                    M= generarMatriz(filas, cols)
                if keys[pygame.K_DELETE]:
                    M= Reiniciar(filas, cols)
                if keys[pygame.K_g]:
                    Guardar(M)
                if keys[pygame.K_c]:
                    M= Cargar()
            if event.type==pygame.MOUSEBUTTONDOWN:
                x,y=pygame.mouse.get_pos()
                fila=y//tam
                col=x//tam
                M[fila][col]=(M[fila][col]+1)%3


        dibujarMatriz(M,tam,window)
        if not pausa:
            M= avance_R(M)
            M= avance_V(M)
        pygame.display.update()

    pygame.quit()
main()
