#!/usr/bin/env python3
"""
RF model prediction for ionic conductivity.
Usage:
  python rf_predict.py --composition "Li20.0Ge2.0P4.0S24.0" --sg-number 137 --a 8.719 --b 8.719 --c 12.639 --alpha 90 --beta 90 --gamma 90 --cif 1
  python rf_predict.py --json '{"composition":"Li20.0Ge2.0P4.0S24.0","sg_number":137,"a":8.719,"b":8.719,"c":12.639,"alpha":90,"beta":90,"gamma":90,"cif":1}'
Output: JSON with predicted IC, optionally error vs true value.
Requires: scikit-learn, pandas
"""
import argparse, json, math, re, sys, os

def parse_comp(formula):
    amounts = {}
    for el, amt in re.findall(r'([A-Z][a-z]?)([0-9]*\.?[0-9]*)', str(formula)):
        amounts[el] = amounts.get(el, 0.0) + float(amt or 1.0)
    return amounts


def predict(composition, sg_number, a, b, c, alpha, beta, gamma, cif_flag, true_ic, model_path):
    import pickle
    import pandas as pd

    with open(model_path, 'rb') as f:
        bundle = pickle.load(f)
    model = bundle['model']
    scaler = bundle['scaler']
    expected_features = list(bundle['train_columns'])[:-1]

    test = {f: 0.0 for f in expected_features}
    for el, amt in parse_comp(composition).items():
        if el in test:
            test[el] = amt
        else:
            print(json.dumps({"warning": f"Element {el} not in training features"}), file=sys.stderr)
    test['Space group number'] = sg_number
    test['a'] = a; test['b'] = b; test['c'] = c
    test['alpha'] = alpha; test['beta'] = beta; test['gamma'] = gamma
    test['CIF'] = float(cif_flag)

    x = pd.DataFrame([test], columns=expected_features)
    lc = [c for c in ['a','b','c','alpha','beta','gamma'] if c in x.columns]
    for col in lc:
        x[col] = x[col].astype(float)
    x.loc[:, lc] = scaler.transform(x.loc[:, lc])

    pred_log = model.predict(x.to_numpy())[0]
    pred = 10.0 ** pred_log

    result = {
        "predicted_log10_ic": round(pred_log, 4),
        "predicted_ic": pred,
        "predicted_ic_str": f"{pred:.4e}",
        "model": "RandomForest (n_estimators=300, log10 target)",
        "sklearn_version": "1.7.2",
    }

    if true_ic:
        pct_err = abs(pred - true_ic) / abs(true_ic) * 100
        log_err = abs(math.log10(pred) - math.log10(true_ic))
        result["true_ic"] = true_ic
        result["true_ic_str"] = f"{true_ic:.4e}"
        result["percentage_error"] = round(pct_err, 2)
        result["log10_error"] = round(log_err, 4)

    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", help="JSON string with all parameters")
    parser.add_argument("--composition")
    parser.add_argument("--sg-number", type=int)
    parser.add_argument("--a", type=float)
    parser.add_argument("--b", type=float)
    parser.add_argument("--c", type=float)
    parser.add_argument("--alpha", type=float, default=90.0)
    parser.add_argument("--beta", type=float, default=90.0)
    parser.add_argument("--gamma", type=float, default=90.0)
    parser.add_argument("--cif", type=int, default=1)
    parser.add_argument("--true-ic", type=float, default=None)
    parser.add_argument("--model-path", default=None)
    args = parser.parse_args()

    if args.model_path is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        args.model_path = os.path.join(script_dir, '..', 'models', 'rf_model_bundle.pkl')

    if args.json:
        params = json.loads(args.json)
        composition = params["composition"]
        sg_number = params["sg_number"]
        a, b, c = params["a"], params["b"], params["c"]
        alpha = params.get("alpha", 90.0)
        beta = params.get("beta", 90.0)
        gamma = params.get("gamma", 90.0)
        cif_flag = params.get("cif", 1)
        true_ic = params.get("true_ic")
    else:
        composition = args.composition
        sg_number = args.sg_number
        a, b, c = args.a, args.b, args.c
        alpha, beta, gamma = args.alpha, args.beta, args.gamma
        cif_flag = args.cif
        true_ic = args.true_ic

    result = predict(composition, sg_number, a, b, c, alpha, beta, gamma, cif_flag, true_ic, args.model_path)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
