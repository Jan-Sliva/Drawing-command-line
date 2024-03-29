# Siamská síť

K rozpoznávání obrázku používám siamskou neuronovou síť. Tato architektura zákoduje obrázek do konstantně velkého vektoru. Podobnost obrázků určí jako vzdálenost zakódovaných vektorů. Tu vypočítám jako součet druhých mocnin rozdílů složek. Čím menší vzdálenost, tím jsou si obrázky podobnější.

![Architektura siamské sítě](https://miro.medium.com/max/1738/1*23mikUF3HBJGUqrX7tMKQQ.png)

Nakreslený tvar přiřadím k symbolu, jehož zakódovaný vektor je nejbližší k vektoru nakresleného tvaru. Pokud je tento vektor příliž daleko od vektorů všech symbolů, tak beprovedu žádnou akci.

Siamské sítě mají výhodu, že můžu přiadávat další symboly, aniž bych musel přetrénovávat celou síť. Nevýhodou je naopak to, že je složitější dosáhnout vyšší přesnosti.

## Popis mé sítě
Moje síť bere na vstupu obrázky velikosti 32x32. Na ně aplikuje 3 konvoluce 3x3. Výstup z poslední konvoluce zploští do jedné dimenza a ten pomocí další vrstvy zredukuje do 32 složkového vektoru. Síť je zadefinována v `NeuralNetwork/runModel.py`

## Triplet loss
K trénovaní sítě jsem použil triplet loss. Dataset jsem rozdělil do trojic, kde v každé trojici na dvou obrázcích je to samé ($A$ a $P$) a na třetím obrázku je něco jiného ($N$). Rovnice pro loss pak vypadá

$$\mathcal  L (A, P, N)= max(\|f(A) - f(P)\|^2 - \|f(A) - f(N)\|^2 + \alpha,  0)$$
kde $f(A)$, $f(P)$, $f(N)$ jsou zakódování obrázků, $\alpha$ je nastavitelné kladná hodnota, která určuje minimální rozpětí mezi stejnými a rozdílnými páry

## Dataset
K trénování sítě jsem použil dataset [HASYv2](https://zenodo.org/record/259444#.Y-lOhC_MKUk) a 600 obrázků vytvořených pomocí aplikace, kterou jsem naprogramoval (dostupná ve složce `dataCreator`).

HASYv2 obsahuje 369 symbolů o rozlišení 32x32. Pomocí mé aplikece jsem vytvořil 12 symbolů v rozlišení 192x192, které jsem ořezal a zmenšil na velikost 32x32. Každý symbol jsem nakreslil 50 krát.

Triplety jsem vytvořil jako všechny možné dvojice různých symbolů v trénovacím setu. Od prvního symbolu jsem náhodně vybral 2 obrázky, od druhého jeden.

## Měření přesnosti
Pro každý symbol jsem našel obrázek, jehož zakódování je nejblíže ke všem ostatním obrázkům tohoto symbolu. Pak jsem vzal všechny obrázky a přiřadil jsem je k nejbližšímu symbolu. Procento správných přiřazení je přesnost.

Vyšlo mi více hodnot, v závislosti na tom, jaký symboli jsem použil. Vždy jsem symboli vybíral z 12 mnou nakreslených symbolů
- 79%, když jsem vzal 6 symbolů, které síť při trénování neviděla
- 72%, když jsem vzal všech 12 symbolů
- 76%, když jsem odstranil symbol "mute", který je hodně podobný symbolu "volume"

# Hlavní aplikace

Aplikace má v json nastaveních určenou velikost plátna a velikost ořezávání. Aplikace vezme nakreslený obrázek, ořeže ho a zmenší do tvaru 32x32.

Aplikace funguje pomocí eventů, kdy například potvrzení obrázku spustí kód, který vezme nakreslený obrázek a zavolá na něj neuronovou síť.

# Převzatý kód
- https://keras.io/examples/vision/siamese_network/
- https://www.tensorflow.org/addons/tutorials/losses_triplet

