# Drawing-command-line
Vytvořil jsem aplikace, která umožňuje ovládat počítač pomocí kreslení symbolů. Když uživatel nakreslí například ikonu file exploreru, otevře se file explorer. Aplikace je primárně zaměřená na notebook s dotykovým displejem, ale funguje i pomocí klasického kreslení myší.

[Dokumentace](#uživatelská-dokumentace)

I created an application that allows user to control their computer by drawing symbols. For example, when the user draws a file explorer icon, the file explorer opens. The application is primarily aimed at a laptop with a touchscreen, but it also works with mouse.

[Documentation](#user-documentation)

# Uživatelská dokumentace

Doporučená verze Pythonu je 3.10.10
## Instalace pro Windows

1. Pokud nemáte, nainstalujte si Python a Git
2. Otevřete příkazovou řádku ve složce, kde chcete mít aplikaci uloženou
3. Naklonujte repozitář z githubu

    `git clone https://github.com/Jan-Sliva/Drawing-command-line`

4. Vytvořte virtuální prostředí Pythonu a spusťte ho

    `python -m venv DCL-venv`\
    `DCL-venv\Scripts\activate`

5. Nainstalujte do prostředí potřebné packages

    `python -m pip install -r Drawing-command-line\requirements.txt`

6. Přejděte do složky `Drawing-command-line\Drawing-command-line`

    `cd Drawing-command-line\Drawing-command-line`

7. Dále v dokumentaci je třeba spustit soubory `Drawing-command-line/main-drawPicture.py` a `Drawing-command-line/main.py`, to se dělá takto:

    `python main-drawPicture.py`\
    `python main.py`

## Úprava nastavení aplikace
1. Otevřete `Drawing-command-line/settings/settings.json`
2. Zde můžete upravit následující věci
    - `X`, `Y` - rozměry plátna
    - `crop` - velikost ořezu obrázku před posláním do neuronové sítě
    - `penWidth` - šířka pera
    - `network` - název souboru obsahující model neuronové síte, tento soubor musí být uložen ve složce `Drawing-command-line/models`

## Kreslení na plátno
- pomocí pera
    - dolní tlačítko vymaže celé plátno
    - horní tlačítko potvrdí obrázek a smaže plátno
- pomocí myši
    - pro kreslení držte levé tlačítko
    - prostřední tlačítko vymaže celé plátno
    - pravé tlačítko potvrdí obrázek a smaže plátno

## Přidávání symbolů
1. Spusťte `Drawing-command-line/main-drawPicture.py`
2. Zadejte jméno podsložky `Drawing-command-line/pictures`, do které chcete nakreslené obrázky ukládat
3. Otevře se plátno, nakreslete na něj symbol, potvrďte
4. Symbol se automaticky uloží do zvolené podsložky
5. Nakreslete kolik dalších obrázků chcete. Všechny se uloží do zvolené podsložky
6. Otevřete `Drawing-command-line/settings/data.json`
7. Zde se nachází json soubor se všemi symboli, které jsou v aplikace. Pro přidání symbolu musíte specifikovat 4 věci
    - `name` - jméno symbolu
    - `pictures` - jméno podsložky, ze které brát obrázky
    - `question` - otázka, co se zobrazí uživateli, když nakreslí daný symbol
    - `command` - příkaz, co se provede pomocí python příkazu `os.system`. Speciální příkaz `$close` zavře aplikaci

## Samotné použití
1. Spusťe `Drawing-command-line/main.py`
2. Nakreslete symbol patřící k akci, kterou chcete spustit
3. Potvrďte
4. Pokud se potvrzený obrázek podobá některému ze symbolů v aplikaci, tak se místo plátna objeví otázka, jestli chcete spustit danou akci
5. Po klinutí na Yes nebo No se na místo otázky vrátí zpět plátno

## Úprava symbolů
1. Symboly jsou uloženy ve složce `Drawing-command-line/pictures`, zde je můžete libovolně upravovat
2. Aplikace po každém spuštění načte obrázky z této složky, a pomocí neuronové sítě je zakóduje do 32-prvkového vektoru

# User documentation

The recommended version of Python is 3.10.10

## Installation on Windows

1. Install Python and Git, if you don't have them 
2. Open a command prompt in the folder where you want to store the application
3. Clone the repository from github

    `git clone https://github.com/Jan-Sliva/Drawing-command-line`

4. Create a Python virtual environment and run it

    `python -m venv DCL-venv`\
    `DCL-venv\Scripts\activate`

5. Install the necessary packages in the environment

    `python -m pip install -r Drawing-command-line\requirements.txt`

6. Navigate to the `Drawing-command-line\Drawing-command-line` folder

    `cd Drawing-command-line\Drawing-command-line`

7. Below in the documentation you need to run files `Drawing-command-line/main-drawPicture.py` and `Drawing-command-line/main.py`, this is done like this:

    `python main-drawPicture.py`\
    `python main.py`

## Edit application settings
1. Open `Drawing-command-line/settings/settings.json`
2. Here you can edit the following things
    - `X`, `Y` - canvas dimensions
    - `crop` - crop size of the image before sending it to the neural network
    - `penWidth` - width of the pen
    - `network` - name of the file containing the neural network model, this file must be stored in the `Drawing-command-line/models` folder

## Drawing on canvas
- using the pen
    - bottom button erases the canvas
    - upper button submits the image and erases the canvas
- using the mouse
    - hold the left button to draw
    - middle button erases the canvas
    - right button submits the image and erases the canvas

## Adding symbols
1. Run `Drawing-command-line/main-drawPicture.py`
2. Enter the name of subfolder  of `Drawing-command-line/pictures` where you want to save the drawn images
3. Open the canvas, draw a symbol on it, submit it
4. The symbol is automatically saved in the selected subfolder
5. Draw as many other pictures as you want. They will all be saved in the selected subfolder
6. Open `Drawing-command-line/settings/data.json`
7. Here is the json file with all the symbols that are in the application. To add a symbol you need to specify 4 things
    - `name` - the name of the symbol
    - `pictures` - the name of the subfolder to take the images from
    - `question` - the question, what will be displayed to the user when they draw the symbol
    - `command` - the command, what is executed using the python command `os.system`. You can use `$close` as special command, that closes the application

## Usage
1. Run `Drawing-command-line/main.py`
2. Draw the symbol belonging to the action you want to run
3. Submit it
4. If the submited image is similar to one of the symbols in the application, a question will appear instead of the canvas asking if you want to run the action
5. After clicking Yes or No, canvas will appear again

## Editing symbols
1. The symbols are stored in the `Drawing-command-line/pictures` folder, here you can edit them
2. The application reads the images from this folder every time it starts, and uses a neural network to encode them into a 32-element vector
