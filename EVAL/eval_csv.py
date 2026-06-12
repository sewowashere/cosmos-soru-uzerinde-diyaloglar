import pandas as pd
import json
import re
import os

def extract_answer(text):
    # Metni #### işaretlerine göre böleriz
    parts = text.split('####')
    if len(parts) > 1:
        # En son #### işaretinden sonra gelen kısmı izole ederiz
        last_part = parts[-1].strip()
        
        # Bu kısmın içindeki İLK sayısal değeri (negatif veya ondalıklı dahil) ararız
        num = re.search(r'-?\d+(?:[.,]\d+)?', last_part)
        if num:
            return num.group(0).replace(',', '.')
            
            
    return None

def clean_gt(gt):
    return str(gt).strip().replace(',', '.')

def reevaluate_file(filepath):
    if not os.path.exists(filepath):
        print(f"Uyarı: {filepath} dosyası bulunamadı, atlanıyor.")
        return None
        
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    correct = 0
    total = len(data)
    
    for item in data:
        gt = clean_gt(item.get("ground_truth", ""))
        raw_out = str(item.get("raw_output", ""))
        extracted = extract_answer(raw_out)
        
        try:
            if float(extracted) == float(gt):
                correct += 1
            elif extracted == gt:
                correct += 1
        except:
            if extracted == gt:
                correct += 1
                
    return {"file": filepath, "acc": (correct/total)*100}

# Dosya listesi (Yorum satırları temizlendi ve virgül hataları giderildi)
files = [
    "ckpt_farkli_yaklasim_test_son.json",
    "ckpt_farkli_yaklasim_train_son.json",
    
    "ckpt_tuzak-2k_test_son.json",
    "ckpt_tuzak-2k_train_son.json",

    "ckpt_kritik_nokta_test_son.json",
    "ckpt_kritik_nokta_train_son.json",
    
    "ckpt_on_bilgi_test_son.json",
    "ckpt_on_bilgi_train_son.json",

    "ckpt_tuzak_test_son.json",
    "ckpt_tuzak_train_son.json",
    
    "ckpt_vanilya_test_son.json",
    "ckpt_vanilya_train_son.json",

    "ckpt_model_trained_w_all_ds_test.json"
]

res_list = []
for f in files:
    r = reevaluate_file(f)
    if r:
        res_list.append(r)

if res_list:
    df_eval = pd.DataFrame(res_list)
    print("\n=== DEĞERLENDİRME SONUÇLARI ===")
    print(df_eval.to_string(index=False))
else:
    print("\nHata: Belirtilen dosyaların hiçbiri dizinde bulunamadı veya okunamadı!")