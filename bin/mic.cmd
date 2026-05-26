@echo off
REM M.I.C. terminal launcher - generic wrapper.
REM
REM Usage:
REM   mic              -> interactive menu of all agents in G:\MIC\agents\
REM   mic <name>       -> direct activation of named agent
REM
REM Add G:\MIC\bin to your user PATH to make this callable from any folder.

if "%~1"=="" (
    python "G:\MIC\launch.py" "G:\MIC\agents"
) else (
    python "G:\MIC\launch.py" "G:\MIC\agents" --agent "%~1"
)
