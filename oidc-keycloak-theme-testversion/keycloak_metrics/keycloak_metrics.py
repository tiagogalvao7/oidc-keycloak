import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates


def read_csv_data_with_timestamp(filepath):
    """Reads CSV data with timestamp, attempting to handle various formats."""
    try:
        df = pd.read_csv(filepath, header=0)  # Read with header
        if not df.empty:
            timestamp_col = df.columns[0]  # Assume first column is timestamp
            value_col = df.columns[1] if len(df.columns) > 1 else None

            try:
                df["timestamp"] = pd.to_datetime(df[timestamp_col], errors="coerce")
            except ValueError as e:
                print(f"Error converting timestamp in {filepath}: {e}")
                return pd.DataFrame(columns=["timestamp", "value"])

            if value_col:
                if "used_heap_memory_mb_max" in filepath:
                    df["value"] = pd.to_numeric(
                        df[value_col].str.replace(" MiB", ""), errors="coerce"
                    )
                else:
                    df["value"] = pd.to_numeric(df[value_col], errors="coerce")
                return df[["timestamp", "value"]].dropna(subset=["timestamp", "value"])
            else:
                return pd.DataFrame(columns=["timestamp", "value"])
        return pd.DataFrame(columns=["timestamp", "value"])
    except Exception as e:
        print(f"General error reading {filepath}: {e}")
        return pd.DataFrame(columns=["timestamp", "value"])


def aggregate_by_two_minutes(df):
    """Aggregates data by two-minute intervals, calculating mean and max."""
    if not df.empty:
        df = df.set_index("timestamp").sort_index()
        aggregated = df["value"].resample("2Min").agg(["mean", "max"]).reset_index()
        return aggregated
    return pd.DataFrame()


def plot_metric_comparison_over_time(all_data):
    """Generates a plot for each metric comparing the mean and max across compliance levels over time."""
    sns.set_style("whitegrid")
    metrics_to_read = sorted(list(set([item["metric"] for item in all_data])))
    compliances = sorted(list(set([item["compliance"] for item in all_data])))

    for metric in metrics_to_read:
        fig, ax = plt.subplots(figsize=(14, 8))
        for compliance in compliances:
            compliance_metric_data = [
                item["data"]
                for item in all_data
                if item["compliance"] == compliance and item["metric"] == metric
            ]
            if compliance_metric_data:
                combined_df = pd.concat(compliance_metric_data, ignore_index=True)
                if not combined_df.empty:
                    grouped = (
                        combined_df.groupby("timestamp")
                        .agg({"mean": "mean", "max": "max"})
                        .reset_index()
                    )
                    ax.plot(
                        grouped["timestamp"],
                        grouped["mean"],
                        marker="o",
                        linestyle="-",
                        alpha=0.7,
                        label=f"{compliance.title()} (Mean)",
                    )
                    ax.plot(
                        grouped["timestamp"],
                        grouped["max"],
                        marker="o",
                        linestyle="--",
                        alpha=0.7,
                        label=f"{compliance.title()} (Maximum)",
                    )

        ax.set_title(
            f'Comparison of {metric.replace("_", " ").title()} between Compliances Over Time'
        )
        ax.set_xlabel("Time")
        ax.set_ylabel("Value")
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
        fig.autofmt_xdate(rotation=45, ha="right")
        ax.legend(title="Compliance Level")
        plt.tight_layout()
        plt.show()


def visualize_comparison_table(all_data):
    """Generates bar plots to visualize the comparison of mean and max values across compliance levels."""
    metrics_to_read = sorted(list(set([item["metric"] for item in all_data])))
    compliances = sorted(list(set([item["compliance"] for item in all_data])))

    for metric in metrics_to_read:
        metric_data = []
        for compliance in compliances:
            compliance_metric_runs = [
                item["data"]
                for item in all_data
                if item["compliance"] == compliance and item["metric"] == metric
            ]
            if compliance_metric_runs:
                combined_df = pd.concat(compliance_metric_runs, ignore_index=True)
                if not combined_df.empty:
                    overall_mean = combined_df["mean"].mean()
                    overall_max = combined_df["max"].mean()
                    metric_data.append(
                        {
                            "Compliance": compliance.title(),
                            "Value": overall_mean,
                            "Type": "Mean",
                        }
                    )
                    metric_data.append(
                        {
                            "Compliance": compliance.title(),
                            "Value": overall_max,
                            "Type": "Maximum",
                        }
                    )

        if metric_data:
            df_plot = pd.DataFrame(metric_data)
            plt.figure(figsize=(10, 6))
            sns.barplot(x="Compliance", y="Value", hue="Type", data=df_plot)
            plt.title(
                f"Comparison of Mean and Maximum of {metric.replace('_', ' ').title()} by Compliance"
            )
            plt.ylabel("Value")
            plt.xlabel("Compliance Level")
            plt.tight_layout()
            plt.show()


if __name__ == "__main__":
    main_folder = "jsons"
    compliance_folders = {
        "veryhigh": "veryhigh",
        "high": "high",
        "medium": "medium",
        "low": "low",
    }
    metrics_to_read = [
        "gc_count_delta",
        "peak_thread_count_max",
        "process_cpu_load_max",
        "thread_count_max",
        "used_heap_memory_mb_max",
    ]

    all_runs_aggregated = []
    for compliance, folder_name in compliance_folders.items():
        full_path = os.path.join(main_folder, folder_name)
        for metric in metrics_to_read:
            metric_runs_data = []
            for filename in os.listdir(full_path):
                if (
                    filename.startswith(metric)
                    and f"_{compliance}_" in filename
                    and filename.endswith(".csv")
                ):
                    try:
                        run_number = int(
                            filename.split(f"_{compliance}_")[1].replace(".csv", "")
                        )
                        if 1 <= run_number <= 5:
                            filepath = os.path.join(full_path, filename)
                            df = read_csv_data_with_timestamp(filepath)
                            if not df.empty:
                                aggregated_df = aggregate_by_two_minutes(df.copy())
                                if not aggregated_df.empty:
                                    aggregated_df["metric"] = metric
                                    metric_runs_data.append(aggregated_df)
                    except ValueError:
                        pass
            if metric_runs_data:
                all_runs_aggregated.extend(
                    [
                        {"compliance": compliance, "metric": metric, "data": run_data}
                        for run_data in metric_runs_data
                    ]
                )

    if all_runs_aggregated:
        plot_metric_comparison_over_time(all_runs_aggregated)
        visualize_comparison_table(all_runs_aggregated)
    else:
        print("No data found for visualization.")
