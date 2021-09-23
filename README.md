


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


### Playing Surviv.io game
```
python play.py --model_path='supporting_assets/model_weights.pth' --chrome_driver_path='supporting_assets/chromedriver' --chrome_adblock='supporting_assets/uBlockOrigin.crx'
```