<details>
  <summary>guide for Windows</summary>
  
  ### [Before the first launch]
  **1.** Check that you have Anaconda3 with python3

  **2.** Check that you have google chrome browser (our agent supports only chrome)

  ### [For the first launch]
  **0.** Earlier you do 1-2 steps from paragraph *[Before the first launch]*

  **1.** Clone repo by *Anaconda Prompt* or dowland zip-file repo and unzip it
  ```
  git clone https://github.com/Laggg/ml-bots-surviv.io.git
  ```
  **2.** Dowland neural net weights from [this link](https://drive.google.com/u/0/uc?id=1l3exfxwT4ZVk1R6V2sxZimTafx1EkNtO&export=download) and put it into *./supporting_files/* folder

  **3.** Dowland driver for your OS and for your chrome version (don't forget to check your google chrome version!) from [link](https://chromedriver.chromium.org/downloads), unzip it and put into *./supporting_files/* folder

  > after 3rd step you can check *./supporting_files/* folder:
  >> ![image](https://user-images.githubusercontent.com/45121687/134749881-a239f8be-ce69-41d3-9988-21e1083e3e3e.png)

  **4.** Open Anaconda prompt inside repo-folder
  > example:
  >> ![image](https://user-images.githubusercontent.com/45121687/134750475-d2ce7f57-c692-4fa6-8441-b90f7117a502.png)

  **5.** Create a virtual environment for this project
  ```
  python –m venv surviv_env
  ```
  **6.** Activate created virtual environment
  ```
  cd surviv_env/scripts && activate && cd ../../
  ```
  **7.** Install all required libraries
  ```
  pip install -r requirements.txt
  ```
  **8.** Launch the agent into the game!
  ```
  python play.py
  ```
  **9.** After all you can deactivate virtual env and close Anaconda prompt window
  
  ### [For the second+ launch]
  **0.** Earlier you do 1-9 steps from paragraph *[For the first launch]*

  **1.** Open Anaconda prompt inside repo-folder

  **2.** ```cd surviv_env/scripts && activate && cd ../../```

  **3.** ```python play.py```

  **4.** After all you can close deactivate virtual env and close Anaconda prompt window
</details>


<details>
  <summary>guide for Ubuntu\MacOS</summary>
  ### [For the first launch]
  **1.**
  ```
  git clone https://github.com/Laggg/ml-bots-surviv.io
  ```
  **2.** Use terminal in this repo-folder
  ```
  python3 -m venv surviv_env 
  source surviv_env/bin/activate
  pip install -r requirements.txt 
  ```
  **3.** ```python play.py```
</details>

### [For the first launch]
**1.** ```git clone https://github.com/Laggg/ml-bots-surviv.io```

**2.** Use terminal in this repo-folder
```
python3 -m venv surviv_env 
source surviv_env/bin/activate
pip install -r requirements.txt 
```

**3.** ```python play.py```
