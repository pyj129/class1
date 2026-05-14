import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from streamlit_drawable_canvas import st_canvas
from scipy.interpolate import interp1d
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="What is Most Similar", layout="wide")
st.title("🎨 What is Most Similar: Draw the Sine Function!")

st.markdown("사인 함수를 캔버스에 그려보세요. 실제 사인 함수와의 유사도를 측정합니다.")

# ============================================================================
# SETTINGS
# ============================================================================
st.sidebar.header("⚙️ Canvas Settings")
canvas_width = st.sidebar.slider("Canvas Width", 500, 800, 700)
canvas_height = st.sidebar.slider("Canvas Height", 300, 500, 400)
stroke_width = st.sidebar.slider("Stroke Width", 1, 20, 3)

# ============================================================================
# CREATE BACKGROUND IMAGE
# ============================================================================
def create_sine_background(width, height):
    """배경에 사인 함수를 점선으로 표시"""
    fig, ax = plt.subplots(figsize=(width/100, height/100), dpi=100)
    fig.patch.set_facecolor('white')
    
    ax.set_xlim(0, width)
    ax.set_ylim(0, height)
    
    # 사인 함수 계산 (0 ~ 2π)
    x_math = np.linspace(0, 2*np.pi, 300)
    y_math = np.sin(x_math)
    
    # Canvas 좌표로 변환
    x_canvas = (x_math / (2*np.pi)) * width
    y_canvas = height/2 - (y_math * height/2.5)
    
    ax.plot(x_canvas, y_canvas, 'gray', linestyle=':', linewidth=2, alpha=0.6)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.axis('off')
    
    fig.tight_layout(pad=0)
    fig.canvas.draw()
    image = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
    image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    plt.close(fig)
    
    return image

bg_image = create_sine_background(canvas_width, canvas_height)

# ============================================================================
# CANVAS
# ============================================================================
st.subheader("✏️ Draw the Sine Function")

canvas_result = st_canvas(
    fill_color="rgba(0,0,0,0)",
    stroke_width=stroke_width,
    stroke_color="#000000",
    background_image=bg_image,
    height=canvas_height,
    width=canvas_width,
    drawing_mode="freedraw",
    key="canvas_sine"
)

# ============================================================================
# ANALYSIS
# ============================================================================
if canvas_result.image_data is not None:
    st.subheader("📊 Analysis Results")
    
    try:
        # 그림 이미지에서 좌표 추출 (검은색 픽셀 찾기)
        img = canvas_result.image_data
        black_pixels = np.where((img[:,:,0] < 50) & (img[:,:,1] < 50) & (img[:,:,2] < 50) & (img[:,:,3] > 200))
        
        if len(black_pixels[0]) > 20:
            # 검은색 픽셀 좌표 정렬
            coords = np.column_stack((black_pixels[1], black_pixels[0]))  # (x, y)
            coords = coords[np.argsort(coords[:, 0])]
            
            # 중복 제거 (x 기준)
            unique_x_indices = np.unique(coords[:, 0], return_index=True)[1]
            coords = coords[unique_x_indices]
            
            if len(coords) > 10:
                x_canvas = coords[:, 0].astype(float)
                y_canvas = coords[:, 1].astype(float)
                
                # Canvas 좌표 → 수학 좌표
                x_math = (x_canvas / canvas_width) * 2 * np.pi
                y_math = (canvas_height/2 - y_canvas) / (canvas_height/2.5)
                
                # 유효한 범위로 제한
                valid_mask = (y_math >= -2) & (y_math <= 2)
                x_math = x_math[valid_mask]
                y_math = y_math[valid_mask]
                
                if len(x_math) > 10:
                    # 보간
                    x_interp = np.linspace(0, 2*np.pi, 100)
                    
                    try:
                        f = interp1d(x_math, y_math, kind='linear', bounds_error=False, fill_value='extrapolate')
                        y_interp = f(x_interp)
                        y_interp = np.clip(y_interp, -2, 2)
                        
                        # 실제 사인 함수
                        y_actual = np.sin(x_interp)
                        
                        # MSE 점수
                        mse = np.mean((y_interp - y_actual) ** 2)
                        mse_score = max(0, 100 - mse * 50)
                        
                        # 코사인 유사도
                        cos_sim = cosine_similarity([y_interp], [y_actual])[0][0]
                        cos_pct = (cos_sim + 1) / 2 * 100
                        
                        # 결과 표시
                        col1, col2, col3 = st.columns(3)
                        col1.metric("MSE Score", f"{mse_score:.1f}")
                        col2.metric("Similarity", f"{cos_pct:.1f}%")
                        
                        with col3:
                            if mse_score > 80:
                                st.success("🎉 Excellent!")
                            elif mse_score > 60:
                                st.info("👍 Good!")
                            else:
                                st.warning("Keep trying!")
                        
                        # 비교 그래프
                        st.subheader("📈 Comparison")
                        fig, ax = plt.subplots(figsize=(10, 5))
                        
                        x_full = np.linspace(0, 2*np.pi, 300)
                        y_full = np.sin(x_full)
                        
                        ax.plot(x_full, y_full, 'b-', linewidth=3, label='Actual Sine', alpha=0.7)
                        ax.plot(x_interp, y_interp, 'r-', linewidth=2.5, label='Your Drawing', alpha=0.8)
                        ax.scatter(x_math, y_math, color='red', s=30, alpha=0.5)
                        
                        ax.set_xlim(0, 2*np.pi)
                        ax.set_ylim(-1.5, 1.5)
                        ax.set_xlabel('Angle (radians)')
                        ax.set_ylabel('sin(θ)')
                        ax.legend()
                        ax.grid(True, alpha=0.3)
                        ax.set_xticks([0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi])
                        ax.set_xticklabels(['0', 'π/2', 'π', '3π/2', '2π'])
                        
                        st.pyplot(fig)
                        plt.close(fig)
                    
                    except Exception as e:
                        st.error(f"보간 오류: {str(e)}")
                else:
                    st.info("더 많은 점을 그려주세요")
            else:
                st.info("캔버스에 선을 그려주세요")
        else:
            st.info("캔버스에 선을 그려주세요")
    
    except Exception as e:
        st.error(f"분석 오류: {str(e)}")
    


