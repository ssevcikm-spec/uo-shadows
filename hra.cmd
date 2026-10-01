@echo off
rem Spusti hru UO Shadows lokalne (bez otevirani Godot editoru).
rem
rem PROC TO EXISTUJE: webova verze na GitHub Pages se stavi z commitu na vetvi
rem `main` (workflow release.yml). Co neni pushnute, na Pages NENI - takze
rem lokalni spusteni je jedina cesta, jak videt zmeny, ktere jeste nejsou v gitu.
rem
rem Godot je zkopirovany v orchestra\tools\godot (instalator ho nikam
rem nepridava do PATH). Kdyz tam neni, nastav FORGE_GODOT.
setlocal
set "HRA=%~dp0"
if "%FORGE_GODOT%"=="" (
  set "FORGE_GODOT=%HRA%..\..\orchestra\tools\godot\Godot_v4.7.2-stable_win64_console.exe"
)
if not exist "%FORGE_GODOT%" (
  echo CHYBA: Godot nenalezen na "%FORGE_GODOT%"
  echo Nastav promennou FORGE_GODOT na cestu ke spustitelnemu souboru Godotu.
  pause
  exit /b 1
)
rem --user-data-dir: Godot si jinak pise do %APPDATA%\Godot a v sandboxu to
rem spadne na "Could not open 'user://' directory". Slozka v TEMP je vzdy zapisovatelna.
set "DATA=%TEMP%\uo-shadows-hrani"
if not exist "%DATA%" mkdir "%DATA%"

echo Startuji UO Shadows...
"%FORGE_GODOT%" --path "%HRA%." --user-data-dir "%DATA%" --resolution 960x540 %*
if errorlevel 1 (
  echo.
  echo Hra skoncila s chybou. Zkus ji spustit s --import, kdyby chybely assety:
  echo   "%FORGE_GODOT%" --headless --path "%HRA%." --import
  pause
)
endlocal
