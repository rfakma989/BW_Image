import cv2 as im
import numpy as np
import os


def imgload(src):
    # return im.imread(src, im.IMREAD_COLOR)
    return im.imdecode(np.fromfile(src, np.uint8), im.IMREAD_COLOR)


def imgsave(name, img):
    # im.imwrite(name, img)
    path = os.path.splitext(name)
    result, encoded_img = im.imencode(".png", img)
    if result:
        with open(path[0] + ".png", mode='w+b') as f:
            encoded_img.tofile(f)


def thumbnail(img):
    h, w = img.shape[:2]
    r = 200 / max(w, h)
    dw = min(200, round(w * r))
    dh = min(200, round(h * r))
    return im.cvtColor(im.resize(img, dsize=(dw, dh), interpolation=im.INTER_AREA), im.COLOR_BGR2RGB)


def img_width_height(img):
    return img.shape[1::-1]


def expand(img, width=0, height=0, void=(0, 0, 0)):
    h, w = img.shape[:2]

    if width > 0:
        img = np.concatenate((np.full((h, width // 2, 3), void), img), axis=1)
        if width > 1:
            img = np.concatenate((img, np.full((h, width - (width // 2), 3), void)), axis=1)
        w += width

    if height > 0:
        img = np.concatenate((np.full((height // 2, w, 3), void), img), axis=0)
        if height > 1:
            img = np.concatenate((img, np.full((height - (height // 2), w, 3), void)), axis=0)
        h += height

    return np.array(img, dtype='uint8')


def generate(image1, image2, bg1, bg2, option1=False, option2=False):  # option : True = calculate, False = half
    gimg1 = im.cvtColor(image1, im.COLOR_BGR2GRAY)
    gimg2 = im.cvtColor(image2, im.COLOR_BGR2GRAY)

    if option1:
        mx = np.max(gimg1)
        mn = np.min(gimg1)
        if mx != mn: gimg1 = (gimg1 - mn) / (mx - mn) * 255

        mx = np.max(gimg2)
        mn = np.min(gimg2)
        if mx != mn: gimg2 = (gimg2 - mn) / (mx - mn) * 255

    if option2:
        m = np.max(gimg1 - gimg2) + 255
        if m != 0:
            r = 255 / m
        else:
            r = 0.5
    else:
        r = 0.5

    gimg1 = gimg1 * r
    gimg2 = 255 - (255 - gimg2) * r

    alpha = 255 - (gimg2 - gimg1)
    color = np.divide(gimg1 * 255, alpha, out=np.zeros_like(alpha), where=alpha != 0)

    layers = []
    for l in range(3):
        layers.append(color * (bg2[l] - bg1[l]) / 255 + bg1[l])

    return im.merge((*layers, alpha))


def addqrcode(img, option=3):  # 0:top left, 1:top right, 2:bottom left, 3:bottom right
    r, c = img.shape[:2]
    if r < 29 or c < 29: return img

    # qr = im.imread("QR Code.png", im.IMREAD_GRAYSCALE) // 255
    # qrr, qrc = qr.shape

    qr = ((0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0),
          (0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0),
          (0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0),
          (0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0),
          (0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0),
          (0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0),
          (0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0),
          (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1),
          (0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1),
          (1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1),
          (0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1),
          (1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0),
          (1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1),
          (0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1),
          (1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0),
          (0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0),
          (0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1),
          (0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1),
          (0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1),
          (0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0),
          (0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1),
          (1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1),
          (0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1),
          (0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0),
          (0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0),
          (0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1),
          (0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1),
          (0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0),
          (0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1))
    qrr, qrc = (len(qr), len(qr[0]))

    if option < 2:
        ro = 0
    else:
        ro = r - qrr

    if option % 2:
        co = c - qrc
    else:
        co = 0

    for i in range(qrr):
        for j in range(qrc):
            img[i + ro][j + co] = [255 for _ in range(4)] if qr[i][j] else [*[0 for _ in range(3)], 255]

    return img
