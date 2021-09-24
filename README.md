## [Windows] 
#### For the first launch 

1) Clone or dowland this repo as zip-file:
```
git clone https://github.com/Laggg/ml-bots-surviv.io.git
```
4) скачать веса модели и положить ее в папку /support_files/
5) скачать драйвер для браузера, который зависит от вашей версии хрома и вашей операционной системы и положить его в папку /support_files/
6) open Anaconda prompt in folder of this repo
7) create a virtual environment: python –m venv surviv_env  (вместо "surviv_env" можете написать любое другое название окружения, с помощью которого будете запускать этот код)
8) cd surviv_env/scripts && activate && cd ../../
9) pip install -r requirements.txt
10) python play.py

#### For the second+ launch 
0) earlier you do 1-10 steps from paragraph "For the first launch"
1) open anaconda prompt in folder with this repo
2) cd surviv_env/scripts && activate && cd ../../
3) python play.py

## [Ubuntu\MacOS] 
### Activating Surviv environment
```
python3 -m venv surviv_env 
source surviv_env/bin/activate
pip install -r requirements.txt 
```

### ChromeDriver

```
https://chromedriver.chromium.org/downloads
```

### Model weights

```
https://drive.google.com/u/0/uc?id=1l3exfxwT4ZVk1R6V2sxZimTafx1EkNtO&export=download
```

### Playing surviv.io game
```
python play.py
```
