# Di dalam file: Stock/management/commands/updateStock.py

from django.core.management.base import BaseCommand
from stocks.models import StockData  # Sesuaikan dengan path yang benar ke model Anda
import yfinance as yf
from datetime import datetime, timedelta
import time

class Command(BaseCommand):
    help = 'Update Stock data'

    def handle(self, *args, **kwargs):
        Stocks = [
            "EMTK.JK", "ACES.JK", "ADRO.JK", "AKRA.JK", "AMRT.JK", "ANTM.JK",
            "ARTO.JK", "ASII.JK", "BBCA.JK", "BBNI.JK", "BBRI.JK", "BBTN.JK",
            "BMRI.JK", "BRPT.JK", "CPIN.JK", "ESSA.JK", "EXCL.JK", "GGRM.JK",
            "HRUM.JK", "ICBP.JK", "INDY.JK", "INKP.JK", "INTP.JK", "ITMG.JK",
            "KLBF.JK", "MAPI.JK", "MDKA.JK", "MEDC.JK", "PTBA.JK", "SCMA.JK",
            "SIDO.JK", "SRTG.JK", "TBIG.JK", "TLKM.JK", "TOWR.JK", "TPIA.JK",
            "UNVR.JK", "BRIS.JK", "BUKA.JK", "GOTO.JK", "SMGR.JK", "UNTR.JK",
            "INCO.JK", "INDF.JK", "PGAS.JK",
        ]

        # Looping terus menerus
        while True:
            for Stock in Stocks:
                self.update_Stock_data(Stock)
            time.sleep(60)  # Tunggu selama 60 detik sebelum memulai lagi

    def update_Stock_data(self, symbol):
        try:
            # Normalisasi simbol: mengganti titik dengan strip
            normalized_symbol = symbol.replace('.', '-')

            end_date = datetime.now()
            start_date = end_date - timedelta(days=7)

            # Cek data terakhir di database menggunakan simbol yang dinormalisasi
            last_entry = StockData.objects.filter(symbol=normalized_symbol).order_by('-datetime').first()
            if last_entry:
                last_date = last_entry.datetime.replace(tzinfo=None)
                if last_date >= start_date:
                    start_date = last_date + timedelta(minutes=1)

            if start_date < end_date:
                new_data = yf.download(symbol, start=start_date, end=end_date, interval='1m')
                if not new_data.empty:
                    new_data.reset_index(inplace=True)

                    for _, row in new_data.iterrows():
                        StockData.objects.create(
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