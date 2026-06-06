# Drawing-command-line

I created an application that allows user to control their computer by drawing symbols. For example, when the user draws a file explorer icon, the file explorer opens. The application is primarily aimed at a laptop with a touchscreen, but it also works with mouse.


#### Siamese Network

I use a siamese neural network for image recognition. This architecture encodes an image into a fixed-size vector. It determines image similarity as the distance between encoded vectors. I compute this as the sum of squared differences of the components. The smaller the distance, the more similar the images are.

![Siamese network architecture](https://miro.medium.com/max/1738/1*23mikUF3HBJGUqrX7tMKQQ.png)

I assign a drawn shape to the symbol whose encoded vector is closest to the encoded vector of the drawn shape. If this vector is too far from the vectors of all symbols, I perform no action.

Siamese networks have the advantage that I can add new symbols without having to retrain the entire network. The disadvantage is that it is harder to achieve higher accuracy.

#### Description of My Network

My network takes 32x32 images as input. It applies 3 convolutions of size 3x3. The output of the last convolution is flattened into one dimension and then reduced to a 32-component vector using another layer. The network is defined in `NeuralNetwork/runModel.py`.

#### Triplet Loss

I used triplet loss to train the network. I split the dataset into triplets, where in each triplet two images are the same ($A$ and $P$) and the third image is something different ($N$). The loss equation then looks like

$$\mathcal  L (A, P, N)= max(\|f(A) - f(P)\|^2 - \|f(A) - f(N)\|^2 + \alpha,  0)$$

where $f(A)$, $f(P)$, $f(N)$ are image encodings, and $\alpha$ is a configurable positive value that determines the minimum margin between same and different pairs.

#### Dataset

I used the [HASYv2](https://zenodo.org/record/259444#.Y-lOhC_MKUk) dataset and 600 images created using an application I programmed (available in the `dataCreator` folder) to train the network.

HASYv2 contains 369 symbols at 32x32 resolution. Using my application, I created 12 symbols at 192x192 resolution, which I cropped and resized to 32x32. I drew each symbol 50 times.

I created triplets as all possible pairs of different symbols in the training set. From the first symbol I randomly selected 2 images, from the second one.

#### Measuring Accuracy

For each symbol, I found the image whose encoding is closest to all other images of that symbol. Then I took all images and assigned them to the nearest symbol. The percentage of correct assignments is the accuracy.

I obtained several values, depending on which symbols I used. I always selected symbols from the 12 symbols I drew:
- 79%, when I used 6 symbols that the network did not see during training
- 72%, when I used all 12 symbols
- 76%, when I removed the "mute" symbol, which is very similar to the "volume" symbol

#### Main Application

The application has canvas size and crop size specified in JSON settings. The application takes the drawn image, crops it, and resizes it to 32x32.

The application works using events, where for example confirming an image triggers code that takes the drawn image and runs it through the neural network.

#### Borrowed Code

- https://keras.io/examples/vision/siamese_network/
- https://www.tensorflow.org/addons/tutorials/losses_triplet

### User documentation

The recommended version of Python is 3.10.10

#### Installation on Windows

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

7. Run the application files as follows:

    `python main-drawPicture.py`\
    `python main.py`

#### Edit application settings

1. Open `Drawing-command-line/settings/settings.json`
2. Here you can edit the following things
    - `X`, `Y` - canvas dimensions
    - `crop` - crop size of the image before sending it to the neural network
    - `penWidth` - width of the pen
    - `network` - name of the file containing the neural network model, this file must be stored in the `Drawing-command-line/models` folder

#### Drawing on canvas

- using the pen
    - bottom button erases the canvas
    - upper button submits the image and erases the canvas
- using the mouse
    - hold the left button to draw
    - middle button erases the canvas
    - right button submits the image and erases the canvas

#### Adding symbols

1. Run `Drawing-command-line/main-drawPicture.py`
2. Enter the name of subfolder of `Drawing-command-line/pictures` where you want to save the drawn images
3. Open the canvas, draw a symbol on it, submit it
4. The symbol is automatically saved in the selected subfolder
5. Draw as many other pictures as you want. They will all be saved in the selected subfolder
6. Open `Drawing-command-line/settings/data.json`
7. Here is the json file with all the symbols that are in the application. To add a symbol you need to specify 4 things
    - `name` - the name of the symbol
    - `pictures` - the name of the subfolder to take the images from
    - `question` - the question, what will be displayed to the user when they draw the symbol
    - `command` - the command, what is executed using the python command `os.system`. You can use `$close` as special command, that closes the application

#### Usage

1. Run `Drawing-command-line/main.py`
2. Draw the symbol belonging to the action you want to run
3. Submit it
4. If the submited image is similar to one of the symbols in the application, a question will appear instead of the canvas asking if you want to run the action
5. After clicking Yes or No, canvas will appear again

#### Editing symbols

1. The symbols are stored in the `Drawing-command-line/pictures` folder, here you can edit them
2. The application reads the images from this folder every time it starts, and uses a neural network to encode them into a 32-element vector

---

## Drawing-command-line

Vytvořil jsem aplikace, která umožňuje ovládat počítač pomocí kreslení symbolů. Když uživatel nakreslí například ikonu file exploreru, otevře se file explorer. Aplikace je primárně zaměřená na notebook s dotykovým displejem, ale funguje i pomocí klasického kreslení myší.

[Specifikace](#specifikace) · [Uživatelská dokumentace](#uživatelská-dokumentace)

### Specifikace

#### Siamská síť

K rozpoznávání obrázku používám siamskou neuronovou síť. Tato architektura zákoduje obrázek do konstantně velkého vektoru. Podobnost obrázků určí jako vzdálenost zakódovaných vektorů. Tu vypočítám jako součet druhých mocnin rozdílů složek. Čím menší vzdálenost, tím jsou si obrázky podobnější.

![Architektura siamské sítě](https://miro.medium.com/max/1738/1*23mikUF3HBJGUqrX7tMKQQ.png)

Nakreslený tvar přiřadím k symbolu, jehož zakódovaný vektor je nejbližší k vektoru nakresleného tvaru. Pokud je tento vektor příliž daleko od vektorů všech symbolů, tak beprovedu žádnou akci.

Siamské sítě mají výhodu, že můžu přiadávat další symboly, aniž bych musel přetrénovávat celou síť. Nevýhodou je naopak to, že je složitější dosáhnout vyšší přesnosti.

#### Popis mé sítě

Moje síť bere na vstupu obrázky velikosti 32x32. Na ně aplikuje 3 konvoluce 3x3. Výstup z poslední konvoluce zploští do jedné dimenza a ten pomocí další vrstvy zredukuje do 32 složkového vektoru. Síť je zadefinována v `NeuralNetwork/runModel.py`

#### Triplet loss

K trénovaní sítě jsem použil triplet loss. Dataset jsem rozdělil do trojic, kde v každé trojici na dvou obrázcích je to samé ($A$ a $P$) a na třetím obrázku je něco jiného ($N$). Rovnice pro loss pak vypadá

$$\mathcal  L (A, P, N)= max(\|f(A) - f(P)\|^2 - \|f(A) - f(N)\|^2 + \alpha,  0)$$

kde $f(A)$, $f(P)$, $f(N)$ jsou zakódování obrázků, $\alpha$ je nastavitelné kladná hodnota, která určuje minimální rozpětí mezi stejnými a rozdílnými páry

#### Dataset

K trénování sítě jsem použil dataset [HASYv2](https://zenodo.org/record/259444#.Y-lOhC_MKUk) a 600 obrázků vytvořených pomocí aplikace, kterou jsem naprogramoval (dostupná ve složce `dataCreator`).

HASYv2 obsahuje 369 symbolů o rozlišení 32x32. Pomocí mé aplikece jsem vytvořil 12 symbolů v rozlišení 192x192, které jsem ořezal a zmenšil na velikost 32x32. Každý symbol jsem nakreslil 50 krát.

Triplety jsem vytvořil jako všechny možné dvojice různých symbolů v trénovacím setu. Od prvního symbolu jsem náhodně vybral 2 obrázky, od druhého jeden.

#### Měření přesnosti

Pro každý symbol jsem našel obrázek, jehož zakódování je nejblíže ke všem ostatním obrázkům tohoto symbolu. Pak jsem vzal všechny obrázky a přiřadil jsem je k nejbližšímu symbolu. Procento správných přiřazení je přesnost.

Vyšlo mi více hodnot, v závislosti na tom, jaký symboli jsem použil. Vždy jsem symboli vybíral z 12 mnou nakreslených symbolů
- 79%, když jsem vzal 6 symbolů, které síť při trénování neviděla
- 72%, když jsem vzal všech 12 symbolů
- 76%, když jsem odstranil symbol "mute", který je hodně podobný symbolu "volume"

#### Hlavní aplikace

Aplikace má v json nastaveních určenou velikost plátna a velikost ořezávání. Aplikace vezme nakreslený obrázek, ořeže ho a zmenší do tvaru 32x32.

Aplikace funguje pomocí eventů, kdy například potvrzení obrázku spustí kód, který vezme nakreslený obrázek a zavolá na něj neuronovou síť.

#### Převzatý kód

- https://keras.io/examples/vision/siamese_network/
- https://www.tensorflow.org/addons/tutorials/losses_triplet

### Uživatelská dokumentace

Doporučená verze Pythonu je 3.10.10

#### Instalace pro Windows

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

7. Spusťte soubory aplikace takto:

    `python main-drawPicture.py`\
    `python main.py`

#### Úprava nastavení aplikace

1. Otevřete `Drawing-command-line/settings/settings.json`
2. Zde můžete upravit následující věci
    - `X`, `Y` - rozměry plátna
    - `crop` - velikost ořezu obrázku před posláním do neuronové sítě
    - `penWidth` - šířka pera
    - `network` - název souboru obsahující model neuronové síte, tento soubor musí být uložen ve složce `Drawing-command-line/models`

#### Kreslení na plátno

- pomocí pera
    - dolní tlačítko vymaže celé plátno
    - horní tlačítko potvrdí obrázek a smaže plátno
- pomocí myši
    - pro kreslení držte levé tlačítko
    - prostřední tlačítko vymaže celé plátno
    - pravé tlačítko potvrdí obrázek a smaže plátno

#### Přidávání symbolů

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

#### Samotné použití

1. Spusťe `Drawing-command-line/main.py`
2. Nakreslete symbol patřící k akci, kterou chcete spustit
3. Potvrďte
4. Pokud se potvrzený obrázek podobá některému ze symbolů v aplikaci, tak se místo plátna objeví otázka, jestli chcete spustit danou akci
5. Po klinutí na Yes nebo No se na místo otázky vrátí zpět plátno

#### Úprava symbolů

1. Symboly jsou uloženy ve složce `Drawing-command-line/pictures`, zde je můžete libovolně upravovat
2. Aplikace po každém spuštění načte obrázky z této složky, a pomocí neuronové sítě je zakóduje do 32-prvkového vektoru
