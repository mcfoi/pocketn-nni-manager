The content of whis directory:
- during "docker build" of Dockerfile, shall be copied into image, in folder specified by ENV VAR named 'STREAMLIT_DATA_DIR' (e.g.:/usr/src/app)
- eventually published as Docker VOLUME