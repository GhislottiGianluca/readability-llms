# Installation

Install [conda](https://docs.anaconda.com/miniconda/) for your system. Then type:

```commandline
conda create -n analysis python=3.8
conda activate analysis
pip install -r requirements.txt
```

# Usage

```commandline
python analyze_stability_data.py --input-file stability_data.json
python analyze_survey_data.py --input-file qualtrics_data.json
```
