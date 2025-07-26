# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['login.py'],
    pathex=[],
    binaries=[],
    datas=[('baymax.png', '.'), ('baymax2.png', '.'), ('bmi.csv', '.'), ('bmi_model_prediction.joblib', '.'), ('chatbot_model.h5', '.'), ('classes.pkl', '.'), ('data_icon.png', '.'), ('diabetes_model.joblib', '.'), ('diabetes_prediction_dataset.csv', '.'), ('emergency_contact.png', '.'), ('emergency_icon.png', '.'), ('first_aid.png', '.'), ('heart.png', '.'), ('heart_disease.csv', '.'), ('heart_disease_model.joblib', '.'), ('intents.json', '.'), ('liver_disease_model.joblib', '.'), ('liver.png', '.'), ('prescription_model.keras', '.'), ('prescription_prediction.png', '.'), ('training_labels.csv', '.'), ('words.pkl', '.'), ('bangladesh_doctors.csv', '.'), ('health.png', '.'), ('ai_prediction.png', '.'), ('diabetes.png', '.'), ('login.spec', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='login',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
