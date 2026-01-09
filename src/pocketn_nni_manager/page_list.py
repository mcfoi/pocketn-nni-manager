import logging
import streamlit as st

from pocketn_nni_manager.dbhelper import DbHelper, Varietà, getInstance

def f(x:range, m:float, q:float) -> list:
    return [m * xi + q for xi in x]

def getLineFigure(x, m, q):
    import matplotlib.pyplot as plt
    plt.figure()
    y = [f(xi, m, q) for xi in x]
    plt.plot(x, y, label=f'f(x) = {m}x + {q}')
    plt.title('Grafico di f(x)')
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.legend()
    fig = plt.gcf()
    return fig

def listPage():
    _logger = logging.getLogger("NNIManager")
    # List page content
    st.markdown("## Lista varietà")
    # st.sidebar.markdown("### ➡ Lista varietà")
    # st.sidebar.markdown("###    Modifica varietà")

    db = getInstance()
    # varList: list[Varietà] = db.getVarieties()
    # varCur = db.getVarietiesCursor()
    varDf = db.getVarietiesPdDataframe()
    x_range = range(0, 5)
    varDf['grafco'] = varDf.apply(lambda row: f(x_range, row.m, row.q), axis=1)
    st.dataframe(
        varDf,
        key="varieties_table",
        row_height=100,
        column_config={
            "id": "ID Varietà",
            "name": "Nome Varietà",
            "m": "Parametro m",
            "q": "Parametro q",
            "nni_cap": "Limite NNI",
            "grafco": st.column_config.LineChartColumn("Curva di calibrazione", y_min=-5, y_max=5, width=10),
        }
        )

    _logger.info(f"Displayed {len(varDf)} varieties.")