import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# -------------------- Wirkungsgradformeln --------------------
def otto_efficiency(r, kappa):
    return 1 - 1 / r**(kappa - 1)

def diesel_efficiency(r, rho, kappa):
    return 1 - (1 / r**(kappa - 1)) * ((rho**kappa - 1) / (kappa * (rho - 1)))

def seliger_efficiency(r, rho, alpha, kappa):
    term1 = 1 / r**(kappa - 1)
    p_ratio = 1 + alpha * ((rho**kappa - 1))
    term2 = (p_ratio - 1) / (kappa * (rho - 1))
    return 1 - term1 * term2

def annotate_states(ax, V, P, labels):
    for i, label in enumerate(labels):
        ax.annotate(label, (V[i], P[i]), textcoords="offset points", xytext=(-15, 15),
                    fontsize=18, color="black", arrowprops=dict(arrowstyle='->', lw=0.7))

# -------------------- Plotfunktion --------------------
def plot_processes(r, rho, kappa, alpha):
    V1 = 1.0
    V2 = V1 / r
    V3 = V2 * rho
    fig, axs = plt.subplots(1, 3, figsize=(24, 8))  # groß für Präsentation

    # OTTO
    Vc = V2
    Vc_exp = np.linspace(V1, V2, 100)
    p_comp = 1 / Vc_exp**kappa
    p_iso = np.linspace(p_comp[-1], p_comp[-1]*3, 20)
    V_iso = np.ones_like(p_iso) * V2
    V_exp = np.linspace(V2, V1, 100)
    p_exp = p_iso[-1] * (V2 / V_exp)**kappa
    p_cool = np.linspace(p_exp[-1], p_comp[0], 20)
    V_cool = np.ones_like(p_cool) * V1
    axs[0].plot(Vc_exp, p_comp, label="1→2 Kompression")
    axs[0].plot(V_iso, p_iso, label="2→3 isochore Verbrennung")
    axs[0].plot(V_exp, p_exp, label="3→4 Expansion")
    axs[0].plot(V_cool, p_cool, label="4→1 Wärmeabgabe")
    annotate_states(axs[0], [V1, V2, V2, V1], [p_comp[0], p_comp[-1], p_iso[-1], p_exp[-1]], ["1", "2", "3", "4"])
    axs[0].set_title(f'Otto-Prozess\nη = {otto_efficiency(r, kappa)*100:.2f} %', fontsize=20)
    axs[0].legend(fontsize=14)
    axs[0].grid(True)

    # DIESEL
    V_diesel_comp = np.linspace(V1, V2, 100)
    p_diesel_comp = 1 / V_diesel_comp**kappa
    V_diesel_iso = np.linspace(V2, V3, 100)
    p_diesel_iso = np.ones_like(V_diesel_iso) * p_diesel_comp[-1]
    V_diesel_exp = np.linspace(V3, V1, 100)
    p_diesel_exp = p_diesel_iso[0] * (V3 / V_diesel_exp)**kappa
    p_cool_d = np.linspace(p_diesel_exp[-1], p_diesel_comp[0], 20)
    V_cool_d = np.ones_like(p_cool_d) * V1
    axs[1].plot(V_diesel_comp, p_diesel_comp, label="1→2 Kompression")
    axs[1].plot(V_diesel_iso, p_diesel_iso, label="2→3 isobare Verbrennung")
    axs[1].plot(V_diesel_exp, p_diesel_exp, label="3→4 Expansion")
    axs[1].plot(V_cool_d, p_cool_d, label="4→1 Wärmeabgabe")
    annotate_states(axs[1], [V1, V2, V3, V1], [p_diesel_comp[0], p_diesel_comp[-1], p_diesel_iso[-1], p_diesel_exp[-1]], ["1", "2", "3", "4"])
    axs[1].set_title(f'Diesel-Prozess\nη = {diesel_efficiency(r, rho, kappa)*100:.2f} %', fontsize=20)
    axs[1].legend(fontsize=14)
    axs[1].grid(True)

    # SELIGER
    V_sel_comp = np.linspace(V1, V2, 100)
    p_sel_comp = 1 / V_sel_comp**kappa
    p_iso_s = np.linspace(p_sel_comp[-1], p_sel_comp[-1]*(1 + alpha * 2.5), 20)
    V_iso_s = np.ones_like(p_iso_s) * V2
    V_isobar = np.linspace(V2, V3, 100)
    p_isobar = np.ones_like(V_isobar) * p_iso_s[-1]
    V_exp = np.linspace(V3, V1, 100)
    p_exp = p_isobar[0] * (V3 / V_exp)**kappa
    p_cool_s = np.linspace(p_exp[-1], p_sel_comp[0], 20)
    V_cool_s = np.ones_like(p_cool_s) * V1
    axs[2].plot(V_sel_comp, p_sel_comp, label="1→2 Kompression")
    axs[2].plot(V_iso_s, p_iso_s, label="2→3 isochore Verbrennung")
    axs[2].plot(V_isobar, p_isobar, label="3→4 isobare Verbrennung")
    axs[2].plot(V_exp, p_exp, label="4→5 Expansion")
    axs[2].plot(V_cool_s, p_cool_s, label="5→1 Wärmeabgabe")
    annotate_states(axs[2], [V1, V2, V2, V3, V1], [p_sel_comp[0], p_sel_comp[-1], p_iso_s[-1], p_isobar[-1], p_exp[-1]], ["1", "2", "3", "4", "5"])
    axs[2].set_title(f'Seliger-Prozess\nη = {seliger_efficiency(r, rho, alpha, kappa)*100:.2f} %', fontsize=20)
    axs[2].legend(fontsize=14)
    axs[2].grid(True)

    for ax in axs:
        ax.set_xlabel("Volumen (V)", fontsize=18)
        ax.set_ylabel("Druck (p)", fontsize=18)
        ax.tick_params(labelsize=14)

    plt.tight_layout()
    return fig

# -------------------- Streamlit-Oberfläche --------------------

st.set_page_config(layout="wide")

with st.sidebar:
    st.markdown("## 🔧 Parameter einstellen", unsafe_allow_html=True)
    
    # Realistische Referenzwerte
    st.markdown("**Typische Werte:**")
    st.markdown("- Kompressionsverhältnis (Otto): 10–14\n- Kompression (Diesel): 16–22\n- ρ = 1.8–2.2\n- κ = 1.4")

    r = st.slider("Kompressionsverhältnis r", 10.0, 25.0, 18.0, 0.1, help="Otto ca. 10–14, Diesel ca. 16–22")
    rho = st.slider("Spreizungsverhältnis ρ", 1.1, 3.0, 2.0, 0.01, help="ρ typisch ca. 1.8–2.2")
    kappa = st.slider("Adiabatenexponent κ", 1.2, 1.67, 1.4, 0.01, help="κ = 1.4 für Luft")
    alpha = st.slider("Anteil isochore Verbrennung im Seliger-Prozess", 0.0, 1.0, 0.5, 0.05, help="0 = Diesel, 1 = Otto")

st.markdown("<h1 style='font-size: 36px;'>Vergleich: Otto-, Diesel- und Seliger-Prozess</h1>", unsafe_allow_html=True)
fig = plot_processes(r, rho, kappa, alpha)
st.pyplot(fig)
