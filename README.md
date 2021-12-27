[cc-by-sa]: http://creativecommons.org/licenses/by-sa/4.0/

[cc-by-sa-image]: https://licensebuttons.net/l/by-sa/4.0/88x31.png
[cc-by-sa-shield]: https://img.shields.io/badge/Licencia-CC--BY--SA%204.0-brightgreen

[![CC BY-SA 4.0][cc-by-sa-shield]][cc-by-sa]

# PyG_RadarGame
Este proyecto está montado en Python, y utiliza al módulo _**"PyGame"**_ para dibujar los gráficos.

_**Versión actual:** v0.5.2a (Alpha) [¡Descargar presionando aquí!](https://github.com/CharlieFuu69/PyG_RadarGame/releases/tag/v0.5.1a)_

---
## Controles:
* **K_UP:** Aceleración de la aeronave.
* **K_LEFT / K_RIGHT:** Alabeo de la aeronave en perspectiva horizontal.

---
## Requisitos y arranque en terminal:

Para que el juego pueda operar de forma óptima, se necesita tener instalado:

* Python 3.x o superior.
* Módulo PyGame (a través de PIP con `pip install pygame`)

El juego debe ser iniciado desde el terminal del dispositivo. Debes navegar hasta la carpeta donde está guardado el script de Python y usar el siguiente comando:

* `python RadarGame.py`

---
## Hints:

* El HUD con los datos de vuelo y navegación (ACMS, Alineación por ILS e IAS) se posicionan
en el área superior izquierda de la pantalla.
* El motor de la aeronave estará inhabilitado para acelerar si el ACMS informa el valor
1 (estado crítico).
* Al llegar a la zona segura (últimos 10 km), el sistema ILS mostrará la alineación para
perfilar al avión respecto de la pista de aterrizaje. La pista de aterrizaje estará a la distancia
indicada en el HUD del radar.
* Cuando la distancia entre el avión y la pista RWY sea menor a 2.5 km, el vector ILS
señalará que la pista está próxima a la aeronave.
* El aterrizaje se ejecutará únicamente mediante el vector ILS. Al llegar a los 0.0 km,
El vector ILS deberá estar lo más centrado posible en el radar. Si está correctamente centrado
(entre 22 y -22), el aterrizaje es exitoso, de lo contrario, el aterrizaje será fallido por
estar muy lejos de la pista.

---
## Glosario:
 
La interfaz mostrará algunos términos comprendidos en el mundo de la aeronáutica.
 
---
|Término | Definición |
|---|---|
| _**ACMS**_ | (Aircraft Condition Monitoring System) Sistema de monitoreo de condición de la aeronave. En el juego, esto mostrará la "vida" restante del avión. |
| _**Fieseler Fi 103 (V-1)**_ | Cohete alemán de aire-aire que posee una ojiva de 850 kg y puede alcanzar una velocidad de 390 mph (unos 630 km/h). |
| _**IAS**_ | (Indicated Air Speed) Velocidad indicada del aire. |
| _**ILS**_ | (Instrument Landing System) El ILS es el sistema que perfila el aterrizaje únicamente con instrumentación. En el día a día, es usado cuando la visibilidad es reducida durante las labores de aproximación a la pista. En el juego, el ILS informará la alineación de la pista en el eje X, y la precisión del perfilado. |
| _**knots**_ | El IAS indica la velocidad del aire respecto de la aeronave en "knots" o "Nudos". |
| _**P-51/D Mustang**_ | El North American P-51 Mustang fue un caza de escolta monomotor estadounidense de largo alcance, utilizado por las Fuerzas Aéreas del Ejército de los Estados Unidos (USAAF) durante la Segunda Guerra Mundial y la Guerra de Corea. Impulsado por un motor Packard V-1650-7, una versión del Rolls-Royce Merlin 66, el P-51/D puede alcanzar una velocidad de crucero de 239 nudos (unos 443 km/h) y una velocidad máxima de 380 nudos (unos 703 km/h). |
| _**PHNL**_ | Código ICAO de la Base Aérea de Pearl Harbor. |
| _**R4M**_ | Cohete aleman de aire-aire que posee una ojiva de 0.4 kg y puede ser disparado sin problemas a un objetivo ubicado a 1000m. |
| _**RWY**_ | (Runway) Pista de aterrizaje. En el juego se indicará la distancia (en kilómetros) que hay entre la pista y la aeronave. Al llegar a la pista, la misión estará completa. |
| _**Werfer-Granate 21**_ | Cohete aleman de aire-aire que posee una ojiva de 40.8 kg y alcanza los 320 m/s. |

---

## Desarrolladores:
* Carlos Cruces (GitHub: CharlieFuu69).
* Diego Castillo G.
* Geovanni Hernandez.

---
## Créditos de Assets:

* La banda sonora y los audios SFX/VOX provienen del juego (actualmente fuera de operaciones) llamado _**"War Wings"**_.
* Los diseños de UI fueron creados por los desarrolladores de RadarGame en Photoshop.
