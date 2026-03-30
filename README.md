# Simulator pentru Acul lui Buffon (Buffon's Needle)

Acest proiect reprezintă o simulare interactivă bazată pe metoda Monte Carlo pentru experimentul probabilistic clasic „Acul lui Buffon”. Aplicația permite estimarea valorii constantei matematice $\pi$ prin simularea aruncării a milioane de ace pe o suprafață plană marcată cu linii paralele echidistante. 

Proiectul integrează o componentă vizuală pentru monitorizarea procesului în timp real și o componentă analitică pentru reprezentarea grafică a convergenței estimării.

---

## Tehnologii Utilizate

Proiectul este dezvoltat exclusiv în Python, utilizând următoarele biblioteci de bază:

* **Python 3.x:** Limbajul de programare de bază.
* **Pygame:** Utilizat pentru randarea interfeței grafice (GUI) și vizualizarea în timp real a intersecțiilor dintre ace și liniile paralele.
* **Matplotlib:** Implementat pentru generarea și actualizarea live a graficelor care urmăresc istoricul estimării valorii $\pi$ în raport cu numărul de eșantioane.
* **NumPy:** Esențial pentru calculele vectorizate și generarea optimizată a numerelor pseudo-aleatoare, permițând rularea eficientă a simulărilor la scară largă (de ordinul milioanelor de iterații).

---

## Caracteristici Principale

* **Arhitectură de Vizualizare Duală:** Rulează simultan interfața de simulare fizică (Pygame) și fereastra de analiză a datelor (Matplotlib).
* **Scenarii Parametrizate:** Permite comutarea în timp real între diverse configurații ale raportului dintre lungimea acului ($L$) și distanța dintre linii ($D$), facilitând studiul comparativ.
* **Scalabilitate a Performanței (Mod Turbo):** Capacitatea de a scala execuția de la loturi standard (5.000 de eșantioane) la loturi masive (1.000.000 de eșantioane) per iterație, pentru a demonstra empiric legea numerelor mari.
* **Sistem de Oprire Condiționată:** Modul de evaluare continuă care întrerupe automat simularea atunci când eroarea absolută a estimării scade sub pragul necesar pentru o precizie de 99.999%.
* **Raportare a Datelor:** Exportul automat al statisticilor finale de rulare în interfața liniei de comandă (CLI) la închiderea programului.

---

## Instalare și Configurare

Pentru a rula acest proiect, este necesară instalarea mediului Python 3 și a dependențelor menționate. 

1. Clonați sau descărcați fișierele proiectului.
2. Instalați pachetele necesare utilizând managerul `pip`:

```bash
pip install pygame numpy matplotlib
