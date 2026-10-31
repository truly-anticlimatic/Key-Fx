# Version 0.2.0
# Author: anticlimatic-xd
# Purpose: Personalize keyboard with sfx

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import config
from config import SPADX, BPADX, PADY
import event_handler


class App:
    """The app itself."""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("KeyFX 0.2.0")
        self.root.geometry("300x300")
        self.tabs = {
            "Volume": tk.Frame(master=self.root),
            "Soundpacks": tk.Frame(master=self.root),
        }
        self.create_toolbar()
        self.root.mainloop()

    def clear_tab(self):
        """Load the requested tab onto the main frame"""
        for tab in self.tabs.values():
            if tab.winfo_ismapped():
                tab.grid_forget()

    def create_volume_tab(self):

        self.clear_tab()

        def set_volume(volume_to_set: int):
            config.volume = int(volume_to_set) / 100  # Helper function to set volume

        curr_vol_lbl = ttk.Label(master=self.tabs["Volume"], text="Current volume:")
        vol_spbox = ttk.Spinbox(
            master=self.tabs["Volume"],
            from_=0,
            to=100,
            wrap=True,
            command=lambda: set_volume(vol_spbox.get()),
        )

        vol_spbox.set(int(config.volume * 100))  # Have a preset ready

        self.tabs["Volume"].grid(row=1, column=0, padx=BPADX, pady=PADY)
        curr_vol_lbl.grid(row=0, column=0, padx=BPADX, pady=PADY)
        vol_spbox.grid(row=1, column=0, padx=BPADX, pady=PADY)  # Place them

        def on_enter(_):
            try:
                get_volume = int(vol_spbox.get())
                if get_volume > 100 or get_volume < 0:
                    pass
                else:
                    set_volume(get_volume)  # Set the volume if volume is within limits

            except ValueError:
                pass

        vol_spbox.bind("<Return>", on_enter)  # Bind it to the spinbox

    def create_soundpack_tab(self):

        self.clear_tab()

        current_category = tk.StringVar(
            master=self.tabs["Soundpacks"]
        )  # Create a stringvar for the category combobox
        category_cbbox = ttk.Combobox(
            master=self.tabs["Soundpacks"],
            state="readonly",
            width=20,
            values=list(config.keyboard_sounds.keys()),
            textvariable=current_category,
        )

        current_soundpack = tk.StringVar(
            master=self.tabs["Soundpacks"]
        )  # Create a stringvar for the soundpack combobox
        soundpack_cbbox = ttk.Combobox(
            master=self.tabs["Soundpacks"],
            state="readonly",
            width=20,
            textvariable=current_soundpack,
        )

        soundpack_confirm_btn = ttk.Button(
            master=self.tabs["Soundpacks"],
            width=9,
            text="Start!",
            command=lambda: event_handler.run(
                current_category.get(), current_soundpack.get()
            ),
        )  # Create a confirm button

        stop_btn = ttk.Button(
            master=self.tabs["Soundpacks"],
            width=9,
            text="Stop",
            command=event_handler.deactivate,
        )  # Create a stop button

        self.tabs["Soundpacks"].grid(column=0, row=2, padx=SPADX, pady=0)

        category_cbbox.grid(column=0, row=1, padx=SPADX, pady=PADY)
        soundpack_cbbox.grid(column=1, row=1, padx=SPADX, pady=PADY)

        soundpack_confirm_btn.grid(column=0, row=2, padx=SPADX, pady=PADY)
        stop_btn.grid(column=1, row=2, padx=SPADX, pady=PADY)  # Place the widgets

        def on_category_select(_):
            if (
                current_category.get() in config.keyboard_sounds
            ):  # If the category is in the keyboard_sounds categories
                soundpack_cbbox["values"] = list(
                    config.keyboard_sounds[current_category.get()].keys()
                )  # Set the values to the category's ones
                soundpack_cbbox.set("")
                soundpack_cbbox.current(0)  # Set the first value

        category_cbbox.bind("<<ComboboxSelected>>", on_category_select)

    def message_user(self):
        messagebox.showinfo(
            "Currently unavailable", "For now, this is is currently unavailable"
        )

    def create_toolbar(self):  # Create the toolbar
        tool_bar_frm = ttk.Frame(master=self.root)  # Create the frame for the toolbar

        select_pack_btn = ttk.Button(
            master=tool_bar_frm,
            command=self.create_soundpack_tab,
            text="Select a sound pack",
            width=19,
        )
        vol_btn = ttk.Button(
            master=tool_bar_frm, command=self.create_volume_tab, text="Volume", width=8
        )
        custom_btn = ttk.Button(
            master=tool_bar_frm,
            command=self.message_user,
            text="Custom packs",
            width=13,
        )  # Creating the buttons for different options

        tool_bar_frm.grid(column=0, row=0, padx=10, pady=PADY)
        vol_btn.grid(row=0, column=0, padx=SPADX, pady=PADY)
        custom_btn.grid(row=0, column=1, padx=SPADX, pady=PADY)
        select_pack_btn.grid(row=0, column=2, padx=SPADX, pady=PADY)  # Place it all


App()
