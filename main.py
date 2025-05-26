import tkinter as tk
from tkinter import ttk, Text, Scrollbar
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

# Kurallar
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
    ctrl.Rule(drive_time['short'], alert_level['low']),
    ctrl.Rule(drive_time['medium'], alert_level['medium']),
    ctrl.Rule(drive_time['long'], alert_level['high']),
    ctrl.Rule(drive_time['short'], break_suggestion['no']),
    ctrl.Rule(drive_time['medium'], break_suggestion['no']),
    ctrl.Rule(drive_time['long'], break_suggestion['yes']),
]

system = ctrl.ControlSystem(rules)

# Ana pencere
pencere = tk.Tk()
pencere.title("Araç Yorgunluk Tespit Sistemi")
pencere.geometry("550x600")
bg_color = "#2d3436"
frame_color = "#636e72"
label_color = "#dfe6e9"
accent_color = "#0984e3"
button_color = "#00b894"
active_button_color = "#55efc4"
text_color = "#2d3436"
slider_bg = "#b2bec3"
slider_fg = "#0984e3"
pencere.configure(bg=bg_color)

style = ttk.Style()
style.theme_use('clam')
style.configure("TScale", background=bg_color, troughcolor=slider_bg, 
                bordercolor=accent_color, lightcolor=accent_color, 
                darkcolor=accent_color, sliderthickness=15)
style.configure("TLabel", background=bg_color, foreground=label_color, 
                font=("Arial", 11, "bold"), padding=5)
style.configure("TButton", background=button_color, foreground=text_color, 
                font=("Arial", 11, "bold"), bordercolor=button_color,
                lightcolor=button_color, darkcolor=button_color, 
                padding=10, focuscolor=active_button_color)
style.map("TButton", background=[('active', active_button_color), ('pressed', active_button_color)])

def create_label(text, row):
    label = ttk.Label(pencere, text=text)
    label.grid(row=row, column=0, padx=10, pady=6, sticky="e")
    return label

def create_scale(row, from_, to_, resolution=1):
    scale = ttk.Scale(pencere, from_=from_, to=to_, length=200, style="TScale")
    scale.grid(row=row, column=1, padx=10, pady=6, sticky="w")
    value_label = ttk.Label(pencere, text=f"{from_}", background=bg_color, 
                            foreground=label_color, font=("Arial", 9))
    value_label.grid(row=row, column=2, padx=5, sticky="w")

    def update_value(val):
        value_label.config(text=f"{float(val):.1f}" if resolution < 1 else f"{int(float(val))}")
    scale.config(command=update_value)
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
        fuzzy_sim.input['blink_rate'] = float(scale_blink.get())
        fuzzy_sim.input['steering_freq'] = float(scale_steering.get())
        fuzzy_sim.input['drive_time'] = float(scale_drive.get())
        fuzzy_sim.input['temp'] = float(scale_temp.get())
        fuzzy_sim.input['music_volume'] = float(scale_music.get())
        fuzzy_sim.compute()
        sonuc = f"\nUyarı Düzeyi: %{fuzzy_sim.output['alert_level']:.2f}\n"
        sonuc += f"Mola Önerisi: {'EVET' if fuzzy_sim.output['break_suggestion'] > 0.5 else 'HAYIR'}\n"
        sonuc_metin.config(state="normal")
        sonuc_metin.delete("1.0", tk.END)
        sonuc_metin.insert(tk.END, sonuc.center(50))
        sonuc_metin.config(state="disabled")
    except Exception as e:
        sonuc_metin.config(state="normal")
        sonuc_metin.delete("1.0", tk.END)
        sonuc_metin.insert(tk.END, f"Hata oluştu: {str(e)}".center(50))
        sonuc_metin.config(state="disabled")

def grafik_goster():
    grafik_pencere = tk.Toplevel(pencere)
    grafik_pencere.title("Üyelik Fonksiyonları")
    grafik_pencere.configure(bg=bg_color)
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
    pencere_kurallar = tk.Toplevel(pencere)
    pencere_kurallar.title("Kural Tablosu")
    pencere_kurallar.configure(bg=bg_color)
    frame = tk.Frame(pencere_kurallar, bg=frame_color)
    frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    metin = Text(frame, wrap='word', width=80, height=20, 
                bg=frame_color, fg=label_color, 
                insertbackground=label_color, font=("Arial", 10))
    metin.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
    scrollbar = ttk.Scrollbar(frame, command=metin.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    metin.config(yscrollcommand=scrollbar.set)
    for i, rule in enumerate(rules):
        metin.insert(tk.END, f"Kural {i + 1}: {rule}\n\n")

# Butonlar
create_button = lambda text, cmd, row: ttk.Button(pencere, text=text, command=cmd, style="TButton").grid(
    row=row, column=0, columnspan=3, pady=4, padx=20, ipadx=8, ipady=4, sticky="we"
)
create_button("Hesapla", hesapla, 5)
create_button("Grafikleri Göster", grafik_goster, 6)
create_button("Kuralları Göster", kurallar_goster, 7)

# Sonuç alanı
sonuc_metin = Text(pencere, height=4, width=50, bg=frame_color, fg=label_color,
                   font=("Arial", 12, "bold"), wrap="word", relief="sunken", bd=2)


sonuc_metin.grid(row=9, column=0, columnspan=3, padx=40, pady=(20, 10), sticky="we")

sonuc_metin.tag_configure("center", justify="center")


sonuc_metin.insert("1.0", "\n\nSonuç burada gösterilecek...")
sonuc_metin.tag_add("center", "1.0", "end")
sonuc_metin.config(state="disabled")

pencere.mainloop()
