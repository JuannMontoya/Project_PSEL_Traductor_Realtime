
# Traductor en tiempo real
[![Python versions](https://img.shields.io/pypi/pyversions/libretranslate)](https://pypi.org/project/libretranslate)

sistema embebido en python para traduccion en tiempo real, traduccion de imagen y traduccion de voz, este proyecto usa la api offline gratuita de [Libretranslate](https://github.com/LibreTranslate/LibreTranslate) ya que es la unica que ofrece paquetes de traduccion sin pagos o sin dejar informacion de pago.




## Dependecias

Para usar este proyecto se tienen las siguientes Dependecias

```bash
  pip install libretranslate
```

```bash
  pip install opencv-python

```
```bash
  pip install pytesseract
```

## Documentation

Ejecutar el main 

```bash
  python main.py
```

Comandos de voz ya que al iniciar el main este hara una escucha continua hasta escuchar la palabra clave "activar" para iniciar un proceso de escucha de segundo comando de confirmacion el cual es "traducir" despues de esto se presentaran tres posibilidades que tambien se activan por comandos de voz.

- FOTO: Hace una unica captura, genera el OCR y hace una peticion http 
- ESCUCHAR: Genera una escucha en microfono retorna el texto y hace una peticion http
- EN PANTALLA: Activa el OCR en tiempo real con la camara activa  y hace una peticion http




## API Reference for libretranslate

#### Get all items

```http
  POST /translate
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `q` | `string` | **Required**. text to translate |
| `source` | `string` | **optional**. lang to text |
| `target` | `string` | **Required**. text target translate |
| `format` | `string` | **Required**. text |


Toma un texto y lo traduce.




## Authors

- [@JuannMontoya](https://github.com/JuannMontoya)

