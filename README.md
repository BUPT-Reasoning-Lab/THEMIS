<div align="center">
<img style="width: 50%; max-width: 560px;" src="themis.png" alt="THEMIS">
<h2 align="center">THEMIS: Towards Holistic Evaluation of MLLMs for Scientific Paper Fraud Forensics</h2>

<a href="https://openreview.net/attachment?id=y3UkklvoW9&name=pdf" target="_blank"><img src="https://img.shields.io/badge/Paper-OpenReview-B31B1B?style=flat" alt="Paper" height="25"></a>
<a href="https://bupt-reasoning-lab.github.io/THEMIS/#" target="_blank"><img alt="Project Page" src="https://img.shields.io/badge/Project%20Page-THEMIS-blue.svg" height="25" /></a>
<a href="https://huggingface.co/datasets/BUPT-Reasoning-Lab/THEMIS" target="_blank"><img src="https://img.shields.io/badge/🤗%20Hugging%20Face-Dataset-yellow" alt="Hugging Face Dataset" height="25"></a>

<p>
    <img src="themis.png" alt="THEMIS" width="700">
</p>
</div>

This repository contains the evaluation code for the paper **"THEMIS: Towards Holistic Evaluation of MLLMs for Scientific Paper Fraud Forensics"**.

## 🔥 Takeaways
- **Real-World Scenarios and Complexity.** THEMIS spans seven representative academic scenarios (e.g., medical imaging and micrographs), with problems derived from authentic retracted cases and carefully constructed synthetic data, ensuring both realism and controllability. Importantly, 60.47\% of the images contain complex textures, which substantially increases the difficulty of manipulation detection.
- **Fraud-Type Diversity and Granularity.** THEMIS systematically covers five challenging fraud methods (e.g., **AI-Generated** and **Duplication**}) and introduces 16 fine-grained manipulation operations (e.g., scaling and color temperature modification). On average, each sample involves 2.08 stacked operations, producing highly diverse manipulations that require robust reasoning over composite alterations.
- **Multi-Dimensional Capability Evaluation.** To dissect model performance on these expert-level tasks, THEMIS establishes a principled mapping from fraud methods to five core reasoning capabilities that characterize expert-level visual forensics. **Expert Knowledge Utilization** evaluates whether models can incorporate prior domain knowledge to contextualize manipulations. **Visual Recognition** tests their ability to accurately perceive and distinguish complex visual elements. **Spatial Reasoning** requires understanding positional and structural relationships among manipulated components. **Region Localization** focuses on precisely identifying tampered areas at the sub-figure level. Finally, **Comparative Reasoning**assesses the ability to contrast multimodal evidence, such as cross-image or text--image consistency.

## 💼 Dataset Creation
THEMIS is a holistic benchmark specifically curated to evaluate the visual reasoning capabilities of multimodal large language models (MLLMs) in identification and localization over scientific paper forgeries. For more detailed information, please refer to our Hugging Face datasets:
- [**🤗 huggingface**](https://huggingface.co/datasets/BUPT-Reasoning-Lab/THEMIS)


## 🛠️ Installation
create a new python environment and install relevant requirements

```bash
uv sync --group benchmark
```

Active Environment:
```bash
source .env
```

### `assets/`
`dataset/`: original dataset

### `scripts`
`benchmark`: evaluation tool

### `.env-example`
`API_KEY` config example

Note: This repository does NOT support reading environment variables from .env files.
Please configure your variables directly in the config files provided.

## Contact
Haihong E: ehaihong@bupt.edu.cn

## Citation
