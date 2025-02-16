import pygame
import random

# Inicializar Pygame
pygame.init()

# Configuración de pantalla
ANCHO = 800
LARGO = 600
PANTALLA = pygame.display.set_mode((ANCHO, LARGO))

# Configuración inicial del juego
pygame.display.set_caption('STAR CAPTURE ONE')
icono = pygame.image.load('Imagenes/Icon/icono.png')
pygame.display.set_icon(icono)
fondo = pygame.image.load('Imagenes/Fondos/fondo3.png')

# Música y sonidos
pygame.mixer.music.load('Musica/Fondo/musica de fondo.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
RED = (255, 0, 0)
amarillo = (255, 255, 93)
MORADO_FONDO = (15, 0, 55)
VERDE = (0, 255, 0)

# Constantes
NUM_METEORITOS = 9
NUM_ESTRELLAS = 5

# Clases del juego -----------------------------------------------------------------
class Meteoritos(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.img_aleatoria = random.randrange(3)
        sizes = [(25, 70), (65, 110), (50, 95)]
        self.image = pygame.transform.scale(pygame.image.load('Imagenes/Meteorites/Meteorito.png'), sizes[self.img_aleatoria])
        self.image.set_colorkey(NEGRO)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(ANCHO - self.rect.width)
        self.rect.y = -self.rect.height
        self.velocidad_y = random.randrange(3, 7)

    def update(self):
        self.rect.y += self.velocidad_y
        if self.rect.top > LARGO:
            self.reset()

    def reset(self):
        self.rect.x = random.randrange(ANCHO - self.rect.width)
        self.rect.y = -self.rect.height
        self.velocidad_y = random.randrange(3, 7)

class Estrellas(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('Imagenes/Stars/star.png'), (30, 30))
        self.image.set_colorkey(NEGRO)
        self.rect = self.image.get_rect()
        self.reset()

    def reset(self):
        self.rect.x = random.randrange(ANCHO - self.rect.width)
        self.rect.y = -self.rect.height
        self.velocidad_y = random.randrange(2, 7)

    def update(self):
        self.rect.y += self.velocidad_y
        if self.rect.top > LARGO:
            self.reset()


#Personaje
class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.normal = pygame.image.load('Imagenes/Personaje/quieto/Idle.png')
        self.mov_derecha = [pygame.image.load(f'Imagenes/Personaje/movderecha/Walk{i}.png') for i in range(1, 9)]
        self.mov_izquierda = [pygame.image.load(f'Imagenes/Personaje/movizquierda/Walk{i}-izq.png') for i in range(1, 9)]
        self.image = self.normal
        self.rect = self.image.get_rect(center=(ANCHO // 2, LARGO - 40))
        self.velocidad = 6
        self.vivo = True
        self.puntos = 0
        self.indice_animacion = 0
        self.mirando_derecha = True

    def update(self):
        if not self.vivo: return

        teclas = pygame.key.get_pressed()

        if teclas[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocidad
            self.animar(self.mov_izquierda)
        elif teclas[pygame.K_RIGHT] and self.rect.right < ANCHO:
            self.rect.x += self.velocidad
            self.animar(self.mov_derecha)
        else:
            self.image = self.normal
            self.indice_animacion = 0

    def animar(self, animacion):
        self.indice_animacion = (self.indice_animacion + 1) % 8
        self.image = animacion[self.indice_animacion]

    def reiniciar(self):
        self.vivo = True
        self.puntos = 0
        self.rect.center = (ANCHO // 2, LARGO - 10)

# Sistema de Menús -----------------------------------------------------------------
class Boton:
    def __init__(self, x, y, ancho, alto, texto, color_base, color_hover):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.texto = texto
        self.color_base = color_base
        self.color_hover = color_hover
        self.color_actual = color_base
        self.fuente = pygame.font.Font(None, 40)

    def dibujar(self, pantalla):
        texto_surf = self.fuente.render(self.texto, True, BLANCO)
        pygame.draw.rect(pantalla, self.color_actual, self.rect, border_radius=5)
        texto_rect = texto_surf.get_rect(center=self.rect.center)
        pantalla.blit(texto_surf, texto_rect)

    def verificar_hover(self, pos_mouse):
        self.color_actual = self.color_hover if self.rect.collidepoint(pos_mouse) else self.color_base

class MenuPrincipal:
    def __init__(self):
        self.fuente_titulo = pygame.font.Font(None, 74)
        self.botones = [
            Boton(ANCHO // 2 - 100, 250, 200, 50, "Jugar", MORADO_FONDO, VERDE),
            Boton(ANCHO // 2 - 100, 320, 200, 50, "Reglas", MORADO_FONDO, VERDE),
            Boton(ANCHO // 2 - 100, 390, 200, 50, "Salir", MORADO_FONDO, VERDE)
        ]

    def dibujar(self, pantalla):
        pantalla.blit(fondo, (0, 0))
        titulo = self.fuente_titulo.render("STAR CAPTURE ONE", True, amarillo)
        pantalla.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, 100))

        for boton in self.botones:
            boton.dibujar(pantalla)

    def manejar_evento(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            for i, boton in enumerate(self.botones):
                if boton.rect.collidepoint(evento.pos):
                    return i 
        return -1

class FinalMenu:
    def __init__(self):
        self.botones = [
            Boton(ANCHO // 2 - 100, LARGO // 2 + 50, 200, 50, "Jugar de nuevo", MORADO_FONDO, VERDE),
            Boton(ANCHO // 2 - 100, LARGO // 2 + 120, 200, 50, "Menú Principal", MORADO_FONDO, VERDE)
        ]
        self.fuente = pygame.font.Font(None, 74)

    def dibujar(self, pantalla, puntos):
        # Fondo semitransparente
        overlay = pygame.Surface((ANCHO, LARGO), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        pantalla.blit(overlay, (0, 0))

        # Texto Game Over
        texto = self.fuente.render('GAME OVER', True, RED)
        pantalla.blit(texto, (ANCHO // 2 - texto.get_width() // 2, LARGO // 2 - 100))

        # Puntos
        puntos_texto = pygame.font.Font(None, 48).render(f'Puntos: {puntos}', True, BLANCO)
        pantalla.blit(puntos_texto, (ANCHO // 2 - puntos_texto.get_width() // 2, LARGO // 2 - 30))

        # Botones
        for boton in self.botones:
            boton.dibujar(pantalla)

    def manejar_evento(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            for i, boton in enumerate(self.botones):
                if boton.rect.collidepoint(evento.pos):
                    return i 
        return -1

# Función para mostrar las reglas
def mostrar_reglas():
    reglas_fuente = pygame.font.Font(None, 36)
    reglas_texto = [
        "Reglas del juego:",
        "1. Captura las estrellas para sumar puntos.",
        "2. Evita los meteoritos, si chocas pierdes.",
        "3. Usa las flechas izquierda y derecha para moverte.",
        "Presione cualquier tecla para volver al menú."
    ]

    while True:
        PANTALLA.blit(fondo, (0, 0))
        y = 100
        for linea in reglas_texto:
            texto_surf = reglas_fuente.render(linea, True, BLANCO)
            PANTALLA.blit(texto_surf, (ANCHO // 2 - texto_surf.get_width() // 2, y))
            y += 40

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            if evento.type == pygame.KEYDOWN or evento.type == pygame.MOUSEBUTTONDOWN:
                return

# Función principal del juego -----------------------------------------------------
def jugar(jugador, meteoritos, estrellas):
    reloj = pygame.time.Clock()
    ejecutando = True

    while ejecutando:
        reloj.tick(60)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False

        if jugador.vivo:
            # Actualizar elementos
            jugador.update()
            meteoritos.update()
            estrellas.update()

            # Verificar colisiones
            if pygame.sprite.spritecollide(jugador, meteoritos, False):
                jugador.vivo = False

            # Recolectar estrellas
            estrellas_recogidas = pygame.sprite.spritecollide(jugador, estrellas, True)
            for _ in estrellas_recogidas:
                jugador.puntos += 1
                estrellas.add(Estrellas())

        # Dibujar
        PANTALLA.blit(fondo, (0, 0))
        meteoritos.draw(PANTALLA)
        estrellas.draw(PANTALLA)
        PANTALLA.blit(jugador.image, jugador.rect)

        # Mostrar puntos
        fuente_puntos = pygame.font.Font(None, 35)
        texto_puntos = fuente_puntos.render(f'Estrellas: {jugador.puntos}', True, amarillo)
        PANTALLA.blit(texto_puntos, (10, 10))

        pygame.display.flip()

        # Manejar Game Over
        if not jugador.vivo:
            final_menu = FinalMenu()
            while True:
                # Actualizar botones
                mouse_pos = pygame.mouse.get_pos()
                for boton in final_menu.botones:
                    boton.verificar_hover(mouse_pos)

                # Dibujar menú final
                final_menu.dibujar(PANTALLA, jugador.puntos)
                pygame.display.flip()

                # Manejar eventos
                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        return False
                    accion = final_menu.manejar_evento(evento)
                    if accion == 0:  # Jugar de nuevo
                        pygame.mixer.music.stop()
                        pygame.mixer.music.play(-1)
                        jugador.reiniciar()
                        meteoritos.empty()
                        estrellas.empty()
                        for _ in range(NUM_METEORITOS):
                            meteoritos.add(Meteoritos())
                        for _ in range(NUM_ESTRELLAS):
                            estrellas.add(Estrellas())
                        return True
                    elif accion == 1: 
                        return True

                reloj.tick(60)

    return True

# Bucle principal del programa ----------------------------------------------------
menu_principal = MenuPrincipal()
en_ejecucion = True
estado = "menu"

while en_ejecucion:
    # Manejar eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            en_ejecucion = False
        if estado == "menu":
            accion = menu_principal.manejar_evento(evento)
            if accion == 0:  # Jugar
                # Inicializar juego
                jugador = Jugador()
                meteoritos = pygame.sprite.Group([Meteoritos() for _ in range(NUM_METEORITOS)])
                estrellas = pygame.sprite.Group([Estrellas() for _ in range(NUM_ESTRELLAS)])
                estado = "jugando"
            elif accion == 1:  # Reglas
                mostrar_reglas()
            elif accion == 2:  # Salir
                en_ejecucion = False

    # Actualizar elementos del menú
    if estado == "menu":
        mouse_pos = pygame.mouse.get_pos()
        for boton in menu_principal.botones:
            boton.verificar_hover(mouse_pos)

        # Dibujar
        menu_principal.dibujar(PANTALLA)
        pygame.display.flip()

    elif estado == "jugando":
        resultado = jugar(jugador, meteoritos, estrellas)
        if not resultado: 
            en_ejecucion = False
        else:
            estado = "menu"  # Volver al menú principal

    pygame.time.Clock().tick(60)

pygame.quit()
