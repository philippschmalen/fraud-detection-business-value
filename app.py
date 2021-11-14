import streamlit as st
import plotly.express as px
from src.utils import create_df_business_value
from src.utils import calc_savings
from src.utils import local_css

# from src.plots import plot_bar_value

st.set_page_config(
    page_title="Fraud solutions business value",
    page_icon="src/favicon_triangle.png",
    layout="centered",
    initial_sidebar_state="collapsed",
)


local_css(file_name="src/style.css")


# events count
c1 = st.container()
c1.write("###### Tägliche Events insgesamt")
events = c1.slider(label="", value=300, min_value=0, max_value=1000, step=25)

# fraud rate
c2 = st.container()
c2.write("###### davon Betrug (%)")
fraud_rate = c2.slider("%", 1, 50, step=1, value=7)

# fraud value
c3 = st.container()
c3.write("###### durchschnittlicher Betrugswert (EUR)")
fraud_value = c3.slider(label="", value=10, min_value=0, max_value=100, step=1)

# data quality
data_quality_labels = [
    "Ausreichend",
    "Viele Events + Betrug eindeutig identifizierbar",
]

c4 = st.container()

with c4:
    st.write("###### Wie gut sind meine Daten?")
    data_infobox = st.expander(label="Entscheidend sind 2 Faktoren")
    with data_infobox:
        st.markdown(
            """
        1. Mehr als ca. 150 Events/Tag <br>
        2. Betrug ist eindeutig identifizierbar
        """,
            unsafe_allow_html=True,
        )
    data_quality = (
        st.radio(
            label="",
            options=range(len(data_quality_labels)),
            format_func=lambda x: data_quality_labels[x],
        )
        + 1
    )
    savings_daily, savings_annual = calc_savings(
        events, fraud_rate, fraud_value, data_quality, data_quality_labels
    )
    st.write(
        "<style>div.row-widget.stRadio > div{flex-direction:row;}</style>",
        unsafe_allow_html=True,
    )

# business value
st.metric("Annual value", f"€ {savings_annual:,.0f}")


"---"

df = create_df_business_value(
    data_quality_labels, events, fraud_value, fraud_rate
)

# plot
# fig = plot_bar_value(
#     df,
#     x="data_quality_label",
#     y="annual_savings",
#     x_label="Datenqualität",
#     y_label="Jährliche Ersparnis",
# )

# st.plotly_chart(fig, use_container_width=True)
