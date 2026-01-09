The content of whis directory:
- during "docker build" of Dockerfile, shall be copied into image, in folder specified by ENV VAR named 'STREAMLIT_DATA_DIR' (e.g.:/usr/src/app)
- eventually published as Docker VOLUME

NOTE:
- varieties.csv : is REQUIRED and will be used to polulate the DATABASE
- nni_manager.db : if present in the folder AND the SQLITE3 is the adopted DB-ENGINE, then will be used as PRODUCTION DB