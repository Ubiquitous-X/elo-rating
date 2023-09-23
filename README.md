# Kvitten Open
En app skriven med Flask som ramverk och Bulma CSS för presentation. Denna app är framtagen för att på ett tydligt sätt en gång för alla avgöra den stora frågan om vem som faktiskt är den bästa pingisspelaren under de blodstänkta matcherna som så ivrigt avgörs på lunchrasterna.

Alla filer ligger lokalt, så ingen internetanslutning krävs, då det kan vara något problematiskt att få in en RaspberryPi på företagets nätverk.

### Elo rating
Elo-rating är en algoritm för att beräkna spelares relativa skicklighet i spel, baserat på deras resultat mot andra spelare. Det används oftast i schack, men också i andra spel som till exempel tennis och brädspel.

För att använda detta system krävs att två spelare identifieras och deras respektive poäng i en match registreras.

En "K-faktor" på 24 används för att anpassa hur mycket en spelares rating kommer att ändras baserat på resultatet. En högre K-faktor leder till större ratingändringar.

Förväntade resultat för varje spelare beräknas med hjälp av Elo-ratingformeln. Detta ger en uppskattning av sannolikheten för att varje spelare kommer att vinna matchen baserat på deras tidigare rating.

Vinnaren av matchen bestäms och poängskillnaden räknas ut. Om en spelare vinner med en högre poäng än den andra, kommer den att få en ratingökning och den andra kommer att få en ratingminskning.

En "min_rating_change" beräknas baserat på den förväntade poängskillnaden mellan spelarna. Detta används för att säkerställa att ratingändringen inte blir för stor eller för liten.

Ett "score_factor" beräknas baserat på poängskillnaden i matchen. Detta påverkar också hur mycket en spelares rating kommer att ändras.

Slutligen beräknas ratingändringen för varje spelare med hjälp av Elo-ratingformeln, och deras rating justeras. Om en spelares rating skulle sjunka under 100, sätts den till 100 för att undvika negativa ratingvärden.