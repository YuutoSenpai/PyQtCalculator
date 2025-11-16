import PyInstaller.__main__
import os
import shutil

print("🔨 Vytvářím Kalkulacka.exe s ikonou...")

# Nejprve zkontrolovat existenci ikony
if not os.path.exists('calculator.ico'):
    print("❌ Soubor calculator.ico nebyl nalezen!")
    print("📁 Ujistěte se, že ikona je ve stejné složce jako calculator.py")
    exit(1)

print("✅ Ikona nalezena")

# Vytvořit EXE s ikonou
PyInstaller.__main__.run([
    'calculator.py',
    '--onefile',
    '--windowed',
    '--name=Kalkulacka',
    '--icon=calculator.ico',
    '--clean',
    '--noconfirm',
])

# Přesunout EXE do hlavní složky
if os.path.exists('dist/Kalkulacka.exe'):
    shutil.copy2('dist/Kalkulacka.exe', 'Kalkulacka.exe')
    print("✅ Hotovo! Kalkulacka.exe s ikonou je připraven.")

    # Uklidit
    for folder in ['build', 'dist']:
        if os.path.exists(folder):
            shutil.rmtree(folder)
else:
    print("❌ Chyba: EXE soubor se nevytvořil")