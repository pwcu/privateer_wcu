# build.ps1
New-Item build -ItemType Directory -Force
Push-Location .\build
cmake ..\
cmake --build .\
Pop-Location
