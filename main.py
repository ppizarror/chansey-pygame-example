# importacion de librerias
import os
import random

import pygame
from pygame.locals import *


class Actor:

    def __init__(self, dx, x, y, vida, size):
        self.x = x
        self.y = y
        self.vida = vida
        self.dx = dx
        self.direccion = 0
        self.initx = x
        self.texture = pygame.image.load("res/actor.png")
        self.muerto = False

    def moverIzquierda(self):
        if self.direccion != -1:
            self.x = self.initx - self.dx
            self.direccion = -1

    def moverDerecha(self):
        if self.direccion != 1:
            self.x = self.initx + self.dx
            self.direccion = 1

    def moverCentro(self):
        if self.direccion != 0:
            self.x = self.initx
            self.direccion = 0

    def getImage(self):
        return self.texture

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getPos(self):
        return (self.x, self.y)

class Huevo:
    def __init__(self, x, y, vel, ac, sound, dx, mono):
        self.x = x + int(random.randint(-1, 1)) * dx
        self.y = y
        self.vel = vel
        self.ac = ac
        self.t = 0
        self.texture = pygame.image.load("res/huevo.png")
        self.sound = sound
        self.mono = mono

    def update(self, lista, i):
        self.vel += self.ac * self.t
        self.y = self.y + self.vel * self.t
        self.t += 0.1

        if self.y > 370:
            lista.pop(i)
            self.mono.vida -= 1
            if self.mono.vida < 0:
                self.mono.muerto = True

        if abs(self.x - self.mono.getX()) < 40 and abs(self.y - self.mono.getY()) < 50:
            try:
                self.mono.vida += 1
                self.sound.play()
                lista.pop(i)
            except: pass

    def getPos(self):
        return (self.x, self.y)

    def getImage(self):
        return self.texture

def main():

    # Se activan las librerias
    pygame.init()

    # Se define el objeto pantalla
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Chansey")
    background = pygame.image.load("res/background.gif")
    grass = pygame.image.load("res/grass.png")
    background = pygame.transform.scale(background, (640, 480))
    icon = pygame.image.load("res/icon.png")
    pygame.display.set_icon(icon)
    clock = pygame.time.Clock()
    bgs = pygame.mixer.Sound("res/sound.wav")
    bgs.play(-1)
    sonidocomer = pygame.mixer.Sound("res/catch.wav")
    scorefont = pygame.font.Font("res/font.ttf", 30)
    fontmuerto = pygame.font.Font("res/font.ttf", 100)

    # Se crean los objetos del juego
    lista_huevos = []
    mono = Actor(120, 278, 370, 3, (100, 100))

    dif = 5
    acel = 0.01

    while True:

        if 1 <= random.randint(1, 100) <= dif:
            h = Huevo(310, 0, 1, acel, sonidocomer, 120, mono)
            lista_huevos.append(h)

        clock.tick(30)
        screen.blit(background, (0, 0))
        screen.blit(grass, (0, 30))

        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_F12:
                    dif += 5
                elif event.key == K_F11:
                    acel += 0.1

        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            mono.moverIzquierda()
        elif keys[K_RIGHT]:
            mono.moverDerecha()
        else:
            mono.moverCentro()

        if not mono.muerto:

            if len(lista_huevos) > 0:
                j = 0
                while True:
                    lista_huevos[j].update(lista_huevos, j)
                    j += 1
                    if j >= len(lista_huevos):
                        break

                for i in lista_huevos:
                    screen.blit(i.getImage(), i.getPos())

            screen.blit(mono.getImage(), mono.getPos())
            f1 = scorefont.render("VIDAS " + str(mono.vida), 1, (0, 0, 0))
            screen.blit(f1, (5, 5))
        else:
            f2 = fontmuerto.render("GAME OVER", 1, (0, 0, 0))
            screen.blit(f2, (40, 170))
        pygame.display.flip()

    try: os.system("taskkill /PID " + str(os.getpid()) + " /F")
    except: pass

if __name__ == "__main__":
    main()
