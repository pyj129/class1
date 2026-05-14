import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from fractions import Fraction
import time

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(page_title="Sine Function Visualization", layout="wide")

# matplotlib 설정 - 한글 폰트 지원
try:
    plt.rcParams['font.family'] = 'AppleGothic'  # Mac
except Exception:
    try:
        plt.rcParams['font.family'] = 'Malgun Gothic'  # Windows
    except Exception:
        plt.rcParams['font.family'] = 'DejaVu Sans'  # Fallback
plt.rcParams['axes.unicode_minus'] = False


def format_angle_as_pi(value: float) -> str:
    frac = Fraction(value / np.pi).limit_denominator(12)
    numerator, denominator = frac.numerator, frac.denominator
    if numerator == 0:
        return "0"
    if denominator == 1:
        return f"{numerator}π" if numerator != 1 else "π"
    if numerator == -1:
        return f"-π/{denominator}"
    if numerator == 1:
        return f"π/{denominator}"
    return f"{numerator}π/{denominator}"

st.title("📈 Sine Function Visualization: From Unit Circle to Graph")

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================
if 'prev_angle_rad' not in st.session_state:
    st.session_state.prev_angle_rad = np.pi / 4
    st.session_state.current_animation_angle = np.pi / 4

# ============================================================================
# SIDEBAR CONTROLS
# ============================================================================
st.sidebar.header("⚙️ Controls")

angle_input_method = st.sidebar.radio(
    "Angle input method",
    ["Slider", "Number input"],
    index=0
)

angle_step = np.pi * 15 / 180

if angle_input_method == "Slider":
    angle_rad = st.sidebar.slider(
        "Angle (radians)",
        min_value=0.0,
        max_value=2 * np.pi,
        value=np.pi / 4,
        step=angle_step
    )
else:
    angle_rad = st.sidebar.number_input(
        "Angle (radians)",
        min_value=0.0,
        max_value=2 * np.pi,
        value=np.pi / 4,
        step=angle_step,
        format="%.3f"
    )

animate = st.sidebar.checkbox("🎬 Start animation", value=False)

animation_speed = 0.05
if animate:
    animation_speed = st.sidebar.slider(
        "Animation speed",
        min_value=0.01,
        max_value=0.5,
        value=0.05,
        step=0.01
    )
    st.sidebar.info("ℹ️ Angle will automatically increment by 15° (π/12) during animation")

# ============================================================================
# STATE MANAGEMENT FOR ANGLE
# ============================================================================
angle_changed = abs(st.session_state.prev_angle_rad - angle_rad) > 1e-6
if angle_changed:
    st.session_state.prev_angle_rad = angle_rad
    if not animate:
        st.session_state.current_animation_angle = angle_rad

if animate:
    current_angle_rad = st.session_state.current_animation_angle
else:
    current_angle_rad = angle_rad

angle_deg = np.degrees(current_angle_rad)
angle_pi = format_angle_as_pi(current_angle_rad)

x_point = np.cos(current_angle_rad)
y_point = np.sin(current_angle_rad)

# ============================================================================
# MAIN CONTENT
# ============================================================================
col1, col2 = st.columns(2)

with col1:
    st.subheader("🔵 Unit Circle")

    fig1 = plt.figure(figsize=(6, 6))
    ax1 = fig1.add_subplot(111)

    circle = Circle((0, 0), 1, fill=False, color='blue', linewidth=2)
    ax1.add_patch(circle)
    ax1.axhline(y=0, color='k', linewidth=0.5)
    ax1.axvline(x=0, color='k', linewidth=0.5)
    ax1.grid(True, alpha=0.3)

    ax1.plot([0, x_point], [0, y_point], 'r-', linewidth=2.5, label=f'θ = {angle_pi} ({angle_deg:.0f}°)')
    ax1.plot(x_point, y_point, 'ro', markersize=10)

    ax1.plot([x_point, x_point], [0, y_point], 'g-', linewidth=3, alpha=0.8, label=f'sin(θ) = {y_point:.3f}')
    ax1.plot([0, x_point], [y_point, y_point], 'orange', linestyle='--', linewidth=1.5, alpha=0.6, label=f'cos(θ) = {x_point:.3f}')

    ax1.text(x_point + 0.1, y_point + 0.1, f'({x_point:.2f}, {y_point:.2f})', fontsize=10, fontweight='bold')
    ax1.plot([-0.15, 0], [y_point, y_point], 'green', linewidth=4)
    ax1.text(-0.35, y_point, f'sin({angle_pi}) = {y_point:.3f}', fontsize=11, color='green', fontweight='bold', va='center', ha='right')

    ax1.set_xlim(-1.8, 1.8)
    ax1.set_ylim(-1.5, 1.5)
    ax1.set_aspect('equal')
    ax1.set_xlabel('cos(θ)', fontsize=12)
    ax1.set_ylabel('sin(θ)', fontsize=12)
    ax1.legend(loc='upper right', fontsize=9)
    ax1.set_title(f'Unit Circle: θ = {angle_pi}', fontsize=14, fontweight='bold')

    st.pyplot(fig1)
    plt.close(fig1)

with col2:
    st.subheader("📈 Sine Graph")

    fig2 = plt.figure(figsize=(6, 6))
    ax2 = fig2.add_subplot(111)

    x_full = np.linspace(0, 2 * np.pi, 500)
    y_full = np.sin(x_full)
    ax2.plot(x_full, y_full, color='gray', linestyle='--', linewidth=1, alpha=0.4, label='Full sine function')

    x_partial = np.linspace(0, current_angle_rad, 100)
    y_partial = np.sin(x_partial)
    ax2.plot(x_partial, y_partial, 'b-', linewidth=4, label='Function up to current angle')
    ax2.fill_between(x_partial, 0, y_partial, alpha=0.4, color='lightblue')

    ax2.plot(current_angle_rad, y_point, 'ro', markersize=12, markeredgecolor='darkred', markeredgewidth=2, label=f'Current point: θ = {angle_pi}')
    ax2.plot([current_angle_rad, current_angle_rad], [0, y_point], 'green', linewidth=3, alpha=0.8, label=f'sin({angle_pi}) = {y_point:.3f}')

    ax2.plot([-0.3, -0.1], [y_point, y_point], 'purple', linewidth=2, alpha=0.7)
    ax2.text(-0.4, y_point, f'y = {y_point:.3f}', fontsize=10, color='purple', fontweight='bold', va='center', ha='right')

    ax2.axhline(y=0, color='k', linewidth=0.8)
    ax2.axvline(x=0, color='k', linewidth=0.8)
    ax2.grid(True, alpha=0.3)
    ax2.axvline(x=current_angle_rad, color='red', linestyle=':', linewidth=1.5, alpha=0.6)

    ax2.set_xlim(-0.5, 2 * np.pi + 0.2)
    ax2.set_ylim(-1.5, 1.5)
    ax2.set_xticks([0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi])
    ax2.set_xticklabels(['0', 'π/2', 'π', '3π/2', '2π'])
    ax2.set_xlabel('Angle (radians)', fontsize=12)
    ax2.set_ylabel('sin(θ)', fontsize=12)
    ax2.legend(loc='upper right', fontsize=9)
    ax2.set_title(f'Sine Function: sin({angle_pi}) = {y_point:.3f}', fontsize=14, fontweight='bold')

    st.pyplot(fig2)
    plt.close(fig2)

# ============================================================================
# ANIMATION LOGIC
# ============================================================================
if animate:
    st.session_state.current_animation_angle = (st.session_state.current_animation_angle + angle_step) % (2 * np.pi)
    time.sleep(animation_speed)
    st.rerun()
    


