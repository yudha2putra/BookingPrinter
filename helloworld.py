import tkinter
from tkinter import messagebox, RIGHT
from escpos.printer import Usb
import tkinter.ttk
import json
import pyautogui
import urllib.request
from PIL import Image, ImageTk

# ========== Configurations ====================

p = Usb(0x0483, 0x5840, 0, 0x81, 0x03)

BUTTON_BACKGROUND = "white"
MAIN_FRAME_BACKGROUND = "cornflowerblue"
BUTTON_LOOK = "flat"  # flat, groove, raised, ridge, solid, or sunken
TOP_BAR_TITLE = "Python Virtual KeyBoard."
TOPBAR_BACKGROUND = "skyblue"
TRANSPARENCY = 0.7
FONT_COLOR = "black"
LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Helvetica", 10)
SMALL_FONT = ("Helvetica", 8)

# ==============================================

keys = [
    [
        # =========================================
        # ===== Keyboard Configurations ===========
        # =========================================

        [
            "Character_Keys",
            ({'side': 'top', 'expand': 'yes', 'fill': 'both'}),
            [
                ('~', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '_', '+', 'backspace'),
                ('tab', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '{', '}', ";", '\''),
                ('caps lock', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ':', "\"", "enter"),
                ("shift", 'z', 'x', 'c', 'v', 'b', 'n', 'm', '<', '>', '?', "shift"),
                ("ctrl", "win", 'alt', 'space  ', 'alt', 'win', '[=]', 'ctrl')
            ]
        ]
    ],
]


# Create key event
def create_keyboard_event():
    return


def button_command(event):
    pyautogui.press(event)
    return

global img


class Keyboard(tkinter.Frame):
    """Class for making virtual keyboard"""

    def __init__(self, *args, **kwargs):
        tkinter.Frame.__init__(self, *args, **kwargs)

        # Function For Creating Buttons
        self.create_frames_and_buttons()

    # Function For Extracting Data From KeyBoard Table
    # and then provide us a well looking
    # keyboard gui
    def create_frames_and_buttons(self):
        # take section one by one
        for key_section in keys:
            # create Separate Frame For Every Section
            store_section = tkinter.Frame(self)
            store_section.pack(side='left', expand='yes', fill='both', padx=10, pady=10, ipadx=10, ipady=10)

            for layer_name, layer_properties, layer_keys in key_section:
                store_layer = tkinter.LabelFrame(store_section)  # , text=layer_name)
                # store_layer.pack(side='top',expand='yes',fill='both')
                store_layer.pack(layer_properties)
                for key_bunch in layer_keys:
                    store_key_frame = tkinter.Frame(store_layer)
                    store_key_frame.pack(side='top', expand='yes', fill='both')
                    for k in key_bunch:
                        k = k.capitalize()
                        if len(k) <= 3:
                            store_button = tkinter.Button(store_key_frame, text=k, width=8, height=4)
                        else:
                            store_button = tkinter.Button(store_key_frame, text=k.center(5, ' '), height=3)
                        if " " in k:
                            store_button['state'] = 'disable'

                        store_button['relief'] = BUTTON_LOOK
                        store_button['bg'] = BUTTON_BACKGROUND
                        store_button['fg'] = FONT_COLOR

                        store_button['command'] = lambda q=k.lower(): button_command(q)
                        store_button.pack(side='left', fill='both', expand='yes')
        return


class SampleApp(tkinter.Tk):
    def __init__(self):
        tkinter.Tk.__init__(self)
        self.attributes("-fullscreen", True)
        self._frame = None
        self.switch_frame(PageOne)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()


class PageOne(tkinter.Frame):  # parent

    def __init__(self, parent):
        tkinter.Frame.__init__(self, parent)
        load = Image.open("images/MountableHome.png")
        render = ImageTk.PhotoImage(load)

        # labels can be text or images
        img = tkinter.Label(self, image=render)
        img.image = render
        img.pack()

        k = Keyboard(self, bg="white")
        k.pack(side='bottom')

        bt = tkinter.Button(self, text="Cari / Search", font=("Arial Bold", 20), bg='#2d4052', fg='white',
                            command=lambda: self.update(parent))
        bt.pack(side='bottom', pady=20)

        global txt
        inputtxt = tkinter.StringVar()
        txt = tkinter.Entry(self, width=40, font=("Arial Bold", 30), justify="center", textvariable=inputtxt)
        txt.focus_set()
        txt.pack(side='right', padx=50, pady=5)

        l1 = tkinter.Label(self, text="Kode Booking / Pembayaran", font=("Arial Bold", 20))
        l1.config(anchor="center")
        l1.pack(side='right')



    def toggle_fullscreen(self):
        self.state = not self.state  # Just toggling the boolean
        self.root.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self):
        self.state = False
        self.root.attributes("-fullscreen", False)
        return "break"

    def update(self, parent):
        print('The value stored in StartPage txt = %s' % txt.get())
        url = 'https://dashboard.mountable.id/api/Data/anggotaKelompokPendaki?id=%s' % txt.get()
        webURL = urllib.request.urlopen(url)
        data = webURL.read()
        encoding = webURL.info().get_content_charset('utf-8')
        global JSON_object
        JSON_object = json.loads(data.decode(encoding))
        print(JSON_object)
        for distro in JSON_object:
            print(distro['nama'])
            print(distro['jenis_kelamin'])
            print(distro['alamat'])
        if not JSON_object:
            messagebox.showinfo("Warning", "Data yang anda masukkan salah. Periksa kembali")
        else:
            parent.switch_frame(PageTwo)


class Test(object):
    def __init__(self, data):
        self.__dict__ = json.loads(data)


class PageTwo(tkinter.Frame):  # child
    def __init__(self, parent):
        self.parent = parent
        tkinter.Frame.__init__(self, parent)

        load = Image.open("images/MountableHome.png")
        render = ImageTk.PhotoImage(load)

        # labels can be text or images
        img = tkinter.Label(self, image=render)
        img.image = render
        img.pack()

        label = tkinter.Label(self, text='Kode Booking', font=LARGE_FONT)
        label.pack(pady=10, padx=10)  # center alignment
        l2 = tkinter.Label(self, text=txt.get(), font=("Arial Bold", 30))
        l2.config(anchor="center")
        l2.pack()

        self.dataGrid()

        button_printer = tkinter.Button(self, text="Print", font=("Arial Bold", 30),
                                        command=lambda : self.printer())
        button_printer.config(anchor="center")
        button_printer.pack(side=RIGHT, padx=300, pady=5)
        button_kembali = tkinter.Button(self, text="Kembali", font=("Arial Bold", 30),
                                        command=lambda: parent.switch_frame(PageOne))
        button_kembali.config(anchor="center")
        button_kembali.pack(side=RIGHT)


    def dataGrid(self):
        self.tree = tkinter.ttk.Treeview(self, columns=("Nama", "Jenis Kelamin", "Alamat"), show="headings", height=len(JSON_object))
        self.tree.pack(side='top')

        self.style = tkinter.ttk.Style()
        self.style.configure("Treeview.Heading", font=("Arial Bold", 20))
        self.style.configure("Treeview", font=("Arial", 20))
        self.style.configure("Treeview", rowheight=40)

        self.tree.heading('Nama', text="Nama")
        self.tree.heading('Jenis Kelamin', text="Jenis Kelamin")
        self.tree.heading('Alamat', text="Alamat")

        self.tree.column('Nama', width=400)
        self.tree.column('Jenis Kelamin', width=400)
        self.tree.column('Alamat', width=400)

        for val in JSON_object:
            self.tree.insert('', 'end', values=(val['nama'], val['jenis_kelamin'], val['alamat']))

    def printer(self):
        """ Seiko Epson Corp. Receipt Printer (EPSON TM-T88III) """
        for val in JSON_object:
            p.set(align='center')
            p.qr(123456789, size=5)
            p.image("mountable.png")
            p.text("\nTiket Pendakian\n")
            p.text("Gunung Gede Pangrango\n")
            p.set(align='left')
            p.text("\n\nNama Pendaki :\n")
            p.set(align='right')
            if(val['jenis_kelamin']=="Laki"):
                p.text("Sdr " + val['nama'] +"\n\n")
            else:
                p.text("Sdri " + val['nama'] + "\n\n")
            p.set(align='left')
            p.text("Asal Pendaki :\n")
            p.set(align='right')
            p.text(val['alamat'] + "\n\n")
            p.set(align='left')
            p.text("Pendakian Keberangkatan :\n")
            p.set(align='right')
            p.text("Cibodas - 15/12/2019\n\n")
            p.set(align='left')
            p.text("Pendakian Kepulangan :\n")
            p.set(align='right')
            p.text("Sukabumi - 17/12/2019\n\n")
            p.set(align='center')
            p.text("-----------------------------\n\n")
            p.text("Mohon untuk menyimpan tiket ini dengan baik dan melakukan scan\n")
            p.text("ketika telah menyelesaikan\n")
            p.text("pendakian\n\n")
            p.set(text_type='b', align='center')
            p.text("Terimakasih dan hati-hati di\n")
            p.text("perjalanan\n")
            p.cut()


if __name__ == '__main__':
    myGUI = SampleApp()
    myGUI.mainloop()
