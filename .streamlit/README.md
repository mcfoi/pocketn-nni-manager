The content of *config.toml* is intentionally left empty, as all configurations are performed using CLI args when starting the Streamlit App.<br/>

This is done in a couple of places:<br/>
- during **DEVELOPEMENT**, in .vscode/launch.json script by setting "args" (for Streamlit configuration) and "envs" (for ENVIRONMENT VARIABLES to make available in image)
- during **PRODUCTION**, adding to `Dockerfile`, in `ENTRYPOINT` line, all configurations (e.g.: "--server.enableStaticServing=true")