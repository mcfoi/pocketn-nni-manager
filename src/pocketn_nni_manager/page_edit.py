import logging
import pandas as pd
import streamlit as st

from pocketn_nni_manager.dbhelper import DbHelper, Varietà, getInstance

def editPage():
    _logger = logging.getLogger(__name__)
    # List page content
    st.markdown("## Modifica varietà")
    # st.sidebar.markdown("###    Lista varietà")
    # st.sidebar.markdown("### ➡ Modifica varietà")

    db = getInstance()
    varList: list[Varietà] = db.getVarieties()
    varCur = db.getVarietiesCursor()
    serverPdDf = db.getVarietiesPdDataframe()
    # serverPdDf.set_index('id', inplace=True)
    hash_before = pd.util.hash_pandas_object(serverPdDf)
    _logger.info(f"hash_before : {hash_before}")
    userPdDf = st.data_editor(serverPdDf,
        key="varieties_editor",
        num_rows="dynamic",
        column_config={
            "id": "ID",
            "name": "Varietà (name)",
            "m": st.column_config.NumberColumn("Inclinazione (m)",format="%.3f",step=0.010),
            "q": st.column_config.NumberColumn("Intercetta (q)",format="%.3f",step=0.010),
        },
        disabled=["id"],
        on_change=persistChanges,
        # args=(varDf,_logger),
        kwargs={"serverPdDf": serverPdDf, "logger": _logger}
        )
    hash_after = pd.util.hash_pandas_object(userPdDf)
    _logger.info(f"hash_after : {hash_after}")
    _logger.info(f"OUTPUT data is (might be unmodified)\n{userPdDf}")
    # Access the changes in st.session_state after user interaction
    changes = st.session_state["varieties_editor"]
    if changes["edited_rows"]:
        _logger.info("#### Edited Rows:\n")
        _logger.info(changes["edited_rows"])
    if changes["added_rows"]:
        _logger.info("#### Added Rows:\n")
        _logger.info(changes["added_rows"])
    if changes["deleted_rows"]:
        _logger.info("#### Deleted Rows:\n")
        _logger.info(changes["deleted_rows"])
    _logger.info(f"Displayed {len(serverPdDf)} varieties.")
    _logger.info(f"= = = = = = = =")

    if st.button("Salva modifiche", type="primary", kwargs={"serverPdDf": serverPdDf, "logger": _logger}):
        salvaModifiche(serverPdDf=serverPdDf, logger=_logger)

def salvaModifiche(**kwargs):
    _logger = kwargs["logger"]
    serverPdDf: pd.DataFrame = kwargs["serverPdDf"]
    changes = st.session_state["varieties_editor"]

    if changes["edited_rows"]:
        db = getInstance()
        updated_ids = []
        for editedRowPosition in changes["edited_rows"]:
            id = serverPdDf["id"].iloc[editedRowPosition]
            row = changes["edited_rows"][editedRowPosition]
            set_clause = ""
            set_spacer = ""
            for edited_column in row:
                edited_value = row[edited_column]
                serverPdDf.at[editedRowPosition, edited_column] = edited_value
                set_clause += f"{set_spacer}{edited_column} = "
                if isinstance(edited_value, str):
                    set_clause += f"'{edited_value}'"
                else:
                    set_clause += f"{edited_value}"
                set_spacer = ", "
            sql_update = f"UPDATE varieties SET {set_clause} WHERE id = {id}"
            db.execute(sql_update)
            updated_ids.append(id)
        st.success(f"Varietà con ID {', '.join(map(str, updated_ids))} aggiornat{'a' if len(updated_ids) == 1 else 'e'} correttamente.")

    if changes["added_rows"]:
        pass

def persistChanges(*args, **kwargs):
    _logger = kwargs["logger"]
    serverPdDf = kwargs["serverPdDf"]
    _logger.info(f"ORIGINAL Dataframe data in persistChanges() is\n{serverPdDf}")
