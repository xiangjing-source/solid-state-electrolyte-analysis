# RF 模型详细信息

## 模型规格

- **算法**: RandomForest (随机森林)
- **树数量**: 300 棵 (n_estimators=300)
- **目标空间**: log10 转换（预测 log10(电导率)，再转回线性值）
- **训练数据**: OBELiX 训练集，479 条数据
- **scikit-learn 版本**: 1.7.2
- **Python 版本**: 3.10.20

## 数据集划分

| 数据集 | 条目数 | 用途 |
|--------|--------|------|
| train.csv | 479 | 模型训练 |
| test.csv | 121 | 模型评估 |
| all.csv | 600 | 完整数据（查询用）|
| processed.csv | 600 | train + test 合并版本 |

**注意**: 查询描述符和实验值时从 OBELiX **全量**（train + test）查，不区分训练/测试。

## 模型特征

- 元素组成（composition 解析后的各元素含量）
- 空间群编号（sg_number）
- 晶格参数（a, b, c, alpha, beta, gamma）
- CIF 可用标记（cif: 1/0）

## 预处理

- 晶格参数使用 StandardScaler 归一化
- 目标值 log10 转换后训练

## 模型文件位置

默认: `models/rf_model_bundle.pkl`

## 环境要求

推荐: Python 3.10+，scikit-learn 1.7.2

## 训练集元素覆盖

训练集数据中**不含**的元素：
- H（氢）
- N（氮）

**警告**: 涉及 H 或 N 的材料预测属于纯外推，数值不可信。
