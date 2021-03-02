from tkinter import filedialog
from PIL import Image
from tkinter import colorchooser
import tkinter as t
import cv2 as i
import numpy as np

true = True
false = False


def com_leftcolor():
    color_code = colorchooser.askcolor(title="Choose color")
    print(color_code)
    btn_leftcolorpick.config(bg=color_code[1])


def com_rightcolor():
    color_code = colorchooser.askcolor(title="Choose color")
    print(color_code)
    btn_rightcolorpick.config(bg=color_code[1])


if __name__ == '__main__':
    mainframe = t.Tk()
    # mainframe.geometry("640x480")
    mainframe.resizable(false, false)

    # 이미지 프레임
    frame_image = t.LabelFrame(mainframe, text="이미지")
    frame_image.pack(padx=10, pady=10)

    # 프레임 3등분
    frame_leftimage = t.LabelFrame(frame_image, text="검은배경 이미지", width=100, height=100)
    frame_leftimage.pack(side="left", padx=10, pady=10)
    frame_switch = t.Frame(frame_image)
    frame_switch.pack(side="left")
    frame_rightimage = t.LabelFrame(frame_image, text="흰배경 이미지")
    frame_rightimage.pack(side="left", padx=10, pady=10)

    # 왼쪽 프레임
    frame_leftbg = t.Frame(frame_leftimage, width=210, height=210, bg="black")
    frame_leftbg.pack(padx=10, pady=10)
    label_leftimage = t.Label(frame_leftimage, text="? x ?")
    label_leftimage.pack()
    btn_leftimage = t.Button(frame_leftimage, text="이미지 불러오기")
    btn_leftimage.pack(padx=10, pady=10)

    # 가운데 프레임
    btn_switch = t.Button(frame_switch, text="이미지 바꾸기")
    btn_switch.pack(padx=10)

    # 오른쪽 프레임
    frame_rightbg = t.Frame(frame_rightimage, width=210, height=210, bg="white")
    frame_rightbg.pack(padx=10, pady=10)
    label_rightimage = t.Label(frame_rightimage, text="? x ?")
    label_rightimage.pack()
    btn_rightimage = t.Button(frame_rightimage, text="이미지 불러오기")
    btn_rightimage.pack(padx=10, pady=10)

    # 옵션 프레임
    frame_option = t.LabelFrame(mainframe, text="옵션")
    frame_option.pack(fill='x', padx=10, pady=10)

    # 여백 배경 색상 옵션
    frame_bgcolor = t.LabelFrame(frame_option, text="여백 색상", padx=5, pady=5)
    frame_bgcolor.pack(side="left", padx=5, pady=5)
    t.Label(frame_bgcolor, text="검은배경 이미지", width=16).grid(row=0, column=0)
    t.Label(frame_bgcolor, text="흰배경 이미지", width=16).grid(row=0, column=1)
    btn_leftcolorpick = t.Button(frame_bgcolor, width=5, height=1, command=com_leftcolor, bg='black')
    btn_leftcolorpick.grid(row=1, column=0)
    btn_rightcolorpick = t.Button(frame_bgcolor, width=5, height=1, command=com_rightcolor, bg='white')
    btn_rightcolorpick.grid(row=1, column=1)

    # 명도 영역 지정 옵션
    frame_brdiv = t.LabelFrame(frame_option, text="명도 영역 지정 방식", padx=5, pady=5)
    frame_brdiv.pack(side="left", padx=5, pady=5, fill='y')
    var1 = t.IntVar()
    btn_radio1 = t.Radiobutton(frame_brdiv, value=0, variable=var1, text="2분할")
    btn_radio2 = t.Radiobutton(frame_brdiv, value=1, variable=var1, text="색상 영역 확장")
    btn_radio1.pack(side="left")
    btn_radio2.pack(side="left")
    btn_radio1.select()

    # mainframe.config(padx=5, pady=5)
    mainframe.mainloop()
