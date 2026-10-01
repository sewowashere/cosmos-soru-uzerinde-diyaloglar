import json

# Dosya yolları (Kendi dosya isimlerine göre düzenleyebilirsin)
girdi_dosyasi = "gsm8k_gemini_2_5_sonuclari-3400.json"
cikti_dosyasi = "gsm8k_gemini_2_5_sonuclari-2000.json"

try:
    # 1. JSON dosyasını oku
    with open(girdi_dosyasi, 'r', encoding='utf-8') as dosya:
        veri = json.load(dosya)
    
    # Verinin bir liste olduğundan emin olalım
    if isinstance(veri, list):
        # 2. 1999. indexten sonrasını sil 
        # ([:2000] ifadesi 0'dan 1999'a kadar olan, toplam 2000 elemanı alır)
        yeni_veri = veri[:2000]
        
        # 3. Kırpılmış veriyi yeni bir JSON dosyasına yaz
        with open(cikti_dosyasi, 'w', encoding='utf-8') as dosya:
            json.dump(yeni_veri, dosya, ensure_ascii=False, indent=2)
            
        print(f"İşlem başarılı! Orijinal eleman sayısı: {len(veri)}")
        print(f"Yeni dosyadaki eleman sayısı: {len(yeni_veri)}")
    else:
        print("Hata: JSON dosyasının kök yapısı bir liste (array) değil.")

except FileNotFoundError:
    print(f"Hata: '{girdi_dosyasi}' adlı dosya bulunamadı.")
except json.JSONDecodeError:
    print("Hata: Dosya içeriği geçerli bir JSON formatında değil.")
