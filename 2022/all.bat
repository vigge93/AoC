@echo off
set days=%1
IF [%1]==[] set days=25
for /l %%x in (1, 1, %days%) do (
    pypy .\day%%x.py
)