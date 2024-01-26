WIN_WIDTH = 640
WIN_HEIGHT = 480
TILE_SIZE = 32
FPS = 60

PLAYER_LAYER = 3
PLAYER_SPEED = 3

SPIKE_LAYER = 2

GROUND_LAYER = 1

# Esto es como un grid de CSS, con filas y columnas, cada celda es 32x32 asi que ancho(640) / 32 = 20 columnas
# y alto (480) / 32 = 15 que son 15 filas
tilemap = [
    'SSSSSSSSSSSSSSSSSSSS',
    'S..................S',
    'S....SSS...........S',
    'S..................S',
    'S........P.........S',
    'S..................S',
    'S..................S',
    'S....SS.....SSSS...S',
    'S..................S',
    'S..................S',
    'S..................S',
    'S..............SSSSS',
    'S.......S.SSS......S',
    'S..................S',
    'SSSSSSSSSSSSSSSSSSSS',
]
