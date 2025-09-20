from gtts import gTTS

text = """大家好，欢迎收听这段语音示例。我是一段二十秒左右的普通话音频，主要是用来测试文字转语音的效果。
无论是学习、演讲练习，还是作为项目的演示素材，这样的音频都能派上用场。
希望这段声音能够清晰自然，给你带来流畅的体验。"""

# 生成普通话语音
tts = gTTS(text=text, lang='zh-cn')

# 保存为 mp3 文件
tts.save("sample_audio.mp3")
print("已生成 sample_audio.mp3")