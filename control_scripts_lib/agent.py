
class SurvivRequest:

    def __init__(self,
                 direction,
                 #x,y,
                 click, dt_click,
                 fKey, actKey,
                 switch_weap):
        
        """Special class for managing surviv.io game
        Args:
           direction ([int]): stop0; 🡹1; 🡽2; 🡺3; 🡾4; 🡻5; 🡿6; 🢀7; 🡼8;
           #x ([int]): x axis, new mouse coordinates   
           #y ([int]): y axis, new mouse coordinates
           click    ([int] 0 1): click or not
           dt_click ([int]) time of mouse holding in ms
           fKey ([int] 0 1): 'f'
           actKey ([int] 0 1 2 3 4 5): 'r'/'7'/'8'/'9'/'0'
           switch_weap ([intl] 0 1 2 3): '1'/'2'/'3'
           
        """
        self.direction = direction
        #self.x = x
        #self.y = y
        self.click = click
        self.dt_click = dt_click
        self.fKey = fKey
        self.actKey = actKey
        self.switch_weap = switch_weap
        
#==== Функции для вытаскивания информации из HTML кода игры =====    
def patronhtml_2_count(s):
    return int(s.split('"ui-loot-count">')[1].split('<')[0])

def weaponhtml1(s):
    b= s.find('"ui-weapon-name">')
    c= s.find('</div>')
    return s[b+17:c]

def hphtml(a):
    b = a.find('%')
    c = a.find('width: ')
    if len(a[c+7:b]) < 10:
        return round(float(a[c+7:b]))
    else:
        return 0
    
def patronhtml_left(s):
    if type(s) != None:
        return int(s)
    
#патроны снизу не в обойме
def patronhtml_right(s):
    if type(s) != None:
        return int(s)

def itemshtml(s):
    return int(s.split('"ui-loot-count">')[1].split('<')[0])

def bottom_invent(s):
    b= s.find(';">')
    if s[b+3:b+8]!='</div' and s[b+3:b+8]!='iv cl':
        return int(s[b+7])
    else: 
        return 0
#=============================================================================

class SurvivAgent:
    def __init__(self,game):
        self.survivGame = game
        #====🡻 Agent's State = His Current Inventory 🡻====
        self.zoom = 1
        self.hp = 100
        self.sp = 0
        self.helmet = 0
        self.vest = 0
        self.backpack = 0
        self.band = 0 # press 7 to use it
        self.medk = 0 # press 8 to use it
        self.cola = 0 # press 9 to use it
        self.pill = 0 # press 0 to use it
        self.ybull = 0
        self.rbull = 0
        self.bbull = 0
        self.gbull = 0
        self.w1 = '' # press 1 to activate it
        self.w2 = '' # press 2 to activate it
        self.w3 = '' # press 3 to activate it
        self.left_bullets = 0
        self.right_bullets = 0
        self.totalkills = 0
        self.mode = 1
        self.use_band = 0
        self.use_medk = 0
        self.use_cola = 0
        self.use_pill = 0
        self.reloading = 0
        #====🡹 Agent's State = His Current Inventory 🡹====
        
    def start_playing(self):
        return self.survivGame.start_playing()
    
    def restart_after_death(self):
        return self.survivGame.restart_after_death()
    
    def update_state(self):
        
#"/html/body/div[3]/div[3]/div[19]/div[1]/div[1]/div/div" # Xpath zoom
#stackoverflow.com/questions/10596417/is-there-a-way-to-get-element-by-xpath-using-javascript-in-selenium-webdriver        
        self.zoom = 1 # пока бот не лутает, не будем заморачиваться
        self.sp = 0 # пока бот не лутает, не будем заморачиваться
        #self.totalkills = ...
        #self.active_weapon = ...
        
        self.hp = hphtml(self.survivGame.browser.execute_script(\
                        "return document.getElementById('ui-health-container').innerHTML"))
        
        self.helmet = bottom_invent(self.survivGame.browser.execute_script(\
                        "return document.getElementById('ui-armor-helmet').innerHTML"))
        self.vest = bottom_invent(self.survivGame.browser.execute_script(\
                        "return document.getElementById('ui-armor-chest').innerHTML"))
        self.backpack = bottom_invent(self.survivGame.browser.execute_script(\
                        "return document.getElementById('ui-armor-backpack').innerHTML"))
        
        self.band = itemshtml(self.survivGame.browser.execute_script(\
                        "return document.getElementById('ui-loot-bandage').innerHTML"))
        self.medk = itemshtml(self.survivGame.browser.execute_script(\
                        "return document.getElementById('ui-loot-healthkit').innerHTML"))
        self.cola = itemshtml(self.survivGame.browser.execute_script(\
                        "return document.getElementById('ui-loot-soda').innerHTML"))
        self.pill = itemshtml(self.survivGame.browser.execute_script(\
                        "return document.getElementById('ui-loot-painkiller').innerHTML"))

        #self.ybull = patronhtml_2_count(self.survivGame.browser.execute_script(\
        #                "return document.getElementById('ui-loot-9mm').innerHTML"))
        #self.rbull = patronhtml_2_count(self.survivGame.browser.execute_script(\
        #                "return document.getElementById('ui-loot-12gauge').innerHTML"))
        #self.bbull = patronhtml_2_count(self.survivGame.browser.execute_script(\
        #                "return document.getElementById('ui-loot-762mm').innerHTML"))
        #self.gbull = patronhtml_2_count(self.survivGame.browser.execute_script(\
        #                "return document.getElementById('ui-loot-556mm').innerHTML"))
        
        #self.w1 = weaponhtml1(self.survivGame.browser.execute_script(\
        #                "return document.getElementById('ui-weapon-id-1').innerHTML"))
        #self.w2 = weaponhtml1(self.survivGame.browser.execute_script(\
        #                "return document.getElementById('ui-weapon-id-2').innerHTML"))
        #self.w3 = weaponhtml1(self.survivGame.browser.execute_script(\
        #                "return document.getElementById('ui-weapon-id-3').innerHTML"))
        
        self.left_bullets = 0 # пока бот не лутает, не будем заморачиваться
        #self.left_bullets = patronhtml_left(self.survivGame.browser.execute_script(\
        #                "return document.getElementById('ui-current-clip').innerHTML"))
        #self.right_bullets = patronhtml_right(self.survivGame.browser.execute_script(\
        #                "return document.getElementById('ui-remaining-ammo').innerHTML"))
        #self.use_smth = # пока бот не лутает, не будем заморачиваться
        
    def print_agentstate(self):
        print('hp:', self.hp)
        print('sp:', self.sp)
        print('weapon_mag:', self.left_bullets)
        print('бинты:', self.band)
        print('аптечка:', self.medk)
        print('сода:', self.cola)
        print('таблетки:', self.pill)
        print('шлем:', self.helmet)
        print('броня:', self.vest)
        print('рюкзак:', self.backpack)
        print('zoom:', self.zoom)
        print('use_band:', self.use_band)
        print('use_medk:', self.use_medk)
        print('use_cola:', self.use_cola)
        print('use_pill:', self.use_pill)
        print('reloading:', self.reloading)
        print('mode:', self.mode)
        print('============================== \n')
        
    def do_all_choosen_actions(self,
                              direction=0, # по умолчанию - не двигаемся
                              #x, y,
                              click=0, dt_click=7,
                              fKey=0, actKey=0,
                              switch_weap=0
                             ):
        cur_request = SurvivRequest(direction,
                                    #x, y,
                                    click, dt_click,
                                    fKey, actKey,
                                    switch_weap)
        self.survivGame.process_all_agents_actions(cur_request)