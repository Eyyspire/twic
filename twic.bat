@echo off
setlocal enabledelayedexpansion

REM Check if the required programs (curl and 7-Zip) are installed
where curl > nul 2>&1
if errorlevel 1 (
    echo Error: curl is not installed or not in the system path.
    echo Please download and install curl from https://curl.se/windows/
    exit /b 1
)

where 7z > nul 2>&1
if errorlevel 1 (
    echo Error: 7-Zip is not installed or not in the system path.
    echo Please download and install 7-Zip from https://www.7-zip.org/download.html
    exit /b 1
)


if "%~1"=="" (
    echo Usage: %~nx0 start_number end_number
    exit /b 1
)
set "start_number=%~1"

if "%~2"=="" (
    set "end_number=%start_number%"
)
if "%~2" NEQ "" (
    set "end_number=%~2"
)


REM Create the "downloaded games" folder in the current working directory
set "downloaded_games_folder=%cd%\downloaded_games"
if exist "%downloaded_games_folder%" rmdir /s /q "%downloaded_games_folder%"
mkdir "%downloaded_games_folder%"


REM Create a new PGN file to store all the games
set "merged_pgn=%downloaded_games_folder%\all_games_!start_number!-!end_number!.pgn"
if exist "%merged_pgn%" del "%merged_pgn%"


for /l %%i in (%start_number%,1,%end_number%) do (
    set "number=%%i"
    set "url=https://theweekinchess.com/zips/twic!number!g.zip"

    echo Downloading: !url!
    curl -O "!url!"

    echo Unzipping: twic!number!g.zip
    7z x "twic!number!g.zip" -o"twic!number!g"

    echo Moving PGN files to "downloaded games" folder
    move "twic!number!g\*.pgn" "%downloaded_games_folder%"

    echo Deleting: twic!number!g.zip and twic!number!g folder
    rmdir /s /q "twic!number!g"
    del "twic!number!g.zip"
)

REM Merge the downloaded PGN files into the "all_games.pgn" file
    for %%f in ("%downloaded_games_folder%\*.pgn") do (
        type "%%f" >> "%merged_pgn%"
    )

echo All files downloaded, unzipped, and merged into %merged_pgn% successfully.