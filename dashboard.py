import streamlit as st
from config import *
import pandas as pd
import numpy as np
import plotly.graph_objects as go 
import json
import requests
import ast
from helper_functions import *


# Layout the app
st.set_page_config(layout="wide")

st.title("PRÊT À DÉPENSER")

# Get clients' main data
@st.cache(allow_output_mutation=True)
def load_data():
    req = requests.get(API_URL+"applications")
    contents = json.loads(req.content.decode("utf-8"))
    json_contents = json.loads(contents)
    app_data = pd.DataFrame(data=json_contents)

    req_credit_scores = requests.get(API_URL+"credit_scores")
    contents = json.loads(req_credit_scores.content.decode("utf-8"))
    json_contents = json.loads(contents)
    credit_score_data = pd.DataFrame(data=json_contents)

    main_data = pd.merge(left=app_data, right=credit_score_data, 
                         left_on='SK_ID_CURR', right_on='SK_ID_CURR')

    return main_data

main_data = load_data()

#-------------------------------------------------------
# Sidebar
#-------------------------------------------------------

# Create text_input and button for retraining model
st.sidebar.title("Service Functions")

# Self Test
st.sidebar.header("Self Test")
self_test_btn = st.sidebar.button("Run")

if self_test_btn:
    req = requests.get(API_URL+"self_check")
    contents = json.loads(req.content.decode("utf-8"))
    msg = ""
    if "detail" in contents:
        msg = contents["detail"]
    else:
        msg = contents
    st.sidebar.text(msg)

# Model Re-Train 
st.sidebar.header("Re-Train Model")
retrain_url = st.sidebar.text_input("Re-Train data URL", "http://")

if retrain_url != "http://":
    requests.put(API_URL+"train_model")
    response = requests.put(API_URL+"train_model",
                data=retrain_url,                         
                headers={'content-type':'text/plain'},
                 )
    
    if response.status_code == 200:
        st.sidebar.text("🤖 🛠 This functionality is\nunder construction... \nPlease come back later.")
    else:
        st.sidebar.text("🤖 🚨 The model can't be retrained.\nContact your sysadmin if the problem\npersists.")

#-------------------------------------------------------
# Filter
#-------------------------------------------------------

# Space out the maps so the first one is 2x the size of the other
left_column_0, _ = st.beta_columns((1, 3))

# Populate filter
left_column_0.header("Client ID")

client_id = left_column_0.selectbox("", main_data["SK_ID_CURR"])

with st.beta_expander("Compare data with clients with same :", expanded=True):
    c1, c2, c3, c4 = st.beta_columns((1, 1, 1, 1))
    age_checkbox = c1.checkbox("Age", value=True, key="Test")
    income_checkbox = c2.checkbox("Income bracket", value=True)
    loan_type_checkbox = c3.checkbox("Type of loan", value=True)
    highest_ed_checkbox = c4.checkbox("Highest education", value=True)
    housing_situation_checkbox = c1.checkbox("Housing situation", value=True)
    family_status_checkbox = c2.checkbox("Family status", value=True)
    income_type_checkbox = c3.checkbox("Income Type", value=True)
    occupation_checkbox = c4.checkbox("Occupation", value=True)

#-------------------------------------------------------
# Information
#-------------------------------------------------------

# Get selected client's main info
client_info = main_data[main_data["SK_ID_CURR"]==client_id].iloc[0]

# Set filter criteria
client_age = client_info["DAYS_BIRTH"] if age_checkbox else "*"

client_income = client_info["AMT_INCOME_TOTAL"] if income_checkbox else "*"
    
client_loan_type = client_info["NAME_CONTRACT_TYPE"] if loan_type_checkbox else "*"

client_highest_ed = client_info["NAME_EDUCATION_TYPE"] if highest_ed_checkbox else "*"
    
client_housing_situation = client_info["NAME_HOUSING_TYPE"] if housing_situation_checkbox else "*"

client_family_status = client_info["NAME_FAMILY_STATUS"] if family_status_checkbox else "*"

client_income_type = client_info["NAME_INCOME_TYPE"] if income_checkbox else "*"

client_occupation_checkbox = client_info["OCCUPATION_TYPE"] if occupation_checkbox else "*"

filter_dict = {"DAYS_BIRTH": client_age \
                             if not (client_age == '' \
                                     or pd.isnull(client_age)) \
                             else "*", 
               "AMT_INCOME_TOTAL": client_income \
                                   if not (client_income == '' \
                                           or pd.isnull(client_income)) \
                                   else "*", 
               "NAME_CONTRACT_TYPE": client_loan_type \
                                     if not (client_loan_type == '' \
                                             or pd.isnull(client_loan_type)) \
                                     else "*", 
               "NAME_EDUCATION_TYPE": client_highest_ed \
                                      if not (client_highest_ed == '' \
                                              or pd.isnull(client_highest_ed)) \
                                      else "*",
               "NAME_HOUSING_TYPE": client_housing_situation \
                                    if not (client_housing_situation == '' \
                                            or pd.isnull(client_housing_situation)) \
                                    else "*",
               "NAME_FAMILY_STATUS": client_family_status \
                                     if not (client_family_status == '' \
                                             or pd.isnull(client_family_status)) \
                                     else "*",
               "NAME_INCOME_TYPE": client_income_type \
                                   if not (client_income_type == '' \
                                           or pd.isnull(client_income_type)) \
                                   else "*",
               "OCCUPATION_TYPE": client_occupation_checkbox \
                                  if not (client_occupation_checkbox == '' \
                                          or pd.isnull(client_occupation_checkbox)) \
                                  else "*"}

# Get filtered data
similar_clients_data = get_filtered_client_data(main_data, filter_dict)

# Space out the maps so the first one is 2x the size of the other
left_column, right_column = st.beta_columns((2, 1))

#-------------------------------------------------------
# Credit Score
#-------------------------------------------------------

# Get client's credit score data
client_score = main_data[main_data["SK_ID_CURR"]==client_id].iloc[0]["Credit Score"]

# Get similar profiles credit score data
similar_clients_credit_score = similar_clients_data["Credit Score"].mean()

# Layout
left_column.header("Default Risk Score")

gauge = go.Figure(go.Indicator(
        mode = "gauge+delta+number",
        value = client_score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        gauge = {'axis': {'range': [None, 100]},
                 'steps' : [
                     {'range': [0, 25], 'color': "lightgreen"},
                     {'range': [25, 50], 'color': "lightyellow"},
                     {'range': [50, 75], 'color': "orange"},
                     {'range': [75, 100], 'color': "red"},
                     ],
                 'threshold': {
                'line': {'color': "black", 'width': 10},
                'thickness': 0.8,
                'value': client_score},

                 'bar': {'color': "black", 'thickness' : 0.2},
                },
        delta = {'reference': similar_clients_credit_score,
        'increasing': {'color': 'red'},
        'decreasing' : {'color' : 'green'}}
        ))

gauge.update_layout(width=600, height=500, 
                    margin=dict(l=50, r=50, b=100, t=100, pad=4))

left_column.plotly_chart(gauge)

cs_text = "LOW RISK"
if 25 < client_score <= 50:
    cs_text = "LOWER RISK"
elif 50 < client_score <= 75:
    cs_text = "HIGHER RISK"
elif 75 < client_score:
    cs_text = "HIGH RISK"

left_column.markdown('The selected client has a **{}** profile'.format(cs_text))
left_column.markdown('Credit Score for similar clients based on the criteria you picked : **{0:.1f}**'.format(similar_clients_credit_score))

#-------------------------------------------------------
# Personal information
#-------------------------------------------------------

# Section title
right_column.header("Personal Data")

# Get selected client's personal info
personal_info_client_df = client_info[list(personal_info_cols.keys())]\
                          .rename(index=personal_info_cols)\
                          .rename("Values")
personal_info_client_df["AGE"] = round(personal_info_client_df["AGE"]/365*(-1),1)
personal_info_client_df["YEARS AT CURRENT JOB"] = round(personal_info_client_df["YEARS AT CURRENT JOB"]/365*(-1),1)

# Populate display
right_column.dataframe(data=personal_info_client_df, 
                       width=700, height=500)

#-------------------------------------------------------
# Most important features compared
#-------------------------------------------------------

st.header("Most Relevant Features")

left_column_2, right_column_2 = st.beta_columns((1, 1))

#-------------------------------------------------------
# For similar profiles

left_column_2.subheader("COMPARISON WITH SIMILAR CLIENTS")

graph_similar_clients_data = pd.DataFrame()
graph_client_info = pd.DataFrame()

graph_similar_clients_data["AGE"] = similar_clients_data["DAYS_BIRTH"]/365*(-1)
graph_similar_clients_data["YEARS AT CURRENT JOB"] = similar_clients_data["DAYS_EMPLOYED"]/365*(-1)
graph_client_info["AGE"] = personal_info_client_df["AGE"]
graph_client_info["YEARS AT CURRENT JOB"] = personal_info_client_df["YEARS AT CURRENT JOB"]


best_cs_value = int(similar_clients_data["Credit Score"].min())
worst_cs_value = int(similar_clients_data["Credit Score"].max())

best_threshold = left_column_2.slider('Ideal client maximum default risk score', best_cs_value, 100, best_cs_value + 25)
best_data = similar_clients_data[similar_clients_data["Credit Score"]<=(best_threshold+1)].copy()
best_data["AGE"] = best_data["DAYS_BIRTH"]/365*(-1)
best_data["YEARS AT CURRENT JOB"] = best_data["DAYS_EMPLOYED"]/365*(-1)

worst_threshold = left_column_2.slider('Worst client minimum default risk score', 0, worst_cs_value, worst_cs_value - 25)
worst_data = similar_clients_data[similar_clients_data["Credit Score"]>=(worst_threshold)].copy()
worst_data["AGE"] = worst_data["DAYS_BIRTH"]/365*(-1)
worst_data["YEARS AT CURRENT JOB"] = worst_data["DAYS_EMPLOYED"]/365*(-1)

# DAYS

fig = go.Figure()
# Best similar clients
fig.add_trace(go.Bar(
    x=list(best_data[most_important_features_days].mean()),
    y=most_important_features_days,
    name='Best Client',
    marker_color='lightgreen',
    orientation='h'
))

# Selected client
fig.add_trace(go.Bar(
    x=list(personal_info_client_df.reindex(most_important_features_days)),
    y=most_important_features_days,
    name='Selected Client',
    marker_color='blue',
    orientation='h'
))

# Average similar clients
fig.add_trace(go.Bar(
    x=list(graph_similar_clients_data[most_important_features_days].mean()),
    y=most_important_features_days,
    name='Average Clients',
    marker_color='lightblue',
    orientation='h'
))

# Worst similar clients
fig.add_trace(go.Bar(
    x=list(worst_data[most_important_features_days].mean()),
    y=most_important_features_days,
    name='Worst Clients',
    marker_color='red',
    orientation='h'
))

# Here we modify the tickangle of the xaxis, resulting in rotated labels.
fig.update_layout(barmode='group', xaxis_tickangle=-45, 
                  title_text="Age and Years at current job",
                  width=1000, height=600)
left_column_2.plotly_chart(fig)

# AMT

fig = go.Figure()
# Best similar clients
fig.add_trace(go.Bar(
    x=list(best_data[most_important_features_amt].mean()),
    y=most_important_features_amt,
    name='Best Client',
    marker_color='lightgreen',
    orientation='h'
))

# Selected client
fig.add_trace(go.Bar(
    x=list(client_info.reindex(most_important_features_amt)),
    y=most_important_features_amt,
    name='Selected Client',
    marker_color='blue',
    orientation='h'
))

# Average similar clients
fig.add_trace(go.Bar(
    x=list(similar_clients_data[most_important_features_amt].mean()),
    y=most_important_features_amt,
    name='Average Clients',
    marker_color='lightblue',
    orientation='h'
))

# Worst similar clients
fig.add_trace(go.Bar(
    x=list(worst_data[most_important_features_amt].mean()),
    y=most_important_features_amt,
    name='Worst Clients',
    marker_color='red',
    orientation='h'
))

# Here we modify the tickangle of the xaxis, resulting in rotated labels.
fig.update_layout(barmode='group', xaxis_tickangle=-45, 
                  title_text="Credit and Annuity Amounts",
                  width=1000, height=600)
left_column_2.plotly_chart(fig)

# EXT

fig = go.Figure()
# Best similar clients
fig.add_trace(go.Bar(
    x=list(best_data[most_important_features_ext].mean()),
    y=most_important_features_ext,
    name='Best Client',
    marker_color='lightgreen',
    orientation='h'
))

# Selected client
fig.add_trace(go.Bar(
    x=list(client_info.reindex(most_important_features_ext)),
    y=most_important_features_ext,
    name='Selected Clients',
    marker_color='blue',
    orientation='h'
))

# Average similar clients
fig.add_trace(go.Bar(
    x=list(similar_clients_data[most_important_features_ext].mean()),
    y=most_important_features_ext,
    name='Average Clients',
    marker_color='lightblue',
    orientation='h'
))

# Worst similar clients
fig.add_trace(go.Bar(
    x=list(worst_data[most_important_features_ext].mean()),
    y=most_important_features_ext,
    name='Worst Clients',
    marker_color='red',
    orientation='h'
))

# Here we modify the tickangle of the xaxis, resulting in rotated labels.
fig.update_layout(barmode='group', xaxis_tickangle=-45, 
                  title_text="Synthetic Indicators",
                  width=1000, height=600)
left_column_2.plotly_chart(fig)

#-------------------------------------------------------
# Globally

right_column_2.subheader("COMPARISON WITH ALL CLIENTS")

graph_main_data = pd.DataFrame()
graph_main_data["AGE"] = main_data["DAYS_BIRTH"]/365*(-1)
graph_main_data["YEARS AT CURRENT JOB"] = main_data["DAYS_EMPLOYED"]/365*(-1)

best_cs_value = int(main_data["Credit Score"].min())
worst_cs_value = int(main_data["Credit Score"].max())

best_global_threshold = right_column_2.slider('Ideal client maximum credit score', best_cs_value, 100, best_cs_value + 25, key="global_best")
worst_global_threshold = right_column_2.slider('Worst client minimum credit score', 0, worst_cs_value, worst_cs_value - 25, key="global_worst")

best_global_data = main_data[main_data["Credit Score"]<=best_global_threshold].copy()
best_global_data["AGE"] = best_global_data["DAYS_BIRTH"]/365*(-1)
best_global_data["YEARS AT CURRENT JOB"] = best_global_data["DAYS_EMPLOYED"]/365*(-1)

worst_global_data = main_data[main_data["Credit Score"]>=worst_global_threshold].copy()
worst_global_data["AGE"] = worst_global_data["DAYS_BIRTH"]/365*(-1)
worst_global_data["YEARS AT CURRENT JOB"] = worst_global_data["DAYS_EMPLOYED"]/365*(-1)

# DAYS

fig = go.Figure()
# Best global clients
fig.add_trace(go.Bar(
    x=list(best_global_data[most_important_features_days].mean()),
    y=most_important_features_days,
    name='Best Client',
    marker_color='lightgreen',
    orientation='h'
))

# Selected client
fig.add_trace(go.Bar(
    x=list(personal_info_client_df.reindex(most_important_features_days)),
    y=most_important_features_days,
    name='Selected Client',
    marker_color='blue',
    orientation='h'
))

# Average global clients
fig.add_trace(go.Bar(
    x=list(graph_main_data[most_important_features_days].mean()),
    y=most_important_features_days,
    name='Average Clients',
    marker_color='lightblue',
    orientation='h'
))

# Worst global clients
fig.add_trace(go.Bar(
    x=list(worst_global_data[most_important_features_days].mean()),
    y=most_important_features_days,
    name='Worst Clients',
    marker_color='red',
    orientation='h'
))

# Here we modify the tickangle of the xaxis, resulting in rotated labels.
fig.update_layout(barmode='group', xaxis_tickangle=-45, 
                  title_text="Age and Years at current job",
                  width=1000, height=600)
right_column_2.plotly_chart(fig)

# AMT

fig = go.Figure()
# Best global clients
fig.add_trace(go.Bar(
    x=list(best_global_data[most_important_features_amt].mean()),
    y=most_important_features_amt,
    name='Best Client',
    marker_color='lightgreen',
    orientation='h'
))

# Selected client
fig.add_trace(go.Bar(
    x=list(client_info.reindex(most_important_features_amt)),
    y=most_important_features_amt,
    name='Selected Client',
    marker_color='blue',
    orientation='h'
))

# Average global clients
fig.add_trace(go.Bar(
    x=list(main_data[most_important_features_amt].mean()),
    y=most_important_features_amt,
    name='Average Clients',
    marker_color='lightblue',
    orientation='h'
))

# Worst global clients
fig.add_trace(go.Bar(
    x=list(worst_global_data[most_important_features_amt].mean()),
    y=most_important_features_amt,
    name='Worst Clients',
    marker_color='red',
    orientation='h'
))

# Here we modify the tickangle of the xaxis, resulting in rotated labels.
fig.update_layout(barmode='group', xaxis_tickangle=-45, 
                  title_text="Credit and Annuity Amounts",
                  width=1000, height=600)
right_column_2.plotly_chart(fig)

# EXT

fig = go.Figure()
# Best global clients
fig.add_trace(go.Bar(
    x=list(best_global_data[most_important_features_ext].mean()),
    y=most_important_features_ext,
    name='Best Client',
    marker_color='lightgreen',
    orientation='h'
))

# Selected client
fig.add_trace(go.Bar(
    x=list(client_info.reindex(most_important_features_ext)),
    y=most_important_features_ext,
    name='Selected Client',
    marker_color='blue',
    orientation='h'
))

# Average global clients
fig.add_trace(go.Bar(
    x=list(main_data[most_important_features_ext].mean()),
    y=most_important_features_ext,
    name='Average Clients',
    marker_color='lightblue',
    orientation='h'
))

# Worst global clients
fig.add_trace(go.Bar(
    x=list(worst_global_data[most_important_features_ext].mean()),
    y=most_important_features_ext,
    name='Worst Clients',
    marker_color='red',
    orientation='h'
))

# Here we modify the tickangle of the xaxis, resulting in rotated labels.
fig.update_layout(barmode='group', xaxis_tickangle=-45, 
                  title_text="Synthetic Indicators",
                  width=1000, height=600)
right_column_2.plotly_chart(fig)
