#*********************************************************************************************************
#*   __     __               __     ______                __   __                      _______ _______   *
#*  |  |--.|  |.---.-..----.|  |--.|   __ \.---.-..-----.|  |_|  |--..-----..----.    |       |     __|  *
#*  |  _  ||  ||  _  ||  __||    < |    __/|  _  ||     ||   _|     ||  -__||   _|    |   -   |__     |  *
#*  |_____||__||___._||____||__|__||___|   |___._||__|__||____|__|__||_____||__|      |_______|_______|  *
#*http://www.blackpantheros.eu | http://www.blackpanther.hu - kbarcza[]blackpanther.hu * Charles K Barcza*
#*************************************************************************************(c)2002-2019********
#
# This make file for creating a static package-wizard executable.
# This requires pandoc and pyinstaller

all: static del 
#readme

# Create s-tui executable
static:
	pyinstaller packagewizard.py -F -n package-wizard
	mv dist/package-wizard .

# Convert the markdown file to .rst file. Markdown for github, rst for PyPi
readme:
	pandoc --from markdown --to rst README.md > README.rst

# Remove files created by pyinstaller
del:
	rm -rf ./build/ 
	rm -rf ./__pycache__/ 
	
# Clear pyinstall cache and delete file
clean:
	pyinstaller --clean package-wizard
	rm -rf ./build/ 
