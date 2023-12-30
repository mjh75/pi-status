#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk
import psutil
import StatsDisplay


class App(tk.Frame):
    def __init__(self, master, width=800, height=480, disks=['/']):
        super().__init__(master)
        self.window = master
        self.width = width
        self.height = height
        self.window.geometry(f"{self.width}x{self.height}")
        style = ttk.Style()
        style.configure("okay.TFrame", foreground="white", background="black")
        style.configure("warn.TFrame", foreground="white", background="yellow")
        style.configure("crit.TFrame", foreground="white", background="red")
        style.configure("okay.TLabel", foreground="white", background="black")
        style.configure("warn.TLabel", foreground="white", background="yellow")
        style.configure("crit.TLabel", foreground="white", background="red")
        self.time_var = tk.StringVar()
        self.create_time_frame()
        self.cpu_var = tk.StringVar()
        self.create_cpu_frame()
        self.temp_var = tk.StringVar()
        self.create_temperature_frame()
        self.battery_var = tk.StringVar()
        self.create_battery_frame()
        self.disk_var = []
        self.create_disk_frame(disks)
        self.stats = StatsDisplay.StatsDisplay()
        for disk in disks:
            self.stats.add_disk(disk)

        self.update_second()
        self.update_15()

    def create_time_frame(self):
        # Time Frame
        frame = ttk.Frame(self.window,
                          name='timeFrame',
                          height=self.height/3,
                          width=self.width,
                          style='okay.TFrame')
        frame.grid(row=0, column=0, columnspan=3)
        frame.grid_propagate(False)

        label = ttk.Label(frame,
                          name='timeLabel',
                          style='okay.TLabel',
                          textvariable=self.time_var,
                          font=("Arial", 35))
        label.place(x=self.width/2, y=self.height/6, anchor="center")

    def create_cpu_frame(self):
        # CPU Load
        frame = ttk.Frame(self.window,
                          name='cpuFrame',
                          height=self.height/3,
                          width=self.width/3,
                          style="ok.TFrame")
        frame.grid(row=1, column=0)

        label = ttk.Label(frame,
                          name='cpuLabel',
                          textvariable=self.cpu_var,
                          font=("Arial", 40))
        label.place(x=self.width/6, y=self.height/6, anchor="center")

    def create_temperature_frame(self):
        frame = ttk.Frame(self.window,
                          name='temperatureFrame',
                          height=self.height/3,
                          width=self.width/3,
                          style="ok.TFrame")
        frame.grid(row=1, column=1)

        label = ttk.Label(frame,
                          name='temperatureLabel',
                          textvariable=self.temp_var,
                          font=("Arial", 40))
        label.place(x=self.width/6, y=self.height/6, anchor="center")

    def create_battery_frame(self):
        frame = ttk.Frame(self.window,
                          name='batteryFrame',
                          height=self.height/3,
                          width=self.width/3,
                          style="ok.TFrame")
        frame.grid(row=1, column=2)
        label = ttk.Label(frame,
                          name='batteryLabel',
                          textvariable=self.battery_var,
                          font=("Arial", 40))
        label.place(x=self.width/6, y=self.height/6, anchor="center")

    def create_disk_frame(self, disks):
        # Time Frame
        frame = ttk.Frame(self.window,
                          name='diskFrame',
                          height=self.height/3,
                          width=self.width,
                          style='okay.TFrame')
        frame.grid(row=2, column=0, columnspan=3)
        frame.grid_propagate(False)

        y = 0
        label_width = 0
        bar_width = self.width
        for idx, disk in enumerate(disks):
            y = y + 20
            self.disk_var.append(tk.StringVar())
            label = ttk.Label(frame,
                              text=disk,
                              style='okay.TLabel',)
            label.place(x=10, y=y)
            self.window.update()
            if label.winfo_width() > label_width:
                label_width = label.winfo_width()
                bar_width = self.width - 30 - label_width

        y = 0
        for idx, disk in enumerate(disks):
            y = y + 20
            progress_bar = ttk.Progressbar(frame,
                                  name=f"disk-{idx}",
                                  mode='determinate',
                                  variable=self.disk_var[idx],
                                  length=bar_width)
            progress_bar.place(x=label_width + 20, y=y)

    def update_second(self):
        self.time_var.set(self.stats.get_time())
        self.window.after(1000, self.update_second)

    def update_15(self):
        cpu = self.stats.get_cpu()
        if cpu <= 60:
            style = "okay"
        elif cpu <= 75:
            style = "warn"
        else:
            style = "crit"
        self.window.nametowidget('.cpuFrame').configure(style=f"{style}.TFrame")
        self.window.nametowidget('.cpuFrame.cpuLabel').configure(style=f"{style}.TLabel")
        self.cpu_var.set(f"{cpu}%")

        temperature = self.stats.get_temp()
        if temperature <= 30:
            style = "okay"
        elif temperature <= 45:
            style = "warn"
        else:
            style = "crit"
        self.window.nametowidget('.temperatureFrame').configure(style=f"{style}.TFrame")
        (self.window.nametowidget('.temperatureFrame.temperatureLabel')
         .configure(style=f"{style}.TLabel"))
        self.temp_var.set(f"{temperature:.2f}ºC")

        battery = self.stats.get_battery()
        if battery >= 50:
            style = "okay"
        elif battery >= 25:
            style = "warn"
        else:
            style = "crit"
        self.window.nametowidget('.batteryFrame').configure(style=f"{style}.TFrame")
        self.window.nametowidget('.batteryFrame.batteryLabel').configure(style=f"{style}.TLabel")
        self.battery_var.set(f"{battery:3d}%")

        disks = self.stats.get_disk()
        for idx, disk in enumerate(disks):
            self.disk_var[idx].set(disk['used'])
        self.window.after(15000, self.update_15)


def main():
    root = tk.Tk()
    disks = []
    disk_partitions = psutil.disk_partitions(True)
    for disk in disk_partitions:
        if 'ext4' in disk.fstype or 'nfs' in disk.fstype:
            disks.append(disk.mountpoint)
    myapp = App(root, disks=disks)
    myapp.mainloop()


if __name__ == "__main__":
    main()
