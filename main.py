import time
import telebot
import yfinance as yf
from finvizfinance.screener.overview import Overview

# إعدادات البوت
BOT_TOKEN = "YOUR_TOKEN_HERE"
CHAT_ID = "YOUR_CHAT_ID_HERE"
bot = telebot.TeleBot(BOT_TOKEN)

def get_top_active_from_finviz():
    try:
        # جلب قائمة الأكثر نشاطاً من Finviz
        foverview = Overview()
        foverview.set_filter(signal='Most Active')
        df = foverview.screener_view()
        # نأخذ أول 100 رمز
        tickers = df['Ticker'].head(100).tolist()
        return tickers
    except Exception as e:
        print(f"خطأ في جلب البيانات من Finviz: {e}")
        return []

def scan_stocks():
    tickers = get_top_active_from_finviz()
    print(f"تم جلب {len(tickers)} سهم من Finviz... جاري الفحص.")
    
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="1mo")
            
            if len(hist) < 20: continue
            
            current_price = hist['Close'].iloc[-1]
            current_vol = hist['Volume'].iloc[-1]
            avg_vol = hist['Volume'].iloc[-20:].mean()
            
            # الفلترة المطلوبة: السعر بين 0.20 و 10$ + فوليوم مؤسسي
            if 0.20 <= current_price <= 10.00 and current_vol > (avg_vol * 3):
                msg = (f"🚀 **فرصة سيولة مؤسسية مكتشفة!**\n\n"
                       f"📌 الرمز: ${ticker}\n"
                       f"💰 السعر: {current_price:.2f}$\n"
                       f"📈 السيولة: {current_vol/avg_vol:.1f}x من المتوسط")
                bot.send_message(CHAT_ID, msg)
                
        except Exception as e:
            continue

if __name__ == "__main__":
    while True:
        scan_stocks()
        time.sleep(300) # انتظار 5 دقائق
