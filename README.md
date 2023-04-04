# Kvitten Open
En app skriven med Flask som ramverk och Bulma CSS för presentation. Denna app är framtagen för att på ett tydligt sätt en gång för alla avgöra den stora frågan om vem som faktiskt är den bästa pingisspelaren under de blodstänkta matcherna som så ivrigt avgörs på lunchrasterna.

Alla filer ligger lokalt, så ingen internetanslutning krävs, då det kan vara något problematiskt att få in en RaspberryPi på företagets nätverk.

### Elo rating
Elo-rating är en algoritm för att beräkna spelares relativa skicklighet i spel, baserat på deras resultat mot andra spelare. Det används oftast i schack, men också i andra spel som till exempel tennis och brädspel.

Beräkningarna som görs i koden syftar till att uppdatera spelarnas Elo-rating efter varje match, beroende på deras förväntade resultat och det faktiska resultatet av matchen. Förväntade resultat beräknas baserat på spelarnas Elo-rating före matchen, och sedan justeras ratingen baserat på det faktiska resultatet.

Flera parametrar används i beräkningen, bland annat antalet spel som spelarna har spelat tidigare, så kallat "K-factor". Detta påverkar hur mycket en spelares rating kommer att förändras efter varje match. Andra faktorer inkluderar skillnaden i rating mellan spelarna, det faktiska resultatet och hur många ratingpoäng som den lägre rankade spelaren bör vinna för att inte förlora för många poäng.

I koden beräknas förväntade poäng för varje spelare baserat på deras Elo-rating före matchen, och sedan jämförs detta med det faktiska resultatet. Baserat på detta beräknas skillnaden i rating som varje spelare ska tilldelas efter matchen. Slutligen uppdateras spelarnas Elo-rating i enlighet med dessa skillnader.

För att se till att ratingen inte sjunker för mycket för en förlorande spelare så finns också en minsta möjliga ratingförändring som kan ske. Detta görs genom att lägga till en konstant, 24, till den minsta möjliga ratingförändringen. Det finns också en faktor som tar hänsyn till hur stor skillnaden i poäng var mellan spelarna för att justera ratingförändringen.

Så sammanfattningsvis, koden använder Elo-rating algoritmen för att uppdatera spelarnas skicklighet efter varje match, baserat på deras förväntade resultat och det faktiska resultatet av matchen. Detta görs genom att beräkna skillnaden i förväntade poäng, den minsta möjliga ratingförändringen och en faktor som justerar ratingförändringen baserat på poängskillnad.