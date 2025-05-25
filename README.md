# 🛑 Araç Yorgunluk Tespit ve Uyarı Sistemi
Bu proje, sürücü yorgunluğunu tahmin etmek ve mola önerisinde bulunmak için bulanık mantık (fuzzy logic) ve kullanıcı dostu bir arayüz kullanır. Sistem; göz kırpma hızı, direksiyon hareketleri, sürüş süresi, araç içi sıcaklık ve müzik seviyesi gibi parametreleri değerlendirir.

# 🔧 Kullanılan Teknolojiler
- Python
- Tkinter (GUI)
- scikit-fuzzy (bulanık mantık motoru)
- matplotlib (grafik çizimi)

# 📁 Dosya İçeriği
1. Gerekli Kütüphanelerin İmport Edilmesi
```python

import tkinter as tk
from tkinter import messagebox, Toplevel, Text, Scrollbar
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

```

2. Bulanık Değişkenlerin Tanımlanması
Girdi (antecedent) ve çıktı (consequent) değişkenleri oluşturulur:
```python

blink_rate = ctrl.Antecedent(np.arange(0.1, 1.1, 0.1), 'blink_rate')
steering_freq = ctrl.Antecedent(np.arange(0, 51, 1), 'steering_freq')
drive_time = ctrl.Antecedent(np.arange(0, 301, 10), 'drive_time')
temp = ctrl.Antecedent(np.arange(10, 41, 1), 'temp')
music_volume = ctrl.Antecedent(np.arange(0, 101, 5), 'music_volume')

alert_level = ctrl.Consequent(np.arange(0, 101, 1), 'alert_level')
break_suggestion = ctrl.Consequent(np.arange(0, 2, 1), 'break_suggestion')

```

3. Üyelik Fonksiyonlarının Tanımlanması
Her değişken için üyelik (membership) fonksiyonları tanımlanır:
```python

blink_rate['low'] = fuzz.trimf(blink_rate.universe, [0.1, 0.1, 0.4])
blink_rate['normal'] = fuzz.trimf(blink_rate.universe, [0.3, 0.5, 0.7])
blink_rate['high'] = fuzz.trimf(blink_rate.universe, [0.6, 1.0, 1.0])
# Diğer değişkenler için de benzer şekilde...

```
4. Bulanık Kuralların Tanımlanması
Sistem, sürücü durumu hakkında karar vermek için kurallara dayanır:
```python

rules = [
    ctrl.Rule(blink_rate['high'] & steering_freq['low'] & drive_time['long'], alert_level['high']),
    ctrl.Rule(blink_rate['high'] & steering_freq['low'] & drive_time['long'], break_suggestion['yes']),
    # Diğer kurallar...
]

```

5. Kontrol Sistemi Tanımlanması
```python

system = ctrl.ControlSystem(rules)

```

6. Tkinter Arayüzünün Oluşturulması
Ana pencere yapılandırılır:
```python

pencere = tk.Tk()
pencere.title("Araç Yorgunluk Tespit Sistemi")
pencere.configure(bg="#1e1e2f")

```

7. Arayüz Elemanları (Etiketler ve Kaydırma Çubukları)
Kullanıcının veri girmesi için kaydırma çubukları oluşturulur:
```python

def create_label(text, row):
    # Etiket oluşturur
def create_scale(row, from_, to_, resolution=1, orient=tk.HORIZONTAL):
    # Kaydırma çubuğu oluşturur

```

Her parametre için kullanıcı giriş alanları:
```python

create_label("Göz Kırpma Hızı (0.1 - 1.0 Hz):", 0)
scale_blink = create_scale(0, 0.1, 1.0, 0.1)
# Diğer parametreler için aynı şekilde...

```

8. Hesaplama Fonksiyonu
Kullanıcıdan alınan girdilerle sistem çalıştırılır ve sonuç gösterilir:
```python

def hesapla():
    fuzzy_sim = ctrl.ControlSystemSimulation(system, clip_to_bounds=True)
    fuzzy_sim.input['blink_rate'] = scale_blink.get()
    # Diğer girişler
    fuzzy_sim.compute()

    sonuc = f"Uyarı Düzeyi: %{fuzzy_sim.output['alert_level']:.2f}\n"
    sonuc += f"Mola Önerisi: {'EVET' if fuzzy_sim.output['break_suggestion'] > 0.5 else 'HAYIR'}"
    messagebox.showinfo("Sonuç", sonuc)

```

9. Grafik Gösterimi
Üyelik fonksiyonlarını matplotlib ile gösterir:
```python

def grafik_goster():
    grafik_pencere = Toplevel(pencere)
    fig, axs = plt.subplots(3, 3, figsize=(14, 10))
    # Üyelik fonksiyonları çizdirilir

```

10. Kuralların Gösterimi
Kural listesini ayrı bir pencerede metin kutusunda gösterir:
```python

def kurallar_goster():
    pencere_kurallar = Toplevel(pencere)
    metin = Text(pencere_kurallar, wrap='word', width=80, height=20)
    for i, rule in enumerate(rules):
        metin.insert(tk.END, f"Kural {i + 1}: {rule}\n\n")

```

11. Butonların Oluşturulması
Arayüzün altına işlem butonları yerleştirilir:
```python

create_button("Hesapla", hesapla, 5)
create_button("Grafikleri Göster", grafik_goster, 6)
create_button("Kuralları Göster", kurallar_goster, 7)

```

12. Arayüzün Başlatılması
```python

pencere.mainloop()

```


# 📝 Notlar
- ```python scikit-fuzzy ```  kütüphanesi yüklü değilse aşağıdaki komutla yüklenebilir:
```python

pip install scikit-fuzzy

```
- Arayüz sade tutulmuştur ve sezgiseldir. İleri geliştirme olarak kullanıcı verilerini kaydetme, sesli uyarı sistemi veya gerçek zamanlı sensör bağlantısı eklenebilir.
