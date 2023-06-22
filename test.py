from TTS.api import TTS

tts = TTS("tts_models/en/jenny/jenny")

# Run TTS with emotion and speed control
tts.tts_to_file(text="Hello Sam, How may I help you?", file_path="./out.wav", emotion="Neutral", speed=3.5)