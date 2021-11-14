# import plotly express
import plotly.express as px


def plot_bar_value(
    df,
    x="data_quality_label",
    y="annual_savings",
    x_label="Datenqualität",
    y_label="Jährliche Ersparnis",
):
    assert x in df.columns
    assert y in df.columns
    assert x_label in df.columns
    assert y_label in df.columns

    fig = px.bar(
        df,
        x=x,
        y=y,
        color=x,
        labels={
            x: x_label,
            y: y_label,
        },
        text="annual_savings_label",
        template="simple_white",
    )
    fig.update_layout(
        showlegend=False,
        xaxis_visible=False,
        yaxis_visible=False,
        font_size=14,
    )

    fig.update_traces(
        hovertemplate="Datenqualität: %{x} <br> Bis zu €%{y:,.0f} einsparen"
    )
    fig.add_annotation(
        text="Jährliche Ersparnis <br>je nach Datenqualität",
        xref="paper",
        yref="paper",
        x=0.05,
        y=0.95,
        showarrow=False,
    )

    return fig
