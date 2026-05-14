import streamlit as st

st.set_page_config(
    page_title="수학 시각화 앱",
    page_icon="📐",
    layout="wide"
)

st.title("📐 Mathematics Visualization App")
st.write("Select a page from the sidebar to explore different mathematical concepts interactively!")

st.divider()

st.subheader("📚 Available Pages")
st.write("• **Sine Function Visualization**: From unit circle to graph")
st.write("• **Cosine Function Visualization**: From unit circle to graph")

st.info("💡 Select any page to explore the mathematical concept interactively.")
