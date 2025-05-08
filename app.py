import streamlit as st
from moviepy.editor import ImageClip
import tempfile
import os
import uuid

st.title("🏡 Immo Foto naar Video Tool")
st.write("Upload een foto van een woning en krijg een korte video met een animatie.")

# Bestandsupload
uploaded_file = st.file_uploader("Upload een afbeelding (JPEG of PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_image:
        temp_image.write(uploaded_file.read())
        image_path = temp_image.name

    st.image(image_path, caption="Voorbeeld van je afbeelding", use_column_width=True)

    # Start knop
    if st.button("Maak video"):
        with st.spinner("Video genereren..."):
            # Tijdelijke bestandsnaam
            output_path = os.path.join(tempfile.gettempdir(), f"{uuid.uuid4()}.mp4")

            # Maak clip en zoom effect
            clip = ImageClip(image_path).set_duration(5)
            zoomed_clip = clip.fx(lambda gf, t: clip.resize(1 + 0.05 * t))  # lichte zoom-in
            zoomed_clip.write_videofile(output_path, fps=24, audio=False)

            # Toon video en downloadlink
            st.video(output_path)
            with open(output_path, "rb") as f:
                st.download_button("Download video", f, file_name="woning_video.mp4")
