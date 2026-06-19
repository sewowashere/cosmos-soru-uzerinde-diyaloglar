import pandas as pd
import json
import re
import os

def extract_answer(text):
    # Metindeki İLK '####' işaretini ve o satırdaki (satır sonuna kadar) karakterleri yakala
    match = re.search(r'####\s*([^\n]+)', text)
    if match:
        # Yakalanan değer (Örn: "6", " 16.00 ", " -14.05 ")
        extracted_raw = match.group(1).strip()
        
        # Sadece rakam, eksi (-) ve virgül/nokta kalsın, geri kalan harf/boşluk vb. silinsin
        clean_str = re.sub(r'[^\d.,-]', '', extracted_raw)
        
        # Virgülleri noktaya çevir ki float'a rahat dönüşsün
        return clean_str.replace(',', '.')
        
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

    "ckpt_model_trained_w_all_ds_test.json",
    "ckpt_model_trained_w_all_ds_train.json",

    "ckpt_model_trained_w-farkli-yaklasim-2k_test.json"
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
