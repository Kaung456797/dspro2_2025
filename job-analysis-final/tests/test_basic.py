def test_dataframe(df):
    assert len(df) > 0
    assert df["salary"].min() > 0
    assert df["skill_count"].min() >= 0