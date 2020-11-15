#!/usr/bin/env python3
import RPi.GPIO as GPIO
import os
import random
import sys
import time
from omxplayer.player import OMXPlayer
from pathlib import Path
from itertools import cycle
from pyfiglet import Figlet

LINE_LENGTH = 80
RANDOM_MODE = "Random-Mode"
TOP20_MODE = "Top#20-Mode"


class FONTS:
    SEASON = 'ogre'
    EPISODE = 'ogre'
    TITLE = 'banner'
    RANDOM = 'cosmike'
    TOP20 = 'alligator2'


class TERM_COLORS:
    SEASON = '\033[95m'
    EPISODE = '\033[94m'
    TITLE = '\033[33m'
    RANDOM = '\033[32m'
    TOP20 = '\033[35m'
    ENDC = '\033[0m\r'


[
    '06x19 - La boda de Lisa.mp4', '05x03 - Homero va a la universidad.mp4',
    '01x09 - Un momento de decisión.mp4', '04x13 - La elección de Selma.mp4',
    '01x07 - La llamada de los Simpson.mp4',
    '05x17 - Bart gana un elefante.mp4', '07x07 - Homero tamaño familiar.mp4',
    '03x22 - El rock de Otto.mp4', '05x20 - El niño que sabía demasiado.mp4',
    '05x21 - El amante de Lady Bouvier.mp4', '03x01 - Papá está loco.mp4',
    '03x10 - Llamarada Moe.mp4', '01x08 - El héroe sin cabeza.mp4',
    '06x04 - La tierra de Tomy y Daly.mp4',
    '03x05 - Homero al diccionario.mp4', '03x17 - Homero al bat.mp4',
    '04x11 - El gran corazón de Homero.mp4', '04x21 - Marge en Cadenas.mp4',
    '03x07 - Especial de día de brujas de los Simpson II.mp4',
    '02x11 - Aviso de Muerte.mp4',
    '05x10 - Springfield próspero o el problema del juego.mp4',
    '04x14 - Hermano mayor hermano menor.mp4', '06x14 - El cometa de Bart.mp4',
    '05x06 - Marge, la rebelde.mp4', '02x16 - El Perro de Bart Reprueba.mp4',
    '06x25 - Quién mató al Sr. Burns (primera parte).mp4',
    '07x11 - El bebé de mamá.mp4', '05x09 - La última tentación de Homero.mp4',
    '03x13 - Bart y la radio.mp4', '02x13 - No Robarás.mp4',
    '03x16 - Bart, el amante.mp4', '03x19 - Nuestro mejor amigo.mp4',
    '05x05 - Especial de noche de brujas IV.mp4',
    '05x16 - Homero ama a Flanders.mp4', '06x20 - Un galgo llamado Monty.mp4',
    '01x10 - La correría de Homero.mp4', '06x03 - Recuerdos de amor.mp4',
    '05x14 - Lisa contra la Baby Malibú.mp4',
    '03x18 - Vocaciones distintas.mp4',
    '07x01 - Quién mató al Sr. Burns (segunda parte).mp4',
    '07x16 - Lisa, la iconoclasta.mp4', '06x18 - Una estrella estrellada.mp4',
    '07x04 - Bart vende su alma.mp4', '04x19 - El intermedio.mp4',
    '06x13 - Y con Maggie son tres.mp4',
    '02x06 - La Sociedad de los Golfistas Muertos.mp4',
    '06x17 - Homero contra Patty y Selma.mp4',
    '05x15 - Homero en el espacio profundo.mp4',
    '03x09 - Tardes de trueno.mp4', '01x03 - La odisea de Homero.mp4',
    '03x23 - Milhouse se enamora.mp4', '05x02 - Cabo de miedosos.mp4',
    '01x04 - Una familia modelo.mp4', '02x02 - Simpson y Dalila.mp4',
    '04x15 - Yo amo a Lisa.mp4', '07x22 - Mi héroe, el abuelo.mp4',
    '07x08 - Mamá Simpson.mp4', '04x04 - La reina de la belleza.mp4',
    '05x08 - Exploradores a fuerza.mp4',
    '06x05 - El regreso de Bob Patiño.mp4',
    '04x17 - La última salida a Springfield.mp4',
    '06x06 - Especial de noche de brujas de Los Simpson 5.mp4',
    '02x10 - Bart es Atropellado.mp4', '03x21 - El viudo negro.mp4',
    '06x07 - La novia de Bart.mp4',
    '07x21 - 22 películas cortas sobre Springfield.mp4',
    '07x03 - Hogar, dulce hogarcirijillo.mp4',
    '07x02 - El hombre radioactivo.mp4', '03x02 - El patriotismo de Lisa.mp4',
    '03x24 - Él es mi hermano.mp4', '02x09 - Tomy, Daly y Marge.mp4',
    '02x17 - Nuestros Años Felices.mp4',
    '02x03 - Especial de Noche de Brujas de Los Simpson.mp4',
    '04x16 - La promesa.mp4', '01x02 - Bart es un genio.mp4',
    '02x07 - Bart Contra el Día de Gracias.mp4',
    '01x13 - Una noche encantadora.mp4', '02x01 - Bart Reprueba.mp4',
    '07x19 - El sueño de amor de Selma.mp4', '05x13 - Homero y Apu.mp4',
    '06x11 - Miedo a volar.mp4',
    '07x10 - El episodio espectacular 138 de Los Simpson.mp4',
    '04x07 - Marge consigue empleo.mp4', '07x12 - El equipo de Homero.mp4',
    '01x05 - El general Bart.mp4', '04x10 - La primera palabra de Maggie.mp4',
    '01x06 - La depresión de Lisa.mp4', '03x20 - Homero el campirano.mp4',
    '05x19 - La canción de Skinner.mp4', '04x18 - A esto hemos llegado.mp4',
    '06x02 - La rival de Lisa.mp4', '06x09 - Homero el malo.mp4',
    '06x10 - El abuelo y la ineficiencia romántica.mp4',
    '06x22 - Por la ciudad de Springfield.mp4', '04x03 - Homero hereje.mp4',
    '05x22 - Secretos de un buen matrimonio.mp4', '02x14 - El Último Tren.mp4',
    '05x04 - El oso de Burns.mp4', '06x23 - Contacto Springfield.mp4',
    '07x05 - Lisa la vegetariana.mp4', '03x12 - Me casé con Marge.mp4',
    '03x11 - Burns y los alemanes.mp4', '06x12 - Homero el grande.mp4',
    '03x08 - El pony de Lisa.mp4', '01x01 - Especial de Navidad.mp4',
    '02x05 - Homero el Animador.mp4', '07x23 - Y dónde está el inmigrante.mp4',
    '04x09 - Don Barredora.mp4', '06x08 - Lisa y los deportes.mp4',
    '05x11 - Homero detective.mp4', '04x22 - El Drama de Krusty.mp4',
    '07x17 - Homero Smithers.mp4', '06x16 - Bart contra Australia.mp4',
    '04x02 - Un tranvía llamado Marge.mp4', '04x01 - Kampo Krusty.mp4',
    '03x06 - De tal padre, tal payaso.mp4', '03x15 - Homero se queda solo.mp4',
    '06x15 - Homie, el payaso.mp4', '03x03 - El día que cayó Flanders.mp4',
    '07x18 - El día que murió la violencia.mp4', '06x21 - Lucha educativa.mp4',
    '04x08 - La chica nueva.mp4', '06x24 - El limón de Troya.mp4',
    '07x13 - El mal vecino.mp4', '05x01 - El cuarteto de Homero.mp4',
    '01x11 - Intercambio cultural.mp4', '02x08 - Bart, el Temerario.mkv',
    '07x20 - Bart recorre el mundo.mp4', '02x12 - Los Años que Vivimos.mp4',
    '05x07 - Filosofía bartiana.mp4', '05x18 - El heredero de Burns.mp4',
    '03x04 - El pequeño padrino.mp4', '02x04 - Dos Autos en Cada Coche.mp4',
    '04x20 - El día del garrote.mp4', '03x14 - Los pronósticos de Lisa.mp4',
    '05x12 - Bart se hace famoso.mp4', '04x06 - Tomy y Daly La película.mp4',
    '01x12 - Krusty va a la cárcel.mp4', '06x01 - El diabólico Bart.mp4',
    '02x15 - Dónde Estás Hermano Mío.mp4',
    '07x06 - Especial de noche de brujas de Los Simpson VI.mp4',
    '07x09 - La última carcajada de Bob Patiño.mp4',
    '04x05 - Especial de noche de brujas III.mp4',
    '07x15 - Bart, el soplón.mp4',
    '07x14 - Lucha de clases en Springfield.mp4',
    '04x12 - Marge contra el Monorriel.mp4'
]
directory = "/home/pi/media/"

modes = cycle([RANDOM_MODE, TOP20_MODE])
mode = RANDOM_MODE

player = None

top_episode_list = []
current_top_episode = 0
with open('top20.txt') as file:
    top_episode_list = file.readlines()

print("🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀")
print("🚀🚀🚀🚀🚀🚀 Simpsons Machine v0.1 🚀🚀🚀🚀🚀🚀🚀🚀")
print("🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀\n\n\n")

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(10, GPIO.BOTH)


def get_top():
    global current_top_episode

    next_in_list = top_episode_list[current_top_episode]
    current_top_episode += 1
    print("next_in_list", next_in_list)
    print(os.listdir(directory))
    next_top_episode = [
        i for i in os.listdir(directory) if i.startswith(next_in_list)
    ]
    print("next_top_episode", next_top_episode)
    return next_top_episode


def get_random():
    return random.choice(os.listdir(directory))


def play():
    print("PLAY NEXT...")
    global player

    if player:
        player.quit()

    filename = get_top() if mode == TOP20_MODE else get_random()
    episode = filename.replace('.mp4', '').replace('.mkv', '').split(' - ')

    print(TERM_COLORS.SEASON + (Figlet(font=FONTS.SEASON, width=LINE_LENGTH)
                                ).renderText('s ' + episode[0].split('x')[0]) +
          TERM_COLORS.ENDC + "\r")

    print(TERM_COLORS.EPISODE +
          (Figlet(font=FONTS.EPISODE, width=LINE_LENGTH)
           ).renderText('e ' + episode[0].split('x')[1]) + TERM_COLORS.ENDC)

    print(TERM_COLORS.TITLE +
          (Figlet(font=FONTS.TITLE, width=LINE_LENGTH)
           ).renderText(episode[1].replace('ü', 'u').replace('ú', 'u').replace(
               'é', 'e').replace('á', 'a').replace('í', 'i').replace(
                   'ó', 'o').replace('ñ', 'n')) + TERM_COLORS.ENDC)
    time.sleep(2)

    # player = OMXPlayer(Path(directory + filename))
    # player.set_aspect_mode('fill')
    print("\n▶ PLAYING")


def mode_change():
    global mode
    global current_top_episode

    mode = next(modes)
    font = FONTS.RANDOM if mode == RANDOM_MODE else FONTS.TOP20
    color = TERM_COLORS.RANDOM if mode == RANDOM_MODE else TERM_COLORS.TOP20

    if mode == TOP20_MODE:
        current_top_episode = 0

    print(color + (Figlet(font=font, width=170)).renderText(mode) +
          TERM_COLORS.ENDC)
    print("\n\n\n")
    time.sleep(2)
    play()


def check_action(hold_value):
    if hold_value < 20000:
        play()
        return

    mode_change()


hold = 0
zero_value_check = 0

mode_change()

while True:
    if GPIO.input(10) == 0:
        if hold > 0:
            zero_value_check += 1

        if zero_value_check > 5:
            check_action(hold)
            zero_value_check = 0
            hold = 0

    else:
        hold += 1