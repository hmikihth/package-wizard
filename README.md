Summary
---------
== English ==

Qt based Software package manager via PackageKit. 
Extra features a fancy gui for Python Pip and Node Npm modules install
and managing. This is a subproject of blackPanther OS distribution development. 

This tool a very easy to use application. 
Click and install any RPM, DEB packages via PkCon (PackageKit)

*****************
Összefoglalás
---------
== Hungarian ==

Qt5 alapú disztrófüggetlen szoftvercsomag kezelő és telepítő PackageKit alapokon
Extra tulajdonsága egy csinos felületent túl, a Python Pip és Node Npm modulok telepítése, 
kezelése.  Ez a fejelsztés a FusionLogic® keretrendszer moduláriS része, ami egy alprojekt 
a blackPanther OS disztribúció fejlesztésében.

© Szabadon elérhető bárkinek a szerzői oldal megjelenítése mellett, és a GPL3 szabályok betartásával.

Ez egy nagyon egyszerű és látványos alkalmazás, csak kattints rá egy RPM, DEB csomagkra és
telepítsd a rendszer-PackageKit használatával.

Az alkalmazás egy roppant könnyen használható program.
Kattintson és telepítsen bármilyen alkalmazáscsomagot kedvenc rendszerére.

Fejlesztés alatt:
 - a képeken is látható arculat beállítása a disztribúciónak megfelelően már a setup szakaszban
 - arculat javítása
 - a kihagyott feliratok honosítása
 - más csomagkezelő alkalmazások használatának figyelése, telepítési folyamat felfüggesztése
 - adatbázis preloader a gyorsabb indításhoz
 
Megvalósításra vár
 - NPM modulok kezelése
 - PIP modulok kezelése
 - egységes csomaglista, csomagkezelő beépítése a kötegelt csomagkezlésekhez
 - packagekit-python tovébbi integrációja és opcionális váltása
 - egyéb csomagkezelő motorok integrációja és opcionális váltása

Telepítés
----------
blackPanther OS magyar disztribúcióra:
```
telepites package-wizard
```

Forrásból más disztribúcióra:
```
cd /egy/hely/ahova/van/írási/jogod (vagy root joggal)
git clone --recurse-submodules https://github.com/blackPantherOS/package-wizard.git
cd package-wizard/fusionlogic-common
python3 setup.py build
# (ezt már root joggal kell futtatnod)
python3 setup.py install

cd ..
python3 setup.py build
python3 setup.py install

```
### Használat:

Egy program telepítés PackageKit csomagadatbázisból, például Gimp:
```
package-wizard gimp
```
Telepítés egy helyi fájlból:
package-wizard /ahol/a/fájlod/van/csomagenve.rpm(vagy deb)
 
Screenshots
----------
![package-wizard-distros](https://raw.githubusercontent.com/blackPantherOS/package-wizard/master/data/screenshots/screenshot-variants.png)
![package-wizard-main](https://raw.githubusercontent.com/blackPantherOS/package-wizard/master/data/screenshots/screenshot-main.png)

