import json
import os
import streamlit as st
from collections import defaultdict
import base64

ALLOWED_LABELS = {
    "mouth",
    "esophagus",
    "stomach",
    "small intestine",
    "colon",
    "z-line",
    "pylorus",
    "ileocecal valve",
    "active bleeding",
    "angiectasia",
    "blood",
    "erosion",
    "erythema",
    "hematin",
    "lymphangioectasis",
    "polyp",
    "ulcer",
}


def tiou(a, b):
    inter = max(0, min(a["end"], b["end"]) - max(a["start"], b["start"]) + 1)
    union = (a["end"] - a["start"] + 1) + (b["end"] - b["start"] + 1) - inter
    return inter / union if union > 0 else 0.0


def extract_by_video_label(data):
    out = defaultdict(lambda: defaultdict(list))
    for v in data["videos"]:
        vid = v["video_id"]
        for e in v["events"]:
            for lbl in e["label"]:
                out[vid][lbl].append({"start": e["start"], "end": e["end"]})
    return out


def sanity_check(gt, pred):
    gt_ids = {v["video_id"] for v in gt["videos"]}
    pr_ids = {v["video_id"] for v in pred["videos"]}

    if gt_ids != pr_ids:
        missing = gt_ids - pr_ids
        extra = pr_ids - gt_ids
        msg = "Video ID mismatch."
        if missing:
            msg += f" Missing in prediction: {missing}."
        if extra:
            msg += f" Extra in prediction: {extra}."
        return False, msg

    for v in pred["videos"]:
        for e in v["events"]:
            for l in e["label"]:
                if l not in ALLOWED_LABELS:
                    return False, f"Invalid label '{l}' in video '{v['video_id']}'."

    return True, "All checks passed"


def average_precision(gt_segs, pr_segs, thr):
    matched = set()
    tp = []
    for p in pr_segs:
        hit = False
        for i, g in enumerate(gt_segs):
            if i in matched:
                continue
            if tiou(p, g) >= thr:
                matched.add(i)
                hit = True
                break
        tp.append(1 if hit else 0)

    if not gt_segs:
        return 0.0 if pr_segs else 1.0

    cum_tp = 0
    prev_r = 0.0
    ap = 0.0

    for i, v in enumerate(tp):
        cum_tp += v
        r = cum_tp / len(gt_segs)
        p = cum_tp / (i + 1)
        ap += p * (r - prev_r)
        prev_r = r

    return ap


def compute_video_maps(gt, pr, thr):
    gt_ev = extract_by_video_label(gt)
    pr_ev = extract_by_video_label(pr)
    video_maps = {}

    for vid in gt_ev:
        aps = []
        for lbl in ALLOWED_LABELS:
            aps.append(
                average_precision(
                    gt_ev[vid].get(lbl, []),
                    pr_ev[vid].get(lbl, []),
                    thr,
                )
            )
        video_maps[vid] = sum(aps) / len(aps)

    return video_maps


st.title("RareEval: ICPR 2026 RARE-VISION TEMPORAL mAP EVALUATOR")

st.markdown("""
⚠️ **Important:**  
This evaluator has been developed **exclusively for the ICPR 2026 RARE-VISION Competition**.  
It is not intended for external benchmarking outside the official competition framework.

---

### 🔗 Official Resources

- 📂 Dataset (GALAR Capsule Endoscopy Dataset):  
  https://plus.figshare.com/articles/dataset/Galar_-_a_large_multi-label_video_capsule_endoscopy_dataset/25304616  

- 📄 ICPR 2026 RARE-VISION Competition Document & Flyer (includes sample report format):  
  https://figshare.com/articles/preprint/ICPR_2026_RARE-VISION_Competition_Document_and_Flyer/30884858?file=60375365  

- 💻 Official GitHub Repository (scripts + JSON generation utilities):  
  https://github.com/RAREChallenge2026/RARE-VISION-2026-Challenge  

---

After computing the mAP scores using this tool,  
📑 **please refer to the Sample Report format provided in the competition document (see link above)** and include your calculated:

- Overall mAP @ 0.5  
- Overall mAP @ 0.95  
- Per-video mAP breakdown  

exactly as specified in the official template.
""")


with st.expander("ℹ️ How to generate the required prediction JSON"):
    st.markdown("""
Using the scripts provided in the official GitHub repository, you can automatically generate the required JSON file from your model's one-hot encoded CSV output.

**Process Overview:**

1. **Frame-Level Predictions:**  
   Your model outputs a CSV where each row corresponds to a frame and columns represent one-hot encoded labels.

2. **Temporal Grouping:**  
   The provided GitHub script processes this CSV frame-by-frame. When continuous frames contain an active label (`1`), they are grouped into a single temporal event.

3. **JSON Structuring:**  
   The script computes `start` and `end` times/frames for contiguous segments and formats them into the required hierarchical JSON structure:

   `videos → events → start, end, label`

This JSON format is mandatory for evaluation in the ICPR 2026 RARE-VISION competition.
""")


gt_b64 = os.environ.get("GROUND_TRUTH_JSON_BASE64")
if gt_b64:
    gt = json.loads(base64.b64decode(gt_b64).decode())
else:
    st.error("GROUND_TRUTH_JSON_BASE64 environment variable not set.")
    gt = None

pred_file = st.file_uploader("Upload prediction JSON", type=["json"])

if pred_file and gt:
    pr = json.load(pred_file)
    passed, message = sanity_check(gt, pr)

    if not passed:
        st.error(message)
    else:
        st.success(message)

        maps_05 = compute_video_maps(gt, pr, 0.5)
        maps_095 = compute_video_maps(gt, pr, 0.95)

        avg_05 = sum(maps_05.values()) / len(maps_05) if maps_05 else 0.0
        avg_095 = sum(maps_095.values()) / len(maps_095) if maps_095 else 0.0

        st.subheader("Overall Averages")
        col1, col2 = st.columns(2)
        col1.metric("Overall mAP @ 0.5", round(avg_05, 4))
        col2.metric("Overall mAP @ 0.95", round(avg_095, 4))

        st.subheader("Per-Video mAP Breakdown")

        results = []
        for vid in sorted(maps_05.keys()):
            results.append({
                "Video ID": vid,
                "mAP @ 0.5": round(maps_05[vid], 4),
                "mAP @ 0.95": round(maps_095[vid], 4)
            })

        st.dataframe(results, use_container_width=True)