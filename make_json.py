import pandas as pd
import json
from pathlib import Path
from tqdm import tqdm


USED_LABELS = [
    "mouth", "esophagus", "stomach", "small intestine", "colon",
    "z-line", "pylorus", "ileocecal valve",
    "active bleeding", "angiectasia", "blood", "erosion", "erythema",
    "hematin", "lymphangioectasis", "polyp", "ulcer",
]


def df_to_events(df: pd.DataFrame, video_id: str, label_columns, index_col: str = "index"):
    df = df.sort_values(index_col).reset_index(drop=True)
    df[index_col] = df[index_col].astype(int)

    def active_labels(row):
        return tuple(sorted([lbl for lbl in label_columns if lbl in row and row[lbl] == 1]))

    df["active"] = df.apply(active_labels, axis=1)

    events = []
    if df.empty:
        return {"video_id": video_id, "events": []}

    current_labels = df.loc[0, "active"]
    start_idx = int(df.loc[0, index_col])

    for i in range(1, len(df)):
        idx = int(df.loc[i, index_col])
        labels = df.loc[i, "active"]
        if labels != current_labels:
            events.append(
                {
                    "start": start_idx,
                    "end": idx - 1,
                    "label": list(current_labels),
                }
            )
            start_idx = idx
            current_labels = labels

    last_idx = int(df.loc[len(df) - 1, index_col])
    events.append(
        {
            "start": start_idx,
            "end": last_idx,
            "label": list(current_labels),
        }
    )

    return {"video_id": video_id, "events": events}


def build_galar_events_json(labels_dir: str, output_json: str):
    labels_path = Path(labels_dir)
    videos = []

    csv_files = sorted(labels_path.glob("*.csv"))

    for csv_path in tqdm(csv_files, desc="Processing label CSVs"):
        video_id = csv_path.stem
        df = pd.read_csv(csv_path)
        label_cols = [c for c in USED_LABELS if c in df.columns]
        video_events = df_to_events(df, video_id=video_id, label_columns=label_cols)
        videos.append(video_events)

    result = {"videos": videos}
    with open(output_json, "w") as f:
        json.dump(result, f, indent=2)


if __name__ == "__main__":
    build_galar_events_json(
        labels_dir="./galar_dataset/Galar_labels_and_metadata/labels",
        output_json="galar_events.json",
    )
