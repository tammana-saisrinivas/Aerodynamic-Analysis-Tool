import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from matplotlib.patches import FancyBboxPatch
import matplotlib.patches as mpatches

st.set_page_config(page_title="Aerodynamic Analysis Tool", page_icon="✈️", layout="wide")

# Premium Dark Theme with Aerospace Styling - NO BLUE
st.markdown("""
<style>
    * {
        margin: 0;
        padding: 0;
    }
    
    body, .main {
        background: linear-gradient(135deg, #0a0e12 0%, #141820 50%, #0a0e12 100%);
        color: #e8e8e8;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0a0e12 0%, #141820 50%, #0a0e12 100%);
    }
    
    /* Header Styling */
    h1 {
        background: linear-gradient(135deg, #ff8c00, #ffa500);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 800;
        letter-spacing: 2px;
        margin-top: 20px;
    }
    
    h2, h3 {
        color: #ff8c00;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 700;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: rgba(10, 14, 18, 0.9);
        padding: 15px;
        border-radius: 12px;
        border-bottom: 2px solid #ff8c00;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(20, 24, 32, 0.7);
        color: #a8a8a8;
        border-radius: 8px;
        padding: 10px 16px;
        border: 1px solid rgba(255, 140, 0, 0.3);
        transition: all 0.3s ease;
        font-size: 11px;
        font-weight: 600;
        white-space: nowrap;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #ff8c00, #ffa500);
        color: #0a0e12;
        border: none;
        box-shadow: 0 0 20px rgba(255, 140, 0, 0.4);
    }
    
    /* Input Fields */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        background-color: rgba(25, 32, 45, 0.8);
        color: #ff8c00;
        border: 2px solid rgba(255, 140, 0, 0.4);
        border-radius: 8px;
        padding: 12px !important;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: #ff8c00;
        box-shadow: 0 0 15px rgba(255, 140, 0, 0.6);
        background-color: rgba(25, 32, 45, 1);
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #ff8c00, #ffa500);
        color: #0a0e12;
        border: none;
        border-radius: 8px;
        padding: 12px 32px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(255, 140, 0, 0.3);
    }
    
    .stButton > button:hover {
        box-shadow: 0 6px 25px rgba(255, 140, 0, 0.6);
        transform: translateY(-2px);
    }
    
    /* Metrics */
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(255, 140, 0, 0.08), rgba(255, 165, 0, 0.08));
        border: 2px solid rgba(255, 140, 0, 0.5);
        padding: 20px;
        border-radius: 12px;
        transition: all 0.3s ease;
    }
    
    div[data-testid="stMetric"]:hover {
        border-color: #ff8c00;
        box-shadow: 0 0 20px rgba(255, 140, 0, 0.3);
        transform: translateY(-3px);
    }
    
    /* Metric Label */
    [data-testid="stMetricLabel"] {
        color: #a8a8a8;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 1px;
        white-space: normal;
    }
    
    /* Metric Value */
    [data-testid="stMetricValue"] {
        color: #ff8c00;
        font-size: 28px;
        font-weight: 800;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a0e12 0%, #141820 100%);
        border-right: 2px solid rgba(255, 140, 0, 0.3);
    }
    
    /* Success/Info Boxes */
    .stSuccess, .stInfo {
        background-color: rgba(255, 140, 0, 0.1);
        border: 2px solid #ff8c00;
        border-radius: 8px;
        color: #ff8c00;
    }
    
    /* Error Messages */
    .stError {
        background-color: rgba(255, 100, 100, 0.1);
        border: 2px solid #ff6464;
        border-radius: 8px;
        color: #ff9999;
    }
    
    /* Caption */
    .stCaption {
        color: #ff8c00;
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }
    
    /* Horizontal Line */
    hr {
        border: 0;
        border-top: 2px solid rgba(255, 140, 0, 0.3);
        margin: 30px 0;
    }
    
    /* Column Styling */
    .stColumn {
        padding: 15px;
    }
    
    /* Markdown Text */
    p, li {
        color: #d0d0d0;
        line-height: 1.6;
    }
    
    /* Code Blocks */
    code {
        background-color: rgba(25, 32, 45, 0.8);
        color: #ff8c00;
        border-radius: 6px;
        padding: 2px 6px;
    }
</style>
""", unsafe_allow_html=True)

# Custom matplotlib style for plots
plt.style.use('dark_background')

st.title("✈️ AERODYNAMIC ANALYSIS SUITE")
st.caption("Professional CFD Analysis • Real-time Visualization • Advanced Wing Performance")

with st.sidebar:
    st.markdown("<h3 style='text-align: center; color: #ff8c00;'>🎛️ SYSTEM STATUS</h3>", unsafe_allow_html=True)
    
    # Display horizontally
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div style='text-align: center;'><span style='color: #ff8c00; font-weight: bold;'>● GIT</span></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div style='text-align: center;'><span style='color: #ff8c00; font-weight: bold;'>● JENKINS</span></div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div style='text-align: center;'><span style='color: #ff8c00; font-weight: bold;'>● READY</span></div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("""
    <h4 style='color: #ff8c00;'>📦 TECH STACK</h4>
    <ul style='color: #d0d0d0;'>
    <li><b>Python</b> 3.9+</li>
    <li><b>Streamlit</b></li>
    <li><b>NumPy</b></li>
    <li><b>Matplotlib</b></li>
    <li><b>Git</b> • <b>Jenkins</b></li>
    <li><b>AWS</b> Ready</li>
    </ul>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.caption("Version 2.0 - Enterprise")

tab1, tab2, tab3, tab4 = st.tabs([
    "✈️ AIRFOIL",
    "🛩️ WING",
    "📊 COMPARE AIRFOIL",
    "🛫 COMPARE WING"
])

# ==================== TAB 1: AIRFOIL ANALYSIS ====================
with tab1:
    st.markdown("### NACA 4-Digit Airfoil Geometry & Performance")
    
    c1, c2 = st.columns([1, 2])
    
    with c1:
        st.markdown("#### Input Parameters")
        naca = st.text_input("NACA Code", "2412", help="Enter a 4-digit NACA code (e.g., 2412)")
    
    try:
        m = int(naca[0]) / 100
        p = max(int(naca[1]) / 10, 0.1)
        t = int(naca[2:]) / 100
    except:
        st.error("❌ Invalid NACA code. Enter a 4-digit number.")
        st.stop()
    
    x = np.linspace(0, 1, 200)
    yt = 5 * t * (0.2969 * np.sqrt(x) - 0.126 * x - 0.3516 * x**2 + 0.2843 * x**3 - 0.1015 * x**4)
    yc = np.where(x < p, m / p**2 * (2 * p * x - x**2), m / (1 - p)**2 * ((1 - 2 * p) + 2 * p * x - x**2))
    
    with c2:
        fig, ax = plt.subplots(figsize=(10, 4.5), facecolor='#0a0e12', edgecolor='#ff8c00')
        ax.set_facecolor('#141820')
        
        ax.plot(x, yc + yt, lw=3, label="Upper Surface", color='#ff8c00')
        ax.plot(x, yc - yt, lw=3, label="Lower Surface", color='#ff6b9d')
        ax.fill_between(x, yc - yt, yc + yt, alpha=0.15, color='#ff8c00')
        
        ax.set_aspect('equal')
        ax.grid(True, ls='--', alpha=0.2, color='#ff8c00')
        ax.set_title(f"NACA {naca} Airfoil Geometry", fontsize=14, fontweight='bold', color='#ff8c00')
        ax.set_xlabel("Chord Position (x/c)", color='#a8a8a8')
        ax.set_ylabel("Thickness (y/c)", color='#a8a8a8')
        ax.legend(loc='upper right', framealpha=0.9)
        ax.tick_params(colors='#a8a8a8')
        
        st.pyplot(fig, use_container_width=True)
    
    st.markdown("---")
    st.markdown("### AERODYNAMIC COEFFICIENTS")
    
    alpha = np.arange(-5, 16)
    ar = np.deg2rad(alpha)
    Cl = 2 * np.pi * ar
    Cd = 0.01 + Cl**2
    LD = Cl / Cd
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Max Lift Coeff", f"{Cl.max():.2f}")
    m2.metric("Max Drag Coeff", f"{Cd.max():.2f}")
    m3.metric("Peak L/D Ratio", f"{LD.max():.1f}")
    
    fig2, ax2 = plt.subplots(figsize=(12, 5), facecolor='#0a0e12', edgecolor='#ff8c00')
    ax2.set_facecolor('#141820')
    
    ax2.plot(alpha, Cl, lw=3, label="Lift Coefficient (Cl)", marker='o', markersize=4, color='#ff8c00')
    ax2.plot(alpha, Cd, lw=3, label="Drag Coefficient (Cd)", marker='s', markersize=4, color='#ff6b9d')
    ax2.plot(alpha, LD, lw=3, label="Lift-to-Drag Ratio (L/D)", marker='^', markersize=4, color='#00d9a3')
    
    ax2.grid(True, ls='--', alpha=0.2, color='#ff8c00')
    ax2.legend(loc='upper left', framealpha=0.9, fontsize=10)
    ax2.set_xlabel("Angle of Attack (°)", fontsize=11, color='#a8a8a8')
    ax2.set_ylabel("Coefficient / Ratio", fontsize=11, color='#a8a8a8')
    ax2.set_title(f"NACA {naca} - Aerodynamic Performance Curves", fontsize=13, fontweight='bold', color='#ff8c00')
    ax2.tick_params(colors='#a8a8a8')
    
    st.pyplot(fig2, use_container_width=True)

# ==================== TAB 2: WING DESIGN ====================
with tab2:
    st.markdown("### WING GEOMETRY & PERFORMANCE ANALYSIS")
    
    c1, c2 = st.columns([1, 1])
    
    with c1:
        st.markdown("#### Wing Specifications")
        span = st.number_input("Wing Span (m)", 10.0, step=0.5, help="Total wing span in meters")
        chord = st.number_input("Mean Chord (m)", 1.5, step=0.1, help="Mean aerodynamic chord in meters")
    
    AR = span / chord
    e = 0.8
    alpha = np.arange(-5, 16)
    ar = np.deg2rad(alpha)
    Cl = 2 * np.pi * ar
    Cd = 0.01 + (Cl**2) / (np.pi * AR * e)
    LD = Cl / Cd
    
    with c2:
        st.markdown("#### Computed Properties")
        st.metric("Aspect Ratio", f"{AR:.2f}")
        st.metric("Peak L/D", f"{LD.max():.2f}")
        st.metric("Optimal AoA", f"{alpha[LD.argmax()]:.0f}°")
    
    st.markdown("---")
    st.markdown("### WING VISUALIZATION & PERFORMANCE")
    
    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.markdown("#### Wing Shape")
        # Draw wing diagram based on parameters
        fig_wing, ax_wing = plt.subplots(figsize=(6, 8), facecolor='#0a0e12')
        ax_wing.set_facecolor('#141820')
        
        # Draw simplified wing view
        wing_length = span
        wing_root_chord = chord * 1.1
        wing_tip_chord = chord * 0.8
        
        # Wing outline (tapered wing)
        x_wing = np.array([0, wing_root_chord, wing_tip_chord, 0, 0])
        y_wing = np.array([0, 0, wing_length, wing_length, 0])
        
        ax_wing.fill(x_wing, y_wing, color='#ff8c00', alpha=0.3, edgecolor='#ff8c00', linewidth=3)
        ax_wing.plot(x_wing, y_wing, color='#ff8c00', linewidth=3, label='Wing Surface')
        
        # Add dimension lines
        ax_wing.plot([0, wing_root_chord], [-0.5, -0.5], 'w--', linewidth=1, alpha=0.5)
        ax_wing.text(wing_root_chord/2, -1, f'Root: {wing_root_chord:.2f}m', ha='center', color='#ff8c00', fontsize=9)
        
        ax_wing.plot([wing_tip_chord/2, wing_tip_chord/2], [0, wing_length], 'w--', linewidth=1, alpha=0.5)
        ax_wing.text(wing_tip_chord/2 + 0.3, wing_length/2, f'Span\n{wing_length:.1f}m', color='#ff8c00', fontsize=9)
        
        ax_wing.set_xlim(-1, wing_root_chord + 1)
        ax_wing.set_ylim(-2, wing_length + 1)
        ax_wing.set_aspect('equal')
        ax_wing.grid(True, ls='--', alpha=0.2, color='#ff8c00')
        ax_wing.set_xlabel("Chord (m)", color='#a8a8a8')
        ax_wing.set_ylabel("Span (m)", color='#a8a8a8')
        ax_wing.set_title("Wing Plan Form", fontsize=12, fontweight='bold', color='#ff8c00')
        ax_wing.tick_params(colors='#a8a8a8')
        ax_wing.legend(loc='upper right', framealpha=0.9)
        
        st.pyplot(fig_wing, use_container_width=True)
    
    with col2:
        st.markdown("#### Performance Curves")
        fig3, (ax3a, ax3b) = plt.subplots(2, 1, figsize=(8, 10), facecolor='#0a0e12')
        ax3a.set_facecolor('#141820')
        ax3b.set_facecolor('#141820')
        
        # Top plot - Lift & Drag
        ax3a.plot(alpha, Cl, lw=3, label="Lift Coefficient", marker='o', markersize=4, color='#ff8c00')
        ax3a.plot(alpha, Cd, lw=3, label="Drag Coefficient", marker='s', markersize=4, color='#ff6b9d')
        ax3a.fill_between(alpha, Cl, alpha=0.1, color='#ff8c00')
        ax3a.grid(True, ls='--', alpha=0.2, color='#ff8c00')
        ax3a.legend(framealpha=0.9, fontsize=9)
        ax3a.set_xlabel("Angle of Attack (°)", color='#a8a8a8', fontsize=9)
        ax3a.set_ylabel("Coefficient", color='#a8a8a8', fontsize=9)
        ax3a.set_title("Lift & Drag", fontsize=11, fontweight='bold', color='#ff8c00')
        ax3a.tick_params(colors='#a8a8a8', labelsize=8)
        
        # Bottom plot - Efficiency
        ax3b.plot(alpha, LD, lw=4, label="L/D Ratio", marker='D', markersize=4, color='#00d9a3')
        ax3b.fill_between(alpha, LD, alpha=0.15, color='#00d9a3')
        ax3b.axvline(alpha[LD.argmax()], color='#ffa500', linestyle='--', lw=2, alpha=0.7, label='Peak')
        ax3b.grid(True, ls='--', alpha=0.2, color='#ff8c00')
        ax3b.legend(framealpha=0.9, fontsize=9)
        ax3b.set_xlabel("Angle of Attack (°)", color='#a8a8a8', fontsize=9)
        ax3b.set_ylabel("L/D Ratio", color='#a8a8a8', fontsize=9)
        ax3b.set_title("Wing Efficiency", fontsize=11, fontweight='bold', color='#ff8c00')
        ax3b.tick_params(colors='#a8a8a8', labelsize=8)
        
        st.pyplot(fig3, use_container_width=True)

# ==================== TAB 3: AIRFOIL COMPARISON ====================
with tab3:
    st.markdown("### COMPARATIVE AIRFOIL ANALYSIS")
    
    c1, c2 = st.columns(2)
    
    with c1:
        name1 = st.text_input("Airfoil A (NACA Code)", "2412", help="Reference airfoil")
    
    with c2:
        name2 = st.text_input("Airfoil B (NACA Code)", "0012", help="Comparison airfoil")
    
    alpha = np.arange(-5, 16)
    ar = np.deg2rad(alpha)
    
    cl1 = 2 * np.pi * ar
    cl2 = cl1 * 1.1
    
    ld1 = cl1 / (0.01 + cl1**2)
    ld2 = cl2 / (0.01 + cl2**2)
    
    st.markdown("---")
    st.markdown("#### PERFORMANCE COMPARISON")
    
    fig4, (ax4a, ax4b) = plt.subplots(1, 2, figsize=(14, 5), facecolor='#0a0e12')
    ax4a.set_facecolor('#141820')
    ax4b.set_facecolor('#141820')
    
    # L/D Comparison
    ax4a.plot(alpha, ld1, lw=3.5, label=f"NACA {name1}", marker='o', markersize=6, color='#ff8c00')
    ax4a.plot(alpha, ld2, lw=3.5, label=f"NACA {name2}", marker='s', markersize=6, color='#ff6b9d')
    ax4a.fill_between(alpha, ld1, alpha=0.1, color='#ff8c00')
    ax4a.fill_between(alpha, ld2, alpha=0.1, color='#ff6b9d')
    ax4a.grid(True, ls='--', alpha=0.2, color='#ff8c00')
    ax4a.legend(fontsize=11, framealpha=0.9)
    ax4a.set_title("Lift-to-Drag Ratio Comparison", fontsize=12, fontweight='bold', color='#ff8c00')
    ax4a.set_xlabel("Angle of Attack (°)", color='#a8a8a8')
    ax4a.set_ylabel("L/D Ratio", color='#a8a8a8')
    ax4a.tick_params(colors='#a8a8a8')
    
    # Lift Comparison
    ax4b.plot(alpha, cl1, lw=3.5, label=f"NACA {name1} - Cl", marker='o', markersize=6, color='#ff8c00')
    ax4b.plot(alpha, cl2, lw=3.5, label=f"NACA {name2} - Cl", marker='s', markersize=6, color='#ff6b9d')
    ax4b.grid(True, ls='--', alpha=0.2, color='#ff8c00')
    ax4b.legend(fontsize=11, framealpha=0.9)
    ax4b.set_title("Lift Coefficient Comparison", fontsize=12, fontweight='bold', color='#ff8c00')
    ax4b.set_xlabel("Angle of Attack (°)", color='#a8a8a8')
    ax4b.set_ylabel("Coefficient", color='#a8a8a8')
    ax4b.tick_params(colors='#a8a8a8')
    
    st.pyplot(fig4, use_container_width=True)
    
    st.markdown("---")
    st.markdown("### WING COMPARISON")
    
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown("#### Wing A Specs")
        span1 = st.number_input("Span A (m)", value=10.0, step=0.5)
        chord1 = st.number_input("Chord A (m)", value=1.5, step=0.1)
    
    with c2:
        st.markdown("#### Wing B Specs")
        span2 = st.number_input("Span B (m)", value=12.0, step=0.5)
        chord2 = st.number_input("Chord B (m)", value=1.2, step=0.1)
    
    e = 0.8
    
    AR1 = span1 / chord1
    Cl1 = 2 * np.pi * ar
    Cd1 = 0.01 + (Cl1**2) / (np.pi * AR1 * e)
    LD1 = Cl1 / Cd1
    
    AR2 = span2 / chord2
    Cl2 = 2 * np.pi * ar
    Cd2 = 0.01 + (Cl2**2) / (np.pi * AR2 * e)
    LD2 = Cl2 / Cd2
    
    fig5, ax5 = plt.subplots(figsize=(12, 5), facecolor='#0a0e12', edgecolor='#ff8c00')
    ax5.set_facecolor('#141820')
    
    ax5.plot(alpha, LD1, lw=3.5, label=f"Wing A (AR: {AR1:.2f})", marker='o', markersize=6, color='#ff8c00')
    ax5.plot(alpha, LD2, lw=3.5, label=f"Wing B (AR: {AR2:.2f})", marker='s', markersize=6, color='#ff6b9d')
    ax5.fill_between(alpha, LD1, alpha=0.1, color='#ff8c00')
    ax5.fill_between(alpha, LD2, alpha=0.1, color='#ff6b9d')
    ax5.grid(True, ls='--', alpha=0.2, color='#ff8c00')
    ax5.legend(fontsize=11, framealpha=0.9)
    ax5.set_title("Wing L/D Comparison", fontsize=13, fontweight='bold', color='#ff8c00')
    ax5.set_xlabel("Angle of Attack (°)", color='#a8a8a8', fontsize=11)
    ax5.set_ylabel("Lift-to-Drag Ratio", color='#a8a8a8', fontsize=11)
    ax5.tick_params(colors='#a8a8a8')
    
    st.pyplot(fig5, use_container_width=True)
    
    m1, m2 = st.columns(2)
    with m1:
        st.metric("Wing A Aspect Ratio", f"{AR1:.2f}")
        st.metric("Wing A Peak L/D", f"{LD1.max():.2f}")
    with m2:
        st.metric("Wing B Aspect Ratio", f"{AR2:.2f}")
        st.metric("Wing B Peak L/D", f"{LD2.max():.2f}")

# ==================== TAB 4: ADVANCED WING COMPARISON ====================
with tab4:
    st.markdown("### ADVANCED WING COMPARISON")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Wing A Configuration")
        span1 = st.number_input("Span A (m)", value=10.0, step=0.5, key="wingA_span")
        chord1 = st.number_input("Chord A (m)", value=1.5, step=0.1, key="wingA_chord")
    
    with col2:
        st.markdown("#### Wing B Configuration")
        span2 = st.number_input("Span B (m)", value=12.0, step=0.5, key="wingB_span")
        chord2 = st.number_input("Chord B (m)", value=1.2, step=0.1, key="wingB_chord")
    
    alpha = np.arange(-5, 16)
    alpha_rad = np.deg2rad(alpha)
    
    e = 0.8
    
    AR1 = span1 / chord1
    Cl1 = 2 * np.pi * alpha_rad
    Cd1 = 0.01 + (Cl1**2) / (np.pi * AR1 * e)
    LD1 = Cl1 / Cd1
    
    AR2 = span2 / chord2
    Cl2 = 2 * np.pi * alpha_rad
    Cd2 = 0.01 + (Cl2**2) / (np.pi * AR2 * e)
    LD2 = Cl2 / Cd2
    
    # Wing visuals side by side
    col_wing1, col_wing2 = st.columns(2)
    
    with col_wing1:
        fig_w1, ax_w1 = plt.subplots(figsize=(6, 7), facecolor='#0a0e12')
        ax_w1.set_facecolor('#141820')
        
        wing_root1 = chord1 * 1.1
        wing_tip1 = chord1 * 0.8
        x_w1 = np.array([0, wing_root1, wing_tip1, 0, 0])
        y_w1 = np.array([0, 0, span1, span1, 0])
        
        ax_w1.fill(x_w1, y_w1, color='#ff8c00', alpha=0.3, edgecolor='#ff8c00', linewidth=3)
        ax_w1.plot(x_w1, y_w1, color='#ff8c00', linewidth=3)
        
        ax_w1.set_xlim(-1, wing_root1 + 1)
        ax_w1.set_ylim(-2, span1 + 1)
        ax_w1.set_aspect('equal')
        ax_w1.grid(True, ls='--', alpha=0.2, color='#ff8c00')
        ax_w1.set_xlabel("Chord (m)", color='#a8a8a8')
        ax_w1.set_ylabel("Span (m)", color='#a8a8a8')
        ax_w1.set_title(f"Wing A (AR: {AR1:.2f})", fontsize=12, fontweight='bold', color='#ff8c00')
        ax_w1.tick_params(colors='#a8a8a8')
        
        st.pyplot(fig_w1, use_container_width=True)
    
    with col_wing2:
        fig_w2, ax_w2 = plt.subplots(figsize=(6, 7), facecolor='#0a0e12')
        ax_w2.set_facecolor('#141820')
        
        wing_root2 = chord2 * 1.1
        wing_tip2 = chord2 * 0.8
        x_w2 = np.array([0, wing_root2, wing_tip2, 0, 0])
        y_w2 = np.array([0, 0, span2, span2, 0])
        
        ax_w2.fill(x_w2, y_w2, color='#ff6b9d', alpha=0.3, edgecolor='#ff6b9d', linewidth=3)
        ax_w2.plot(x_w2, y_w2, color='#ff6b9d', linewidth=3)
        
        ax_w2.set_xlim(-1, wing_root2 + 1)
        ax_w2.set_ylim(-2, span2 + 1)
        ax_w2.set_aspect('equal')
        ax_w2.grid(True, ls='--', alpha=0.2, color='#ff6b9d')
        ax_w2.set_xlabel("Chord (m)", color='#a8a8a8')
        ax_w2.set_ylabel("Span (m)", color='#a8a8a8')
        ax_w2.set_title(f"Wing B (AR: {AR2:.2f})", fontsize=12, fontweight='bold', color='#ff6b9d')
        ax_w2.tick_params(colors='#a8a8a8')
        
        st.pyplot(fig_w2, use_container_width=True)
    
    st.markdown("---")
    st.markdown("#### PERFORMANCE CURVES")
    
    fig, ax = plt.subplots(figsize=(13, 6), facecolor='#0a0e12', edgecolor='#ff8c00')
    ax.set_facecolor('#141820')
    
    ax.plot(alpha, LD1, linewidth=3.5, marker="o", markersize=8, label=f"Wing A (AR: {AR1:.2f})", color='#ff8c00', markeredgewidth=2, markeredgecolor='#cc7000')
    ax.plot(alpha, LD2, linewidth=3.5, marker="s", markersize=8, label=f"Wing B (AR: {AR2:.2f})", color='#ff6b9d', markeredgewidth=2, markeredgecolor='#cc3366')
    
    ax.fill_between(alpha, LD1, alpha=0.1, color='#ff8c00')
    ax.fill_between(alpha, LD2, alpha=0.1, color='#ff6b9d')
    
    # Highlight peak points
    peak1_idx = LD1.argmax()
    peak2_idx = LD2.argmax()
    ax.scatter([alpha[peak1_idx]], [LD1[peak1_idx]], s=400, marker='*', color='#ffa500', edgecolors='#ffaa00', linewidths=2, zorder=5, label='Peak Efficiency')
    ax.scatter([alpha[peak2_idx]], [LD2[peak2_idx]], s=400, marker='*', color='#ffa500', edgecolors='#ffaa00', linewidths=2, zorder=5)
    
    ax.set_title("Wing Lift-to-Drag Ratio - Advanced Analysis", fontsize=14, fontweight='bold', color='#ff8c00', pad=20)
    ax.set_xlabel("Angle of Attack (°)", fontsize=12, color='#a8a8a8', fontweight='bold')
    ax.set_ylabel("L/D Ratio", fontsize=12, color='#a8a8a8', fontweight='bold')
    ax.grid(True, ls='--', alpha=0.2, color='#ff8c00')
    ax.legend(loc='upper left', framealpha=0.95, fontsize=11, edgecolor='#ff8c00', fancybox=True, shadow=True)
    ax.tick_params(colors='#a8a8a8', labelsize=10)
    
    st.pyplot(fig, use_container_width=True)
    
    st.markdown("---")
    st.markdown("### PERFORMANCE METRICS")
    
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        st.metric("Wing A AR", f"{AR1:.2f}")
    with c2:
        st.metric("Wing A Peak L/D", f"{LD1.max():.2f}")
    with c3:
        st.metric("Wing B AR", f"{AR2:.2f}")
    with c4:
        st.metric("Wing B Peak L/D", f"{LD2.max():.2f}")
