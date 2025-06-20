# Der folgende Code ist eine aktualisierte Version von `app.py` mit:
# 1. Vergrößerten Diagrammen (figsize explizit größer und Streamlit-Anzeige optimiert)
# 2. Korrekt gerenderten Latex-Formeln
# 3. Checkboxen für Prozessabschnitte statt Radiobuttons

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Schrift- und Liniengröße explizit setzen
plt.rcParams.update({
    'font.size': 22,
    'axes.titlesize': 26,
    'axes.labelsize': 24,
    'xtick.labelsize': 20,
    'ytick.labelsize': 20,
    'legend.fontsize': 22,
    'lines.linewidth': 4
})

# Wirkungsgrad-Funktionen
def otto_efficiency(r, kappa):
    return 1 - 1 / r**(kappa - 1)

def diesel_efficiency(r, rho, kappa):
    return 1 - (1 / r**(kappa - 1)) * ((rho**kappa - 1) / (kappa * (rho - 1)))

def seliger_efficiency(r, rho, alpha, kappa):
    eta_diesel = diesel_efficiency(r, rho, kappa)
    eta_otto = otto_efficiency(r, kappa)
    return (1 - alpha) * eta_diesel + alpha * eta_otto

colors = {
    "kompression": "blue",
    "isochor": "orange",
    "isobar": "red",
    "expansion": "green",
    "waermeabgabe": "gray"
}

# Prozessplot-Funktion
def plot_processes(r, rho, kappa, alpha, show_komp, show_verbrennung, show_abgabe):
    V1 = 1.0
    V2 = V1 / r
    V3 = V2 * rho
    fig, axs = plt.subplots(1, 3, figsize=(36, 12))

    processes = ['Otto', 'Diesel', 'Seliger']
    for idx, name in enumerate(processes):
        ax = axs[idx]
        ax.set_title(f"{name}-Prozess")
        ax.set_xlabel("Volumen (V)")
        ax.set_ylabel("Druck (p)")
        ax.grid(True)

        if show_komp:
            Vc = np.linspace(V1, V2, 100)
            pc = 1 / Vc**kappa
            ax.plot(Vc, pc, color=colors['kompression'], label="Kompression")
            p1, p2 = pc[0], pc[-1]
        else:
            p1 = p2 = 1 / V1**kappa

        if show_verbrennung:
            if name == 'Otto':
                p_iso = np.linspace(p2, p2 * 3, 20)
                ax.plot(np.ones_like(p_iso)*V2, p_iso, color=colors['isochor'], label="isochore Verbrennung")
                V_exp = np.linspace(V2, V1, 100)
                p_exp = p_iso[-1] * (V2 / V_exp)**kappa
                ax.plot(V_exp, p_exp, color=colors['expansion'], label="Expansion")
                p4 = p_exp[-1]
            elif name == 'Diesel':
                V_iso = np.linspace(V2, V3, 100)
                ax.plot(V_iso, np.ones_like(V_iso)*p2, color=colors['isobar'], label="isobare Verbrennung")
                V_exp = np.linspace(V3, V1, 100)
                p_exp = p2 * (V3 / V_exp)**kappa
                ax.plot(V_exp, p_exp, color=colors['expansion'], label="Expansion")
                p4 = p_exp[-1]
            elif name == 'Seliger':
                V_current = V2
                p_current = p2
                if alpha > 0:
                    p_iso = np.linspace(p_current, p_current * (1 + alpha * 2.5), 20)
                    ax.plot(np.ones_like(p_iso)*V2, p_iso, color=colors['isochor'], label="isochore Verbrennung")
                    p_current = p_iso[-1]
                if alpha < 1:
                    V_iso2 = np.linspace(V2, V3, 100)
                    ax.plot(V_iso2, np.ones_like(V_iso2)*p_current, color=colors['isobar'], label="isobare Verbrennung")
                    V_current = V3
                V_exp = np.linspace(V_current, V1, 100)
                p_exp = p_current * (V_current / V_exp)**kappa
                ax.plot(V_exp, p_exp, color=colors['expansion'], label="Expansion")
                p4 = p_exp[-1]
        else:
            p4 = p2

        if show_abgabe:
            ax.plot(np.ones(20)*V1, np.linspace(p4, p1, 20), color=colors['waermeabgabe'], label="Wärmeabgabe")

        eta = {
            'Otto': otto_efficiency(r, kappa),
            'Diesel': diesel_efficiency(r, rho, kappa),
            'Seliger': seliger_efficiency(r, rho, alpha, kappa)
        }[name]
        ax.legend(title=f"Wirkungsgrad: {eta*100:.2f} %")

    return fig

# Streamlit App
st.set_page_config(layout="wide")

with st.sidebar:
    st.markdown("## 🔧 Einstellungen")
    r = st.slider("Kompressionsverhältnis r", 10.0, 25.0, 18.0, 0.1)
    rho = st.slider("Spreizungsverhältnis ρ", 1.1, 3.0, 2.0, 0.01)
    kappa = st.slider("Adiabatenexponent κ", 1.2, 1.67, 1.4, 0.01)
    alpha = st.slider("Anteil isochorer Verbrennung (Seliger)", 0.0, 1.0, 0.5, 0.05)

    st.markdown("---")
    st.markdown("### 🔍 Abschnitte anzeigen")
    show_komp = st.checkbox("Kompression", value=True)
    show_verbrennung = st.checkbox("Verbrennung & Expansion", value=True)
    show_abgabe = st.checkbox("Wärmeabgabe", value=True)

st.markdown("""
### η-Wirkungsgradformeln
- Otto: $\eta_O = 1 - \frac{1}{r^{\kappa - 1}}$
- Diesel: $\eta_D = 1 - \frac{1}{r^{\kappa - 1}} \cdot \frac{\rho^{\kappa} - 1}{\kappa(\rho - 1)}$
- Seliger (explizit):
\[ 
\eta_S = 1 - \frac{1}{r^{\kappa - 1}} \left[ \frac{\rho^\kappa - 1}{\kappa(\rho - 1)} + \alpha \left( \frac{\rho^\kappa - 1}{\rho^\kappa} - \ln(\rho) \right) \right]
\]
- Seliger (vereinfacht im Code): $\eta_S = (1 - \alpha) \cdot \eta_D + \alpha \cdot \eta_O$
""")

fig = plot_processes(r, rho, kappa, alpha, show_komp, show_verbrennung, show_abgabe)
st.pyplot(fig, use_container_width=True)
