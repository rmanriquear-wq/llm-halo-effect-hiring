# LLM Halo Effect in Hiring — Empirical Study

> **Do Large Language Models replicate the halo effect in personnel selection?**  
> An empirical study using Claude Sonnet 4.6 and GPT-4o via automated API calls.

---

## Overview

This repository contains all the code, prompts, and synthetic CV assets used in an undergraduate thesis project at **TECNUN — Universidad de Navarra**, supervised by **Prof. Gonzalo Fernández Duval** (Industrial Organization Department).

The study investigates whether Large Language Models simulate the **halo effect** — a well-documented cognitive bias in which one salient positive attribute inflates evaluations across unrelated dimensions — when evaluating job candidates in a personnel selection context. Two models, two job positions, four CV versions per position, and four evaluator role prompts are combined in a fully automated pipeline to generate 320 structured evaluations.

---

## Experiment Design

| Parameter | Value |
|-----------|-------|
| Models tested | Claude Sonnet 4.6 · GPT-4o |
| Job positions | Junior Backend Developer (Unnax, Barcelona) · Digital Marketing Analyst (Wink TTD, Madrid) |
| Candidates | James Mitchell (Backend) · Laura Sánchez (Marketing) — synthetic, medium competence |
| CV versions | 4 per position (Control · Elite University · Prestigious Employer · Award) |
| Evaluator roles | 4 (HR Officer · Head of HR · CTO · CEO) |
| Evaluation dimensions | 5 (Technical Skills · Communication · Leadership Potential · Teamwork · Cultural Fit) |
| Iterations per combination | 5 (temperature = 0) |
| Total API calls | 320 (2 models × 2 positions × 4 CVs × 4 roles × 5 iterations) |
| API gateway | OpenRouter |
| Automation | n8n Cloud |
| Total cost | ~$1.92 USD |

---

### Halo attributes tested

#### Backend Developer — James Mitchell

| Version | Halo attribute | Element modified |
|---------|---------------|-----------------|
| Control | None | University of Zaragoza · Unnax |
| Test A | Elite university | Massachusetts Institute of Technology (MIT) |
| Test B | Prestigious employer | Google |
| Test C | Award / recognition | Google Hash Code International 2023 — Top 5% globally |

#### Digital Marketing Analyst — Laura Sánchez

| Version | Halo attribute | Element modified |
|---------|---------------|-----------------|
| Control | None | Universidad Complutense de Madrid · Wink TTD |
| Test A | Elite university | London School of Economics (LSE) |
| Test B | Prestigious employer | Unilever |
| Test C | Award / recognition | Cannes Lions Young Lions 2023 — Gold (Digital category) |

---

### Evaluator role prompts

Each of the four prompts simulates how a real professional in that role naturally evaluates a candidate, without any instruction to correct or neutralize bias. The goal is to observe how the halo effect manifests across the organizational hierarchy.

| Role | Evaluation focus |
|------|-----------------|
| HR Recruitment Officer | Operational screening against minimum requirements |
| Head of HR | Long-term fit, cultural alignment, development potential |
| CTO | Rigorous technical depth and evidence-based assessment |
| CEO | Strategic business impact and overall candidate impression |

---

## Repository Structure

```
llm-halo-effect-hiring/
│
├── n8n/
│   ├── code_node.js          # Generates 320 experiment combinations with full payloads
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
│   ├── james_mitchell_test_c_award.html
│   ├── laura_sanchez_control.html
│   ├── laura_sanchez_test_a_lse.html
│   ├── laura_sanchez_test_b_unilever.html
│   └── laura_sanchez_test_c_cannes.html
│
├── analysis/
│   └── statistical_analysis.py   # Full statistical analysis in Python (6 blocks)
│
├── data/
│   └── CVsDataset_final.xlsx     # Experiment results (320 rows, 23 columns)
│
└── README.md
```

---

## Pipeline Architecture

```
[Manual Trigger]
       ↓
[Code Node] → generates 320 combinations (model × position × CV × role × iteration)
       ↓
[HTTP Request] → POST to OpenRouter API (routes to Claude or GPT-4o)
       ↓
[Wait Node] → 1.5s between calls (rate limit protection)
       ↓
[Parser Node] → extracts 5 scores, justification, cost, tokens, model version, timestamp
       ↓
[Google Sheets] → stores all 320 results as structured rows (23 columns)
```

The Code node builds the complete `messages_payload` for each combination before any API call is made, avoiding JSON serialization issues with multiline text. The Parser node derives `model_id` and `model_label` directly from the API response (`model_used` field) rather than relying on upstream fields that the HTTP Request node may not propagate reliably.

---

## Dataset Structure

The output dataset (`CVsDataset_final.xlsx`) contains 320 rows and 23 columns:

| Column | Description |
|--------|-------------|
| `call_id` | Sequential identifier (1–320) |
| `model_id` | Model identifier (`claude-sonnet-4-6` / `gpt-4o`) |
| `model_label` | Human-readable model name |
| `position_id` | Job position identifier |
| `position_label` | Job position name |
| `cv_id` | CV version identifier |
| `cv_label` | CV version name |
| `role_id` | Evaluator role identifier |
| `role_label` | Evaluator role name |
| `iteration` | Iteration number (1–5) |
| `technical_skills` | Score 1–10 |
| `communication` | Score 1–10 |
| `leadership_potential` | Score 1–10 |
| `teamwork` | Score 1–10 |
| `cultural_fit` | Score 1–10 |
| `justification` | Free-text justification from the model |
| `model_used` | Exact model version string from the API |
| `cost_usd` | Cost of the API call in USD |
| `prompt_tokens` | Input token count |
| `completion_tokens` | Output token count |
| `total_tokens` | Total token count |
| `timestamp` | ISO 8601 timestamp of the call |
| `error` | Boolean error flag |

---

## Statistical Analysis

The Python analysis script (`analysis/statistical_analysis.py`) implements six analytical blocks:

1. **Descriptive statistics** — means, standard deviations, and coefficient of variation (SD/mean) by CV version, model, and position
2. **Intra-profile variance** — std across 5 iterations per combination to verify systematic (non-stochastic) bias
3. **Mean differences** — Test minus Control per dimension, model, and position (heatmaps)
4. **Effect size** — Cohen's d for each Test vs Control comparison
5. **Hypothesis testing** — Mann-Whitney U test (α = 0.05, two-sided)
6. **Inter-dimensional correlation** — Pearson correlation matrices (Control vs Test) to verify the Thorndike contamination mechanism
7. **Model and role comparison** — Claude vs GPT-4o, and susceptibility by evaluator role

### Requirements

```bash
pip install pandas scipy matplotlib seaborn openpyxl
```

### Usage

```python
# Set your file path at the top of the script
FILE_PATH = 'data/CVsDataset_final.xlsx'

# Run the full analysis
python analysis/statistical_analysis.py
```

---

## Key Findings

- **Intra-profile variance = 0 (median)** across all model/position combinations — bias is systematic, not random noise
- **Claude amplifies the halo effect** of the Award attribute in Leadership Potential (Cohen's d = 3.07 for Backend Developer), exceeding effect sizes documented for human evaluators in the behavioral psychology literature
- **GPT-4o replicates the same pattern** but with smaller magnitude (d = 1.38 for the same combination)
- **The Award is the most potent halo attribute** across both models and both job positions — a counterintuitive finding given that MIT/LSE (elite university) produces no statistically significant differences
- **Google/Unilever consistently produces a horn effect** in Cultural Fit (negative d) across both models — interpreted as a coherence-based penalization mechanism when a prestigious employer is inconsistent with a junior-level profile
- **The pattern replicates across job positions** — Backend Developer and Digital Marketing Analyst show qualitatively consistent results, supporting the external validity of the findings
- **Coefficient of variation** is systematically higher in Claude than in GPT-4o, indicating greater cross-role sensitivity to halo cues in Claude

---

## Theoretical Background

The halo effect was first documented by **Thorndike (1920)** as a "constant error in psychological ratings." This study extends that concept to LLM evaluation behavior, building on recent empirical work:

- Thorndike, E. L. (1920). *A constant error in psychological ratings*. Journal of Applied Psychology.
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

**[Your name]**  
TECNUN — Universidad de Navarra  
[your.email@alumni.unav.es]
