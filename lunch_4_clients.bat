set loopcount=4
:loop
cd .\client
start "" python Game.py loopcount
set /a loopcount=loopcount-1
if %loopcount%==0 goto exitloop
goto loop
:exitloop