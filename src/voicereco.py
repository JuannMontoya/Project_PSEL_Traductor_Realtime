import speech_recognition as sr

def recognize():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Calibrando el micrófono para el ruido ambiente...")
        r.adjust_for_ambient_noise(source)  # Ajusta el umbral de ruido
        print("¡Di algo!")
        audio = r.listen(source)

        # Lista de idiomas soportados (códigos de idioma de Google)
        languages = ["es-ES", "en-US", "fr-FR", "de-DE", "it-IT", "pt-BR", "ja-JP", "zh-CN"]

        # Intentar reconocer el audio en cada idioma
        for lang in languages:
            try:
                print(f"Intentando reconocer en {lang}...")
                text = r.recognize_google(audio, language=lang)
                print(f"Idioma detectado: {lang}")
                print(f"Has dicho: {text}")
                return text, lang
            except sr.UnknownValueError:
                print(f"No se pudo entender el audio en {lang}")
            except sr.RequestError as e:
                print(f"Error en la solicitud para {lang}: {e}")
            except Exception as e:
                print(f"Ocurrió un error con {lang}: {e}")

        print("No se pudo detectar el idioma o reconocer el audio.")
        return None, None


text, detected_lang = recognize()
if text:
    print(f"Texto reconocido: {text} (Idioma: {detected_lang})")
else:
    print("No se pudo reconocer el audio.")