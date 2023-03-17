# Kvitten Cup
Elo rating är en metod för att beräkna den relativa styrkan hos spelare inom spel eller sport, särskilt i schack men också i andra spel som tennis, bridge och go. Elo-rating systemet är uppbyggt på ett antal principer för att utvärdera en spelares prestation, och beräkningar av spelarens nya rating efter varje spel.

En spelares Elo-rating beräknas utifrån antalet matcher som spelaren har spelat och antalet matcher som spelaren har vunnit eller förlorat. Efter varje spel justeras spelarnas Elo-rating i förhållande till hur de presterade i spelet och styrkan hos deras motståndare. Ju högre ratingen är, desto starkare är spelaren.

Den här koden implementerar Elo-rating för att beräkna ratingen för två spelare baserat på resultatet av en match. Koden beräknar först antalet spel som har spelats för de två spelarna. Baserat på detta bestämmer koden vilken faktor (K_FACTOR) som ska användas i beräkningen av ratingen efter matchen.

Efter det hämtar koden de två spelarnas aktuella Elo-rating och matchresultaten från formuläret som skickades in. Koden beräknar sedan vad spelarnas förväntade poäng skulle ha varit baserat på deras rating och det så kallade "S" -värdet, som är antingen 1 eller 0 beroende på om en spelare vann eller förlorade.

Därefter används spelarnas faktiska poäng (vinst eller förlust) och den förväntade poängen för att beräkna hur mycket en spelares rating borde ändras efter matchen. Koden beräknar sedan det minsta antal ratingpoäng som den lägre rankade spelaren borde få, beroende på deras förväntade poäng. Slutligen beräknar koden den faktiska förändringen i ratingpoäng och lägger till den nya ratingpoängen för varje spelare.
