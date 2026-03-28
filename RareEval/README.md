# RareEval — ICPR 2026 RARE-VISION Temporal mAP Evaluator

A web application built exclusively for the **ICPR 2026 RARE-VISION Competition** to evaluate participant submissions for capsule endoscopy temporal event detection.

---

## What the App Does

Participants upload their prediction file to the app. RareEval validates the submission and computes **mean Average Precision (mAP)** scores against the private ground truth, reporting:

- **Overall mAP @ 0.5** — aggregate score across all videos at a 50% overlap threshold
- **Overall mAP @ 0.95** — aggregate score across all videos at a 95% overlap threshold
- **Per-video mAP breakdown** — individual scores for each video in the dataset

The ground truth is never exposed; it is loaded privately on the server side. If the uploaded file contains invalid video IDs or unrecognized labels, the app rejects it with a descriptive error before any scoring takes place.

---

## The Temporal mAP Metric

### What it measures

Temporal mAP evaluates how well a model detects **when** events occur in a video — not just whether they occur. Each predicted event is a time segment with a start frame and an end frame, paired with one or more labels (e.g. `polyp`, `ulcer`, `active bleeding`). The metric rewards predictions that closely overlap with the ground-truth segments and penalizes missed detections or false alarms.

### How it is calculated

**Step 1 — Temporal IoU (tIoU)**

For each pair of a predicted segment and a ground-truth segment, the app computes Temporal Intersection over Union:

```
tIoU = overlap duration / union duration
```

A tIoU of 1.0 means the prediction perfectly matches the ground truth. A tIoU of 0.0 means no overlap at all. A prediction is considered a true positive only if its tIoU with an unmatched ground-truth segment meets or exceeds the threshold (0.5 or 0.95).

**Step 2 — Average Precision (AP) per label per video**

For each video and each of the 17 labels, predictions are matched greedily to ground-truth segments. The app then builds a precision-recall curve and computes the area under it as the AP for that (video, label) pair.

**Step 3 — Per-video mAP**

The APs across all 17 labels are averaged to produce a single mAP score for that video.

**Step 4 — Overall mAP**

The per-video mAP scores are averaged across all videos to produce the final competition score, reported at both thresholds.

---

## Official Resources

- **Dataset** (GALAR Capsule Endoscopy Dataset): https://plus.figshare.com/articles/dataset/Galar_-_a_large_multi-label_video_capsule_endoscopy_dataset/25304616
- **Competition Document & Flyer** (includes sample report format): https://figshare.com/articles/preprint/ICPR_2026_RARE-VISION_Competition_Document_and_Flyer/30884858
- **GitHub Repository** (scripts + JSON generation utilities): https://github.com/RAREChallenge2026/RARE-VISION-2026-Challenge

---

## License & Reuse

This tool was developed exclusively for the **ICPR 2026 RARE-VISION Competition**.

**Prior written permission from the competition organizers is required for any reuse, redistribution, modification, or adaptation of this software outside the official competition framework.**

It is not intended for external benchmarking or commercial use.
