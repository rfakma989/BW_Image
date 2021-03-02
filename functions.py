import cv2 as im
import numpy as np


def match_images(image1, image2, bgc1=np.zeros(3), bgc2=np.zeros(3)):
    r1, c1, d = image1.shape
    r2, c2, d = image2.shape

    if r1 == r2 and c1 == c2: return (image1, image2)

    if r1 > r2:
        ofst = (r1 - r2) // 2
        if ofst > 0:
            blank = np.zeros((ofst, image2.shape[1], 3))
            blank[:][:] = bgc2
            image2 = np.concatenate((blank, image2), axis=0)
        blank = np.zeros((r1 - r2 - ofst, image2.shape[1], 3))
        blank[:][:] = bgc2
        image2 = np.concatenate((image2, blank), axis=0)
    else:
        ofst = (r2 - r1) // 2
        if ofst > 0:
            blank = np.zeros((ofst, image1.shape[1], 3))
            blank[:][:] = bgc1
            image1 = np.concatenate((blank, image1), axis=0)
        blank = np.zeros((r2 - r1 - ofst, image1.shape[1], 3))
        blank[:][:] = bgc1
        image1 = np.concatenate((image1, blank), axis=0)

    if c1 > c2:
        ofst = (c1 - c2) // 2
        if ofst > 0:
            blank = np.zeros((image2.shape[0], ofst, 3))
            blank[:][:] = bgc2
            image2 = np.concatenate((blank, image2), axis=1)
        blank = np.zeros((image2.shape[0], c1 - c2 - ofst, 3))
        blank[:][:] = bgc2
        image2 = np.concatenate((image2, blank), axis=1)
    else:
        ofst = (c2 - c1) // 2
        if ofst > 0:
            blank = np.zeros((image1.shape[0], ofst, 3))
            blank[:][:] = bgc1
            image1 = np.concatenate((blank, image1), axis=1)
        blank = np.zeros((image1.shape[0], c2 - c1 - ofst, 3))
        blank[:][:] = bgc1
        image1 = np.concatenate((image1, blank), axis=1)

    return (image1, image2)


def Generate(image_b, image_w, p_check=True):  # grayscaled image
    if image_b.shape != image_w.shape:
        return "ERROR"

    m = 0
    r, c = image_b.shape

    if p_check:
        m = np.max(image_b + image_w)
    else:
        m = 510

    if m > 255:
        image_b = image_b / m * 255
        image_w = 255 - ((255 - image_w) / m * 255)

    layer_alpha = (255 - image_w) + image_b
    layer_color = np.divide(image_b * 255, layer_alpha, out=np.zeros_like(layer_alpha), where=layer_alpha != 0)

    return im.merge((layer_color, layer_color, layer_color, layer_alpha))


def main_call(img_1, img_2):
    image_b = im.imread(img_1, im.IMREAD_COLOR)
    image_w = im.imread(img_2, im.IMREAD_COLOR)

    nimg1, nimg2 = match_images(image_b, image_w)

    print(nimg1.shape)
    print(nimg2.shape)

    nimg = Generate(im.cvtColor(np.float32(nimg1), im.COLOR_BGR2GRAY),
                    im.cvtColor(np.float32(nimg2), im.COLOR_BGR2GRAY))

    im.imwrite('extract.png', nimg)
    print("DONE")
    return 0
