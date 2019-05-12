from aip import AipSpeech

app_id = "14975947"
api_key = "X9f3qewZCohppMHxlunznUbi"
secret_key = "LupWgIIFzZ9kTVNZSH5G0guNGZIqqTom"

client = AipSpeech(app_id, api_key, secret_key)
result = client.synthesis("声音测试,Good morning!", "zh", 4, {
    "vol": 9, # 音量
    "spd": 5, # 语速
    "pit": 7, # 语调
    "per": 4, # 音色,0为女声，1为男声，3为情感合成-度逍遥，4为情感合成-度丫丫，默认为普通女
})

with open("Test.mp3", "wb") as f:
    f.write(result)