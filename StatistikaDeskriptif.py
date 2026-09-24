import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display, HTML

plt.style.use("dark_background")
warna = ["#00e5ff", "#7c4dff", "#ff2bd6", "#b6ff3b", "#ffb300", "#ff5252"]


# Tabel
def buat_tabel(df, warna_header, judul):
    return df.style.set_caption(judul).set_table_styles([
        {'selector': '', 'props': [('width', '100%'), ('border-collapse', 'collapse')]},
        {'selector': 'caption', 'props': [('color', warna_header), ('font-size', '16px'),
                                          ('font-weight', 'bold'), ('text-align', 'left'),
                                          ('padding-bottom', '6px')]},
        {'selector': 'thead th', 'props': [('background-color', warna_header), ('color', 'black'),
                                           ('text-align', 'center'), ('position', 'sticky'),
                                           ('top', '0')]},
        {'selector': 'tbody td', 'props': [('background-color', '#111827'), ('color', 'white'),
                                           ('border', '1px solid #333'), ('text-align', 'center')]},
        {'selector': 'tbody th', 'props': [('background-color', '#1f2937'), ('color', warna_header)]},
        {'selector': 'tbody tr:nth-child(even) td', 'props': [('background-color', '#1f2937')]},
    ])

dataraw = pd.read_excel("DataScore.xlsx")

# Tabel frekuensi
datafrq = pd.crosstab(index=dataraw["Grade"], columns="Frekuensi")

# Statistika deskriptif
dataraw["Final Score"] = pd.to_numeric(dataraw["Final Score"], errors="coerce")
dt = dataraw["Final Score"]

stats = dt.describe()
stats["Standard Error"] = dt.sem()
stats["Median"] = dt.median()
stats["Mode"] = dt.mode().iloc[0]
stats["variance"] = dt.var()
stats["range"] = dt.max() - dt.min()
stats["skewness"] = dt.skew()
stats["kurtosis"] = dt.kurtosis()

df_stats = stats.to_frame(name="Nilai")
df_stats.index.name = "Indikator Statistik"

tabel_data = buat_tabel(dataraw, warna[0], "Tabel Data Score").to_html()
tabel_frek = buat_tabel(datafrq, warna[3], "Tabel Frekuensi Grade").to_html()
tabel_stat = buat_tabel(df_stats, warna[2], "Statistika Final Score").format("{:.2f}").to_html()

display(HTML(f"""
<div style="background:#0b0f1a; padding:20px; border-radius:12px;
            font-family:'Segoe UI', sans-serif;">
    <h2 style="color:{warna[0]}; margin:0 0 16px 0; letter-spacing:2px;">
        ◈ DASHBOARD ANALISIS SCORE
    </h2>
    <div style="display:flex; gap:24px; align-items:flex-start;">
        <div style="flex:2; max-height:560px; overflow-y:auto;">{tabel_data}</div>
        <div style="flex:1;">
            {tabel_frek}
            <div style="height:24px;"></div>
            {tabel_stat}
        </div>
    </div>
</div>
"""))


fig, axes = plt.subplots(1, 3, figsize=(18, 5))
fig.suptitle("Analisis Grade", fontsize=20, fontweight="bold", color=warna[0])

# Grafik garis
sns.lineplot(data=datafrq, x=datafrq.index, y="Frekuensi", ax=axes[0],
             marker="o", markersize=9, linewidth=3, color=warna[0])
axes[0].set_title("Grafik Garis: Trend Grade", fontweight="bold", pad=10)
axes[0].grid(alpha=0.2)

# Grafik batang
sns.barplot(x=datafrq.index, y=datafrq["Frekuensi"], ax=axes[1],
            hue=datafrq.index, palette=sns.color_palette(warna, len(datafrq)), legend=False)
axes[1].set_title("Grafik Batang: Frekuensi Grade", fontweight="bold", pad=10)
axes[1].grid(alpha=0.2)
for container in axes[1].containers:
    axes[1].bar_label(container, padding=3)

# Pie chart 
axes[2].pie(datafrq["Frekuensi"], labels=datafrq.index, autopct="%1.0f%%",
            colors=warna[:len(datafrq)], startangle=90, pctdistance=0.78,
            wedgeprops={"width": 0.45, "edgecolor": "#0b0f1a", "linewidth": 2})
axes[2].set_title("Pie Chart: Persentase Grade", fontweight="bold", pad=10)

plt.tight_layout(rect=[0, 0, 1, 0.93])
plt.show()