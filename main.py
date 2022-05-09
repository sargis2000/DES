from tkinter import Tk
from des import DesKey
import tkinter as tk
from abc import ABC
from typing import Callable


class Window(ABC):
    def __init__(self, height: int, weight: int, win_name: str, image_url: str, toplevel=False) -> None:
        if toplevel:
            self.window = tk.Toplevel()
        else:
            self.window = tk.Tk()
        self.window.title(win_name.title())
        self.window.geometry(f'{height}x{weight}')
        self.window.iconphoto(False, tk.PhotoImage(file=image_url))
        self.window.resizable(False, False)

    def get_window(self) -> Tk:
        return self.window


class GUIDes:
    def __init__(self) -> None:
        self.window = Window(height=800, weight=600, win_name='data encription standart',
                             image_url='cyber-security.png').get_window()
        self.key_entry = tk.Entry(self.window)
        self.key_entry.place(x=25, y=5, height=50, width=750)
        self.key_entry.insert(0, " Key ...")
        self.key_entry.bind('<FocusIn>', self.__del_key_event)

        # text entry
        self.text_entry = tk.Text(self.window)
        self.text_entry.place(x=25, y=65, height=480, width=750)
        self.text_entry.insert(1.0, "Enter text ...")
        self.text_entry.bind('<FocusIn>', self.__del_text_event)

        # encrypt button
        self.encrypt_button = tk.Button(self.window, text="Encrypt", command=self.__encrypt)
        self.encrypt_button.place(x=300, y=555)

        # padding buttons
        self.padding = tk.BooleanVar()
        self.radiobuttonTrue = tk.Radiobutton(self.window, text='Padding ON', variable=self.padding, value=True)
        self.radiobuttonFalse = tk.Radiobutton(self.window, text='Padding OFF', variable=self.padding, value=False)
        self.radiobuttonTrue.place(x=500, y=550)
        self.radiobuttonFalse.place(x=500, y=570)

        # decrypt button
        self.decrypt_button = tk.Button(self.window, text="Decrypt", command=self.__decrypt)
        self.decrypt_button.place(x=400, y=555)

        # singleton for events variables
        self.key_event_called = False
        self.text_event_called = False

        self.window.mainloop()

    def __del_key_event(self, event) -> None:
        if not self.key_event_called:
            self.key_entry.delete(0, 'end')
            self.key_event_called = True

    def __del_text_event(self, event) -> None:
        if not self.text_event_called:
            self.text_entry.delete(1.0, 'end')
            self.text_event_called = True

    def __get_widgets(self) -> dict:
        return {'key': self.key_entry.get(), 'text': self.text_entry.get(1.0, 'end').rstrip('\n'),
                'padding': self.padding.get()}

    @staticmethod
    def __close(win: Tk) -> Callable:
        def __wrapper(*args, **kwargs):
            win.destroy()
        return __wrapper

    def __error_window(self, error: Exception) -> None:
        self.err_window = Window(height=650, weight=110, win_name='ERROR', image_url='warning.png',
                                 toplevel=True).get_window()
        self.err_label = tk.Text(self.err_window, height=4, width=80)
        self.err_label.insert(1.0, str(error))
        self.err_label.config(state='disabled')
        self.err_label.place(x=1, y=1)
        # close button
        self.close_button = tk.Button(self.err_window, text='Close', command=self.__close(self.err_window))
        self.close_button.pack(side='bottom')

    def __result_window(self, text: str) -> None:
        self.res_window = Window(height=800, weight=600, win_name='RESULT', image_url='data-encryption.png',
                                 toplevel=True).get_window()
        self.result_text = tk.Text(self.res_window)
        self.result_text.insert(1.0, text)
        self.result_text.place(x=25, y=5, height=550, width=740)
        self.close_button = tk.Button(self.res_window, text='Close', command=self.__close(self.res_window))
        self.close_button.pack(side='bottom')

    def __encrypt(self) -> None:
        self.widgets = self.__get_widgets()
        try:
            self.key = DesKey(self.widgets['key'].encode('latin-1'))
            self.encrypted_text = self.key.encrypt(self.widgets['text'].encode('latin-1'),
                                                   padding=self.widgets['padding'])
            self.__result_window(self.encrypted_text)
        except AssertionError as e:
            self.__error_window(e)

        except UnicodeEncodeError as e:
            self.__error_window(e)

    def __decrypt(self) -> None:
        self.widgets = self.__get_widgets()
        try:
            self.key = DesKey(self.widgets['key'].encode('latin-1'))
            self.decrypted_text = self.key.decrypt(self.widgets['text'].encode('latin-1'),
                                                   padding=self.widgets['padding'])
            self.__result_window(self.decrypted_text)

        except AssertionError as e:
            self.__error_window(e)

        except UnicodeEncodeError as e:
            self.__error_window(e)


GUIDes()
