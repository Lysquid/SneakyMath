rm -f files/scores
pyinstaller --noconfirm --onefile --windowed --icon "icon.ico" --add-data "data:data/" --distpath "output-linux/dist" --workpath "output-linux/build"  "SneakyMath.py" 