import streamlit as st
import numpy as np

st.set_page_config(page_title="Diesel-Wirkungsgrad", layout="centered")

st.title("🔧 Wirkungsgrad des idealen Diesel-Prozesses")

r = st.slider("Kompressionsverhältnis (r)", 10.0, 25.0, 18.0, 0.1)
rho = st.slider("Spreizungsverhältnis (ρ)", 1.1, 3.0, 2.0, 0.01)
kappa = 1.4

term1 = 1 / r**(kappa - 1)
term2 = (rho**kappa - 1) / (kappa * (rho - 1))
eta = 1 - term1 * term2

st.metric("Wirkungsgrad η", f"{eta*100:.2f} %")
