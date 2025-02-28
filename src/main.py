import ctypes
import os
import logging
import contextlib
import cv2
import numpy as np
import pytesseract
from picamera2 import Picamera2
from langdetect import detect
import speech_recognition as sr
from ApiManager import ApiManager
import Realtime
import time

# ---------------------------
# Anulación de mensajes de error de ALSA
def no_alsa_error_handler(filename, line, function, err, fmt):
    pass

ERROR_HANDLER_FUNC = ctypes.CFUNCTYPE(
    None, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p
)
c_error_handler = ERROR_HANDLER_FUNC(no_alsa_error_handler)
try:
    asound = ctypes.cdll.LoadLibrary("libasound.so")
    asound.snd_lib_error_set_handler(c_error_handler)
except Exception:
    pass

# ---------------------------
# Anulación de mensajes de error de JACK
def no_jack_error_handler(msg):
    pass

JACK_ERROR_FUNC = ctypes.CFUNCTYPE(None, ctypes.c_char_p)
c_jack_error_handler = JACK_ERROR_FUNC(no_jack_error_handler)
try:
    libjack = ctypes.cdll.LoadLibrary("libjack.so")
    libjack.jack_set_error_function(c_jack_error_handler)
except Exception:
    pass

# ---------------------------
os.environ["LIBCAMERA_LOG_LEVEL"] = "0"
logging.disable(logging.CRITICAL)

@contextlib.contextmanager
def suppress_stderr():
    with open(os.devnull, 'w') as f, contextlib.redirect_stderr(f):
        yield

# Clase para manejar el OCR
class OCR:
    @staticmethod
    def take_photo():
        with suppress_stderr():
            picam2 = Picamera2()
            picam2.configure(picam2.create_still_configuration())
            picam2.start()
            image = picam2.capture_array()
            cv2.imwrite('image.jpg', image)
        return image

    @staticmethod
    def preprocess(image_path):
        with suppress_stderr():
            image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            image = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
            image = cv2.GaussianBlur(image, (5, 5), 0)
            _, image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        cv2.imwrite("preprocessed.jpg", image)
        return image

    @staticmethod
    def get_text(image):
        if isinstance(image, str):
            image = cv2.imread(image)
        try:
            with suppress_stderr():
                text = pytesseract.image_to_string(image, lang='eng+spa', config='--oem 3 --psm 6')
                detected_lang = detect(text)
                lang_map = {'en': 'eng', 'es': 'spa'}
                final_lang = lang_map.get(detected_lang, 'eng+spa+fra+deu')
                return pytesseract.image_to_string(image, lang=final_lang, config='--oem 3 --psm 6')
        except Exception:
            return None

# Clase para reconocimiento de voz
class VoiceRecognizer:
    @staticmethod
    def recognize():
        with suppress_stderr():
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print("Escuchando...")
                # Se incrementa la duración para ajustar el ruido ambiental
                r.adjust_for_ambient_noise(source, duration=2)
                audio = r.listen(source)
        languages = ["es-ES", "en-US"]
        for lang in languages:
            try:
                text = r.recognize_google(audio, language=lang)
                # Imprime datos de depuración para verificar el texto y el idioma detectado
                print(f"Reconocido ({lang}):", text)
                return text.lower(), lang[:2]
            except sr.UnknownValueError:
                continue
            except sr.RequestError:
                return None, None
        return None, None



def main():
    api = ApiManager("http://127.0.0.1:8001")
    recognizer = VoiceRecognizer()

    wake_word = "activar"
    stop_word = "traducir"

    while True:
        print("Esperando comando de activación...")
        text, _ = recognizer.recognize()
        if text and wake_word in text:
            print("Sistema activado. Escuchando comandos...")
            break
        elif text:
            print(f"Comando no reconocido: {text}")
        else:
            print("No se pudo reconocer el audio.")

    while True:
        text, detected_lang = recognizer.recognize()
        if text:
            print(f"Comando recibido: {text}")
            if stop_word in text:
                print("Modo de traducción activado. ¿Qué desea traducir?")
                break
            elif "foto" in text:
                OCR.preprocess("image.jpg")
                translated_text = OCR.get_text("preprocessed.jpg")
                print("Texto detectado:", translated_text)
            elif "voz" in text:
                print("Capturando texto de voz para traducción...")
                text, detected_lang = recognizer.recognize()
                data = {"q": text, "source": detected_lang, "target": "es", "format": "text"}
                translation = api.post("/translate", data)
                print("Traducción:", translation)
            elif "pantalla" in text:
                print("Iniciando OCR en tiempo real...")
                pass
            else:
                print("Comando no reconocido.")
        else:
            print("No se pudo reconocer el audio.")

    while True:
        print("Seleccione modo de traducción: [foto/voz/pantalla]")
        mode, _ = recognizer.recognize()
        print("Modo detectado:", mode)
        if mode:
            if "foto" in mode:
                OCR.preprocess("image.jpg")
                translated_text = OCR.get_text("preprocessed.jpg")
                print("Texto traducido:", translated_text)
            elif "escuchar" in mode or "voz" in mode:
                print("Capturando texto de voz para traducción...")
                text, detected_lang = recognizer.recognize()
                data = {"q": text, "source": detected_lang, "target": "es", "format": "text"}
                translation = api.post("/translate", data)
                print("Traducción:", translation)
            elif "pantalla" in mode:
                print("Iniciando OCR en tiempo real...")
                timereal = Realtime.OCRProcessor()
                timereal.run()
                print("Proceso iniciado. Presione Ctrl+C para detenerlo.")
            else:
                print("Modo no reconocido.")
        else:
            print("No se pudo reconocer el audio.")
        # Pequeña pausa antes de la siguiente iteración
        time.sleep(1)

if __name__ == "__main__":
    main()
