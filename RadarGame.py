"""RadarGame v0.5.2a (Alpha)

Desarrolladores:
> Carlos Cruces (GitHub: CharlieFuu69).
> Diego Castillo G.
> Geovanni Hernandez.
-----------------------------------------------------------------------------------------------------------

GITHUB : El juego está disponible (incluyendo su código fuente) en GitHub.
>>> URL del repositorio :

-----------------------------------------------------------------------------------------------------------
### Controles ###

K_LEFT y K_RIGHT : Alabear hacia los costados.
K_UP : Acelerar.

-----------------------------------------------------------------------------------------------------------
### Hints ###

- El HUD con los datos de vuelo y navegación (ACMS, Alineación por ILS e IAS) se posicionan
en el área superior izquierda de la pantalla.

- El motor de la aeronave estará inhabilitado para acelerar si el ACMS informa el valor
1 (estado crítico).

- Al llegar a la zona segura (últimos 10 km), el sistema ILS mostrará la alineación para
perfilar al avión respecto de la pista de aterrizaje. La pista de aterrizaje estará a la distancia
indicada en el HUD del radar.

- Cuando la distancia entre el avión y la pista RWY sea menor a 2.5 km, el vector ILS
señalará que la pista está próxima a la aeronave.

- El aterrizaje se ejecutará únicamente mediante el vector ILS. Al llegar a los 0.0 km,
El vector ILS deberá estar lo más centrado posible en el radar. Si está correctamente centrado
(entre 22 y -22), el aterrizaje es exitoso, de lo contrario, el aterrizaje será fallido por
estar muy lejos de la pista.

-----------------------------------------------------------------------------------------------------------
### Glosario ###

La interfaz mostrará algunos términos comprendidos en el mundo de la aeronáutica.

- ACMS (Aircraft Condition Monitoring System):
Sistema de monitoreo de condición de la aeronave. En el juego mostrará la vida restante
del avión.

- Fieseler Fi 103 (V-1):
Cohete alemán de aire-aire que posee una ojiva de 850 kg y puede alcanzar una velocidad de 390 mph (unos 630 km/h).

- IAS (Indicated Air Speed):
Velocidad indicada del aire.

- ILS (Instrument Landing System):
El ILS es el sistema que perfila el aterrizaje únicamente con instrumentación. En el día a día, es usado cuando la visibilidad es reducida durante las labores de aproximación a la pista.
En el juego, el ILS informará la alineación de la pista en el eje X, y la precisión del perfilado.

- knots:
El IAS indica la velocidad del aire respecto de la aeronave en "knots" o "Nudos".

- P-51/D Mustang:
El North American P-51 Mustang fue un caza de escolta monomotor estadounidense de largo alcance, utilizado por las Fuerzas Aéreas del Ejército de los Estados Unidos (USAAF) durante la Segunda Guerra Mundial y la Guerra de Corea.
Impulsado por un motor Packard V-1650-7, una versión del Rolls-Royce Merlin 66, el P-51/D puede alcanzar una velocidad de crucero de 239 nudos (unos 443 km/h) y una velocidad máxima de 380 nudos (unos 703 km/h).

- PHNL:
Código ICAO de la base aérea de Pearl Harbor. Su código IATA es HNL.
[Nota de ejemplo: el código ICAO del aeropuerto Arturo Merino Benitez es "SCEL".]

- R4M:
Cohete aleman de aire-aire que posee una ojiva de 0.4 kg y puede ser disparado sin problemas a un objetivo ubicado a 1000m.

- RWY (Runway):
Pista de aterrizaje. En el juego se indicará la distancia (en kilómetros) que hay entre la pista y la aeronave. Al llegar a la pista, la misión estará completa.

- Werfer-Granate 21:
Cohete aleman de aire-aire que posee una ojiva de 40.8 kg y alcanza los 320 m/s.
"""

import pygame #Importamos la libreria PyGame
import random ## Valores al azar
import time ## Usado para detenciones con time.sleep()
import threading ## Multiprocesamiento

#############################################################
## Etapa de inicialización

print("> Inicializando PyGame...")
pygame.init() ## PyGame
pygame.mixer.pre_init(44100, 16, 2, 4096) ## Mezclador de audio

#############################################################
## Configuración

RES = (1280, 720)
FPS = 60

## Diccionario de colores
COLOR = {
"white" : (255, 255, 255),
"yellow" : (255, 255, 0),
"red" : (255, 0, 0),
"green" : (0, 255, 0),
"black" : (0, 0, 0)}

pantalla = pygame.display.set_mode(RES) ## Resolución
font = pygame.font.Font("assets/din_medium.ttf", 17)

## Configuración del HUD/UI del radar
radar_template = pygame.image.load("assets/ui/ui_radar.png")
radar_sweepbar = pygame.image.load("assets/ui/ui_radar_sweep_fs.png")
swpbar_rect = radar_sweepbar.get_rect(center = (640, 360))

## Títulos
game_titles = {
"downed" : pygame.image.load("assets/titles/tl_aircraft_downed.png"),
"landing_failed" : pygame.image.load("assets/titles/tl_landing_failed.png"),
"success" : pygame.image.load("assets/titles/tl_mission_success.png")}


#############################################################
## Audio

pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.load("assets/AudioAssets/bgm_0001.mp3")

## Diccionario de canales de audio
AudioChannel = {
"ch_sfx1" : pygame.mixer.Channel(2),
"ch_sfx2" : pygame.mixer.Channel(3),
"ch_sfx3" : pygame.mixer.Channel(4),
"ch_vox" : pygame.mixer.Channel(5)}

## Configuración de volumen por canal
AudioChannel["ch_sfx1"].set_volume(0.1)
AudioChannel["ch_sfx2"].set_volume(0.2)
AudioChannel["ch_sfx3"].set_volume(0.2)
AudioChannel["ch_vox"].set_volume(0.6)

## Diccionario de audio SFX y VOX
SFX_Paths = {
"engine_st" : pygame.mixer.Sound("assets/AudioAssets/sfx/sfx_engine_started.wav"),
"engine_dmg" : pygame.mixer.Sound("assets/AudioAssets/sfx/sfx_engine_damage.wav"),
"radar_snd" : pygame.mixer.Sound("assets/AudioAssets/sfx/sfx_radar_sweep.wav"),
"dmg1" : pygame.mixer.Sound("assets/AudioAssets/sfx/sfx_damage_01.wav"),
"dmg2" : pygame.mixer.Sound("assets/AudioAssets/sfx/sfx_damage_02.wav"),
"dmg3" : pygame.mixer.Sound("assets/AudioAssets/sfx/sfx_damage_03.wav"),
"downed" : pygame.mixer.Sound("assets/AudioAssets/sfx/sfx_damage_downed.wav")}

VOX_Paths = {
"dmg1" : pygame.mixer.Sound("assets/AudioAssets/vox/vox_damage_01.wav"),
"dmg2_1" : pygame.mixer.Sound("assets/AudioAssets/vox/vox_damage_02_1.wav"),
"dmg2_2" : pygame.mixer.Sound("assets/AudioAssets/vox/vox_damage_02_2.wav"),
"dmg3_1" : pygame.mixer.Sound("assets/AudioAssets/vox/vox_damage_03_1.wav"),
"dmg3_2" : pygame.mixer.Sound("assets/AudioAssets/vox/vox_damage_03_2.wav")}

vox_medium_list = [VOX_Paths["dmg2_1"], VOX_Paths["dmg2_2"]]
vox_critical_list = [VOX_Paths["dmg3_1"], VOX_Paths["dmg3_2"]]

## Variables de comportamiento en tiempo de ejecución
aircraft_hp = 4
aircraft_rwy_approach = 30.0
aircraft_windspeed = 239
missile_active = False
run = True
angle = 0

#############################################################
## Clases

class Aircraft(pygame.sprite.Sprite):
    """La aeronave. Simplemente es una imagen de 10x10 píxeles posicionado en
    el centro del radar."""

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('assets/ui/ui_radar_aircraft.png')
        self.rect = self.image.get_rect()

        self.rect.x = 635
        self.rect.y = 355

        self.alive = True

class MissileObject(pygame.sprite.Sprite):
    """Los misiles/cohetes en el radar."""

    def __init__(self, missile_id, yset):
        super().__init__()
        self.image = pygame.image.load('assets/ui/ui_missile.png')
        self.missile_id = font.render(missile_id, True, COLOR["green"])
        self.rect = self.image.get_rect()
        self.rect_id = self.missile_id.get_rect()

        ## Posición inicial de los misiles
        self.rect.x = yset
        self.rect.y = 0

        ## Posición de la ID de los misiles detectados.
        self.rect_id.x = self.rect.x + 40
        self.rect_id.y = self.rect.y

        ## Velocidad lineal de los misiles (es el equivalente a la velocidad del avión sin maniobrar)
        self.missile_speed = 5

        ## Velocidad del avión (Maniobras)
        self.aircraft_roll_speed = 1 # (Velocidad de alabeo)
        self.aircraft_thrust_speed = 2 # (Velocidad de empuje)

    def update(self):
        pantalla.blit(self.missile_id, self.rect_id)
        boton = pygame.key.get_pressed()

        ## Desplazamiento lineal de los misiles (Sin maniobras del avión).
        self.rect.y += self.missile_speed
        self.rect_id.y += self.missile_speed

        ## Maniobras del avión (afecta la velocidad lineal base de los misiles)
        ## El mapa de controles no permitirá al avión retroceder. Siempre irá
        ## con velocidad de empuje positivo.
        if aircraft_class.alive:
            if boton[pygame.K_RIGHT]:
                self.rect.x -= (self.missile_speed + self.aircraft_roll_speed)
                self.rect_id.x -= (self.missile_speed + self.aircraft_roll_speed)

            if boton[pygame.K_LEFT]:
                self.rect.x += (self.missile_speed + self.aircraft_roll_speed)
                self.rect_id.x += (self.missile_speed + self.aircraft_roll_speed)

            if aircraft_hp > 1:
                if boton[pygame.K_UP]:
                    self.rect.y += (self.missile_speed + self.aircraft_thrust_speed)
                    self.rect_id.y += (self.missile_speed + self.aircraft_thrust_speed)

class RadarILS(pygame.sprite.Sprite):
    """El asistente ILS para perfilar el aterrizaje."""

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('assets/ui/ui_ils_signal.png')
        self.ils_text = font.render("PHNL RWY [ILS to align]", True, COLOR["yellow"])
        self.ils_distance = font.render("Runway is near!", True, COLOR["yellow"])

        ## Rectángulos
        self.rect = self.image.get_rect() ## Vector ILS.
        self.ils_rect = self.ils_text.get_rect() ## Texto ILS.
        self.ils_dist_rect = self.ils_distance.get_rect() ## Distancia por ILS.

        ## Posición inicial del los vectores ILS
        self.rect.x = random.randint(200, 1080) ## ¿Donde aparecerá la pista en el eje X?
        self.rect.y = 350

        ## Texto del vector ILS
        self.ils_rect.x = self.rect.x - 75
        self.ils_rect.y = self.rect.y + 60

        self.ils_dist_rect.x = self.rect.x - 75
        self.ils_dist_rect.y = self.rect.y + 80

        ## Precisión del aterrizaje
        self.landing_accuracy = 0

        ## Velocidad del avión (Maniobras)
        self.aircraft_roll_speed = 6 # (Velocidad de alabeo)
        self.aircraft_thrust_speed = 2 # (Velocidad de empuje)
        self.aircraft_linear_t_speed = 2 # (Velocidad de empuje sin acelerar)

    def update(self):
        boton = pygame.key.get_pressed()
        pantalla.blit(self.image, self.rect)
        pantalla.blit(self.ils_text, self.ils_rect)

        ## Si la distancia de la aeronave con la pista es igual o menor a 2.5 km, se mostrará la alerta
        ## de que la pista está cerca.
        if aircraft_rwy_approach <= 2.5:
            pantalla.blit(self.ils_distance, self.ils_dist_rect)

        self.landing_accuracy = self.rect.x - 638

        ## Si la distancia del avión es menor a 1.5 km, se muestra el vector RWY
        if aircraft_rwy_approach > 0.0:
            if boton[pygame.K_RIGHT]:
                self.rect.x -= self.aircraft_roll_speed
                self.ils_rect.x -= self.aircraft_roll_speed
                self.ils_dist_rect.x -= self.aircraft_roll_speed

            if boton[pygame.K_LEFT]:
                self.rect.x += self.aircraft_roll_speed
                self.ils_rect.x += self.aircraft_roll_speed
                self.ils_dist_rect.x += self.aircraft_roll_speed

#############################################################
## Funciones de comportamiento

def missile_drop():
    """Asiste al dropeo de misiles (Debe ejecutarse con Multithreading).
    La posición del dropeo respecto del eje X será al azar, y el rango de dropeo estará fijado en
    los píxeles 10 a 1240 en la pantalla."""

    print("Misiles activos")
    missile_id = ["Werfer-Granate 21", "R4M", "Fi 103 (V-1)"]
    while missile_active:
        misil = MissileObject(random.choice(missile_id), random.randint(10, 1240))
        missile_group.add(misil)
        time.sleep(0.1) ## Dropeará 1 misil en la pantalla cada 100 ms.
    print("Misiles inactivos")

def rotate_surface(displayable, angle):
    """Asiste la rotación contínua de un displayable."""

    rot_displayable = pygame.transform.rotate(displayable, -angle)
    rot_rect = rot_displayable.get_rect(center = (640, 360))

    return rot_displayable, rot_rect

def play_sfx(hp):
    """Está atento a los daños percibidos por la aeronave. Reproduce los SFXs y VOX
    respectivos al daño recibido."""

    for i in range(hp + 1):
        if i == hp and hp == 3:
            AudioChannel["ch_sfx2"].play(SFX_Paths["dmg1"])
            AudioChannel["ch_vox"].play(VOX_Paths["dmg1"])
        elif i == hp and hp == 2:
            AudioChannel["ch_sfx2"].play(SFX_Paths["dmg2"])
            AudioChannel["ch_vox"].play(random.choice(vox_medium_list))
        elif i == hp and hp == 1:
            AudioChannel["ch_sfx1"].stop()
            AudioChannel["ch_sfx1"].play(SFX_Paths["engine_dmg"], -1)
            AudioChannel["ch_sfx2"].play(SFX_Paths["dmg3"])
            AudioChannel["ch_vox"].play(random.choice(vox_critical_list))
        elif i == hp and hp == 0:
            AudioChannel["ch_sfx1"].stop()
            AudioChannel["ch_sfx3"].stop()
            pygame.mixer.find_channel(True).play(SFX_Paths["downed"])

def aircraft_flight_data():
    """Entrega todos los datos de vuelo."""

    status = font.render("> ACMS STATUS: %s" % str(aircraft_hp), True, COLOR["green"])
    rwy_distance = font.render("> RWY APPROACH: %s km" % str(round(aircraft_rwy_approach, 2)), True, COLOR["green"])
    aircraft_speed = font.render("> IAS: %s knots." % str(aircraft_windspeed), True, COLOR["green"])
    pantalla.blit(status, (3, 25))
    pantalla.blit(rwy_distance, (3, 45))
    pantalla.blit(aircraft_speed, (3, 65))

    if aircraft_hp <= 1:
        acms_warning = font.render("[ACMS: CRITICAL DAMAGE]", True, COLOR["red"])
        pantalla.blit(acms_warning, (3, 85))

    ## Activación del ILS por debajo de 9 kilómetros
    if aircraft_rwy_approach < 9.0:
        aircraft_ils.update()

        ils_value = font.render("> LANDING ACCURACY: %s" % int(aircraft_ils.landing_accuracy), True, COLOR["yellow"])
        pantalla.blit(ils_value, (3, 115))

        if aircraft_ils.landing_accuracy in range(-22, 22):
            ils_warning = font.render("[ILS: ALIGNED]", True, COLOR["green"])
            pantalla.blit(ils_warning, (3, 135))
        else:
            ils_warning = font.render("[ILS: OUT OF RANGE]", True, COLOR["red"])
            pantalla.blit(ils_warning, (3, 135))

def radar_sweep():
    """El sonido del barrido del radar. (Puede ser optimizable)."""
    while True:
        AudioChannel["ch_sfx3"].play(SFX_Paths["radar_snd"])
        time.sleep(4.0)

def speed_controller():
    """Muestra los datos de vuelo IAS y de aproximación en el HUD del radar."""
    global aircraft_rwy_approach
    global aircraft_windspeed

    if aircraft_rwy_approach > 0.0:

        ## El avión acelerará si su ACMS es óptimo.
        if aircraft_hp > 1:
            if pygame.key.get_pressed()[pygame.K_UP]:
                aircraft_rwy_approach -= 0.03
                aircraft_windspeed = 380
            else:
                aircraft_rwy_approach -= 0.01
                aircraft_windspeed = 239
        else:
            if aircraft_hp <= 0:
                aircraft_rwy_approach = 0
                aircraft_windspeed = 0
            else:
                aircraft_rwy_approach -= 0.01
                aircraft_windspeed = 239

    else:
        aircraft_windspeed = 0
        aircraft_rwy_approach = 0.0

def titlehandler():
    if aircraft_hp <= 0:
        pantalla.blit(game_titles["downed"], (0, 0))
    else:
        if aircraft_rwy_approach <= 0.0:
            if aircraft_ils.landing_accuracy in range(-22, 22):
                pantalla.blit(game_titles["success"], (0, 0))
            else:
                pantalla.blit(game_titles["landing_failed"], (0, 0))


#############################################################
## Preparación y ejecución.

aircraft_class = Aircraft() ## La aeronave
aircraft_ils = RadarILS() ## La señal ILS

## Grupos de objetos
aircraft_group = pygame.sprite.Group()
missile_group = pygame.sprite.Group()

aircraft_group.add(aircraft_class)

## Ticks del juego
clock = pygame.time.Clock()

#Ciclo principal
print("> Ejecutando...")

## Reproducción de la música de ambiente.
pygame.mixer.music.play(-1, 0.0)
AudioChannel["ch_sfx1"].play(SFX_Paths["engine_st"], loops = -1)

threading.Thread(target = radar_sweep).start()

#############################################################
## Actividades

while run:

    ## FPS de muestreo del juego
    clock.tick(FPS)

    #RECORREMOS LA LISTA DE EVENTOS EN BUSCA DE EL EVENTO CERRAR VENTANA
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            run = False

    #DIBUJANDO LA PANTALLA
    pantalla.fill(COLOR["black"]) ## Coloración negra

    ## ¿Está activo el drop de misiles?
    if not missile_active and aircraft_rwy_approach > 10.0:
        missile_active = True
        threading.Thread(target = missile_drop).start() ## Multithreading
    else:
        if aircraft_rwy_approach < 10.0:
            missile_active = False

    ## IAS
    speed_controller()

    ## Colisión entre el avión y los cohetes no dirigidos.
    hit = pygame.sprite.groupcollide(aircraft_group, missile_group, False, True)

    for i in hit:
        if i:
            aircraft_hp -= 1
            play_sfx(hp = aircraft_hp)
            if aircraft_hp <= 0:
                aircraft_class.alive = False

    ## Actualización del radar y de la posición de los misiles
    aircraft_group.update()
    missile_group.update()

    ## Dibujamos todos los objetos de los grupos en pantalla
    aircraft_group.draw(pantalla)
    missile_group.draw(pantalla)

    ## Datos de vuelo
    aircraft_radar = font.render("P-51/D Mustang", True, COLOR["green"])
    pantalla.blit(aircraft_radar, (730, 410))

    aircraft_flight_data() ## Muestra los datos de vuelo detallados

    ## Comportamiento del HUD del radar
    angle += 4.7
    rotated, rtd_rect = rotate_surface(radar_sweepbar, angle) ## Efecto Sweep
    pantalla.blit(rotated, rtd_rect)
    pantalla.blit(radar_template, (0, 0))

    ## Lanza un marco si se ha cumplido la misión o ha ocurrido otro evento.
    titlehandler()

    pygame.display.update() #Refresca la pantalla

#SE LIBERAN TODOS LOS RECURSOS CARGADOS
print("> Deteniendo...")
pygame.mixer.quit()
pygame.quit()
