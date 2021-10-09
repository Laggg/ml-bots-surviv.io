import os
import cv2
import mss
import time
import gdown
import torch
import argparse
import numpy as np
from utils import (NeuralNet, BRAIN, 
	check_device, get_driver_path, get_model_weights)
from control_scripts_lib import SurvivAgent, Game


def get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('--chrome_adblock', type=str,
						default="supporting_files/uBlockOrigin.crx")
	parser.add_argument('--device', type=str, default='cpu')
	parser.add_argument('--n_iter', type=int, default=500)
	parser.add_argument('--print_metrics', type=bool, default=False)
	parser.add_argument('--plot_states', type=bool, default=False)
	parser.add_argument('--save_video', type=bool, default=False)
	parser.add_argument('--video_output_path', type=str, default='game.mp4')
	return parser.parse_args()


def load_model(device: str):
	''' loading action model '''
	url = 'https://drive.google.com/u/0/uc?id=1l3exfxwT4ZVk1R6V2sxZimTafx1EkNtO&export=download'
	output = 'supporting_files/model_weights.pth'
	if os.path.isfile(output):
		print(f'File is found in {output}')
	else:
		print('Downloading')
		gdown.download(url, output, quiet=False)

	model = NeuralNet()
	model.load_state_dict(
		torch.load(output, map_location=torch.device(device))
	)
	model.eval()
	return model


def play_game(agent, agent_control, game, monitor,
			  n_iter) -> (list, float, float):
	screen_shots = list()

	start_time = time.time()
	agent.update_state()

	for i in range(n_iter):
		with mss.mss() as sct:
			screen = sct.grab(monitor)
		p = np.array(screen)[:, :, :3]
		screen_shots.append(p)
		agent.update_state()
		actions = agent_control.choose_action(p)
		agent.do_all_choosen_actions(direction=actions + 1)

	end_time = time.time()
	game.close_current_tab()

	return screen_shots, start_time, end_time


def save_video(output_file: str, screen_shots, fps: int = 60,
			   width: int = 1280, height: int = 814) -> None:
	''' save gameplay video '''
	#h, w, _ = screen_shots[0].shape
	# out = cv2.VideoWriter(
	#	output_file,
	#	cv2.VideoWriter_fourcc(*"DIVX"), fps, (width, height))
	# cv2.VideoWriter_fourcc(*"MPEG"), fps,  (w, h))
	# for shot in screen_shots:
	#	out.write(shot)
	# out.release()
	# print(screen_shots[-1].shape)
	#cv2.imshow('image', screen_shots[-1])
	# cv2.waitKey(0)
	raise NotImplementedError()


def main():
	args = get_args()

	args.device = check_device(args.device)

	model = load_model(args.device)
	game_env = Game(args.chrome_adblock)
	agent = SurvivAgent(game_env)
	agent_control = BRAIN(
		agent=agent,
		model=model,
		device=args.device,
		plot_state=args.plot_states
	)

	agent.start_playing()

	screen_position, screen_dim = game_env.get_window_size()

	monitor = {
		"top": screen_position['y'],
		"left": screen_position['x'],
		"width": screen_dim['width'],
		"height": screen_dim['height']
	}

	screen_shots, start_time, end_time = play_game(
		agent, agent_control, game_env, monitor, args.n_iter)

	if args.print_metrics:
		print('AVG fps: ',
			  round(args.n_iter / (end_time - start_time), 2))
		print('AVG 1 circle: ',
			  round((end_time - start_time) / args.n_iter, 3))

	if args.save_video:
		save_video(
			args.video_output_path,
			screen_shots,
			round(args.n_iter / (end_time - start_time), 2),
			screen_dim['width'],
			screen_dim['height']
		)


if __name__ == '__main__':
	main()
