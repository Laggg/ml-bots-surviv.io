[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

# Intro
We present our **machine learning bot** (ml-bot is in alpha testing), which can play the [surviv.io](https://surviv.io/) game.

This bot tries to solve only **the locomotion problem** by training on human gameplay. To train this agent, we have used [100 youtube-videos](for_annotators/video_data) containing 1.2 million frames (equivalent to ~12 hours of gameplay recordings).

![Image of Yaktocat](jupyter_demo/for_preview.png)

![](jupyter_demo/h7vndtkzlinfkyoqzpcmjxecubu.gif)

#### Main features:
- our bot can get closer to the boxes with loot
- our bot knows how to avoid red zone
- our bot is trying to get out of the red zone (if the zone has covered it)
- our bot begins to move chaotically, when enemies shoot at him
- our bot likes to build a route through the bushes

# Motivation
The goal is to develop a bot that is interesting to watch. The behavior of the bot should not differ from the behavior of a person in similar situations. Our research will help raise the level of AI in games, make games more interesting, and bots in them more similar to the actions of a real person.

We assume that if people are interested in watching other gamers (professional or not) through [twitch](https://www.twitch.tv/), then they will be interested in watching our agent as well. 

# Technical stack
- python3
- selenium *(agent actions execution in game environment)*
- openCV *(screenshots processing)*
- torch *(action selection)*
- mss *(do screenshots)*

# Installation guides

<details>
  <summary>Windows</summary>
  
  __1. Clone GitHub repository__
  
  ```
  git clone https://github.com/Laggg/ml-bots-surviv.io
  ```
  __2. Download supporting files__

  Download model weights from [here](https://drive.google.com/u/0/uc?id=1l3exfxwT4ZVk1R6V2sxZimTafx1EkNtO&export=download) and chromedriver, that suits your chrome version, from [here](https://chromedriver.chromium.org/downloads). 

  Locate both files to `./supporting_files/` folder.

  > ![image](https://user-images.githubusercontent.com/45121687/134749881-a239f8be-ce69-41d3-9988-21e1083e3e3e.png)


  __3. Create python virtual environment and install requirements.txt__
  
  ```
  cd ml-bots-surviv.io
  python –m venv surviv_env 
  cd surviv_env/scripts && activate && cd ../../
  pip install -r requirements.txt 
  ``` 
  >![image](https://user-images.githubusercontent.com/45121687/134750475-d2ce7f57-c692-4fa6-8441-b90f7117a502.png)

  __4. Run the agent__
  ```
  python play.py
  ```

  ### Later usage

  __1. Activate python environment__
  ```
  cd surviv_env/scripts && activate && cd ../../
  ``` 

  __2. Run the agent__
  ```
  python play.py
  ```
</details>

<details>
  <summary>Ubuntu\MacOS</summary>
</br>
  
  __1. Clone GitHub repository__
  
  ```
  git clone https://github.com/Laggg/ml-bots-surviv.io
  ```

  __2. Download supporting files__

  Download model weights from [here](https://drive.google.com/u/0/uc?id=1l3exfxwT4ZVk1R6V2sxZimTafx1EkNtO&export=download) and chromedriver, that suits your chrome version, from [here](https://chromedriver.chromium.org/downloads). 

  Locate both files to `./supporting_files/` folder.

  
  __3. Create python virtual environment and install requirements.txt__
  
  ```
  cd ml-bots-surviv.io
  python -m venv surviv_env 
  source surviv_env/bin/activate
  pip install -r requirements.txt 
  ```
  
  __4. Run the agent__
  ```
  python play.py
  ```
  
  ### Later usage

  __1. Activate python environment__
  ```
  source surviv_env/bin/activate
  ``` 

  __2. Run the agent__
  ```
  python play.py
  ```
</details>
