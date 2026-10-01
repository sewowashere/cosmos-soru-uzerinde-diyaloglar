import pandas as pd
import json
import re
import os

def extract_answer(text):
    # Metni #### işaretlerine göre böleriz
    parts = text.split('####')
    
    if len(parts) > 1:
        last_part = parts[-1].strip()
        # Bu kısmın içindeki İLK sayısal değeri (negatif veya ondalıklı dahil) ararız
        num = re.search(r'-?\d+(?:[.,]\d+)?', last_part)
        
        if num:
            return num.group(0).replace(',', '.')
    return None

def clean_gt(gt):
    return str(gt).strip().replace(',', '.')

def check_correctness(gt, extracted):
    """Çıkarılan cevabın ground_truth ile eşleşip eşleşmediğini kontrol eder."""
    if extracted is None:
        return False
    try:
        if float(extracted) == float(gt):
            return True
        elif extracted == gt:
            return True
    except ValueError:
        if extracted == gt:
            return True
    return False

def compare_two_files(file1, file2):
    if not os.path.exists(file1) or not os.path.exists(file2):
        print("Hata: Belirtilen dosyalardan biri veya her ikisi bulunamadı!")
        return None
        
    with open(file1, 'r', encoding='utf-8') as f1, open(file2, 'r', encoding='utf-8') as f2:
        # Verileri "idx" key'ine göre bir sözlüğe (dictionary) dönüştürüyoruz 
        # Böylece iki dosyadaki aynı soruları eşleştirebiliriz.
        data1 = {item.get("idx"): item for item in json.load(f1)}
        data2 = {item.get("idx"): item for item in json.load(f2)}
        
    differences = []
    
    # Her iki dosyada da ortak olan idx'leri bulalım
    common_indices = set(data1.keys()).intersection(set(data2.keys()))
    
    for idx in sorted(common_indices):
        item1 = data1[idx]
        item2 = data2[idx]
        
        gt = clean_gt(item1.get("ground_truth", ""))
        question_text = str(item1.get("question", ""))
        
        # Dosya 1 için değerlendirme
        ext1 = extract_answer(str(item1.get("raw_output", "")))
        corr1 = check_correctness(gt, ext1)
        
        # Dosya 2 için değerlendirme
        ext2 = extract_answer(str(item2.get("raw_output", "")))
        corr2 = check_correctness(gt, ext2)
        
        # Eğer sonuçlar birbirinden farklıysa (biri doğru biri yanlış VEYA farklı sayılar çıkarmışlar)
        if (corr1 != corr2) or (ext1 != ext2):
            differences.append({
                "idx": idx,
                "ground_truth": gt,
                "dosya1_cevap": ext1,
                "dosya1_dogru_mu": corr1,
                "dosya2_cevap": ext2,
                "dosya2_dogru_mu": corr2,
                "fark_turu": "Biri Doğru / Diğeri Yanlış" if corr1 != corr2 else "İkisi de Yanlış ama Farklı",
                "soru_kisa": question_text[:60] + "..." # Ekrana sığması için sorunun ilk 60 karakteri
            })
            
    if differences:
        df_diff = pd.DataFrame(differences)
        print("\n=== FARKLI ÇÖZÜLEN SORULAR ===")
        print(df_diff.to_string(index=False))
        return df_diff
    else:
        print("\nSonuç: İki dosyadaki tüm çözümler birebir aynı!")
        return None

# ==========================================
# KULLANIM:
# Aşağıdaki yolları kendi dosya isimlerinizle değiştirin
# ==========================================

dosya_1 = "ckpt_top2_tuzak-kritik-1000-disjoint-deneme5_test.json"
#dosya_2 = "ckpt_top2_tuzak50-kritik50_test.json"
dosya_2 = "ckpt_top2_tuzak-kritik-1000-disjoint-deneme6_test.json"

#dosya_1 = "ckpt_top2_tuzak-kritik-1000-disjoint_test.json"
#dosya_2 = "ckpt_top2_tuzak-kritik-1000-disjoint_test-yeni.json"


df_farklar = compare_two_files(dosya_1, dosya_2)

# İsterseniz farklı çözülen soruları ayrı bir CSV veya Excel olarak da kaydedebilirsiniz:
# if df_farklar is not None:
#     df_farklar.to_excel("farkli_cozulenler.xlsx", index=False)
