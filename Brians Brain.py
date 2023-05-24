from random import randint
from copy import deepcopy
import pygame

def generarMatriz(filas, cols):
    M = []
    for f in range(filas):
        fila = []
        for c in range(cols):
            fila.append(randint(0, 2))
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
    
def imprimir(M):
    for fila in M:
        for c in fila:
            print(f"{c} ", end="")
        print()

def nuevoEstado(M, fila, col):
    if M[fila][col]==0:
        v=vecinos(M,fila,col)
        if v.count(2)==2:
            return 2
        else:
            return 0
    if M[fila][col]==2:
        return 1
    if M[fila][col]==1:
        return 0

def nuevaGeneracion(M):
    M2=deepcopy(M)
    filas=len(M)
    cols=len(M[0])
    for f in range(filas):
        for c in range(cols):
            M2[f][c]=nuevoEstado(M,f,c)
    del M
    return M2

def generarColorViva():
    return(255,255,0)
def generarColorMuriendo():
    return(128,255,0)

def dibujarMatriz(M, tam, window):
    fila=len(M)
    cols=len(M[0])
    window.fill((0,0,0))
    for f in range(fila):
        for c in range(cols):
            if M[f][c]==2:
                pygame.draw.rect(window, generarColorViva(),(c*tam, f*tam, tam, tam))
            if M[f][c]==1:
                pygame.draw.rect(window, generarColorMuriendo(),(c*tam, f*tam, tam, tam))
    
def main():
    pygame.init()
    filas=200
    cols=400
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
                    M=generarMatriz(filas, cols)
                if keys[pygame.K_DELETE]:
                    M=generarMatrizMuerta(filas, cols)
            if event.type==pygame.MOUSEBUTTONDOWN:
                x,y=pygame.mouse.get_pos()
                fila=y//tam
                col=x//tam
                M[fila][col]=(M[fila][col]+1)%3


        dibujarMatriz(M,tam,window)
        if not pausa:
            M=nuevaGeneracion(M)
        pygame.display.update()

    pygame.quit()
main()
