import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Berechnungsfunktionen
def diesel_efficiency(r, rho, kappa):
    return 1 - (1 / r**(kappa - 1)) * ((rho**kappa - 1) / (kappa * (rho - 1)))

def otto_efficiency(r, kappa):
    return 1 - 1 / r**(kappa - 1)

def seliger_efficiency(r, rho, kappa):
    term1 = 1 / r**(kappa - 1)
    term2 = (rho**kappa - 1) / (kappa * (rho - 1))
    return 1 - term1 * term2

def plot_processes(r, rho, kappa):
    V1 = 1.0
    V2 = V1 / r
    V3 = V2 * rho

    fig, axs = plt.subplots(1, 3, figsize=(18, 5))

    # Otto
    V_otto_comp = np.linspace(V1, V2, 100)
    p_otto_comp = 1 / V_otto_comp**kappa
    V_otto_exp = np.linspace(V2, V1, 100)
    p_otto_exp = (p_otto_comp[-1]*5) / V_otto_exp**kappa
    axs[0].plot(V_otto_comp, p_otto_comp, label="Kompression")
    axs[0].plot(V_otto_exp, p_otto_exp, label="Expansion")
    axs[0].set_title(f'Otto-Prozess\nη = {otto_efficiency(r, kappa)*100:.2f} %')
    axs[0].legend()
    axs[0].grid(True)

    # Diesel
    V_diesel_comp = np.linspace(V1, V2, 100)
    p_diesel_comp = 1 / V_diesel_comp**kappa
    V_diesel_iso = np.linspace(V2, V3, 100)
    p_diesel_iso = np.ones_like(V_diesel_iso) * p_diesel_comp[-1]
    V_diesel_exp = np.linspace(V3, V1, 100)
    p_diesel_exp = p_diesel_iso[0] * (V3 / V_diesel_exp)**kappa
    axs[1].plot(V_diesel_comp, p_diesel_comp, label="Kompression")
    axs[1].plot(V_diesel_iso, p_diesel_iso, label="isobare Verbrennung")
    axs[1].plot(V_diesel_exp, p_diesel_exp, label="Expansion")
    axs[1].set_title(f'Diesel-Prozess\nη = {diesel_efficiency(r, rho, kappa)*100:.2f} %')
    axs[1].legend()
    axs[1].grid(True)

    # Seliger
    p_seliger_comp = 1 / V_diesel_comp**kappa
    p_isochor = np.linspace(p_seliger_comp[-1], p_seliger_comp[-1]*2.5, 20)
    V_isochor = np.ones_like(p_isochor) * V2
    p_isobar = np.ones(100) * p_isochor[-1]
    V_isobar = np.linspace(V2, V3, 100)
    V_exp = np.linspace(V3, V1, 100)
    p_exp = p_isobar[0] * (V3 / V_exp)**kappa
    axs[2].plot(V_diesel_comp, p_seliger_comp, label="Kompression")
    axs[2].plot(V_isochor, p_isochor, label="isochore Verbrennung")
    axs[2].plot(V_isobar, p_isobar, label="isobare Verbrennung")
    axs[2].plot(V_exp, p_exp, label="Expansion")
    axs[2].set_title(f'Seliger-Prozess\nη = {seliger_efficiency(r, rho, kappa)*100:.2f} %')
    axs[2].legend()
    axs[2].grid(True)

    for ax in axs:
        ax.set_xlabel("Volumen (V)")
        ax.set_ylabel("Druck (p)")

    plt.tight_layout()
    return fig

# Streamlit-Oberfläche
st.title("🔧 Vergleich: Otto-, Diesel- und Seliger-Prozess")

r = st.slider("Kompressionsverhältnis r", 10.0, 25.0, 18.0, 0.1)
rho = st.slider("Spreizungsverhältnis ρ", 1.1, 3.0, 2.0, 0.01)
kappa = st.slider("Adiabatenexponent κ", 1.2, 1.67, 1.4, 0.01)

fig = plot_processes(r, rho, kappa)
st.pyplot(fig)
