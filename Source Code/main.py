from tkinter import filedialog, colorchooser, messagebox
from PIL import Image as PILimage
from PIL import ImageTk as PILimagetk

import numpy as np
import tkinter as t
import image_functions as i

# Const
global true
global false
global image_1_exist
global image_2_exist
global image_1_original
global image_2_original
global image_1_match
global image_2_match

true = True
false = False
image_1_exist = false
image_2_exist = false
image_1_original = ""
image_2_original = ""
image_1_match = ""
image_2_match = ""

initdir = "/"
bgcolor1 = (0, 0, 0)  # BGR
bgcolor2 = (255, 255, 255)  # BGR
voidcolor1 = (0, 0, 0)  # BGR
voidcolor2 = (255, 255, 255)  # BGR


def refresh():
    global image_1_original
    global image_2_original

    if image_1_exist:
        w1, h1 = i.img_width_height(image_1_original)
    else:
        w1, h1 = (0, 0)

    if image_2_exist:
        w2, h2 = i.img_width_height(image_2_original)
    else:
        w2, h2 = (0, 0)

    mw = max(w1, w2)
    mh = max(h1, h2)

    if image_1_exist:
        global image_1_match
        image_1_match = i.expand(image_1_original, mw - w1, mh - h1, voidcolor1)
        # i.imgsave("match1.png", image_1_match)

        # i.imgsave("thumb1.png", i.thumbnail(image_1_match))
        # tmb1 = t.PhotoImage(file="thumb1.png")

        tmb1 = PILimagetk.PhotoImage(image=PILimage.fromarray(i.thumbnail(image_1_match)))

        thumb_left.configure(image=tmb1)
        thumb_left.image = tmb1

    if image_2_exist:
        global image_2_match
        image_2_match = i.expand(image_2_original, mw - w2, mh - h2, voidcolor2)
        # i.imgsave("match2.png", image_2_match)

        # i.imgsave("thumb2.png", i.thumbnail(image_2_match))
        # tmb2 = t.PhotoImage(file="thumb2.png")

        tmb2 = PILimagetk.PhotoImage(image=PILimage.fromarray(i.thumbnail(image_2_match)))

        thumb_right.config(image=tmb2)
        thumb_right.image = tmb2


def load():
    global initdir
    filename = filedialog.askopenfilename(
        initialdir=initdir,
        title="Select image file",
        filetypes=(
            ("Image files", "*.jpg *.jpeg *.png *.bmp"),
            ("All files", "*.*")
        )
    )
    initdir = filename
    print(filename)
    return filename


def save():
    global initdir
    filename = filedialog.asksaveasfilename(
        initialdir=initdir,
        title="Save file",
        filetypes=(("PNG file", ".png"),)
    )
    initdir = filename
    return filename


# Command functions

def imageswitch():
    if image_1_exist and image_2_exist:
        global image_1_original
        global image_2_original

        image_1_original, image_2_original = (image_2_original, image_1_original)
        refresh()


def loadimage1():
    l = load()
    if l != "":
        global image_1_original
        global image_1_exist
        image_1_original = i.imgload(l)
        image_1_exist = true
        w, h = i.img_width_height(image_1_original)
        label_leftimage.config(text=str(w) + " x " + str(h))
        refresh()


def loadimage2():
    l = load()
    if l != "":
        global image_2_original
        global image_2_exist
        image_2_original = i.imgload(l)
        image_2_exist = true
        w, h = i.img_width_height(image_2_original)
        label_rightimage.config(text=str(w) + " x " + str(h))
        refresh()


def com_leftbgcolor():
    color_code = colorchooser.askcolor(title="Choose color")
    if color_code != (None, None):
        btn_leftbgcolor.config(bg=color_code[1])
        frame_leftbg.config(bg=color_code[1])
        thumb_left.config(bg=color_code[1])
        global bgcolor1
        bgcolor1 = tuple(map(int, color_code[0][::-1]))


def com_rightbgcolor():
    color_code = colorchooser.askcolor(title="Choose color")
    if color_code != (None, None):
        btn_rightbgcolor.config(bg=color_code[1])
        frame_rightbg.config(bg=color_code[1])
        thumb_right.config(bg=color_code[1])
        global bgcolor2
        bgcolor2 = tuple(map(int, color_code[0][::-1]))


def com_leftvoidcolor():
    color_code = colorchooser.askcolor(title="Choose color")
    if color_code != (None, None):
        btn_leftvoidcolor.config(bg=color_code[1])
        global voidcolor1
        voidcolor1 = tuple(map(int, color_code[0][::-1]))
        refresh()


def com_rightvoidcolor():
    color_code = colorchooser.askcolor(title="Choose color")
    if color_code != (None, None):
        btn_rightvoidcolor.config(bg=color_code[1])
        global voidcolor2
        voidcolor2 = tuple(map(int, color_code[0][::-1]))
        refresh()


def com_generate():
    s = save()
    print(s)
    result = i.generate(image_1_match, image_2_match, bgcolor1, bgcolor2, var0, var1)
    i.imgsave(s, i.addqrcode(result))
    messagebox.showinfo("BW Image Generator", "Image has Saved")


if __name__ == '__main__':
    mainframe = t.Tk()
    mainframe.title("BW Image Generator")
    # mainframe.geometry("640x480")
    mainframe.resizable(false, false)

    # 이미지 프레임
    frame_image = t.LabelFrame(mainframe, text="이미지")
    frame_image.pack(padx=10, pady=10)

    # 프레임 3등분
    frame_leftimage = t.LabelFrame(frame_image, text="이미지 1")
    frame_leftimage.pack(side="left", padx=10, pady=10)
    frame_switch = t.Frame(frame_image)
    frame_switch.pack(side="left")
    frame_rightimage = t.LabelFrame(frame_image, text="이미지 2")
    frame_rightimage.pack(side="left", padx=10, pady=10)

    # 왼쪽 프레임
    frame_leftbg = t.Frame(frame_leftimage, width=210, height=210, bg="black")
    frame_leftbg.pack(padx=10, pady=10)
    thumb_left = t.Label(frame_leftbg, bg="black")
    thumb_left.pack(expand=true)
    frame_leftbg.propagate(0)
    label_leftimage = t.Label(frame_leftimage, text="? x ?")
    label_leftimage.pack()
    btn_leftimage = t.Button(frame_leftimage, text="이미지 불러오기", command=loadimage1)
    btn_leftimage.pack(padx=10, pady=10)

    # 가운데 프레임
    btn_switch = t.Button(frame_switch, text="이미지\n바꾸기", command=imageswitch)
    btn_switch.pack(padx=10)

    # 오른쪽 프레임
    frame_rightbg = t.Frame(frame_rightimage, width=210, height=210, bg="white")
    frame_rightbg.pack(padx=10, pady=10)
    thumb_right = t.Label(frame_rightbg, bg="white")
    thumb_right.pack(expand=true)
    frame_rightbg.propagate(0)
    label_rightimage = t.Label(frame_rightimage, text="? x ?")
    label_rightimage.pack()
    btn_rightimage = t.Button(frame_rightimage, text="이미지 불러오기", command=loadimage2)
    btn_rightimage.pack(padx=10, pady=10)

    # 옵션 프레임
    frame_option = t.LabelFrame(mainframe, text="옵션")
    frame_option.pack(fill='x', padx=10, pady=0)

    # 색상 옵션
    frame_bgcolor = t.LabelFrame(frame_option, text="색상 지정", padx=5, pady=5)
    frame_bgcolor.pack(side='left', padx=5, pady=5)
    t.Label(frame_bgcolor, text="배경 1", width=7).grid(row=0, column=0)
    t.Label(frame_bgcolor, text="배경 2", width=7).grid(row=0, column=1)
    t.Label(frame_bgcolor, text="여백 1", width=7).grid(row=2, column=0)
    t.Label(frame_bgcolor, text="여백 2", width=7).grid(row=2, column=1)
    btn_leftbgcolor = t.Button(frame_bgcolor, width=5, height=1, command=com_leftbgcolor, bg='black')
    btn_leftbgcolor.grid(row=1, column=0)
    btn_rightbgcolor = t.Button(frame_bgcolor, width=5, height=1, command=com_rightbgcolor, bg='white')
    btn_rightbgcolor.grid(row=1, column=1)
    btn_leftvoidcolor = t.Button(frame_bgcolor, width=5, height=1, command=com_leftvoidcolor, bg='black')
    btn_leftvoidcolor.grid(row=3, column=0)
    btn_rightvoidcolor = t.Button(frame_bgcolor, width=5, height=1, command=com_rightvoidcolor, bg='white')
    btn_rightvoidcolor.grid(row=3, column=1)

    # 색상 확장 옵션
    frame_colorextend = t.LabelFrame(frame_option, text="색상 확장")
    frame_colorextend.pack(side='left', padx=5, pady=5, ipadx=20, fill='y')
    var0 = t.IntVar()
    btn_cxfalse = t.Radiobutton(frame_colorextend, value=0, variable=var0, text="원본 사용")
    btn_cxtrue = t.Radiobutton(frame_colorextend, value=1, variable=var0, text="색상 확장")
    btn_cxfalse.pack(side="top", pady=10)
    btn_cxtrue.pack(side="top", pady=10)
    btn_cxfalse.select()

    # 명도 영역 지정 옵션
    frame_brdiv = t.LabelFrame(frame_option, text="색상 영역 분할 방식")
    frame_brdiv.pack(side='left', padx=5, pady=5, ipadx=20, fill='y')
    var1 = t.IntVar()
    btn_radio1 = t.Radiobutton(frame_brdiv, value=0, variable=var1, text="1:1")
    btn_radio2 = t.Radiobutton(frame_brdiv, value=1, variable=var1, text="이미지 색상 비례")
    btn_radio1.pack(side="top", pady=10)
    btn_radio2.pack(side="top", pady=10)
    btn_radio1.select()

    # QR코드 위치 지정
    frame_qr = t.LabelFrame(frame_option, text="QR코드 위치")
    frame_qr.pack(side='left', padx=5, pady=5, fill='y')
    var2 = t.IntVar()
    direction = "↖↗↙↘"
    btn_qr = [t.Radiobutton(frame_qr, value=i, variable=var2, text=direction[i]) for i in range(4)]
    for _ in range(4):
        btn_qr[_].grid(row=_ // 2, column=_ % 2, padx=10, pady=10)
    btn_qr[3].select()

    # 하단 영역
    frame_bottom = t.Frame(mainframe)
    frame_bottom.pack(padx=10, pady=10, fill='x')
    btn_save = t.Button(frame_bottom, text="이미지 저장", command=com_generate)
    btn_save.pack(side="right")

    # mainframe.config(padx=5, pady=5)
    mainframe.mainloop()
