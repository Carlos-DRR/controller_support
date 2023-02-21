import hid
import pydirectinput as pdi
import pyautogui as pag
from multiprocessing import Process
import json

weight = 7
tolerance = 2
screen_offset = 70
pag.PAUSE = 0
pag.FAILSAFE = False

gamepad = hid.device()
gamepad.open(0x054c, 0x05c4)
gamepad.set_nonblocking(True)

f = open("C:/Users/carlo/Desktop/controller_support/config.json")
data_json = json.load(f)

f.close()

# verifica se a posição desejada pelo input é possível em cada eixo (x, y)
# portanto são quatro possibilidades: (true, true), (true, false),(false, true), (false, false)
# Os inputs são executados apenas quando e posição é válida (dentro da tela) ex: (true, false) = em x é aceito o input e y é zero
def check_valid_cursor_direction(axis_x, axis_y):
    screen_width = pag.position()[0]
    screen_height = pag.position()[1]
    axis_x_valid = pag.onScreen(screen_width + axis_x, 0)
    axis_y_valid = pag.onScreen(0, screen_height + axis_y)
    if not axis_x_valid and not axis_y_valid:
        return 0, 0
    if axis_x_valid and axis_y_valid:
        return axis_x, axis_y
    elif not axis_x_valid:
        return 0, axis_y
    else:
        return axis_x, 0

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
            if datastream[data_json["cursor_posistion"]["axis_x"]["id"]] > data_json["cursor_posistion"]["axis_x"]["values"]["no_movement"] + tolerance:
                axis_x = minmax(datastream[1])
            elif datastream[1] < 127 - tolerance:
                axis_x = minmax(datastream[1])
            
            axis_x = int(axis_x * weight)
                
            #[2] eixo y
            if datastream[data_json["cursor_posistion"]["axis_y"]["id"]] > data_json["cursor_posistion"]["axis_y"]["values"]["no_movement"] + tolerance:
                axis_y = minmax(datastream[2])
                
            elif datastream[data_json["cursor_posistion"]["axis_y"]["id"]] < data_json["cursor_posistion"]["axis_y"]["values"]["no_movement"] - tolerance:
                axis_y = minmax(datastream[2])

            axis_y = int(axis_y * weight)
            
            axis_x, axis_y = check_valid_cursor_direction(axis_x, axis_y)
            pag.move(axis_x, axis_y)

def add_times_pressed(times_pressed):
    if times_pressed > 1:
        return times_pressed
    elif times_pressed <= 1:
        return times_pressed + 1


def get_clicks():
    times_clicked_right = 0
    times_clicked_left = 0
    while True:
        datastream = gamepad.read(64)
        if datastream:

            click_r1 = datastream[data_json["cursor_btns"]["right_btn"]["id"]] == data_json["cursor_btns"]["right_btn"]["values"]["right_click"]
            if click_r1:
                #times_clicked_right += 1
                times_clicked_right = add_times_pressed(times_clicked_right)
                if(times_clicked_right == 1):
                    pag.mouseDown(button='right')
            else:    
                if times_clicked_right >= 1:
                    times_clicked_right = 0
                    pag.mouseUp(button='right')
            
            
            click_l1 = datastream[data_json["cursor_btns"]["left_btn"]["id"]] == data_json["cursor_btns"]["left_btn"]["values"]["left_click"]
            if click_l1:
                #times_clicked_left += 1
                times_clicked_left = add_times_pressed(times_clicked_left)
                if(times_clicked_left == 1):
                    pag.mouseDown(button='left')
                    
            else:
                if times_clicked_left >= 1:
                    times_clicked_left = 0
                    pag.mouseUp(button='left')

def get_skill_buttons():
    # datastream[data_json["skill_btns"]["btn_1"]["id"]]
    times_pressed_skill_1 = 0
    times_pressed_skill_2 = 0
    times_pressed_skill_3 = 0
    times_pressed_skill_4 = 0
    while True:
        datastream = gamepad.read(64)
        if datastream:
            btn = datastream[data_json["skill_btns"]["btn_1"]["id"]] # 136 ta apertado o triangulo
            #print('btn:', datastream[6])
            #datastream[6] F = 64, D = 128
            # 136 ta apertado
            # 24 é quadrado
            # x é 40
            # bolinha é 72
            if (btn == data_json["skill_btns"]["btn_1"]["values"]["skill_q"]):
                times_pressed_skill_1 += add_times_pressed(times_pressed_skill_1)
                if(times_pressed_skill_1 == 1):
                    pdi.keyDown(data_json["skill_btns"]["btn_1"]["keys"][0])
            else:
                if(times_pressed_skill_1 >= 1):
                    times_pressed_skill_1 = 0
                    pdi.keyUp(data_json["skill_btns"]["btn_1"]["keys"][0])

            if (btn == data_json["skill_btns"]["btn_1"]["values"]["skill_w"]):
                times_pressed_skill_2 += add_times_pressed(times_pressed_skill_2)
                if(times_pressed_skill_2 == 1):
                    pdi.keyDown(data_json["skill_btns"]["btn_1"]["keys"][1])
            else:
                if(times_pressed_skill_2 >= 1):
                    times_pressed_skill_2 = 0
                    pdi.keyUp(data_json["skill_btns"]["btn_1"]["keys"][1])
            if (btn == data_json["skill_btns"]["btn_1"]["values"]["skill_e"]):
                times_pressed_skill_3 += add_times_pressed(times_pressed_skill_3)
                if(times_pressed_skill_3 == 1):
                    pdi.keyDown(data_json["skill_btns"]["btn_1"]["keys"][2])
            else:
                if(times_pressed_skill_3 >= 1):
                    times_pressed_skill_3 = 0
                    pdi.keyUp(data_json["skill_btns"]["btn_1"]["keys"][2])
            if (btn == data_json["skill_btns"]["btn_1"]["values"]["skill_r"]):
                times_pressed_skill_4 += add_times_pressed(times_pressed_skill_4)
                if(times_pressed_skill_4 == 1):
                    pdi.keyDown(data_json["skill_btns"]["btn_1"]["keys"][3])
            else:
                if(times_pressed_skill_4 >= 1):
                    times_pressed_skill_4 = 0
                    pdi.keyUp(data_json["skill_btns"]["btn_1"]["keys"][3])


def get_spell_buttons():
    times_pressed_spell1 = 0
    times_pressed_spell2 = 0
    while True:
        datastream = gamepad.read(64)
        if datastream:
            #datastream[data_json["spell_btns"]["btn_1"]["id"]]
            key = datastream[data_json["spell_btns"]["btn_1"]["id"]]
            if key == data_json["spell_btns"]["btn_1"]["values"]["spell_1"]:
                times_pressed_spell1 += add_times_pressed(times_pressed_spell1)
                if(times_pressed_spell1 == 1):
                    pdi.keyDown(data_json["spell_btns"]["btn_1"]["keys"][0])
            else:
                if(times_pressed_spell1 >= 1):
                    times_pressed_spell1 = 0
                    pdi.keyUp(data_json["spell_btns"]["btn_1"]["keys"][0])

            if key == data_json["spell_btns"]["btn_1"]["values"]["spell_2"]:
                times_pressed_spell2 += add_times_pressed(times_pressed_spell2)
                if(times_pressed_spell2 == 1):
                    pdi.keyDown(data_json["spell_btns"]["btn_1"]["keys"][1])
            else:
                if(times_pressed_spell2 >= 1):
                    times_pressed_spell2 = 0                
                    pdi.keyUp(data_json["spell_btns"]["btn_1"]["keys"][1])
                    

def get_utilities():        
    times_pressed_utl_1 = 0
    times_pressed_utl_2 = 0
    times_pressed_utl_3 = 0
    times_pressed_utl_4 = 0
    times_pressed_utl_5 = 0
    times_pressed_utl_6 = 0
    while True:
        datastream = gamepad.read(64)
        if datastream:
            #datastream[data_json["utilities_btns"]["btn_1"]["id"]]
            key = datastream[data_json["utilities_btns"]["btn_1"]["id"]]
            if key == data_json["utilities_btns"]["btn_1"]["values"]["arrow_1"]:
                times_pressed_utl_1 = add_times_pressed(times_pressed_utl_1)
                if(times_pressed_utl_1 == 1):
                    pdi.press('4')
            else:
                if(times_pressed_utl_1 >= 1):
                    times_pressed_utl_1 = 0                  
                    pdi.keyUp('4')

            if key == data_json["utilities_btns"]["btn_1"]["values"]["arrow_2"]:
                times_pressed_utl_2 = add_times_pressed(times_pressed_utl_2)
                if(times_pressed_utl_2 == 1):
                    pdi.keyDown('1')
            else:
                if(times_pressed_utl_2 >= 1):
                    times_pressed_utl_2 = 0
                    pdi.keyUp('1')

            if key == data_json["utilities_btns"]["btn_1"]["values"]["arrow_3"]:
                times_pressed_utl_3 = add_times_pressed(times_pressed_utl_3)
                if(times_pressed_utl_3 == 1):
                    pdi.keyDown('b')
            else:
                if(times_pressed_utl_3 >= 1):
                    times_pressed_utl_3 = 0
                    pdi.keyUp('b')

            if key == data_json["utilities_btns"]["btn_1"]["values"]["arrow_4"]:
                times_pressed_utl_4 = add_times_pressed(times_pressed_utl_4)
                if(times_pressed_utl_4 == 1):
                    pdi.keyDown('p')
            else:
                if(times_pressed_utl_4 >= 1):
                    times_pressed_utl_4 = 0
                    pdi.keyUp('p')
                
            if datastream[data_json["utilities_btns"]["btn_2"]["id"]] > data_json["utilities_btns"]["btn_2"]["values"]["utl_1"]:# centralizar no personagem (espaço)
                times_pressed_utl_5 = add_times_pressed(times_pressed_utl_5)
                if(times_pressed_utl_5 == 1):
                    pdi.keyDown(data_json["utilities_btns"]["btn_2"]["keys"][0])
            else:
                if(times_pressed_utl_5 >= 1):
                    times_pressed_utl_5 = 0                    
                    pdi.keyUp(data_json["utilities_btns"]["btn_2"]["keys"][0])

            if datastream[data_json["utilities_btns"]["btn_3"]["id"]] > data_json["utilities_btns"]["btn_3"]["values"]["utl_1"]:# tab
                times_pressed_utl_6 = add_times_pressed(times_pressed_utl_6)
                if(times_pressed_utl_6 == 1):
                    pdi.keyDown(data_json["utilities_btns"]["btn_3"]["keys"][0])
            else:
                if(times_pressed_utl_6 >= 1):
                    times_pressed_utl_6 = 0                  
                    pdi.keyUp(data_json["utilities_btns"]["btn_3"]["keys"][0])

                    

if __name__ == '__main__': 
    Process(target=get_mouse_cursor_position).start() 
    Process(target=get_clicks).start()
    Process(target=get_skill_buttons).start()
    Process(target=get_spell_buttons).start()
    Process(target=get_utilities).start()

