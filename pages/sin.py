import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.animation import FuncAnimation
import time

st.set_page_config(page_title="사인 함수 시각화", layout="wide")
st.title("📊 사인 함수 시각화: 단위원에서 그래프까지")

# 사이드바에서 컨트롤 설정
st.sidebar.header("⚙️ 컨트롤")

# 각도 조절 슬라이더 (도 단위)
animate = st.sidebar.checkbox("🎬 애니메이션 시작", value=False)
angle_deg = st.sidebar.slider("각도 (°)", min_value=0, max_value=360, value=45, step=1)

# 애니메이션 속도
if animate:
    animation_speed = st.sidebar.slider("애니메이션 속도", min_value=0.01, max_value=0.5, value=0.1, step=0.01)
else:
    animation_speed = 0.1

# 각도를 라디안으로 변환
angle_rad = np.radians(angle_deg)

# 레이아웃 설정: 왼쪽에 단위원, 오른쪽에 사인 그래프
col1, col2 = st.columns(2)

with col1:
    st.subheader("🔵 단위원")
    
    # 단위원 시각화
    fig1, ax1 = plt.subplots(figsize=(6, 6))
    
    # 단위원 그리기
    circle = Circle((0, 0), 1, fill=False, color='blue', linewidth=2)
    ax1.add_patch(circle)
    
    # 좌표축 그리기
    ax1.axhline(y=0, color='k', linewidth=0.5)
    ax1.axvline(x=0, color='k', linewidth=0.5)
    ax1.grid(True, alpha=0.3)
    
    # 각도 선 그리기
    x_point = np.cos(angle_rad)
    y_point = np.sin(angle_rad)
    
    # 원점에서 점까지의 선
    ax1.plot([0, x_point], [0, y_point], 'r-', linewidth=2.5, label=f'θ = {angle_deg}°')
    
    # 점 표시
    ax1.plot(x_point, y_point, 'ro', markersize=10)
    
    # sin(θ) 값을 y축으로 표시 (수직선)
    ax1.plot([x_point, x_point], [0, y_point], 'g--', linewidth=2, alpha=0.7, label=f'sin(θ) = {y_point:.3f}')
    
    # cos(θ) 값을 x축으로 표시 (수평선)
    ax1.plot([0, x_point], [y_point, y_point], 'orange', linestyle='--', linewidth=2, alpha=0.7, label=f'cos(θ) = {x_point:.3f}')
    
    # 점의 좌표 표시
    ax1.text(x_point + 0.1, y_point + 0.1, f'({x_point:.2f}, {y_point:.2f})', fontsize=10, fontweight='bold')
    
    # sin(θ) 값을 y축 위에 표시
    ax1.plot([-0.15, 0], [y_point, y_point], 'g-', linewidth=3)
    ax1.text(-0.35, y_point, f'{y_point:.3f}', fontsize=10, color='green', fontweight='bold')
    
    ax1.set_xlim(-1.5, 1.5)
    ax1.set_ylim(-1.5, 1.5)
    ax1.set_aspect('equal')
    ax1.set_xlabel('cos(θ)', fontsize=12)
    ax1.set_ylabel('sin(θ)', fontsize=12)
    ax1.legend(loc='upper right', fontsize=10)
    ax1.set_title(f'각도: {angle_deg}°', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    st.pyplot(fig1)

with col2:
    st.subheader("📈 사인 그래프")
    
    # 사인 그래프 시각화
    fig2, ax2 = plt.subplots(figsize=(6, 6))
    
    # 전체 사인 곡선 (옅은 색으로)
    x_full = np.linspace(0, 2 * np.pi, 500)
    y_full = np.sin(x_full)
    ax2.plot(x_full, y_full, 'b--', linewidth=1, alpha=0.3, label='전체 사인 함수')
    
    # 현재 각도까지의 사인 곡선 (채워진 색으로)
    x_partial = np.linspace(0, angle_rad, 100)
    y_partial = np.sin(x_partial)
    ax2.plot(x_partial, y_partial, 'b-', linewidth=3, label='현재까지의 함수')
    ax2.fill_between(x_partial, 0, y_partial, alpha=0.3, color='blue')
    
    # 현재 점
    ax2.plot(angle_rad, y_point, 'ro', markersize=10, label=f'현재 점: ({angle_rad:.3f}, {y_point:.3f})')
    
    # 연결선: 단위원에서 그래프로 (시각적 연결)
    ax2.plot([angle_rad, angle_rad], [0, y_point], 'g--', linewidth=2, alpha=0.7)
    ax2.plot([0, angle_rad], [y_point, y_point], 'orange', linestyle=':', linewidth=2, alpha=0.5)
    
    # 좌표축 표시
    ax2.axhline(y=0, color='k', linewidth=0.5)
    ax2.axvline(x=0, color='k', linewidth=0.5)
    ax2.grid(True, alpha=0.3)
    
    # 레이블 설정
    ax2.set_xlim(-0.2, 2 * np.pi + 0.2)
    ax2.set_ylim(-1.5, 1.5)
    
    # x축 레이블 (라디안과 도)
    ax2.set_xticks([0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi])
    ax2.set_xticklabels(['0', 'π/2', 'π', '3π/2', '2π'])
    ax2.set_xlabel('각도 (라디안)', fontsize=12)
    ax2.set_ylabel('sin(θ)', fontsize=12)
    ax2.legend(loc='upper right', fontsize=10)
    ax2.set_title(f'사인 함수 (θ = {angle_deg}° = {angle_rad:.3f} rad)', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    st.pyplot(fig2)

# 정보 표시 섹션
st.divider()
st.subheader("📝 현재 값")

info_col1, info_col2, info_col3, info_col4 = st.columns(4)

with info_col1:
    st.metric("각도 (도)", f"{angle_deg}°")

with info_col2:
    st.metric("각도 (라디안)", f"{angle_rad:.4f}")

with info_col3:
    st.metric("sin(θ)", f"{y_point:.4f}")

with info_col4:
    st.metric("cos(θ)", f"{x_point:.4f}")

# 애니메이션 로직
if animate:
    placeholder = st.empty()
    progress_bar = st.progress(0)
    
    # session state에서 현재 각도 추적
    if 'current_angle' not in st.session_state:
        st.session_state.current_angle = 0
    
    # 애니메이션 실행
    for i in range(360):
        st.session_state.current_angle = (st.session_state.current_angle + animation_speed * 10) % 360
        progress_bar.progress(int(st.session_state.current_angle) / 360)
        time.sleep(0.05)
        st.rerun()

# 설명 섹션
st.divider()
st.subheader("💡 설명")

explanation_col1, explanation_col2 = st.columns(2)

with explanation_col1:
    st.write("""
    **단위원 (왼쪽)**
    - 반지름이 1인 원 위의 점이 각도 θ에 따라 이동
    - **빨간 선**: 각도 θ를 나타내는 반지름
    - **초록 점선**: y좌표 = sin(θ)
    - **주황 점선**: x좌표 = cos(θ)
    """)

with explanation_col2:
    st.write("""
    **사인 그래프 (오른쪽)**
    - 각도 0°부터 현재 각도까지의 사인 함수
    - **파란 실선**: 현재까지 그려진 함수
    - **파란 점선**: 전체 사인 함수
    - **초록 점선**: 단위원의 y값을 그래프로 표시
    """)

st.info(
    "🎯 **핵심 개념**: 단위원에서 점의 y좌표가 바로 sin(θ) 값이며, "
    "이것이 각도에 따라 변하는 모습을 사인 그래프로 표현할 수 있습니다!"
)
