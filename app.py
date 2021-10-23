import streamlit as st
import plotly.express as px
import pandas as pd

st.set_page_config(
    page_title=" Testpage",
    page_icon="👁⃤",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.title("Calculate business value")

c1 = st.container()
c1.subheader("Daily events")
events = c1.slider(
    label="",
    value=200,
    min_value=0,
    max_value=1000,
    step=25,
    kwargs={"font-size": "100px"},
)

# "---"

c2 = st.container()
c2.subheader("Fraud rate")
fraud_rate = c2.slider("%", 0, 100, step=5, value=10)

# "---"

c3 = st.container()
c3.subheader("Event value")
fraud_value = c3.slider(
    label="EUR", value=10, min_value=0, max_value=100, step=5
)

# "---"

c4 = st.container()
c4.subheader("Data quality")
data_quality_labels = ["basic", "solid", "great"]
data_quality = (
    c4.radio(
        label="",
        options=range(len(data_quality_labels)),
        format_func=lambda x: data_quality_labels[x],
    )
    + 1
)
st.write(
    "<style>div.row-widget.stRadio > div{flex-direction:row;}</style>",
    unsafe_allow_html=True,
)

"---"

savings_daily = (events * (fraud_rate / 100) * fraud_value) * (
    data_quality / len(data_quality_labels)
)
savings_annual = savings_daily * 365

st.header(f"Save each day up to {savings_daily:,.0f}€")
st.header(f"Estiamted savings ~{savings_annual:,.0f}€ annually")


df_len = len(data_quality_labels)
df = pd.DataFrame(
    {
        "events": [events] * df_len,
        "data_quality_label": data_quality_labels,
        "data_quality": range(1, df_len + 1),
        "fraud_value": [fraud_value] * df_len,
        "fraud_rate": [fraud_rate] * df_len,
    }
).assign(
    annual_savings=lambda x: (
        (x.events * (x.fraud_rate / 100)) * x.fraud_value * 365
    )
    * (x.data_quality / df_len)
)
"", df


fig = px.bar(
    df,
    x="data_quality_label",
    y="annual_savings",
    color="data_quality_label",
    labels={
        "data_quality_label": "Data quality",
        "annual_savings": "Annual savings",
    },
)

st.plotly_chart(fig)
