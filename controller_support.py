import hid
import pydirectinput as pdi
import pyautogui as pag
from multiprocessing import Process
import time

weight = 7
tolerance = 2
screen_offset = 200
pag.PAUSE = 0

gamepad = hid.device()
gamepad.open(0x054c, 0x05c4)
gamepad.set_nonblocking(True)

def check_valid_cursor_direction(axis_x, axis_y):
    screen_width = pag.position()[0]
    screen_height = pag.position()[1]
    #print(screen_width + axis_x, screen_height + axis_y)
    return pag.onScreen(screen_width + axis_x, screen_height + axis_y)

def minmax(val):
    minimo = 0
    maximo = 255
    return 2 * ((val - minimo) / (maximo - minimo)) - 1

def get_mouse_cursor_position():
    while True:
        datastream = gamepad.read(64)
        if datastream:
            # o valor varia de 0 a 255 no eixo x e y onde 127 é o botão parado
            #[1] eixo x
            axis_x = 0
            axis_y = 0
            if datastream[1] > 127 + tolerance:
                axis_x = minmax(datastream[1])
            elif datastream[1] < 127 - tolerance:
                axis_x = minmax(datastream[1])
            
            axis_x = int(axis_x * weight)
                
            #[2] eixo y
            if datastream[2] > 127 + tolerance:
                axis_y = minmax(datastream[2])
                
            elif datastream[2] < 127 - tolerance:
                axis_y = minmax(datastream[2])

            axis_y = int(axis_y * weight)
            
            
            if not check_valid_cursor_direction(axis_x, axis_y):
                axis_x = 0
                axis_y = 0
            pag.move(axis_x, axis_y)

def get_clicks():
    while True:
        datastream = gamepad.read(64)
        if datastream:
            click_r1 = datastream[6] == 2
            if click_r1:
                pag.mouseDown(button='right')
                pag.mouseUp(button='right')
                time.sleep(0.4)
        
            click_l1 = datastream[6] == 1
            if click_l1:
                pag.mouseDown(button='left')
                pag.mouseUp(button='left')
                time.sleep(0.4)

def get_skill_buttons():
    while True:
        datastream = gamepad.read(64)
        if datastream:
            btn = datastream[5] # 136 ta apertado o triangulo
            #print('btn:', datastream[6])
            #datastream[6] F = 64, D = 128
            # 136 ta apertado
            # 24 é quadrado
            # x é 40
            # bolinha é 72
            
            match btn:
                case 40:
                    pdi.keyDown('w')
                    pdi.keyUp('w')
                    #print('w')
                    #time.sleep(0.15)

                case 24:
                    pdi.keyDown('q')
                    pdi.keyUp('q')
                    #print('q')
                    #time.sleep(0.15)

                case 136:
                    pdi.keyDown('r')
                    pdi.keyUp('r')
                    #print('r')
                    #time.sleep(0.15)
  
                case 72:
                    pdi.keyDown('e')
                    pdi.keyUp('e')
                    #print('e')
                    #time.sleep(0.15)


def get_spell_buttons():
    while True:
        datastream = gamepad.read(64)
        if datastream:
            key = datastream[6]
            match key:
                case 64:
                    pdi.keyDown('d')
                    pdi.keyUp('d')
                    time.sleep(0.15)

                case 128:
                    pdi.keyDown('f')
                    pdi.keyUp('f')
                    time.sleep(0.15)

def get_utilities():
    while True:
        datastream = gamepad.read(64)
        if datastream:
            #print(datastream[5]) # 0 é seta pra cima
            key = datastream[5]
            match key:
                case 0: # seta pra cima
                    pdi.keyDown('4')
                    pdi.keyUp('4')
                    time.sleep(0.3)

                case 4: # seta pra baixo
                    pdi.keyDown('1')
                    pdi.keyUp('1')
                    time.sleep(0.3)
                case 6: # seta esquerda
                    pdi.keyDown('b')
                    pdi.keyUp('b')
                    time.sleep(0.3)
                case 2: # seta direita
                    pdi.keyDown('p')
                    pdi.keyUp('p')
                    time.sleep(0.3)
                case _ if key < 20: 
                    while(datastream and datastream[8] > 20):# centralizar no personagem (espaço)
                        pdi.keyDown("space")
                        datastream = gamepad.read(64)
                    pdi.keyUp("space")
                    while(datastream and datastream[9] > 20):# tab
                        pdi.keyDown("tab")
                        datastream = gamepad.read(64)
                    pdi.keyUp("tab")

if __name__ == '__main__': 
    Process(target=get_mouse_cursor_position).start() 
    Process(target=get_clicks).start()
    Process(target=get_skill_buttons).start()
    Process(target=get_spell_buttons).start()
    Process(target=get_utilities).start()

