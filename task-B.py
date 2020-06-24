import pandas as pd
import numpy as np
from pandas import ExcelWriter


def find_avg_coverage_each_weekday(coverage):  # task B.1
    coverage = coverage.drop(columns="chatDepartment")

    # Add new column weekday to dataframe and convert hour data type to show the hour
    coverage["hour"] = pd.to_datetime(coverage["hour"])
    coverage["weekday"] = coverage["hour"].dt.day_name()
    coverage["hour"] = coverage["hour"].dt.hour

    # Group data by weekday and hour and take the average coverage
    coverage_gb = coverage.groupby(["weekday", "hour"])
    result = coverage_gb.mean()

    # Export to excel
    with ExcelWriter("./results/Average-coverage-each-weekday.xlsx") as writer:
        result.to_excel(
            excel_writer=writer,
            header="Mean pctCoverage",
            sheet_name="Grouped-by-weekday",
        )

    # Show Average value grouped by weekdays and hours
    print(result)


def estimate_chat_for_full_coverage(chat, coverage):  # task B.2
    chat = chat.drop(columns="chatDepartment")

    # Add a new column 'time' to merge with coverage dataframe
    chat["time"] = pd.to_datetime(chat["dateChatStarted"]) + pd.to_timedelta(
        chat.pop("hourChatStarted"), unit="H"
    )
    chat = chat.sort_values(by="time")

    # Add a new column 'time' to merge with chat dataframe
    coverage["time"] = pd.to_datetime(coverage["hour"])
    coverage["time"] = coverage["time"].dt.tz_convert(None)
    coverage = coverage.drop(columns=["hour", "chatDepartment"])

    # Merge coverage and chat dataframes
    merged = pd.merge_asof(coverage, chat, on="time", by="time")
    merged = merged.drop(columns="dateChatStarted")

    # Calculate the required number of chats for full coverage
    nChats_required = []
    nChats_fixed = []  # For converting NaN value to 0 in nChats

    for i in range(len(merged)):
        nChats = merged.loc[i, "nChats"]
        pctCoverage = merged.loc[i, "pctCoverage"]
        if np.isnan(nChats):
            nChats_fixed.append(0)
            nChats_required.append(0)
        else:
            nChats_fixed.append(nChats)
            nChats_required.append(nChats / pctCoverage)
    merged["nChats"] = nChats_fixed  # Convert NaN value to 0 in nChats
    merged["nChatsRequired"] = nChats_required

    # Add 'weekday' and 'hour' columns to dataframe
    merged["weekday"] = merged["time"].dt.day_name()
    merged["hour"] = merged["time"].dt.hour

    # Group data by 'weekday' and 'hour' columns and take the average values
    merged_gb = merged.groupby(["weekday", "hour"]).agg(
        {"pctCoverage": "mean", "nChats": "mean", "nChatsRequired": "mean"}
    )
    merged_gb.columns = ["pctCoverage", "nChats", "nChatsRequired"]
    merged_gb = merged_gb.reset_index()

    # Export to excel
    with ExcelWriter("./results/Required-chats-for-full-coverage.xlsx") as writer:
        merged_gb.to_excel(
            excel_writer=writer,
            sheet_name="Grouped-by-weekday-&-hour",
            columns=["pctCoverage", "nChats", "nChatsRequired"],
            header=[
                "Average Coverage",
                "Average # of chats",
                "Estimate # of chats for full coverage (average)",
            ],
        )
        merged.to_excel(excel_writer=writer, sheet_name="Full-result")

    print(merged_gb)


if __name__ == "__main__":
    pd.set_option("display.max_rows", None, "display.max_columns", None)

    # Load datasets
    chat_dataset = pd.read_csv("chatsReceived.csv")
    coverage_dataset = pd.read_csv("coverage.csv")

    # For task B.1
    find_avg_coverage_each_weekday(coverage=coverage_dataset)

    # For task B.2
    estimate_chat_for_full_coverage(chat=chat_dataset, coverage=coverage_dataset)
