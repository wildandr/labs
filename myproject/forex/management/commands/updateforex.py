# Di dalam file: Forex/management/commands/updateForex.py

from django.core.management.base import BaseCommand
from forex.models import ForexData  # Sesuaikan dengan path yang benar ke model Anda
import yfinance as yf
from datetime import datetime, timedelta
import time

class Command(BaseCommand):
    help = 'Update Forex data'

    def handle(self, *args, **kwargs):
        Forexs = [
            "EURUSD=X", "USDJPY=X", "GBPUSD=X", "AUDUSD=X", "NZDUSD=X",
            "EURJPY=X", "GBPJPY=X", "EURGBP=X", "EURCAD=X", "EURSEK=X",
            "EURCHF=X", "EURHUF=X", "USDCNY=X", "USDHKD=X", "USDSGD=X",
            "USDINR=X", "USDMXN=X", "USDPHP=X", "USDIDR=X", "USDTHB=X",
            "USDMYR=X", "USDZAR=X", "USDRUB=X"
        ]

        # Looping terus menerus
        while True:
            for Forex in Forexs:
                self.update_Forex_data(Forex)
            time.sleep(60)  # Tunggu selama 60 detik sebelum memulai lagi

    def update_Forex_data(self, symbol):
        try:
            # Normalisasi simbol: mengganti titik dengan strip
            normalized_symbol = symbol.replace('=', '-')

            end_date = datetime.now()
            start_date = end_date - timedelta(days=7)

            # Cek data terakhir di database menggunakan simbol yang dinormalisasi
            last_entry = ForexData.objects.filter(symbol=normalized_symbol).order_by('-datetime').first()
            if last_entry:
                last_date = last_entry.datetime.replace(tzinfo=None)
                if last_date >= start_date:
                    start_date = last_date + timedelta(minutes=1)

            if start_date < end_date:
                new_data = yf.download(symbol, start=start_date, end=end_date, interval='1m')
                if not new_data.empty:
                    new_data.reset_index(inplace=True)

                    for _, row in new_data.iterrows():
                        ForexData.objects.create(
                            symbol=normalized_symbol,  # Gunakan simbol yang dinormalisasi
                            datetime=row['Datetime'],
                            open_price=row['Open'],
                            high_price=row['High'],
                            low_price=row['Low'],
                            close_price=row['Close'],
                            volume=row['Volume']
                        )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error updating data for {symbol}: {e}'))