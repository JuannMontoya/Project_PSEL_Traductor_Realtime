import pytesseract
import cv2
import numpy as np
from picamera2 import Picamera2
from langdetect import detect

def take_photo():
    picam2 = Picamera2()
    picam2.start()
    image = picam2.capture_array()
    cv2.imwrite('image.jpg', image)
    return image

def preprocess(image):
 
    imagen = cv2.imread(image, cv2.IMREAD_GRAYSCALE)

    imagen = cv2.resize(imagen, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    imagen = cv2.GaussianBlur(imagen, (5, 5), 0)
    imagen = cv2.adaptiveThreshold(imagen, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                   cv2.THRESH_BINARY, 11, 2)

    kernel = np.ones((2,2), np.uint8)
    imagen = cv2.morphologyEx(imagen, cv2.MORPH_CLOSE, kernel)

    cv2.imwrite("preprocesada.jpg", imagen)
    return imagen

def get_text(image):

    if isinstance(image, str):
        image = cv2.imread(image)
        
    try:

        multi_lang = 'eng+spa+fra+deu'
        text_inicial = pytesseract.image_to_string(image, lang=multi_lang, config='--oem 3 --psm 6')
        print("Texto inicial:")
        print(text_inicial)
        
  
        try:
            idioma_detectado = detect(text_inicial)
            print("Idioma detectado:", idioma_detectado)

            lang_map = {'en': 'eng', 'es': 'spa', 'fr': 'fra', 'de': 'deu'}
            tesseract_lang = lang_map.get(idioma_detectado, multi_lang)
        except Exception as e:
            print("No se pudo detectar el idioma, se usará OCR multi-idioma")
            tesseract_lang = multi_lang

        text_final = pytesseract.image_to_string(image, lang=tesseract_lang, config='--oem 3 --psm 6')
        print("Texto final:")
        print(text_final)
        return text_final

    except pytesseract.pytesseract.TesseractError:
        print("No se pudo extraer el texto de la imagen")
        return None
    except Exception as e:
        print(e)
        return None


take_photo()
preprocess('image.jpg')
get_text('preprocesada.jpg')
