import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 🧩 Matplotlib-Stil: große, klare Schrift
plt.rcParams.update({
    'font.size': 16,
    'axes.titlesize': 20,
    'axes.labelsize': 18,
    'xtick.labelsize': 16,
    'ytick.labelsize': 16,
    'legend.fontsize': 16
})

# Wirkungsgrade
def otto_efficiency(r, kappa):
    return 1 - 1 / r**(kappa - 1)

def diesel_efficiency(r, rho, kappa):
    return 1 - (1 / r**(kappa - 1)) * ((rho**kappa - 1) / (kappa * (rho - 1)))

# ✅ korrigierter Seliger-Wirkungsgrad (gewichtete Mischung)
def seliger_efficiency(r, rho, alpha, kappa):
    eta_diesel = diesel_efficiency(r, rho, kappa)
    eta_otto = otto_efficiency(r, kappa)
    return (1 - alpha) * eta_diesel + alpha * eta_otto

# Zustände beschriften
def annotate_states(ax, V, P, labels):
    for i, label in enumerate(labels):
        ax.annotate(label, (V[i], P[i]), textcoords="offset points", xytext=(-15, 15),
                    fontsize=18, color="black", arrowprops=dict(arrowstyle='->', lw=0.7))

# Diagramme erzeugen
def plot_processes(r, rho, kappa, alpha, selected_takt):
    V1 = 1.0
    V2 = V1 / r
    V3 = V2 * rho
    fig, axs = plt.subplots(1, 3, figsize=(24, 8))

    # ----- OTTO -----
    axs[0].set_title(f'Otto-Prozess\nη = {otto_efficiency(r, kappa)*100:.2f} %')
    if selected_takt in ["Alle Takte", "Nur Kompression"]:
        Vc = np.linspace(V1, V2, 100)
        pc = 1 / Vc**kappa
        axs[0].plot(Vc, pc, label="1→2 Kompression")
        p1, p2 = pc[0], pc[-1]
    else:
        p1 = p2 = None

    if selected_takt in ["Alle Takte", "Nur Verbrennung/Expansion"]:
        p_iso = np.linspace(p2, p2*3, 20)
        V_iso = np.ones_like(p_iso) * V2
        axs[0].plot(V_iso, p_iso, label="2→3 isochore Verbrennung")
        V_exp = np.linspace(V2, V1, 100)
        p_exp = p_iso[-1] * (V2 / V_exp)**kappa
        axs[0].plot(V_exp, p_exp, label="3→4 Expansion")
        p4 = p_exp[-1]
    else:
        p4 = None

    if selected_takt in ["Alle Takte", "Nur Wärmeabgabe"] and p1 and p4:
        V_cool = np.ones(20) * V1
        p_cool = np.linspace(p4, p1, 20)
        axs[0].plot(V_cool, p_cool, label="4→1 Wärmeabgabe")

    axs[0].set_xlabel("Volumen (V)")
    axs[0].set_ylabel("Druck (p)")
    axs[0].grid(True)
    axs[0].legend()
    if selected_takt == "Alle Takte":
        annotate_states(axs[0], [V1, V2, V2, V1], [p1, p2, p_iso[-1], p4], ["1", "2", "3", "4"])

    # ----- DIESEL -----
    axs[1].set_title(f'Diesel-Prozess\nη = {diesel_efficiency(r, rho, kappa)*100:.2f} %')
    if selected_takt in ["Alle Takte", "Nur Kompression"]:
        Vc = np.linspace(V1, V2, 100)
        pc = 1 / Vc**kappa
        axs[1].plot(Vc, pc, label="1→2 Kompression")
        p1, p2 = pc[0], pc[-1]
    else:
        p1 = p2 = None

    if selected_takt in ["Alle Takte", "Nur Verbrennung/Expansion"]:
        V_iso = np.linspace(V2, V3, 100)
        p_iso = np.ones_like(V_iso) * p2
        axs[1].plot(V_iso, p_iso, label="2→3 isobare Verbrennung")
        V_exp = np.linspace(V3, V1, 100)
        p_exp = p2 * (V3 / V_exp)**kappa
        axs[1].plot(V_exp, p_exp, label="3→4 Expansion")
        p4 = p_exp[-1]
    else:
        p4 = None

    if selected_takt in ["Alle Takte", "Nur Wärmeabgabe"] and p1 and p4:
        V_cool = np.ones(20) * V1
        p_cool = np.linspace(p4, p1, 20)
        axs[1].plot(V_cool, p_cool, label="4→1 Wärmeabgabe")

    axs[1].set_xlabel("Volumen (V)")
    axs[1].grid(True)
    axs[1].legend()
    if selected_takt == "Alle Takte":
        annotate_states(axs[1], [V1, V2, V3, V1], [pc[0], pc[-1], p_iso[-1], p_exp[-1]], ["1", "2", "3", "4"])

    # ----- SELIGER -----
    axs[2].set_title(f'Seliger-Prozess\nη = {seliger_efficiency(r, rho, alpha, kappa)*100:.2f} %')
    if selected_takt in ["Alle Takte", "Nur Kompression"]:
        Vc = np.linspace(V1, V2, 100)
        pc = 1 / Vc**kappa
        axs[2].plot(Vc, pc, label="1→2 Kompression")
        p1, p2 = pc[0], pc[-1]
    else:
        p1 = p2 = None

    if selected_takt in ["Alle Takte", "Nur Verbrennung/Expansion"]:
        p_iso = np.linspace(p2, p2*(1 + alpha*2.5), 20)
        V_iso = np.ones_like(p_iso) * V2
        axs[2].plot(V_iso, p_iso, label="2→3 isochore Verbrennung")
        V_iso2 = np.linspace(V2, V3, 100)
        p_iso2 = np.ones_like(V_iso2) * p_iso[-1]
        axs[2].plot(V_iso2, p_iso2, label="3→4 isobare Verbrennung")
        V_exp = np.linspace(V3, V1, 100)
        p_exp = p_iso2[0] * (V3 / V_exp)**kappa
        axs[2].plot(V_exp, p_exp, label="4→5 Expansion")
        p5 = p_exp[-1]
    else:
        p5 = None

    if selected_takt in ["Alle Takte", "Nur Wärmeabgabe"] and p1 and p5:
        V_cool = np.ones(20) * V1
        p_cool = np.linspace(p5, p1, 20)
        axs[2].plot(V_cool, p_cool, label="5→1 Wärmeabgabe")

    axs[2].set_xlabel("Volumen (V)")
    axs[2].grid(True)
    axs[2].legend()
    if selected_takt == "Alle Takte":
        annotate_states(axs[2], [V1, V2, V2, V3, V1],
                        [pc[0], pc[-1], p_iso[-1], p_iso2[-1], p_exp[-1]],
                        ["1", "2", "3", "4", "5"])

    plt.tight_layout()
    return fig

# -------------------- Streamlit UI --------------------
st.set_page_config(layout="wide")

with st.sidebar:
    st.markdown("## 🔧 Parameter einstellen")
    r = st.slider("Kompressionsverhältnis r", 10.0, 25.0, 18.0, 0.1)
    rho = st.slider("Spreizungsverhältnis ρ", 1.1, 3.0, 2.0, 0.01)
    kappa = st.slider("Adiabatenexponent κ", 1.2, 1.67, 1.4, 0.01)
    alpha = st.slider("Anteil isochorer Verbrennung", 0.0, 1.0, 0.5, 0.05)

    st.markdown("---")
    selected_takt = st.radio("🧭 Anzeigemodus (Takte)", [
        "Alle Takte",
        "Nur Kompression",
        "Nur Verbrennung/Expansion",
        "Nur Wärmeabgabe"
    ])

st.markdown("<h1 style='font-size: 36px;'>Vergleich: Otto-, Diesel- und Seliger-Prozess</h1>", unsafe_allow_html=True)

fig = plot_processes(r, rho, kappa, alpha, selected_takt)
st.pyplot(fig)
