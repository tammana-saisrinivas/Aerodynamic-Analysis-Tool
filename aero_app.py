import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

st.title("✈️ Aerodynamic Analysis Tool")

# ===== TABS =====
tab1, tab2, tab3 = st.tabs(["Airfoil Analysis", "Wing Analysis", "Comparison"])

# =========================
# ✈️ AIRFOIL ANALYSIS
# =========================
with tab1:
    st.header("Airfoil Analysis")

    naca = st.text_input("Enter NACA 4-digit (e.g., 2412)", "2412")

    if len(naca) == 4:
        m = int(naca[0]) / 100
        p = int(naca[1]) / 10
        t = int(naca[2:]) / 100
    else:
        st.error("Enter valid 4-digit NACA")
        st.stop()

    x = np.linspace(0, 1, 100)

    yt = 5 * t * (0.2969*np.sqrt(x) - 0.1260*x - 0.3516*x**2 +
                  0.2843*x**3 - 0.1015*x**4)

    yc = np.where(x < p,
                  m/p**2 * (2*p*x - x**2),
                  m/(1-p)**2 * ((1-2*p) + 2*p*x - x**2))

    # Plot Airfoil
    fig1, ax1 = plt.subplots()
    ax1.plot(x, yc + yt)
    ax1.plot(x, yc - yt)
    ax1.set_title(f"NACA {naca}")
    ax1.axis('equal')
    st.pyplot(fig1)

    # Aerodynamics
    alpha = np.arange(-5, 15, 1)
    alpha_rad = np.deg2rad(alpha)

    Cl = 2 * np.pi * alpha_rad
    Cd = 0.01 + Cl**2
    LD = Cl / Cd

    fig2, ax2 = plt.subplots()
    ax2.plot(alpha, Cl, label="Cl")
    ax2.plot(alpha, Cd, label="Cd")
    ax2.plot(alpha, LD, label="L/D")
    ax2.legend()
    ax2.grid()
    st.pyplot(fig2)

# =========================
# 🛫 WING ANALYSIS
# =========================
with tab2:
    st.header("Wing Analysis")

    span = st.number_input("Span", value=10.0)
    chord = st.number_input("Chord", value=1.5)

    AR = span**2 / (span * chord)
    e = 0.8

    alpha = np.arange(-5, 15, 1)
    alpha_rad = np.deg2rad(alpha)

    Cl = 2 * np.pi * alpha_rad
    Cd = 0.01 + (Cl**2)/(np.pi * AR * e)
    LD = Cl / Cd

    fig3, ax3 = plt.subplots()
    ax3.plot(alpha, Cl, label="Cl")
    ax3.plot(alpha, Cd, label="Cd")
    ax3.plot(alpha, LD, label="L/D")
    ax3.set_title("Wing Performance")
    ax3.legend()
    ax3.grid()
    st.pyplot(fig3)

# =========================
# 🔥 COMPARISON
# =========================
with tab3:
    st.header("Comparison")

    mode = st.radio("Select Comparison Type", ["Airfoil", "Wing"])

    alpha = np.arange(-5, 15, 1)
    alpha_rad = np.deg2rad(alpha)

    # =====================
    # AIRFOIL COMPARISON
    # =====================
    if mode == "Airfoil":

        st.subheader("Airfoil Comparison")

        naca1 = st.text_input("Airfoil 1", "2412")
        naca2 = st.text_input("Airfoil 2", "0012")

        Cl1 = 2*np.pi*alpha_rad
        Cl2 = 2*np.pi*alpha_rad * 1.1   # slight variation

        Cd1 = 0.01 + Cl1**2
        Cd2 = 0.01 + Cl2**2

        LD1 = Cl1 / Cd1
        LD2 = Cl2 / Cd2

        fig, ax = plt.subplots()
        ax.plot(alpha, LD1, label=f"NACA {naca1}")
        ax.plot(alpha, LD2, label=f"NACA {naca2}")
        ax.set_title("Airfoil L/D Comparison")
        ax.legend()
        ax.grid()
        st.pyplot(fig)

    # =====================
    # WING COMPARISON 🔥
    # =====================
    else:

        st.subheader("Wing Comparison")

        st.write("Wing A")
        span1 = st.number_input("Span A", value=10.0)
        chord1 = st.number_input("Chord A", value=1.5)

        st.write("Wing B")
        span2 = st.number_input("Span B", value=12.0)
        chord2 = st.number_input("Chord B", value=1.2)

        e = 0.8

        # Wing A
        AR1 = span1**2 / (span1 * chord1)
        Cl1 = 2*np.pi*alpha_rad
        Cd1 = 0.01 + (Cl1**2)/(np.pi * AR1 * e)
        LD1 = Cl1 / Cd1

        # Wing B
        AR2 = span2**2 / (span2 * chord2)
        Cl2 = 2*np.pi*alpha_rad
        Cd2 = 0.01 + (Cl2**2)/(np.pi * AR2 * e)
        LD2 = Cl2 / Cd2

        # Plot
        fig, ax = plt.subplots()
        ax.plot(alpha, LD1, label="Wing A")
        ax.plot(alpha, LD2, label="Wing B")
        ax.set_title("Wing L/D Comparison")
        ax.legend()
        ax.grid()
        st.pyplot(fig)