# LLM Halo Effect in Hiring — Empirical Study

> **Do Large Language Models replicate the halo effect in personnel selection?**  
> An empirical study using Claude Sonnet 4.6 and GPT-4o via automated API calls.

---

## Overview

This repository contains all the code, prompts, and synthetic CV assets used in an undergraduate thesis project at **TECNUN — Universidad de Navarra**, supervised by **Prof. Gonzalo Fernández Duval** (Industrial Organization Department).

The study investigates whether Large Language Models simulate the **halo effect** — a well-documented cognitive bias in which one salient positive attribute inflates evaluations across unrelated dimensions — when evaluating job candidates in a personnel selection context.

---

## Experiment Design

| Parameter | Value |
|-----------|-------|
| Models tested | Claude Sonnet 4.6 · GPT-4o |
| Job position | Junior Backend Developer (real job posting, Unnax — Barcelona) |
| Candidate | James Mitchell (synthetic, medium competence profile) |
| CV versions | 4 (Control · MIT · Google · Google Hash Code Award) |
| Evaluator roles | 4 (HR Officer · Head of HR · CTO · CEO) |
| Iterations per combination | 5 (temperature = 0) |
| Total API calls | 160 (2 models × 4 CVs × 4 roles × 5 iterations) |
| API gateway | OpenRouter |
| Automation | n8n Cloud |
| Total cost | ~$0.96 USD |

### Halo attributes tested

| Version | Halo attribute | Element modified |
|---------|---------------|-----------------|
| Control | None | University of Zaragoza · Unnax |
| Test A | Elite university | Massachusetts Institute of Technology (MIT) |
| Test B | Prestigious employer | Google |
| Test C | Award / recognition | Google Hash Code International 2023 — Top 5% globally |

### Evaluation dimensions (scored 1–10)

- Technical skills
- Communication
- Leadership potential
- Cultural fit

---

## Repository Structure

```
llm-halo-effect-hiring/
│
├── n8n/
│   ├── code_node.js          # Generates 160 experiment combinations
│   └── parser_node.js        # Cleans and extracts scores from API responses
│
├── prompts/
│   ├── hr_officer.txt        # HR Recruitment Officer system prompt
│   ├── head_hr.txt           # Head of HR system prompt
│   ├── cto.txt               # CTO system prompt
│   └── ceo.txt               # CEO system prompt
│
├── cvs/
│   ├── james_mitchell_control.html
│   ├── james_mitchell_test_a_mit.html
│   ├── james_mitchell_test_b_google.html
│   └── james_mitchell_test_c_award.html
│
├── analysis/
│   └── statistical_analysis.py   # Full statistical analysis (Python)
│
├── data/
│   └── CVsDataset.xlsx           # Raw experiment results (160 rows)
│
└── README.md
```

---

## Pipeline Architecture

```
[Manual Trigger]
       ↓
[Code Node] → generates 160 combinations (model × CV × role × iteration)
       ↓
[HTTP Request] → POST to OpenRouter API (Claude / GPT-4o)
       ↓
[Wait Node] → 1.5s between calls (rate limit protection)
       ↓
[Parser Node] → extracts scores, cost, tokens, timestamp, model version
       ↓
[Google Sheets] → stores all 160 results as structured rows
```

---

## Statistical Analysis

The Python analysis script (`analysis/statistical_analysis.py`) covers:

1. **Descriptive statistics** — means and standard deviations by CV version and model
2. **Intra-profile variance** — std across 5 iterations per combination (consistency check)
3. **Mean differences** — Test vs Control per dimension and model
4. **Effect size** — Cohen's d (Control vs each Test version)
5. **Hypothesis testing** — Mann-Whitney U test (α = 0.05)
6. **Inter-dimensional correlation** — Pearson correlation matrix (Control vs Test)
7. **Model comparison** — Claude vs GPT-4o across all halo attributes and evaluator roles

### Requirements

```bash
pip install pandas scipy matplotlib seaborn openpyxl
```

### Usage

```python
# Set your file path at the top of the script
FILE_PATH = 'data/CVsDataset.xlsx'

# Run the full analysis
python analysis/statistical_analysis.py
```

---

## Key Findings (Preliminary)

- **Intra-profile variance ≈ 0** across all combinations → bias is systematic, not random noise
- **Claude** shows a pronounced halo effect in `leadership_potential` with the Award attribute (Cohen's d = large effect)
- **GPT-4o** shows smaller and more distributed differences across versions
- The most potent halo attribute is **not MIT** (elite university) but the **Google Hash Code Award** — a counterintuitive finding
- The Google employer attribute **lowers** GPT-4o scores slightly, suggesting the model may penalize profile inconsistency

---

## Theoretical Background

The halo effect was first documented by **Thorndike (1920)** as a "constant error in psychological ratings." This study extends that concept to LLM evaluation behavior, building on recent empirical work:

- An et al. (2025) — *Measuring gender and racial biases in LLMs* (PNAS)
- Kim et al. (2025) — *Unveiling the Halo Effect of MLLM in AI Hiring* (ACL)
- Iso et al. (2025) — *Evaluating Bias in LLMs for Job-Resume Matching* (ACL/NAACL)
- Cheung et al. (2025) — *LLMs show amplified cognitive biases in moral decision-making* (PNAS)

---

## Academic Context

| | |
|---|---|
| Institution | TECNUN — Universidad de Navarra |
| Department | Industrial Organization |
| Supervisor | Prof. Gonzalo Fernández Duval |
| Degree | Industrial Engineering (GIOI) |
| Academic year | 2024–2025 |

---

## License

This repository is shared for academic and research purposes.  
Please cite this work if you use or build upon it.

---

## Author

Ricardo Manrique Arosemena
TECNUN — Universidad de Navarra  
[rmanriquear@alumni.unav.es]
