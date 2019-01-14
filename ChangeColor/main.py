import math
import matplotlib.pyplot as plt
import numpy as np
import re
import matplotlib.colors as mcolors
import cv2
from numpy.core.multiarray import ndarray

plt.rcParams['image.cmap'] = 'gray'


class HEX(object):
    def __init__(self):
        pass

    def is_valid_hex_color(self, value, verbose=True):
        """Return True is the string can be interpreted as hexadecimal color
        Valid formats are
         * #FFF
         * #0000FF
         * 0x0000FF
         * 0xFA1
        """
        try:
            self.get_standard_hex_color(value)
            return True
        except Exception as err:
            if verbose:
                print(err)
            return False

    def get_standard_hex_color(self, value):
        """Verifica el color en estandar hexadecimal

        Por estándar, una cadena que representa el color en hex inicia con
        el sigmobo # seguido de 6 u 8 digitos, e.g. #AABBFF
        """
        if isinstance(value, str) == False:
            raise TypeError("El valor debe ser un string")
        if len(value) <= 3:
            raise ValueError("La entrada debe ser del tipo: 0xFFF, 0xFFFFFF or #FFF or #FFFFFF")

        if value.startswith("0x") or value.startswith("0X"):
            value = value[2:]
        elif value.startswith("#"):
            value = value[1:]
        else:
            raise ValueError("La cadena hexadesimal debe iniciar con '#' sign or '0x' string")
        value = value.upper()
        # Now, we have either FFFFFF or FFF
        # now check the length
        for x in value:
            if x not in "0123456789ABCDEF":
                raise ValueError("Se encontró un caracter no valido: {0}".format(x))

        if len(value) == 6:
            value = "#" + value[0:6]
        elif len(value) == 8:
            value = "#" + value[0:8]
        elif len(value) == 3:
            value = "#" + value[0] * 2 + value[1] * 2 + value[2] * 2
        else:
            raise ValueError("La cadena hexa string debe tener 3, 6 o 8 digitos. Si son 8 digitos")
        return value

# Define how many square colors are printed. For default we have 2 rows and 3 columns
def imageRandomColor(row=1, colum=3, channel=4):
    # creación colores aleatoreos
    colors = np.random.random_integers(255, size=(row, colum, channel))
    print(colors)
    # a = np.array([[[0,0,0,0]]])
    # np.append
    # for a in range(5):
    #    np.append(a,np.array([[[a,0,0,0]]]))

    # print(a)
    # print(a.shape)
    return colors


def plotImagen(imagen, ver_canales=False):
    if ver_canales == True:
        print(imagen)
    plt.imshow(imagen, vmin=0, vmax=1)
    plt.show()


def cambiarTipoColor(color, tipo=2, transparency = 1):
    """
    Para el cambio de color si es HEX a RGB se ingresa un string
    Por ejemplo: color="#0f265c"
    Si es de RGB a HEX se ingresa una tupla
    Por ejemplo: color=(15,38,92)

    Tipo 1-> RGBA a HEXA
    Tipo 2-> HEXA a RGBA
    """
    if tipo == 1:
        if transparency == 0:
            print("Cambio de RGB a HEXA")
            salida = '#%02X%02X%02X' % (color[0], color[1], color[2])
            print("{} <=> {}".format(color, salida))
            return salida
        if transparency == 1:
            print("Cambio de RGBA a HEXA")
            salida = '#%02X%02X%02X%02X' % (color[0], color[1], color[2], color[3])
            print("{} <=> {}".format(color, salida))
            return salida
    elif tipo == 2:
        print("Cambio de HEXA a RGBA")
        color = HEX().get_standard_hex_color(color)[1:]
        if len(color) == 8:
            r, g, b, a = int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16), int(color[6:8], 16)
            print("{} <=> {}".format(color, [r, g, b, a]))
            return [r, g, b, a]
        if len(color) == 6 and transparency == 1:
            r, g, b, a = int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16), 255
            print("{} <=> {}".format(color, [r, g, b, a]))
            return [int(r), int(g), int(b), int(a)]
        if len(color) == 6 and transparency == 0:
            r, g, b = int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16)
            print("{} <=> {}".format(color, [r, g, b]))
            return [int(r), int(g), int(b)]

# Generate an array of hex colrs
def array_HEX_colors(hex_colors):
    list_hex_colors = []
    for x in hex_colors:
        if x:
            # print("%s \n" % x.group(0))
            list_hex_colors.append("#"+x.group(0))
    return list_hex_colors

def rgb2hsv(r, g, b):
    r, g, b = r/255.0, g/255.0, b/255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx-mn
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g-b)/df) + 360) % 360
    elif mx == g:
        h = (60 * ((b-r)/df) + 120) % 360
    elif mx == b:
        h = (60 * ((r-g)/df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = df/mx
    v = mx
    return [h, s, v]

def hsv2rgb(h, s, v):
    h = float(h)
    s = float(s)
    v = float(v)
    h60 = h / 60.0
    h60f = math.floor(h60)
    hi = int(h60f) % 6
    f = h60 - h60f
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    r, g, b = 0, 0, 0
    if hi == 0: r, g, b = v, t, p
    elif hi == 1: r, g, b = q, v, p
    elif hi == 2: r, g, b = p, v, t
    elif hi == 3: r, g, b = p, q, v
    elif hi == 4: r, g, b = t, p, v
    elif hi == 5: r, g, b = v, p, q
    r, g, b = int(r * 255), int(g * 255), int(b * 255)
    if r > 255: r= 255;
    if g > 255: g = 255;
    if b > 255: b = 255;
    return r, g, b

def increase_hue(color, diff):
    if color+diff >360:
        return 360-(color+diff)
    elif color+diff <0:
        return 360+(color+diff)
    else:
        return color+diff

def main():
    # Read file with colors
    old_hex = array_HEX_colors([re.search('(?<=\'#)[a-fA-F\d]+', line) for line in open('Colors.css')])

    # Change iput list to numpy array with RGB format
    colors_rgb: ndarray = np.zeros((len(old_hex),10, 3),dtype=np.int32)
    for i,color_hex in enumerate(old_hex):
        for j in range(0,10):
            colors_rgb[i][j] = np.array(cambiarTipoColor(color_hex,transparency=0), dtype=np.int32)

    # TODO change  colors  to HSV(HUE SATURATION value)  # Logiciel color h = 300 base color 208. Diff = 83
    diff_hue = -28
    colors_hvs: ndarray = np.zeros((len(old_hex), 10, 3), dtype=np.float64)
    for i, color_hex in enumerate(old_hex):
        for j in range(0, 10):
            colors_hvs[i][j] = np.array(rgb2hsv(colors_rgb[i][j][0], colors_rgb[i][j][1], colors_rgb[i][j][2]),
                                        dtype=np.float64)
            if colors_hvs[i][j][1] >= 0.1 and colors_hvs[i][j][2]>= 0.1:
                colors_hvs[i][j] = np.array(rgb2hsv(increase_hue(colors_rgb[i][j][0], diff_hue), colors_rgb[i][j][1], colors_rgb[i][j][2]),
                                        dtype=np.float64)

    #Combert to hsv to rgb
    new_rgb: ndarray = np.zeros((len(old_hex), 10, 3), dtype=np.float32)
    for i, color in enumerate(old_hex):
        for j in range(0, 10):
            new_rgb[i][j] = np.array(hsv2rgb(colors_hvs[i][j][0], colors_hvs[i][j][1], colors_hvs[i][j][2]),
                                     dtype=np.int32)

    # TODO print the result and comparation
    fig = plt.figure(figsize=(7,6.5)) #W, H

    a = fig.add_subplot(1, 2, 1)
    imgplot = plt.imshow(colors_rgb)
    a.set_title('Before')
    plt.axis('off')

    a = fig.add_subplot(1, 2, 2)
    imgplot = plt.imshow(new_rgb.astype(int))
    a.set_title('After')
    plt.axis('off')

    plt.show()

    # TODO save a file with especific format
    new_hex = []
    for i,color_hex in enumerate(old_hex):
        new_hex.append(cambiarTipoColor((new_rgb[i][0][0].astype(int),new_rgb[i][0][1].astype(int),new_rgb[i][0][2].astype(int)),transparency=0, tipo=1))

    f = open("ColorsMapping.css", "w+")
    f.write("$VAR1 = [\n")
    for i, old_Hex in enumerate(old_hex):
        if old_Hex != new_hex[i]:
            f.write("\'"+old_Hex+"\', \'"+new_hex[i]+"\'\n")
    f.write("];")
    f.close()

if __name__ == "__main__":
    main()
