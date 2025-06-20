import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Großer Stil
plt.rcParams.update({
    'font.size': 18,
    'axes.titlesize': 20,
    'axes.labelsize': 18,
    'xtick.labelsize': 16,
    'ytick.labelsize': 16,
    'legend.fontsize': 18,
    'lines.linewidth': 3
})

# Wirkungsgrade
def otto_efficiency(r, kappa):
    return 1 - 1 / r**(kappa - 1)

def diesel_efficiency(r, rho, kappa):
    return 1 - (1 / r**(kappa - 1)) * ((rho**kappa - 1) / (kappa * (rho - 1)))

def seliger_efficiency(r, rho, alpha, kappa):
    eta_diesel = diesel_efficiency(r, rho, kappa)
    eta_otto = otto_efficiency(r, kappa)
    return (1 - alpha) * eta_diesel + alpha * eta_otto

# Zustandspunkte beschriften
def annotate_states(ax, V, P, labels):
    for i, label in enumerate(labels):
        ax.annotate(label, (V[i], P[i]), textcoords="offset points", xytext=(-15, 15),
                    fontsize=18, color="black", arrowprops=dict(arrowstyle='->', lw=1.5))

# Farben für Prozessschritte
colors = {
    "kompression": "blue",
    "isochor": "orange",
    "isobar": "red",
    "expansion": "green",
    "waermeabgabe": "gray"
}

# Hauptdiagrammfunktion
def plot_processes(r, rho, kappa, alpha, selected_takt):
    V1 = 1.0
    V2 = V1 / r
    V3 = V2 * rho
    fig, axs = plt.subplots(1, 3, figsize=(24, 8))

    # === OTTO ===
    axs[0].set_title(f'Otto-Prozess\nη = {otto_efficiency(r, kappa)*100:.2f} %')
    if selected_takt in ["Alle Takte", "Nur Kompression"]:
        Vc = np.linspace(V1, V2, 100)
        pc = 1 / Vc**kappa
        axs[0].plot(Vc, pc, label="1→2 Kompression", color=colors["kompression"])
        p1, p2 = pc[0], pc[-1]
    else:
        p1 = p2 = 1 / V1**kappa

    if selected_takt in ["Alle Takte", "Nur Verbrennung/Expansion"]:
        p_iso = np.linspace(p2, p2 * 3, 20)
        axs[0].plot(np.ones_like(p_iso)*V2, p_iso, label="2→3 isochore Verbrennung", color=colors["isochor"])
        V_exp = np.linspace(V2, V1, 100)
        p_exp = p_iso[-1] * (V2 / V_exp)**kappa
        axs[0].plot(V_exp, p_exp, label="3→4 Expansion", color=colors["expansion"])
        p4 = p_exp[-1]
    else:
        p4 = p2

    if selected_takt in ["Alle Takte", "Nur Wärmeabgabe"]:
        axs[0].plot(np.ones(20)*V1, np.linspace(p4, p1, 20), label="4→1 Wärmeabgabe", color=colors["waermeabgabe"])

    axs[0].set_xlabel("Volumen (V)")
    axs[0].set_ylabel("Druck (p)")
    axs[0].legend()
    axs[0].grid(True)
    if selected_takt == "Alle Takte":
        annotate_states(axs[0], [V1, V2, V2, V1], [p1, p2, p_iso[-1], p_exp[-1]], ["1", "2", "3", "4"])

    # === DIESEL ===
    axs[1].set_title(f'Diesel-Prozess\nη = {diesel_efficiency(r, rho, kappa)*100:.2f} %')
    if selected_takt in ["Alle Takte", "Nur Kompression"]:
        Vc = np.linspace(V1, V2, 100)
        pc = 1 / Vc**kappa
        axs[1].plot(Vc, pc, label="1→2 Kompression", color=colors["kompression"])
        p1, p2 = pc[0], pc[-1]
    else:
        p1 = p2 = 1 / V1**kappa

    if selected_takt in ["Alle Takte", "Nur Verbrennung/Expansion"]:
        V_iso = np.linspace(V2, V3, 100)
        axs[1].plot(V_iso, np.ones_like(V_iso)*p2, label="2→3 isobare Verbrennung", color=colors["isobar"])
        V_exp = np.linspace(V3, V1, 100)
        p_exp = p2 * (V3 / V_exp)**kappa
        axs[1].plot(V_exp, p_exp, label="3→4 Expansion", color=colors["expansion"])
        p4 = p_exp[-1]
    else:
        p4 = p2

    if selected_takt in ["Alle Takte", "Nur Wärmeabgabe"]:
        axs[1].plot(np.ones(20)*V1, np.linspace(p4, p1, 20), label="4→1 Wärmeabgabe", color=colors["waermeabgabe"])

    axs[1].set_xlabel("Volumen (V)")
    axs[1].legend()
    axs[1].grid(True)
    if selected_takt == "Alle Takte":
        annotate_states(axs[1], [V1, V2, V3, V1], [pc[0], pc[-1], p2, p_exp[-1]], ["1", "2", "3", "4"])

    # === SELIGER ===
    axs[2].set_title(f'Seliger-Prozess\nη = {seliger_efficiency(r, rho, alpha, kappa)*100:.2f} %')
    if selected_takt in ["Alle Takte", "Nur Kompression"]:
        Vc = np.linspace(V1, V2, 100)
        pc = 1 / Vc**kappa
        axs[2].plot(Vc, pc, label="1→2 Kompression", color=colors["kompression"])
        p1, p2 = pc[0], pc[-1]
    else:
        p1 = p2 = 1 / V1**kappa

    if selected_takt in ["Alle Takte", "Nur Verbrennung/Expansion"]:
        V_current = V2
        p_current = p2
        labels = ["2"]
        if alpha > 0:
            p_iso = np.linspace(p_current, p_current * (1 + alpha * 2.5), 20)
            axs[2].plot(np.ones_like(p_iso)*V2, p_iso, label="2→3 isochore Verbrennung", color=colors["isochor"])
            p_current = p_iso[-1]
            labels.append("3")

        if alpha < 1:
            V_iso2 = np.linspace(V2, V3, 100)
            axs[2].plot(V_iso2, np.ones_like(V_iso2)*p_current, label="3→4 isobare Verbrennung", color=colors["isobar"])
            V_current = V3
            labels.append("4")

        V_exp = np.linspace(V_current, V1, 100)
        p_exp = p_current * (V_current / V_exp)**kappa
        axs[2].plot(V_exp, p_exp, label="4→5 Expansion", color=colors["expansion"])
        p5 = p_exp[-1]
    else:
        p5 = p2

    if selected_takt in ["Alle Takte", "Nur Wärmeabgabe"]:
        axs[2].plot(np.ones(20)*V1, np.linspace(p5, p1, 20), label="5→1 Wärmeabgabe", color=colors["waermeabgabe"])

    axs[2].set_xlabel("Volumen (V)")
    axs[2].legend()
    axs[2].grid(True)
    if selected_takt == "Alle Takte":
        annotate_states(axs[2], [V1, V2, V2, V3, V1],
                        [p1, p2, p_current, p_current, p_exp[-1]],
                        ["1", "2", "3", "4", "5"][:5 if alpha < 1 else 4])

    plt.tight_layout()
    return fig

# -------------------- Streamlit UI --------------------

st.set_page_config(layout="wide")

with st.sidebar:
    st.markdown("## 🔧 Parameter einstellen")
    
    r = st.slider("Kompressionsverhältnis r", 10.0, 25.0, 18.0, 0.1)
    st.caption("Otto: 10–14 | Diesel: 16–22")

    rho = st.slider("Spreizungsverhältnis ρ", 1.1, 3.0, 2.0, 0.01)
    st.caption("Typisch: 1.8–2.2")

    kappa = st.slider("Adiabatenexponent κ", 1.2, 1.67, 1.4, 0.01)
    st.caption("Trockenluft: ≈ 1.4")

    alpha = st.slider("Anteil isochorer Verbrennung (Seliger)", 0.0, 1.0, 0.5, 0.05)
    st.caption("α = 0 → Diesel, α = 1 → Otto")

    st.markdown("---")
    selected_takt = st.radio("🧭 Sichtbare Takte", [
        "Alle Takte",
        "Nur Kompression",
        "Nur Verbrennung/Expansion",
        "Nur Wärmeabgabe"
    ])

    st.markdown("---")
    st.markdown("### 📐 Formeln")
    st.markdown(r"""
- Kompression: $r = \frac{V_1}{V_2}$
- Spreizung: $\rho = \frac{V_3}{V_2}$
- Otto-Wirkungsgrad: $\eta_O = 1 - \frac{1}{r^{\kappa - 1}}$
- Diesel-Wirkungsgrad: $\eta_D = 1 - \frac{1}{r^{\kappa - 1}} \cdot \frac{\rho^{\kappa} - 1}{\kappa(\rho - 1)}$
- Seliger: $\eta_S = (1 - \alpha)\cdot \eta_D + \alpha \cdot \eta_O$
""", unsafe_allow_html=True)

# Hauptanzeige
st.markdown("### 🔍 Gemeinsame Prämissen")
st.markdown("""
- Ideales Gasverhalten  
- Isentrope Kompression und Expansion  
- Konstante Gasmasse  
- Keine Wärmeverluste  
- Eingetragene Wärme beim Verbrennungsschritt  
""")

fig = plot_processes(r, rho, kappa, alpha, selected_takt)
st.pyplot(fig)
