import tkinter as tk
from tkinter import messagebox, Toplevel, Text, Scrollbar
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Fuzzy değişkenler
blink_rate = ctrl.Antecedent(np.arange(0.1, 1.1, 0.1), 'blink_rate')
steering_freq = ctrl.Antecedent(np.arange(0, 51, 1), 'steering_freq')
drive_time = ctrl.Antecedent(np.arange(0, 301, 10), 'drive_time')
temp = ctrl.Antecedent(np.arange(10, 41, 1), 'temp')
music_volume = ctrl.Antecedent(np.arange(0, 101, 5), 'music_volume')
alert_level = ctrl.Consequent(np.arange(0, 101, 1), 'alert_level')
break_suggestion = ctrl.Consequent(np.arange(0, 2, 1), 'break_suggestion')

# Üyelik fonksiyonları
blink_rate['low'] = fuzz.trimf(blink_rate.universe, [0.1, 0.1, 0.4])
blink_rate['normal'] = fuzz.trimf(blink_rate.universe, [0.3, 0.5, 0.7])
blink_rate['high'] = fuzz.trimf(blink_rate.universe, [0.6, 1.0, 1.0])

steering_freq['low'] = fuzz.trimf(steering_freq.universe, [0, 0, 20])
steering_freq['normal'] = fuzz.trimf(steering_freq.universe, [15, 25, 35])
steering_freq['high'] = fuzz.trimf(steering_freq.universe, [30, 50, 50])

# Daha yumuşak ve overlaplı sürüş süresi üyelik fonksiyonları
drive_time['short'] = fuzz.trimf(drive_time.universe, [0, 0, 120])
drive_time['medium'] = fuzz.trimf(drive_time.universe, [100, 150, 220])
drive_time['long'] = fuzz.trimf(drive_time.universe, [200, 300, 300])

temp['cold'] = fuzz.trimf(temp.universe, [10, 10, 20])
temp['comfortable'] = fuzz.trimf(temp.universe, [18, 23, 28])
temp['hot'] = fuzz.trimf(temp.universe, [26, 40, 40])

music_volume['low'] = fuzz.trimf(music_volume.universe, [0, 0, 30])
music_volume['medium'] = fuzz.trimf(music_volume.universe, [25, 50, 75])
music_volume['high'] = fuzz.trimf(music_volume.universe, [70, 100, 100])

alert_level['low'] = fuzz.trimf(alert_level.universe, [0, 0, 40])
alert_level['medium'] = fuzz.trimf(alert_level.universe, [30, 50, 70])
alert_level['high'] = fuzz.trimf(alert_level.universe, [60, 100, 100])

break_suggestion['no'] = fuzz.trimf(break_suggestion.universe, [0, 0, 1])
break_suggestion['yes'] = fuzz.trimf(break_suggestion.universe, [0, 1, 1])

# Kurallar - tüm sürüş sürelerini kapsayacak şekilde genişletildi
rules = [
    ctrl.Rule(blink_rate['high'] & steering_freq['low'] & drive_time['long'], alert_level['high']),
    ctrl.Rule(blink_rate['high'] & steering_freq['low'] & drive_time['long'], break_suggestion['yes']),
    
    ctrl.Rule(blink_rate['normal'] & steering_freq['normal'] & drive_time['medium'], alert_level['medium']),
    ctrl.Rule(blink_rate['normal'] & steering_freq['normal'] & drive_time['medium'], break_suggestion['no']),
    
    ctrl.Rule(blink_rate['low'] & steering_freq['high'] & drive_time['short'], alert_level['low']),
    ctrl.Rule(blink_rate['low'] & steering_freq['high'] & drive_time['short'], break_suggestion['no']),
    
    ctrl.Rule(temp['hot'] & drive_time['long'], alert_level['high']),
    ctrl.Rule(temp['hot'] & drive_time['long'], break_suggestion['yes']),
    
    ctrl.Rule(music_volume['low'] & blink_rate['high'], alert_level['high']),
    ctrl.Rule(music_volume['low'] & blink_rate['high'], break_suggestion['yes']),
    
    ctrl.Rule(music_volume['high'] & blink_rate['low'], alert_level['low']),
    ctrl.Rule(music_volume['high'] & blink_rate['low'], break_suggestion['no']),
    
    # Yeni eklenen sürüş süresi odaklı kurallar:
    ctrl.Rule(drive_time['short'], alert_level['low']),
    ctrl.Rule(drive_time['medium'], alert_level['medium']),
    ctrl.Rule(drive_time['long'], alert_level['high']),
    
    ctrl.Rule(drive_time['short'], break_suggestion['no']),
    ctrl.Rule(drive_time['medium'], break_suggestion['no']),
    ctrl.Rule(drive_time['long'], break_suggestion['yes']),
]

system = ctrl.ControlSystem(rules)

# Arayüz başlat
pencere = tk.Tk()
pencere.title("Araç Yorgunluk Tespit Sistemi")
pencere.configure(bg="#1e1e2f")

label_fg = "#ffffff"
button_bg = "#3f51b5"
button_fg = "#ffffff"
button_active_bg = "#5c6bc0"
font_label = ("Arial", 11, "bold")
font_button = ("Arial", 11, "bold")

def create_label(text, row):
    label = tk.Label(pencere, text=text, bg=pencere['bg'], fg=label_fg, font=font_label)
    label.grid(row=row, column=0, padx=10, pady=6, sticky="e")

def create_scale(row, from_, to_, resolution=1, orient=tk.HORIZONTAL):
    scale = tk.Scale(pencere, from_=from_, to=to_, resolution=resolution,
                     orient=orient, length=200, bg="#2e2e3f", fg="#ffffff", highlightbackground="#2e2e3f")
    scale.grid(row=row, column=1, padx=10, pady=6, sticky="w")
    return scale

create_label("Göz Kırpma Hızı (0.1 - 1.0 Hz):", 0)
scale_blink = create_scale(0, 0.1, 1.0, 0.1)

create_label("Direksiyon Hareketi (0 - 50 /dk):", 1)
scale_steering = create_scale(1, 0, 50)

create_label("Sürüş Süresi (0 - 300 dk):", 2)
scale_drive = create_scale(2, 0, 300)

create_label("Araç İçi Sıcaklık (10°C - 40°C):", 3)
scale_temp = create_scale(3, 10, 40)

create_label("Müzik Seviyesi (0 - 100):", 4)
scale_music = create_scale(4, 0, 100)

def hesapla():
    try:
        fuzzy_sim = ctrl.ControlSystemSimulation(system, clip_to_bounds=True)

        fuzzy_sim.input['blink_rate'] = scale_blink.get()
        fuzzy_sim.input['steering_freq'] = scale_steering.get()
        fuzzy_sim.input['drive_time'] = scale_drive.get()
        fuzzy_sim.input['temp'] = scale_temp.get()
        fuzzy_sim.input['music_volume'] = scale_music.get()

        fuzzy_sim.compute()

        sonuc = f"Uyarı Düzeyi: %{fuzzy_sim.output['alert_level']:.2f}\n"
        sonuc += f"Mola Önerisi: {'EVET' if fuzzy_sim.output['break_suggestion'] > 0.5 else 'HAYIR'}"
        messagebox.showinfo("Sonuç", sonuc)

    except Exception as e:
        messagebox.showerror("Hata", f"Bir hata oluştu: {str(e)}")

def grafik_goster():
    grafik_pencere = Toplevel(pencere)
    grafik_pencere.title("Üyelik Fonksiyonları")

    fig, axs = plt.subplots(3, 3, figsize=(14, 10))
    axs = axs.flatten()

    variables = [
        (blink_rate, "Göz Kırpma Hızı (Hz)"),
        (steering_freq, "Direksiyon Hareketi (/dk)"),
        (drive_time, "Sürüş Süresi (dk)"),
        (temp, "Araç İçi Sıcaklık (°C)"),
        (music_volume, "Müzik Seviyesi"),
        (alert_level, "Uyarı Düzeyi"),
        (break_suggestion, "Mola Önerisi")
    ]

    for i, (var, title) in enumerate(variables):
        ax = axs[i]
        for term_name, mf in var.terms.items():
            ax.plot(var.universe, mf.mf, label=term_name)
        ax.set_title(title)
        ax.set_xlabel("Değerler")
        ax.set_ylabel("Üyelik")
        ax.legend()
        ax.grid(True)

    for j in range(len(variables), len(axs)):
        fig.delaxes(axs[j])

    plt.tight_layout()
    canvas = FigureCanvasTkAgg(fig, master=grafik_pencere)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def kurallar_goster():
    pencere_kurallar = Toplevel(pencere)
    pencere_kurallar.title("Kural Tablosu")
    metin = Text(pencere_kurallar, wrap='word', width=80, height=20)
    metin.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar = Scrollbar(pencere_kurallar, command=metin.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    metin.config(yscrollcommand=scrollbar.set)

    for i, rule in enumerate(rules):
        metin.insert(tk.END, f"Kural {i + 1}: {rule}\n\n")

def create_button(text, command, row):
    btn = tk.Button(pencere, text=text, command=command, bg=button_bg, fg=button_fg,
                    activebackground=button_active_bg, font=font_button, relief="raised", bd=3)
    btn.grid(row=row, column=0, columnspan=2, pady=8, padx=20, ipadx=10, ipady=4, sticky="we")

create_button("Hesapla", hesapla, 5)
create_button("Grafikleri Göster", grafik_goster, 6)
create_button("Kuralları Göster", kurallar_goster, 7)

pencere.mainloop()