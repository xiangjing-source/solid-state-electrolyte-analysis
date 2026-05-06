#!/usr/bin/env python3
"""OBELiX + Materials Project data source query."""
import argparse, json, re, sys, os

import typing
if not hasattr(typing, 'NotRequired'):
    import typing_extensions
    typing.NotRequired = typing_extensions.NotRequired


def parse_comp(formula):
    amounts = {}
    for el, amt in re.findall(r'([A-Z][a-z]?)([0-9]*\.?[0-9]*)', str(formula)):
        amounts[el] = amounts.get(el, 0.0) + float(amt or 1.0)
    return amounts


def query_obelix(formula, all_csv):
    import pandas as pd
    df = pd.read_csv(all_csv)
    norm = lambda x: str(x).strip().replace(' ', '').lower()
    matches = df[df['Reduced Composition'].apply(norm) == norm(formula)]
    if matches.empty:
        return None
    row = matches.iloc[0]
    result = {
        "obelix_id": str(row['ID']),
        "formula": str(row['Reduced Composition']),
        "source": "obelix",
        "true_ic": None,
        "sg_symbol": None, "sg_number": None,
        "a": None, "b": None, "c": None,
        "alpha": None, "beta": None, "gamma": None,
        "composition": None, "doi": None, "cif_available": False,
    }
    try:
        ic = float(row['Ionic conductivity (S cm-1)'])
        if ic > 0: result["true_ic"] = ic
    except: pass
    comp = row.get('True Composition')
    if pd.notna(comp) and str(comp).strip():
        result["composition"] = str(comp)
    sg_sym = row.get('Space group')
    if pd.notna(sg_sym) and str(sg_sym).strip():
        result["sg_symbol"] = str(sg_sym).strip()
    sg_num = row.get('Space group #')
    if pd.notna(sg_num):
        try: result["sg_number"] = int(sg_num)
        except: pass
    for key in ["a", "b", "c", "alpha", "beta", "gamma"]:
        val = row.get(key)
        if pd.notna(val):
            try: result[key] = float(val)
            except: pass
    cif_id = row.get('Cif ID')
    result["cif_available"] = pd.notna(cif_id) and str(cif_id).strip().lower() not in ('', 'nan', 'not available', 'none')
    return result


def query_mp(formula, api_key):
    from mp_api.client import MPRester
    try:
        with MPRester(api_key) as mpr:
            docs = mpr.materials.summary.search(
                formula=formula,
                fields=["material_id","structure","energy_above_hull",
                        "formula_pretty","formation_energy_per_atom",
                        "band_gap","is_metal","density","volume","elements","symmetry"])
            if not docs: return None
            docs.sort(key=lambda x: x.energy_above_hull or 999)
            doc = docs[0]
            s = doc.structure
            sg_symbol, sg_number = s.get_space_group_info()
            l = s.lattice
            comp_str = "".join(f"{el}{amt:.1f}" for el, amt in s.composition.items())
            return {
                "mp_id": str(doc.material_id), "formula_pretty": doc.formula_pretty,
                "source": "materials_project",
                "sg_symbol": sg_symbol, "sg_number": sg_number,
                "a": round(l.a,4), "b": round(l.b,4), "c": round(l.c,4),
                "alpha": round(l.alpha,4), "beta": round(l.beta,4), "gamma": round(l.gamma,4),
                "density": doc.density, "band_gap": doc.band_gap,
                "formation_energy": doc.formation_energy_per_atom,
                "energy_above_hull": doc.energy_above_hull,
                "elements": [str(e) for e in doc.elements], "composition": comp_str,
            }
    except Exception as e:
        return {"error": str(e), "source": "materials_project"}


def parse_cif(cif_path):
    from pymatgen.core import Structure
    try:
        s = Structure.from_file(cif_path)
        sg_symbol, sg_number = s.get_space_group_info()
        l = s.lattice
        comp_str = "".join(f"{el}{amt:.1f}" for el, amt in s.composition.items())
        return {
            "source": "cif_file", "cif_path": cif_path,
            "sg_symbol": sg_symbol, "sg_number": sg_number,
            "a": round(l.a,4), "b": round(l.b,4), "c": round(l.c,4),
            "alpha": round(l.alpha,4), "beta": round(l.beta,4), "gamma": round(l.gamma,4),
            "composition": comp_str, "reduced_formula": s.composition.reduced_formula,
            "cif_available": True, "true_ic": None,
        }
    except Exception as e:
        return {"error": str(e), "source": "cif_file"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--formula")
    parser.add_argument("--cif")
    parser.add_argument("--all-csv", default=None)
    parser.add_argument("--api-key", default="A5m28omuixgqrlfR7yopNNCJ16Tqz0AI")
    args = parser.parse_args()

    if args.all_csv is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        args.all_csv = os.path.join(script_dir, '..', 'data', 'all.csv')

    result = {"descriptors": {}, "true_ic": None, "mp_data": None, "obelix_data": None, "data_source": None}

    if args.cif:
        cif_data = parse_cif(args.cif)
        if "error" in cif_data:
            print(json.dumps({"error": cif_data["error"]}, indent=2)); sys.exit(1)
        result["descriptors"] = cif_data
        result["data_source"] = "cif_file"
        reduced = cif_data.get("reduced_formula", "")
        if os.path.exists(args.all_csv) and reduced:
            obelix = query_obelix(reduced, args.all_csv)
            if obelix and obelix.get("true_ic"):
                result["true_ic"] = obelix["true_ic"]
                result["obelix_data"] = obelix
                result["data_source"] = "cif_file+obelix_ic"
        mp = query_mp(reduced, args.api_key)
        result["mp_data"] = mp
    elif args.formula:
        obelix = query_obelix(args.formula, args.all_csv) if os.path.exists(args.all_csv) else None
        if obelix:
            result["descriptors"] = obelix
            result["data_source"] = "obelix"
            if obelix.get("true_ic"): result["true_ic"] = obelix["true_ic"]
            result["obelix_data"] = obelix
        mp = query_mp(args.formula, args.api_key)
        result["mp_data"] = mp
        if not obelix and mp and "error" not in mp:
            result["descriptors"] = mp
            result["data_source"] = "materials_project"
    else:
        print(json.dumps({"error": "Provide --formula or --cif"}, indent=2)); sys.exit(1)

    if result.get("mp_data") and "error" in result["mp_data"] and result["data_source"] == "materials_project":
        result["error"] = "No data found in OBELiX or Materials Project"

    print(json.dumps(result, indent=2, ensure_ascii=False, default=str))


if __name__ == "__main__":
    main()
