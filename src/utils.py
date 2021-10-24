"""
Helpers for streamlit app
"""

import pandas as pd


def calc_savings(
    events, fraud_rate, fraud_value, data_quality, data_quality_labels
):
    savings_daily = (events * (fraud_rate / 100) * fraud_value) * (
        data_quality / len(data_quality_labels)
    )
    savings_annual = savings_daily * 365

    return savings_daily, savings_annual


def create_df_business_value(
    data_quality_labels, events, fraud_value, fraud_rate
):
    df_len = len(data_quality_labels)
    df = (
        pd.DataFrame(
            {
                "events": [events] * df_len,
                "data_quality_label": data_quality_labels,
                "data_quality": range(1, df_len + 1),
                "fraud_value": [fraud_value] * df_len,
                "fraud_rate": [fraud_rate] * df_len,
            }
        )
        .assign(
            annual_savings=lambda x: (
                (x.events * (x.fraud_rate / 100)) * x.fraud_value * 365
            )
            * (x.data_quality / df_len)
        )
        .assign(
            annual_savings_label=lambda x: x.annual_savings.apply(
                lambda y: f"€ {y:,.0f}"
            )
        )
    )

    return df
