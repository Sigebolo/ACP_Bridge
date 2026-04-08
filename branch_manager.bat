@echo off
echo === ACP Bridge Branch Manager ===
echo.
echo 1. Main Branch (Public) - Only ACP Bridge core files
echo 2. Private Branch (Backup) - All files including projects
echo.
echo Current branch:
git branch --show-current
echo.
echo Available branches:
git branch
echo.
echo Switch to main (public):     git checkout main
echo Switch to private (backup):  git checkout private-backup
echo.
echo Sync private to main:
echo   git checkout main
echo   git merge private-backup --no-ff
echo   git push origin main
echo.
echo Sync all files to private:
echo   git checkout private-backup
echo   git add .
echo   git commit -m "Update private backup"
echo   git push origin private-backup
echo.
pause
