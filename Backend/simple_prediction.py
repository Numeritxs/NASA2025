#!/usr/bin/env python3
"""
Simple exoplanet prediction script based on the notebook
"""
import os
import numpy as np
import pandas as pd
import joblib

def load_models(model_dir: str = "modelos"):
    """Load the trained models and metadata."""
    clf_bin = None
    p_bin = os.path.join(model_dir, "clf_is_exoplanet.joblib")
    if os.path.exists(p_bin):
        clf_bin = joblib.load(p_bin)
    clf_type = joblib.load(os.path.join(model_dir, "clf_exoplanet_type.joblib"))
    meta = joblib.load(os.path.join(model_dir, "metadata.joblib"))
    return clf_bin, clf_type, meta

def predict_exoplanet(example: dict, model_dir: str = "modelos") -> dict:
    """Predict exoplanet characteristics from input data."""
    clf_bin, clf_type, meta = load_models(model_dir)
    cols = meta["num_cols"] + meta["cat_cols"]
    X = pd.DataFrame([{c: example.get(c, np.nan) for c in cols}])
    out = {}
    if clf_bin is not None:
        proba = clf_bin.predict_proba(X)[0, 1]
        out["is_exoplanet"] = int(proba >= 0.5)
        out["is_exoplanet_proba"] = float(proba)
    proba_type = clf_type.predict_proba(X)[0]
    pred_type = clf_type.predict(X)[0]
    classes = clf_type.named_steps["clf"].classes_
    topk = np.argsort(proba_type)[::-1][:3]
    out["type"] = str(pred_type)
    out["type_top3"] = [(str(classes[i]), float(proba_type[i])) for i in topk]
    return out

def main():
    """Main function to test the prediction."""
    print("🚀 Simple Exoplanet Prediction Script")
    print("=" * 50)
    
    # Check if models exist
    model_dir = "modelos"
    required_files = ["clf_exoplanet_type.joblib", "metadata.joblib"]
    
    for file in required_files:
        if not os.path.exists(os.path.join(model_dir, file)):
            print(f"❌ Missing required file: {file}")
            return
    
    print("✅ All required model files found")
    
    # Example data from the notebook
    example = {
        "koi_prad": 11.2,
        "koi_teq": 1400,
        "koi_period": 3.5,
        "koi_model_snr": 12.0,
        "koi_steff": 5600.0,
        "koi_srad": 1.0,
    }
    
    print(f"\n📊 Input data:")
    for key, value in example.items():
        print(f"  {key}: {value}")
    
    try:
        print("\n🔮 Making prediction...")
        result = predict_exoplanet(example)
        
        print("\n🎯 Prediction Results:")
        print(f"  Type: {result['type']}")
        print(f"  Top 3 Predictions:")
        for i, (type_name, probability) in enumerate(result['type_top3'], 1):
            print(f"    {i}. {type_name}: {probability:.4f} ({probability*100:.2f}%)")
        
        if 'is_exoplanet' in result:
            print(f"  Is Exoplanet: {result['is_exoplanet']} (probability: {result['is_exoplanet_proba']:.4f})")
        
        print("\n✅ Prediction completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error during prediction: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
