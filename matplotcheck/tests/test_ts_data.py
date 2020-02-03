import pytest


def test_assert_xydata_timeseries(pt_time_line_plt, pd_df_timeseries):
    """Tests that assert_xydata correctly passes with time data and xtime=True"""
    pt_time_line_plt.assert_xydata(
        pd_df_timeseries, xcol="time", ycol="A", xtime=True
    )
