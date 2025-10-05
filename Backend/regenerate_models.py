#!/usr/bin/env python3
"""
Regenerate models from the notebook using current environment
This script extracts the key parts from the notebook and retrains the models
"""
import os
from typing import Optional, Tuple
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.ensemble import HistGradientBoostingClassifier
import joblib

MJUP_TO_MEARTH = 317.828

def first_present(df, candidates):
    """Find first present column from candidates."""
    for c in candidates:
        if c in df.columns:
            return c
    return None

def _size_class(row: pd.Series, col_pl_rade, col_pl_bmasse, col_pl_bmassj) -> Optional[str]:
    """Classify by size (radius/mass)."""
    r  = row.get(col_pl_rade,  np.nan)  # Earth radii
    me = row.get(col_pl_bmasse, np.nan) # Earth masses
    mj = row.get(col_pl_bmassj, np.nan) # Jupiter masses

    if pd.notna(mj) and pd.isna(me):
        me = mj * MJUP_TO_MEARTH

    # Prefer radius
    if pd.notna(r):
        if r < 0.8:
            return "subterrestre"
        elif r < 1.5:
            return "terraneo"
        elif r < 2.5:
            return "super_tierra"
        elif r < 4.0:
            return "mini_neptuno"
        elif r < 6.0:
            return "neptuniano"
        else:
            if pd.notna(me) and me >= 2 * MJUP_TO_MEARTH:
                return "super_jupiter"
            return "joviano"

    # Fallback to mass (if available)
    if pd.notna(me):
        if me < 0.5:                 return "subterrestre"
        elif me < 2:                 return "terraneo"
        elif me < 10:                return "super_tierra"
        elif me < 20:                return "mini_neptuno"
        elif me < 50:                return "neptuniano"
        elif me >= 2 * MJUP_TO_MEARTH: return "super_jupiter"
        else:                        return "joviano"
    return None

def _thermal_class(row: pd.Series, col_pl_eqt) -> Optional[str]:
    """Classify by thermal properties."""
    teq = row.get(col_pl_eqt, np.nan)
    if pd.notna(teq):
        if teq < 400:
            return "frio"
        elif teq < 700:
            return "templado"
        elif teq < 1000:
            return "caliente"
        else:
            return "muy_caliente"
    return None

def main():
    """Main function to regenerate models."""
    print("🚀 Regenerating Exoplanet Models")
    print("=" * 50)
    
    # Load dataset
    csv_path = "kepler.csv"  # Use the kepler.csv file
    if not os.path.exists(csv_path):
        print(f"❌ Dataset file not found: {csv_path}")
        return
    
    print(f"📊 Loading dataset from {csv_path}...")
    try:
        df = pd.read_csv(csv_path, comment="#", encoding="utf-8-sig", engine="python")
    except Exception as e:
        print(f"❌ Error loading CSV: {e}")
        return
    
    print(f"✅ Dataset loaded: {df.shape}")
    
    # Detect table type and map columns
    IS_KOI = any(c.startswith("koi_") for c in df.columns)
    IS_PS  = any(c.startswith("pl_")  for c in df.columns)
    
    print(f"Detected: KOI={IS_KOI}, PS={IS_PS}")
    
    # Column mapping
    COL_PL_RADE   = first_present(df, ["pl_rade", "koi_prad"])
    COL_PL_BMASSE = first_present(df, ["pl_bmasse"])
    COL_PL_BMASSJ = first_present(df, ["pl_bmassj"])
    COL_PL_EQT    = first_present(df, ["pl_eqt", "koi_teq"])
    COL_PERIOD    = first_present(df, ["pl_orbper", "koi_period"])
    COL_ST_TEFF   = first_present(df, ["st_teff", "koi_steff"])
    COL_ST_RAD    = first_present(df, ["st_rad", "koi_srad"])
    COL_INSOL     = first_present(df, ["koi_insol"])
    
    print(f"Column mapping: RADE={COL_PL_RADE}, EQT={COL_PL_EQT}, PERIOD={COL_PERIOD}")
    
    # Build labels
    print("🏷️  Building labels...")
    
    # Size-based labels
    df["size_label"] = df.apply(lambda row: _size_class(row, COL_PL_RADE, COL_PL_BMASSE, COL_PL_BMASSJ), axis=1)
    df["thermal_label"] = df.apply(lambda row: _thermal_class(row, COL_PL_EQT), axis=1)
    
    # Combined type label (size + thermal)
    df["type_label"] = df["size_label"]
    if COL_PL_EQT is not None:
        thermal_mask = df["thermal_label"] == "muy_caliente"
        df.loc[thermal_mask, "type_label"] = df.loc[thermal_mask, "size_label"] + "_caliente"
    
    # Filter valid samples
    valid_mask = df["type_label"].notna()
    df_valid = df[valid_mask].copy()
    
    print(f"✅ Valid samples: {len(df_valid)}")
    print(f"Type distribution:")
    print(df_valid["type_label"].value_counts())
    
    # Feature columns
    num_cols = []
    cat_cols = []
    
    # Numerical features
    for col in [COL_PL_RADE, COL_PL_EQT, COL_PERIOD, COL_ST_TEFF, COL_ST_RAD, COL_INSOL]:
        if col is not None and col in df_valid.columns:
            num_cols.append(col)
    
    print(f"Numerical features: {num_cols}")
    print(f"Categorical features: {cat_cols}")
    
    # Prepare features and target
    X = df_valid[num_cols + cat_cols].copy()
    y_type = df_valid["type_label"]
    
    print(f"Feature matrix shape: {X.shape}")
    print(f"Target classes: {sorted(y_type.unique())}")
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_type, test_size=0.2, random_state=42, stratify=y_type
    )
    
    print(f"Training set: {X_train.shape}, Test set: {X_test.shape}")
    
    # Build preprocessing pipeline
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", SimpleImputer(strategy="median"), num_cols),
            ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols),
        ],
        remainder="drop"
    )
    
    # Type classifier
    print("🤖 Training type classifier...")
    clf_type = Pipeline([
        ("preprocessor", preprocessor),
        ("clf", HistGradientBoostingClassifier(
            random_state=42,
            max_iter=100,
            learning_rate=0.1
        ))
    ])
    
    clf_type.fit(X_train, y_train)
    
    # Evaluate type classifier
    y_pred_type = clf_type.predict(X_test)
    print("Type Classifier Performance:")
    print(classification_report(y_test, y_pred_type))
    
    # Binary classifier (optional - using type_label as proxy)
    print("🤖 Training binary classifier...")
    y_bin = (y_type != "unknown").astype(int)  # Simple binary classification
    
    X_train_bin, X_test_bin, y_train_bin, y_test_bin = train_test_split(
        X, y_bin, test_size=0.2, random_state=42, stratify=y_bin
    )
    
    clf_bin = Pipeline([
        ("preprocessor", preprocessor),
        ("clf", HistGradientBoostingClassifier(
            random_state=42,
            max_iter=100,
            learning_rate=0.1
        ))
    ])
    
    clf_bin.fit(X_train_bin, y_train_bin)
    
    # Evaluate binary classifier
    y_pred_bin = clf_bin.predict(X_test_bin)
    print("Binary Classifier Performance:")
    print(classification_report(y_test_bin, y_pred_bin))
    
    # Save models
    print("💾 Saving models...")
    os.makedirs("modelos", exist_ok=True)
    
    joblib.dump(clf_type, "modelos/clf_exoplanet_type.joblib")
    joblib.dump(clf_bin, "modelos/clf_is_exoplanet.joblib")
    
    # Save metadata
    meta = {
        "num_cols": num_cols,
        "cat_cols": cat_cols,
        "classes_type": sorted(y_type.unique().tolist()),
        "is_koi": bool(IS_KOI),
        "is_ps": bool(IS_PS),
        "col_alias": {
            "R_earth": COL_PL_RADE,
            "M_earth": COL_PL_BMASSE,
            "M_jup": COL_PL_BMASSJ,
            "T_eq": COL_PL_EQT,
            "period_days": COL_PERIOD,
            "st_teff": COL_ST_TEFF,
            "st_rad": COL_ST_RAD,
            "insol": COL_INSOL,
        },
    }
    
    joblib.dump(meta, "modelos/metadata.joblib")
    
    print("✅ Models saved successfully!")
    print("📁 Files created:")
    print("  - modelos/clf_exoplanet_type.joblib")
    print("  - modelos/clf_is_exoplanet.joblib") 
    print("  - modelos/metadata.joblib")
    
    # Test prediction
    print("\n🧪 Testing prediction...")
    example = {
        "koi_prad": 11.2,
        "koi_teq": 1400,
        "koi_period": 3.5,
        "koi_steff": 5600.0,
        "koi_srad": 1.0,
    }
    
    try:
        # Test the models
        clf_bin_test, clf_type_test, meta_test = load_models()
        cols = meta_test["num_cols"] + meta_test["cat_cols"]
        X_test_example = pd.DataFrame([{c: example.get(c, np.nan) for c in cols}])
        
        result = {}
        if clf_bin_test is not None:
            proba = clf_bin_test.predict_proba(X_test_example)[0, 1]
            result["is_exoplanet"] = int(proba >= 0.5)
            result["is_exoplanet_proba"] = float(proba)
        
        proba_type = clf_type_test.predict_proba(X_test_example)[0]
        pred_type = clf_type_test.predict(X_test_example)[0]
        classes = clf_type_test.named_steps["clf"].classes_
        topk = np.argsort(proba_type)[::-1][:3]
        result["type"] = str(pred_type)
        result["type_top3"] = [(str(classes[i]), float(proba_type[i])) for i in topk]
        
        print("✅ Prediction test successful!")
        print(f"Result: {result}")
        
    except Exception as e:
        print(f"❌ Prediction test failed: {e}")
        import traceback
        traceback.print_exc()

def load_models(model_dir: str = "modelos"):
    """Load the trained models and metadata."""
    clf_bin = None
    p_bin = os.path.join(model_dir, "clf_is_exoplanet.joblib")
    if os.path.exists(p_bin):
        clf_bin = joblib.load(p_bin)
    clf_type = joblib.load(os.path.join(model_dir, "clf_exoplanet_type.joblib"))
    meta = joblib.load(os.path.join(model_dir, "metadata.joblib"))
    return clf_bin, clf_type, meta

if __name__ == "__main__":
    main()
