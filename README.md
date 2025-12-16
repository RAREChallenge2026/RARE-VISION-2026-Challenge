# ICPR 2026 RARE-VISION Competition

ICPR 2026 RARE-VISION: Robust AI for Rare Events in Video Capsule Endoscopy (VCE) Vision Competition
## Abstract
A growing burden of gastrointestinal (GI) diseases has increased reliance on video capsule endoscopy (VCE) for non-invasive visualization of the GI tract, thereby overcoming limitations of conventional endoscopic methods in evaluating GI tract pathology. The sheer volume of video data, coupled with the rarity of clinically relevant anomalies, introduced machine learning into this field to assist in efficient and accurate analysis by addressing challenges such as class imbalance and reducing the time required for manual review of these video data. 

The ICPR 2026 RARE-VISION Competition aims to advance this field by encouraging the development of machine learning models designed specifically to address the class imbalance challenge inherent in VCE data. Running virtually from December 15, 2025 to March 1, 2026, the competition focuses on robust classification of anatomical regions and rare pathological findings within continuous, noisy VCE video streams.

Participants will work with the Galar dataset, a large, imbalanced, multi-label VCE dataset that reflects real-world clinical conditions. Their goal is to detect both common and rare events while demonstrating innovative strategies—such as advanced sampling, loss-function engineering, data augmentation, or temporal modeling—to handle class imbalance effectively.

Submissions will be evaluated based on event-level performance metrics and the creativity and effectiveness of the proposed class-balance strategies, ensuring fairness, generalizability, and clinical relevance.

## Important links
- [Registration form](https://forms.gle/67EbJSmuQ8nBLq3q8) (open from Dec. 15, 2025 to Feb. 14, 2026)
- [Challenge Hosting Website and Github repository](https://github.com/RAREChallenge2026/RARE-VISION-2026-Challenge)
- [Challenge Document (Figshare)](https://figshare.com/articles/preprint/ICPR_2026_RARE-VISION_Competition_Document_and_Flyer/30884858?file=60375365)
- [Dataset for AI model development Link](https://doi.org/10.25452/figshare.plus.25304616)
- [Testing Dataset Link] (To be released on Feb. 14, 2026)
- [Sample Report Overleaf] (To be released on Feb. 14, 2026)
- [Submission Sanity Checker] (To be released on Feb. 14, 2026)
## Table of Content
- [Competition Overview, Timeline and Dataset Information can be found at: ](#challenge-overview)

  [Competition document](https://figshare.com/articles/preprint/ICPR_2026_RARE-VISION_Competition_Document_and_Flyer/30884858)
  [Data article](https://www.nature.com/articles/s41597-025-05112-7)
- [Sample Scripts for Participants](https://github.com/RAREChallenge2026/RARE-VISION-2026-Challenge/tree/main/sample_codes)
  - [How to download the dataset?](https://github.com/RAREChallenge2026/RARE-VISION-2026-Challenge/blob/main/sample_codes/download_dataset.py)

    Note: Participants are requested to do a disk space check before downloading the dataset. A minimum of 600 GB space is needed. The dataset is freely available at plus Figshare. The participants can also download seperate 7z files from there. This sample code will download all relevant files. 
  - [How to perform train-test splits?](https://github.com/RAREChallenge2026/RARE-VISION-2026-Challenge/blob/main/sample_codes/train_test_split.py)

      Note: Participants are allowed to choose different train-validation-test splits.
  - [How to create a JASON file?](https://github.com/RAREChallenge2026/RARE-VISION-2026-Challenge/blob/main/sample_codes/make_json.py)

     Note: Participants are ONLY allowed to use the following 17 labels -
      - Anatomical region: mouth, esophagus, stomach, small intestine, colon, z-line, pylorus, ileocecal valve (8) 
      - Pathological	findings: active	bleeding,	angiectasia,	blood,	erosion,	erythema,	hematin, lymphangioectasis, polyp, ulcer (9)
  - [Sample JASON file](https://github.com/RAREChallenge2026/RARE-VISION-2026-Challenge/blob/main/sample_codes/make_json.py)
- [Submission Format] (To be released on Feb. 14, 2026)
