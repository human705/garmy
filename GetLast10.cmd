@echo off
C:\Users\me\miniconda3\condabin\conda.bat env list

C:\Users\me\miniconda3\condabin\conda.bat activate garmy
C:\Users\me\miniconda3\envs\garmy\python.exe C:\AllRepos\myGitHubRepos\garmy\examples\cycling_activities.py
C:\Users\me\miniconda3\condabin\conda.bat deactivate


REM  c:; cd 'c:\AllRepos\myGitHubRepos\garmy'; & 'c:\Users\me\miniconda3\envs\garmy\python.exe' 'c:\Users\me\.vscode\extensions\ms-python.debugpy-2025.18.0-win32-x64\bundled\libs\debugpy\launcher' '38548' '--' 'C:\AllRepos\myGitHubRepos\garmy\examples\cycling_activities.py'