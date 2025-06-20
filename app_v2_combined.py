# Der folgende Code ist eine aktualisierte Version von `app.py` mit LaTeX-Darstellung der Wirkungsgradformeln

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update({
    'font.size': 44,
    'axes.titlesize': 52,
    'axes.labelsize': 48,
    'xtick.labelsize': 40,
    'ytick.labelsize': 40,
    'legend.fontsize': 44,
    'lines.linewidth': 8
})

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

def plot_processes(r, rho, kappa, alpha, show_komp, show_isochor, show_isobar, show_exp, show_abgabe):
    V1 = 1.0
    V2 = V1 / r
    V3 = V2 * rho
    fig, axs = plt.subplots(1, 3, figsize=(48, 16))

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

        p4 = p2
        if name == 'Otto':
            if show_isochor:
                p_iso = np.linspace(p2, p2 * 3, 20)
                ax.plot(np.ones_like(p_iso)*V2, p_iso, color=colors['isochor'], label="isochore Verbrennung")
                p4 = p_iso[-1]
            if show_exp:
                V_exp = np.linspace(V2, V1, 100)
                p_exp = p4 * (V2 / V_exp)**kappa
                ax.plot(V_exp, p_exp, color=colors['expansion'], label="Expansion")
                p4 = p_exp[-1]

        elif name == 'Diesel':
            if show_isobar:
                V_iso = np.linspace(V2, V3, 100)
                ax.plot(V_iso, np.ones_like(V_iso)*p2, color=colors['isobar'], label="isobare Verbrennung")
            if show_exp:
                V_exp = np.linspace(V3, V1, 100)
                p_exp = p2 * (V3 / V_exp)**kappa
                ax.plot(V_exp, p_exp, color=colors['expansion'], label="Expansion")
                p4 = p_exp[-1]

        elif name == 'Seliger':
            V_current = V2
            p_current = p2
            if show_isochor and alpha > 0:
                p_iso = np.linspace(p_current, p_current * (1 + alpha * 2.5), 20)
                ax.plot(np.ones_like(p_iso)*V2, p_iso, color=colors['isochor'], label="isochore Verbrennung")
                p_current = p_iso[-1]
            if show_isobar and alpha < 1:
                V_iso2 = np.linspace(V2, V3, 100)
                ax.plot(V_iso2, np.ones_like(V_iso2)*p_current, color=colors['isobar'], label="isobare Verbrennung")
                V_current = V3
            if show_exp:
                V_exp = np.linspace(V_current, V1, 100)
                p_exp = p_current * (V_current / V_exp)**kappa
                ax.plot(V_exp, p_exp, color=colors['expansion'], label="Expansion")
                p4 = p_exp[-1]

        if show_abgabe:
            ax.plot(np.ones(20)*V1, np.linspace(p4, p1, 20), color=colors['waermeabgabe'], label="Wärmeabgabe")

        eta = {
            'Otto': otto_efficiency(r, kappa),
            'Diesel': diesel_efficiency(r, rho, kappa),
            'Seliger': seliger_efficiency(r, rho, alpha, kappa)
        }[name]
        ax.legend(title=f"Wirkungsgrad: {eta*100:.2f} %")

    return fig

st.set_page_config(layout="wide")

with st.sidebar:
    st.markdown("## 🔧 Einstellungen")
    r = st.slider("Kompressionsverhältnis r", 10.0, 25.0, 18.0, 0.1)
st.caption("Typisch: 16–20 für moderne Diesel, 10–14 für Ottomotoren")
    rho = st.slider("Spreizungsverhältnis ρ", 1.1, 3.0, 2.0, 0.01)
st.caption("Typisch: 1.8–2.5 bei Direkteinspritzung")
    kappa = st.slider("Adiabatenexponent κ", 1.2, 1.67, 1.4, 0.01)
st.caption("Typisch: 1.3–1.4 für Luft bei Raumtemperatur")
    alpha = st.slider("Anteil isochorer Verbrennung (Seliger)", 0.0, 1.0, 0.5, 0.05)
st.caption("0 = Diesel, 1 = Otto, typisch ca. 0.3–0.6")

    st.markdown("---")
    st.markdown("### 🔍 Abschnitte anzeigen")
    show_komp = st.checkbox("Kompression", value=True)
    show_isochor = st.checkbox("isochore Verbrennung", value=True)
    show_isobar = st.checkbox("isobare Verbrennung", value=True)
    show_exp = st.checkbox("Expansion", value=True)
    show_abgabe = st.checkbox("Wärmeabgabe", value=True)

st.markdown(r'''
### Wirkungsgradformeln
- Otto: $\eta_O = 1 - \frac{1}{r^{\kappa - 1}}$
- Diesel: $\eta_D = 1 - \frac{1}{r^{\kappa - 1}} \cdot \frac{\rho^{\kappa} - 1}{\kappa(\rho - 1)}$
- Seliger (explizit): $\eta_S = 1 - \frac{1}{r^{\kappa - 1}} \left[ \frac{\rho^{\kappa} - 1}{\kappa(\rho - 1)} + \alpha \left( \frac{\rho^{\kappa} - 1}{\rho^{\kappa}} - \ln(\rho) \right) \right]$
- Seliger (vereinfacht): $\eta_S = (1 - \alpha) \cdot \eta_D + \alpha \cdot \eta_O$
''')

fig = plot_processes(r, rho, kappa, alpha, show_komp, show_isochor, show_isobar, show_exp, show_abgabe)
st.pyplot(fig, use_container_width=True)
