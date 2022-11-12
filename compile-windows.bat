del files\scores
pyinstaller --noconfirm --onefile --windowed --icon "icon.ico" --add-data "data;data/" --distpath "output-windows/dist" --workpath "output-windows/build"  "SneakyMath.py" 
pause