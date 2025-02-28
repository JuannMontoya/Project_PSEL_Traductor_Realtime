import cv2
import pytesseract

def ocr_from_image(image_path):
    img = cv2.imread(image_path)
    if img is None:
        print("Error: No se pudo cargar la imagen")
        return
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, threshold = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    text = pytesseract.image_to_string(threshold, lang='spa')
    return text

if __name__ == "__main__":
    image_path = "test.jpg"
    extracted_text = ocr_from_image(image_path)
    print("Texto extraído:")
    print(extracted_text)