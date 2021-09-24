## [Windows] 
#### For the first launch 

**1)** Clone repo by *Anaconda Prompt* or dowland zip-file repo and unzip it:
```
git clone https://github.com/Laggg/ml-bots-surviv.io.git
```
**2)** Dowland neural net weights from [this link](https://drive.google.com/u/0/uc?id=1l3exfxwT4ZVk1R6V2sxZimTafx1EkNtO&export=download) and put it into *./support_files/* folder

**3)** Dowland driver for your OS and for your chrome version (check your google chrome version!) from [link](https://chromedriver.chromium.org/downloads), unzip it and put into *./support_files/* folder

> after 3rd step you can check you *./support_files/* folder:
>> ![image](https://user-images.githubusercontent.com/45121687/134749881-a239f8be-ce69-41d3-9988-21e1083e3e3e.png)

**4)** open Anaconda prompt in folder of this repo
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
