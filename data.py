import pandas as pd


daily_df = pd.read_csv("data/daily_report.csv")

# 전세계 확진자, 사망자, 완치자 df
totals_df = (
    daily_df[["Confirmed", "Deaths", "Recovered"]].sum().reset_index(name="count")
)
totals_df = totals_df.rename(columns={"index": "condition"})

# 나라별 확진자, 사망자, 완치자 df
countries_df = daily_df[["Country_Region", "Confirmed", "Deaths", "Recovered"]]
countries_df = (
    countries_df.groupby("Country_Region")
    .sum()
    .sort_values(by="Confirmed", ascending=False)
    .reset_index()
)


conditions = ["confirmed", "deaths", "recovered"]


# 전세계 날짜별 확진자, 사망자, 완치자 df
def make_global_df():
    def make_df(condition):
        # 파일 read
        df = pd.read_csv(f"data/time_{condition}.csv")
        # 필요 없는 columns 제거, colum 합, column 명 변경
        df = (
            df.drop(["Province/State", "Country/Region", "Lat", "Long"], axis=1)
            .sum()
            .reset_index(name=condition)
        )
        df = df.rename(columns={"index": "date"})
        return df

    final_df = None
    for condition in conditions:
        condition_df = make_df(condition)
        if final_df is None:  # 첫 df 처리 시
            final_df = condition_df
        else:  # 두 번째 df 처리시 merge
            final_df = final_df.merge(condition_df)
    return final_df


# 특정나라 날짜별 확진자, 사망자, 완치자 df
def make_country_df(country):
    def make_df(condition):
        # 파일 read
        df = pd.read_csv(f"data/time_{condition}.csv")
        # Country/Region Column이 country와 같은 row만 가져옴
        df = df.loc[df["Country/Region"] == country]
        df = (
            df.drop(columns=["Province/State", "Country/Region", "Lat", "Long"])
            .sum()
            .reset_index(name=condition)
        )
        df = df.rename(columns={"index": "date"})

        return df

    final_df = None
    for condition in conditions:
        condition_df = make_df(condition)
        if final_df is None:  # 첫 df 처리 시
            final_df = condition_df
        else:  # 두 번째 df 처리시 merge
            final_df = final_df.merge(condition_df)

    return final_df
