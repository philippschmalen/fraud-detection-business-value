import streamlit as st
import plotly.express as px
from src.utils import create_df_business_value
from src.utils import calc_savings

st.set_page_config(
    page_title=" Testpage",
    page_icon="src/favicon_triangle.png",
    layout="centered",
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


savings_daily, savings_annual = calc_savings(
    events, fraud_rate, fraud_value, data_quality, data_quality_labels
)


st.header(
    f"Save each day up to € {savings_daily:,.0f} ➟ € {savings_annual:,.0f} annually"
)


df = create_df_business_value(
    data_quality_labels, events, fraud_value, fraud_rate
)

# plot
fig = px.bar(
    df,
    x="data_quality_label",
    y="annual_savings",
    color="data_quality_label",
    labels={
        "data_quality_label": "Data quality",
        "annual_savings": "Annual savings",
    },
    text="annual_savings_label",
    template="simple_white",
)
fig.update_layout(showlegend=False)
fig.update_traces(
    hovertemplate="%{x} data quality <br> €%{y:,.0f}<extra></extra>"
)

st.plotly_chart(fig)
