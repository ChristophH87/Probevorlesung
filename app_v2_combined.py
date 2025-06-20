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
    p_cool = np.li_
