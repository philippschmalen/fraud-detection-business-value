import streamlit as st
import plotly.express as px
from src.utils import create_df_business_value
from src.utils import calc_savings

# from src.utils import local_css

st.set_page_config(
    page_title="Fraud solutions business value",
    page_icon="src/favicon_triangle.png",
    layout="centered",
    initial_sidebar_state="collapsed",
)


def local_css(file_name):
    """https://discuss.streamlit.io/t/are-you-using-html-in-markdown-tell-us-why/96/25"""
    with open(file_name) as f:
        st.markdown(
            "<style>{}</style>".format(f.read()), unsafe_allow_html=True
        )


local_css(file_name="src/style.css")


# events count
c1 = st.container()
c1.write("##### Tägliche Events insegsamt")
events = c1.slider(label="", value=300, min_value=0, max_value=1000, step=25)

# fraud rate
c2 = st.container()
c2.write("##### davon Betrug (%)")
fraud_rate = c2.slider("%", 1, 50, step=1, value=7)

# fraud value
c3 = st.container()
c3.write("##### durchschnittlicher Betrugswert (EUR)")
fraud_value = c3.slider(label="", value=10, min_value=0, max_value=100, step=5)

# data quality
data_quality_labels = ["Niedrig", "Mittel", "Hoch"]

c4 = st.container()
c4_col1, c4_col2 = st.columns(2)
with c4:
    with c4_col1:
        st.write("##### Wie gut sind meine Daten?")
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

    with c4_col2:
        data_infobox = st.expander(label="Entscheidend sind 2 Faktoren")
        with data_infobox:
            st.markdown(
                """
            1. Mehr als ca. 150 Events/Tag <br>
            2. Betrug ist eindeutig identifizierbar
            """,
                unsafe_allow_html=True,
            )


t = f"""
    <div>
        Business value bis zu <br>
        <span class='highlight bold blue'>
            € {savings_annual:,.0f} jährlich
        </span>
    </div>"""
st.markdown(t, unsafe_allow_html=True)


"---"

df = create_df_business_value(
    data_quality_labels, events, fraud_value, fraud_rate
)

# plot
fig = px.bar(
    df,
    y="data_quality_label",
    x="annual_savings",
    color="data_quality_label",
    labels={
        "data_quality_label": "Datenqualität",
        "annual_savings": "Jährliche Ersparnis",
    },
    text="annual_savings_label",
    template="simple_white",
)
fig.update_layout(
    showlegend=False, xaxis_visible=False, yaxis_visible=False, font_size=20
)

fig.update_traces(
    hovertemplate="Datenqualität: %{y} <br> Bis zu €%{x:,.0f} einsparen"
)
fig.add_annotation(
    text="Jährliche Ersparnis <br>je nach Datenqualität",
    xref="paper",
    yref="paper",
    x=0.8,
    y=0.95,
    showarrow=False,
    font_size=20,
)

st.plotly_chart(fig, use_container_width=True)
