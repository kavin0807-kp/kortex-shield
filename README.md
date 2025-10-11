 # kortex-shield

 # Kortex Shield - Architecture & Enhancements

## Overview
Kortex Shield is an experimental pipeline to detect malicious web traffic using a learned model and multi-source telemetry. It includes:

- Nginx front-proxy + Tomcat JSP apps (demo vulnerable apps)
- A benign traffic generator (benign_crawler)
- Log parsing & normalization pipeline
- Tokenizer & training pipeline (HuggingFace-style)
- Inference service (FastAPI) exposing `/analyze` endpoint and Prometheus metrics
- Continuous fine-tuning script
- Monitoring via Prometheus (optionally Grafana)

## Key model improvements to reduce false positives / negatives
1. **Balanced sampling & class weighting**: ensures minority classes (attacks) are seen during training to avoid dominant benign bias.
2. **Data normalization**: careful canonicalization of URLs/params reduces noisy features.
3. **Data augmentation**: simple transformations (id masking, parameter shuffling) increase model robustness.
4. **Validation and early stopping**: prevents overfitting and reduces false positives on unseen benign data.
5. **Checkpointing and warm-start fine-tuning**: enables continuous learning with human-in-the-loop label correction.
6. **Calibration**: (recommended) run a Platt scaling or isotonic regression calibration step on validation set to make model scores actionable.
7. **Monitoring & metrics**: track request rates, inference latency, label distribution, and alerts on model drift.

## Deployment notes
- **Do not deploy demo vulnerable JSPs to public networks.** Use an isolated lab/VPC.
- **Tokenization & model artifacts** should be managed in an artifact registry.
- **Production model** should be trained on properly labeled datasets and audited.

## Next steps
- Replace synthetic labeling heuristics with curated labeled datasets.
- Add adversarial training (bug-hunting vs. red-team lab).
- Implement safe rollback and shadow deployment to validate model changes before live use.
