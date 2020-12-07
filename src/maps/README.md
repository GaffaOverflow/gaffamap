# Mastermaps

**master.join** ist das abgestimmte Template für den Bau der Maps. Festgelegt wurden die Namen, Positionen und die Nutzung der Layer.
Der "Interactive" Layer ist ein Platzhalter, welcher mit einem oder mehreren Layern für die entsprechenden Aktion ersetzt wird. Benötigt werden pro Ereignis, auch für unterschiedliche Orte, ein Layer.

Unterstützt wird:

 + Aufruf einer Webseite Custom Properties: openWebsite https://…
 + Sprung auf eine andere Map Custom Properties: exitUrl mapname.json 
 + Aufruf von Jitsi Custom Properties: jitsiRoom raumname
 
 Siehe auch Dokumentation https://codimd.c3d2.de/WA-Zone-Einstieg-00# .
 
 An allen Stellen wo ein Tiles eingezeichnet ist, findet die Interaktion statt.
 Die Namen können sprechend gewählt werden. 



+ silent
	Bereiche für Unterhaltungen bei Begegnung können hier deaktiviert werden ( die Anzeige der Bereiche des Lagers kann mit inaktivieren von „visiable“ in den Layer Properties unterdrückt werden.

+ Bridge
	Dinge die den Spieler verdecken (Beispiel Lichterkette, Brücke)

+ floorLayer (object layer)
	Für Programm notwendig. Die Ebene auf der sich die Spielfigur befindet.
	Was darüber liegt verdeckt die Spielfigur, was darunter liegt ist unter dem Spieler.

+ start
	wenn dort ein Tile liegt ist das der Startpunkt für die Map.
	Liegen dort mehrere Tiles, entscheidet der Zufall auf welchem davon man startet.

+ Objects_Top
	wird überwiegend leer bleiben. Wird nur verwendet, wenn Objekte auf Objekten platziert werden sollen (z.B. eine Kerze auf einem Tisch)

+ Objects_Bottom
	Objekte wie Tische/ICs, Widerstände aber auch alle Wände befinden sich auf dieser Ebene

+ Routes
	Wege zur Verbindung von Räumen/PCBs (Flachbandkabel, Gaffa)

+ Base
	Boden der Räume (PCBs)

+ Background
	Hintergrund (unterste Ebene) befindet sich unterhalb der Räume und ist der sonst nicht weiter definierte Raum 

+ Interactive (Platzhalter s.o)
	Je verschiedener Interaktion ein Layer 
+ Collision
	Tiles auf dieser Ebene definieren Stellen die der Spieler nicht passieren kann (z.B. für Wände). Die Tiles müssen die Eigenschaft "collides = true" haben.
	Hinweis1: Man kann zunächst durch alles durch laufen, bis es auf dieser Ebene blockiert wird.
	Hinweis2: Kann während der Entwicklung weiter oben platziert werden um die Blockierten stellen einfacher zu definieren.

## Beispiel Maps

**mastertest1.join**   Beispiel für eine Brücke unter der eine Spielfigur durchlaufen kann 
**mastertest2.join**   Anzeige der neuen Tides 

