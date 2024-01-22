from django.core.management.commands.runserver import Command as RunserverCommand
import subprocess
import os
import sys

class Command(RunserverCommand):
    help = 'Runs the development server and starts the forex and crypto update scripts.'

    def handle(self, *args, **options):
        # Jalankan skrip updateforex.py dan updatecrypto.py
        self.start_script('myproject/forex/management/commands/updateforex.py')
        self.start_script('myproject/crypto/management/commands/updatecrypto.py')

        # Jalankan server
        super().handle(*args, **options)

    def start_script(self, script_path):
        # Pastikan script_path adalah path yang benar dari manage.py
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        full_script_path = os.path.join(base_dir, script_path)
        
        # Menjalankan skrip dengan subprocess dan mencetak outputnya
        process = subprocess.Popen(
            ['python', full_script_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False
        )
        # Mencetak output
        for line in iter(process.stdout.readline, b''):
            sys.stdout.write(line.decode(sys.stdout.encoding))
        # Mencetak error jika ada
        for line in iter(process.stderr.readline, b''):
            sys.stderr.write(line.decode(sys.stderr.encoding))
