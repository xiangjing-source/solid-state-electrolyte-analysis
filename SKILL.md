---
name: solid-state-electrolyte-analysis
description: "All-in-one skill for solid-state battery electrolyte analysis: acquire data (OBELiX + Materials Project + CIF), predict ionic conductivity (RandomForest), and generate comprehensive assessment reports. Orchestrates obelix-data-source and rf-conductivity-predict, then adds LLM-supplemented non-numerical info (safety, supply chain, literature). Output is a standardized 7-section markdown report with full data provenance. Triggers: user asks to generate a material report, predict ionic conductivity for a solid-state battery material, or analyze a chemical formula/CIF file for battery application."
---

# Solid-State Electrolyte Analysis

All-in-one skill for solid-state battery electrolyte candidate analysis: data acquisition → model prediction → report generation.

## Workflow

```
Input (formula or CIF file)
  │
  ├─→ Step 1: Data Acquisition (obelix-data-source)
  │       ├─ Query OBELiX dataset (all.csv, 600 entries)
  │       ├─ Query Materials Project API (mp_id, structural data)
  │       └─ Parse CIF file (if provided)
  │
  ├─→ Step 2: RF Model Prediction (rf-conductivity-predict)
  │       ├─ Use pre-trained RandomForest model (300 trees)
  │       └─ Output predicted ionic conductivity with optional error calculation
  │
  └─→ Step 3: Report Generation (LLM + template)
          ├─ Combine structured data with LLM-supplemented info
          └─ Generate 7-section markdown report with full data provenance
```

## Step 1: Data Acquisition

```bash
# Formula mode
python scripts/obelix_query.py --formula "Li10GeP2S12"

# CIF mode
python scripts/obelix_query.py --cif /path/to/file.cif
```

Parse JSON output. Extract: composition, sg_number, a/b/c/α/β/γ, true_ic, mp_id.

If `{"error": "..."}` → material not found anywhere. Tell user: provide CIF file, or choose a different material.

## Step 2: Run RF Model Prediction

```bash
python scripts/rf_predict.py --json '{
  "composition": "Li20.0Ge2.0P4.0S24.0",
  "sg_number": 137,
  "a": 8.719, "b": 8.719, "c": 12.639,
  "alpha": 90, "beta": 90, "gamma": 90,
  "cif": 1,
  "true_ic": 0.0121
}'
```

Parse JSON output. Extract: predicted_ic, percentage_error (if true_ic exists).

## Step 3: Generate Report

Use the 7-section template (see references/report_template.md).

**Critical rules for report content:**

1. **Data provenance**: Every numerical field must tag its source
   - `（来源：OBELiX 数据集 ID: xxx｜训练集）`
   - `（来源：Materials Project｜mp-xxxxx）`
   - `（来源：RF 模型预测）`
   - `（来源：LLM 知识补全）` — only for non-numerical fields
2. **No fabricated numbers**: Never use LLM "knowledge recall" for space groups, lattice parameters, conductivity
3. **Unseen materials**: If material not in OBELiX, explicitly state prediction is extrapolation with low confidence
4. **CIF vs DB mismatch**: If CIF parameters differ from OBELiX/MP, flag in report
5. **MP link**: Always append at report end:
   `https://next-gen.materialsproject.org/materials/{mp_id}?formula={化学式}`
   If MP has no entry: state "Materials Project 中暂无收录"

## Report Sections

1. 基础化学信息（分子式、MW、外观、密度）
2. 晶体结构与理化性质（空间群、晶胞参数、热稳定性）
3. 电化学核心性能（预测电导率、真实值、误差、窗口）
4. 安全与风险评估
5. 商用试剂与供应链
6. 标准化数据与补充信息（SMILES、MP数据、文献）
7. 固态电池材料适配性推荐结论（优势/短板/最终推荐）

## Confidence Levels

| Condition | Confidence | Report Label |
|-----------|-----------|-------------|
| In OBELiX train set | High | 模型训练集内验证 |
| In OBELiX test set | Medium | 模型测试集，已知材料 |
| Not in OBELiX, elements in training | Low | 训练集外推，方向参考 |
| Not in OBELiX, elements NOT in training | Very Low | 纯外推，不可信 |

## Environment & Dependencies

### Python Environment

- **Recommended**: Create a virtual environment
- **Required packages**: pandas, pymatgen, mp-api, scikit-learn, typing-extensions

```bash
# Create and activate venv
python3 -m venv venv
source venv/bin/activate
pip install pandas pymatgen mp-api scikit-learn typing-extensions
```

### Proxy for MP API (if needed)

```bash
export http_proxy=http://127.0.0.1:7897
export https_proxy=http://127.0.0.1:7897
```

## Key Rules & Warnings

**⚠️ Core Lessons (详见 references/lessons_learned.md):**
- ⚠️ Scientific parameters must come from data sources, prohibit LLM fabrication (space groups, lattice parameters, etc.)
- ⚠️ mp_id must come from real query, prohibit fabrication
- ⚠️ CIF file parameters may differ from OBELiX/MP, flag differences
- ⚠️ Training set does not contain elements H, N — predictions with these are pure extrapolation, unreliable
- ⚠️ Unseen materials must be labeled with low confidence

## Model Details

- **Algorithm**: RandomForest, 300 trees, log10 target space
- **Training data**: OBELiX train set, 479 entries
- **scikit-learn version**: 1.7.2
- **Model file**: models/rf_model_bundle.pkl

## Data Locations

- **OBELiX dataset**: data/all.csv (600 entries, train + test)
- **RF model**: models/rf_model_bundle.pkl (if available)
- **Report template**: references/report_template.md
- **Lessons learned**: references/lessons_learned.md
- **MP API notes**: references/mp_api_notes.md
- **Model details**: references/model_details.md
- **Example materials**: references/example_materials.md

## Usage Examples

### Li₁₀GeP₂S₁₂ (LGPS)
- OBELiX: ID j8q, train set
- Predicted conductivity: ~1.1e-2 S/cm
- True experimental value: ~1.2e-2 S/cm
- Error: ~8%
- Confidence: High

### Li₃ErCl₆
- Not in OBELiX, MP ID: mp-676361
- Type: unseen (extrapolation)
- Confidence: Low

---

> **Previous skills integrated:** obelix-data-source, rf-conductivity-predict, material-assessment-report
