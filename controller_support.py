import hid
import pydirectinput as pdi
import pyautogui as pag
from multiprocessing import Process
import time
weight = 10
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

def get_cursor_direction():
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

def get_click():
    while True:
        datastream = gamepad.read(64)
        if datastream:
            click_r1 = datastream[6] == 2
            if click_r1:
                pag.mouseDown(button='right')
                pag.mouseUp(button='right')
                time.sleep(0.5)
        
            click_l1 = datastream[6] == 1
            if click_l1:
                pag.mouseDown(button='left')
                pag.mouseUp(button='left')
                time.sleep(0.5)

def get_buttons():
    while True:
        datastream = gamepad.read(64)
        if datastream:
            btn = datastream[5] # 136 ta apertado o triangulo
            trigger_l2 = datastream[8] > 20 # 0 a 255
            trigger_r2 = datastream[9] > 20 # 0 a 255
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
            if trigger_l2:
                #pdi.keyDown('space')
                pdi.press('space')
                #time.sleep(0.2)
            if trigger_r2:
                pdi.press('tab')
                #pdi.keyUp('tab')
                #time.sleep(0.2)

                

if __name__ == '__main__': 
    Process(target=get_cursor_direction).start() 
    Process(target=get_click).start()
    Process(target=get_buttons).start()

