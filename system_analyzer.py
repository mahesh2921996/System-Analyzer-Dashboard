# Importing necessary libraries
import streamlit as st
# import altair as alt
from streamlit_option_menu import option_menu
import plotly.express as px
import plotly.graph_objects as go
from systemprocessor.system_processor import SystemProcessor
from functions.manage_db import entry_into_serverinfo_table, get_serverinfo
import os

selected_server_name = None
path = None
all_files = None
prof_df = None

# Initialiting and set the layout of page.
sys_processor_obj = SystemProcessor()
st.set_page_config(layout="wide")
st.title("System Analyzer Dashboard")

#------------------- Add server----------------------------
st.subheader("Add server")

def add_db_list():
    entry_into_serverinfo_table(1, server_name, server_path)
    st.session_state["name"] = ""
    st.session_state["path"] = ""

server_name = st.text_input("Server Name", key="name")
server_path = st.text_input("Server Path", key="path")

st.button(label="Submit", on_click=add_db_list)

#----------------------------------------------------------------------------------------------------

#------------------------------------ Choose Server -------------------------------------------------

df_db = get_serverinfo()

if len(df_db["Server_Name"].to_list()) != 0:

    selected_server_name = option_menu("Choose Server", df_db["Server_Name"].to_list())

#----------------------------------------------------------------------------------------------------

#-------------------- Overall summary --------------------------------------------------------
if selected_server_name!=None:
    st.header(f"Overall statistics of {selected_server_name} server.")
    # st.markdown("<h1 style=\"text-align: center;\">Overall statistics of server.</h1>")

    for i in range(len(df_db)):
        if df_db["Server_Name"].at[i] == selected_server_name:
            path = df_db["Server_Sytem_Path"].at[i]

    if len(path) != 0:
        all_files = [files for root, dirs, files in os.walk(path + "\\system_info")]

    # if all_files != None:
    prof_df = sys_processor_obj.create_df_from_prof_folder(all_files[0])

    # print(prof_df)
    columns = st.columns(3)
    # if prof_df != None:
    x = prof_df["method"].value_counts()

    with columns[0]:
        with st.container():
            st.subheader("Usage of Http Methods")
            fig = go.Figure(
                go.Pie(
                    labels=x.index,
                    values=x,
                    hoverinfo="value",
                    textinfo="label+percent"
                ))
            st.plotly_chart(fig, use_container_width=True)

    tem_fun_time = prof_df.groupby(by=["server_function", "method"])[["time"]].sum()

    tem_fun_time["server_function"] = tem_fun_time.index.get_level_values(0)
    tem_fun_time["method"] = tem_fun_time.index.get_level_values(1)

    with columns[1]:
        with st.container():
            st.subheader("Server Time Performance Breakdown")
            fig = px.bar(data_frame=tem_fun_time, x=tem_fun_time["method"], y="time",
                         color=tem_fun_time["server_function"], barmode='group', width=450)  # width=500

            st.write(fig, use_container_width=True)

    # print(tem_fun_time)

    with columns[2]:
        with st.container():
            st.subheader("Total Time Distribution Across Server Functions")
            fig = px.bar_polar(tem_fun_time, r='time', theta='server_function')
            # fig = go.Figure(
            #     go.Pie(
            #     labels = tem_fun_time.index.get_level_values(0),
            #     values = tem_fun_time["time"],
            #     hoverinfo = "value",
            #     textinfo = "label+percent"
            # ))
            st.plotly_chart(fig, use_container_width=True)

    # --------------------------------end overall summary of server --------------------------------------
    ######################################################################################

    st.header("Concise summaries of individual profile files.")

    selected_files = st.selectbox("Select Files", all_files[0])

    df = sys_processor_obj.create_df_from_prof_files(path,
                                                     selected_files)  # D:\iasys\practice\poc_system_dashboard\profiles\GET.root.1ms.1697973785.prof

    copy_df = df.copy()

    # Count the number of files in each directory
    df_1 = copy_df.groupby(['short_path']).size().reset_index()

    df_1.columns = ["short_path", "frequency"]

    columns = st.columns(1)

    with columns[0]:

        with st.container():
            st.subheader("Frequency of System Files")
            fig = px.bar(df_1, x='frequency', y='short_path', orientation='h', width=1200)
            st.write(fig, use_container_width=True)

    ######################################################################################################

    columns = st.columns(3)

    x = copy_df["directory"].value_counts()

    with columns[0]:

        with st.container():
            st.subheader("Summary of System Directory")
            fig = go.Figure(
                go.Pie(
                    labels=x.index,
                    values=x,
                    hoverinfo="label+percent",
                    textinfo="value"
                ))
            st.plotly_chart(fig, use_container_width=True)

    x = copy_df["drive"].value_counts()
    with columns[1]:

        with st.container():
            st.subheader("Summary of System Drive's Usage")
            fig = px.bar(x, x=x.index, y=x, width=500)
            st.write(fig, use_container_width=True)

    tem = copy_df.groupby(by=["function"])
    call_function = tem[["ncalls"]].count().sort_values("ncalls", ascending=False)[:10]

    with columns[2]:

        with st.container():
            st.subheader("Top 10 call's of function.")

            fig = px.line(call_function, x=list(call_function.index), y="ncalls")
            st.write(fig, use_container_width=True)
