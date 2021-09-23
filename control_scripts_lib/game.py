# selenium: !conda install -c conda-forge selenium -y
from selenium.webdriver import Chrome, ChromeOptions #, Firefox, FirefoxOptions
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

from enum import Enum
import json
import time


class Key(Enum):
	W = "w"
	A = "a"
	S = "s"
	D = "d"
	F = "f" # переделать так, чтобы F через keyDown
	R = "r"
	V = "v"
	N1 = "1"
	N2 = "2"
	N3 = "3"
	N7 = "7"
	N8 = "8"
	N9 = "9"
	N0 = "0"

	def __str__(self):
		return self.value

	@staticmethod
	def fromDirection(id_dir):
		"""Direction schema
		Args:
			direction ([int]): stop0; 🡹1; 🡽2; 🡺3; 🡾4; 🡻5; 🡿6; 🢀7; 🡼8;
		Returns:
			[Key]: array of key enum
		"""
		d_dir = {0: [],
				 1: [Key.W],
				 2: [Key.W, Key.D],
				 3: [Key.D],
				 4: [Key.D, Key.S],
				 5: [Key.S],
				 6: [Key.A, Key.S],
				 7: [Key.A],
				 8: [Key.A, Key.W]}
		
		return d_dir[id_dir]


class Direction(Enum):
	Up = "keyUp"
	Down = "rawKeyDown"

	def __str__(self):
		return self.value

class Game:
	def __init__(self, chrome_driver, chrome_adblock, custom_config=True, classic_mode=True):
		self.game_url ='https://surviv.io/'
		#https://chromedriver.chromium.org/downloads
		#self.chrome_driver = '/home/laggg/RL_surviv/control_architecture/control_scripts_lib/support_files_for_selenium/chromedriver'
		self.chrome_driver = chrome_driver
		#https://www.crx4chrome.com/crx/31931/
		#self.chrome_adblock = '/home/laggg/RL_surviv/control_architecture/control_scripts_lib/support_files_for_selenium/uBlockOrigin.crx' 
		self.chrome_adblock = chrome_adblock
		chrOptions = ChromeOptions()
		chrOptions.add_extension(self.chrome_adblock)
		chrOptions.add_argument("disable-infobars")
		chrOptions.add_argument("--mute-audio")
		self.browser = Chrome(executable_path=self.chrome_driver, chrome_options=chrOptions)
		self.browser.set_window_position(x=-10,y=0)
		self.browser.get(self.game_url)
		self.browser.implicitly_wait(3)
		self.browser.maximize_window()
		#для поиска id кнопок нужно ctrl+shift+I 
		try:
			self.browser.find_element_by_xpath("/html/body/div[9]/div[34]/div[1]/div[1]/span").click()
		except:
			print('Not found')
		#self.browser.find_element_by_id("modal-account-incentive-btn").click()
		try:
			self.browser.find_element_by_xpath("/html/body/div[9]/div[29]/div/div[1]/span").click()
		except:
			print('Not found')
		try:
			self.browser.find_element_by_xpath("/html/body/div[9]/div[40]/div/div[1]/span").click()
		except:
			print('Not found')
		try:
			self.browser.find_element_by_xpath("/html/body/div[9]/div[18]/div/div[1]/span").click()
		except:
			print('Not found')
		if classic_mode:     # выбрать классический режим игры (если дефолтно стоит другой)
			self.browser.find_element_by_id("index-play-mode-selected").click()
			self.browser.find_element_by_xpath(\
			"/html/body/div[9]/div[19]/div[12]/div[2]/div[4]/div[3]/div[3]/div[1]/div[3]/div/div[1]").click()
			
		  
		self.callCounters = {}  # call counter for each key
		self.previousDirection = 0  # pvious dirrection for caching optimization
									# and for easier cancelling last movement direction
		
	def close_current_tab(self):
		self.browser.close()

	def get_window_size(self):
		dim = self.browser.get_window_size()
		position = self.browser.get_window_position()
		position['y'] += dim['height'] - self.browser.find_element_by_tag_name('body').size['height']
		dim['height'] = self.browser.find_element_by_tag_name('body').size['height']
		return position, dim

	# действия агента оправляются через селениум, который инициализируется в классе Game,
	# поэтому все взаимодействия агента и среды должны быть прописаны в классе Game,
	# которые, в свою очередь, вызываются внутри агента
	# (агент - класс, у которого есть атрибут - класс Game).
	
	def start_playing(self):
		self.browser.find_element_by_id("btn-start-battle").click()
		#self.browser.find_element_by_xpath("/html/body/div[6]/div/div[1]/span").click()
		
	def restart_after_death(self):
		#Продолжить игру # взято отсюда https://habr.com/en/post/250975/
		try:
			print('поиск кнопки "Играть еще"')
			self.browser.find_element_by_xpath('/html/body/div[3]/div[4]/div[2]/div[1]/div[3]/a').click()
			print('нажал кнопку "Играть еще"')
		except:
			print('не нашел кнопку "Играть еще"')
			pass
		try:
			print('поиск кнопки "закрыть лишнее окно"')
			self.browser.find_element_by_xpath("/html/body/div[4]/div[28]/div/div[1]/span").click()
			print('нажал кнопку "закрыть лишнее окно"')
		except:
			print('не нашел кнопку "закрыть лишнее окно"')
			pass
		try:
			print('поиск кнопки "В бой"')
			self.start_playing()
			print('нажал кнопку "В бой"')
		except:
			print('не нашел кнопку "В бой"')
			pass
		
	 
		
#    def get_crashed(self):
#    def get_score(self):
#    def get_highscore(self):
	
	#==================================================================================================
	#================🡻 LOCOMOTION ACTIONS 🡻==========================================================
	
	# NOTE: Why not just use ActionChains.key_up(...)/key_down(...) !?
	# for keys like WASD, up, down etc. it is not possible to click and push them via ActionChains
	def _dispatchKeyEvent(self, name, options={}):
		options["type"] = name
		body = json.dumps({"cmd": "Input.dispatchKeyEvent", "params": options})
		resource = "/session/%s/chromium/send_command" % self.browser.session_id
		url = self.browser.command_executor._url + resource
		self.browser.command_executor._request("POST", url, body)

	def _holdKey(self, directStr, keyStr):
		options = {
			"code": "Key" + keyStr.upper(),  # Uppercase is required
			"key": keyStr.upper(),
			"text": keyStr.upper(),
			"unmodifiedText": keyStr.upper(),
			"nativeVirtualKeyCode": ord(keyStr.upper()),
			"windowsVirtualKeyCode": ord(keyStr.upper())
		}
		self._dispatchKeyEvent(directStr, options)
		
	def keyDown(self, key):
		self._holdKey(str(Direction.Down), str(key))
		
	def keyUp(self, key):
		self._holdKey(str(Direction.Up), str(key))
	
	def stop_moving(self):
		# отпускаем все кнопки, которые были нажаты ранее (даже если не были)
		self.keyUp(Key.A)
		self.keyUp(Key.S)
		self.keyUp(Key.D)
		self.keyUp(Key.W)
		
	def move(self, keys):
		self.stop_moving()
		for key in keys:
			self.keyDown(key) # зажимаем все кнопки движения, перечисленные во входном списке
			
	#================🡹 LOCOMOTION ACTIONS 🡹==========================================================
	#==================================================================================================
	
	def _createActionWithMoveTo(self, x, y):
		'''
		Функция для нескольких одновременных действий (начать двигаться, зажать ЛКМ и нажать доп клавишу)
		'''
		# action
		# https://stackoverflow.com/questions/32167577/how-to-move-the-mouse-in-selenium
		# https://selenium-python.readthedocs.io/api.html#module-selenium.webdriver.common.action_chains
		action = ActionChains(self.browser)
		#element = self.browser.find_element_by_id("game-touch-area")
		#size = element.size
		#centerBias = {"x": int(size["width"] / 2),
		#              "y": int(size["height"] / 2)}
		# -y because html axis "y" is inverted
		#return action.move_to_element_with_offset(
		#    element, centerBias["x"] + int(x), centerBias["y"] + int(-y))
		return action    #.move_by_offset(0,0)
		# ВСЯ ПРОБЛЕМА В медленной работе ФУНКЦИИ move_to_element_with_offset/move_by_offset
	#==================================================================================================
	#================🡻   MOUSE ACTIONS   🡻==========================================================
	
	def moveMouseTo(self, x, y):
		"""Move mouse relatively screen center
		Args:
			x ([int]): x axis
			y ([int]): y axis
		"""
		actions = self._createActionWithMoveTo(x, y)
		actions.perform()
	
	#================🡹   MOUSE ACTIONS    🡹==========================================================
	#==================================================================================================
	#==================================================================================================
	#================🡻 ADDITIONAL BUTTONS 🡻==========================================================
	
	def press(self, key): # F, R, N7, N8, N9, N0, N1, N2, N3
		self.keyDown(key)
		time.sleep(0.001)
		self.keyUp(key)
	
	# V - Свернуть миникарту
	
	#================🡹 ADDITIONAL BUTTONS 🡹==========================================================
	#==================================================================================================
	#==================================================================================================
	#================🡻 PROCESS AGENT'S ACTIONS 🡻=====================================================
	
	def keySwitch(self, key):
		keyStr = str(key)
		self.callCounters[keyStr] = self.callCounters.get(keyStr, 0) + 1
		if self.callCounters[keyStr] % 2 != 0:
			self.keyDown(key)
		else:
			self.keyUp(key)
			
	def _switchDirection(self, direction):
		keys = Key.fromDirection(direction)
		for key in keys:
			self.keySwitch(key)
					
	def process_all_agents_actions(self, request):
		""" Process request by surviv processor
			Args:
				request ([SurvivRequest]): Special class for managing surviv.io game
		"""
		# разобраться с приоритетами дествий внутри всего request'a
		if request.fKey == 1:
			self.press(Key.F)
		if request.actKey == 5: #перезарядка
			self.press(Key.R)
		elif request.actKey == 3: #сода
			self.press(Key.N9)          
		elif request.actKey == 4: #таблетки
			self.press(Key.N0)  
		elif request.actKey == 1: #бинты
			self.press(Key.N7) 
		elif request.actKey == 2: #аптечка
			self.press(Key.N8)
			
		if request.click == 1:
			action = ActionChains(self.browser)
			action.click_and_hold()
			action.perform()
		
		if request.switch_weap == 1: #переключиться на оружие 1
			self.press(Key.N1)
		elif request.switch_weap == 2: #переключиться на оружие 2
			self.press(Key.N2)          
		elif request.switch_weap == 3: #переключиться на оружие 3
			self.press(Key.N3)

		if self.previousDirection != request.direction:
			self._switchDirection(self.previousDirection)
			self._switchDirection(request.direction)
			self.previousDirection = request.direction
			
		if request.click == 1:
			time.sleep(request.dt_click/1000)  #длина очереди стрельбы
			post_act = ActionChains(self.browser) #поднимаем ЛКМ
			post_act.release()
			post_act.perform()
		
	#================🡹 PROCESS AGENT'S ACTIONS 🡹=====================================================
	#==================================================================================================