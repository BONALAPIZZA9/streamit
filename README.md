# StreamIt — By Ema

## Installazione
Aggiungi https://bonalapizza9.github.io/streamit/ in Kodi → Gestione file → Aggiungi sorgente.
Installa repository.streamit-1.0.8.zip, poi StreamIt da Installa da repository.

[Repository](https://bonalapizza9.github.io/streamit/repository.streamit-1.0.8.zip) · [StreamIt 1.11.0](https://bonalapizza9.github.io/streamit/plugin.video.streamit/plugin.video.streamit-1.11.0.zip)

## Lingua audio
Scegli Italiano o Inglese alla prima apertura. La scelta è salvata e il dialogo non ricompare.
Puoi cambiarla in Impostazioni → Generale → Lingua audio.
La preferenza viene applicata prima dell’avvio; il servizio seleziona la traccia anche quando il video viene reindirizzato, senza continuare a forzare la lingua durante la visione.
Se la traccia richiesta manca o non è identificabile, compare una notifica e resta l’audio disponibile.
Non è possibile creare una traccia audio che il video non contiene.

## Aggiornamenti
Controllo degli aggiornamenti all’avvio di Kodi (dopo 30 secondi) e ogni sei ore, rinviato durante la riproduzione.
Il controllo usa il gestore repository di Kodi. L’installazione automatica segue le impostazioni e le regole di aggiornamento di Kodi.
Puoi disattivare il controllo in Impostazioni → Generale → Controlla aggiornamenti automaticamente.
La pubblicazione su GitHub continua a generare automaticamente indice, pacchetti e pagina di download.

## Immagini e rete
Locandine alla risoluzione pubblicata dal sito, senza alterare gli URL per ingrandirle. Poster e immagini panoramiche sono assegnati ai rispettivi campi di Kodi; viene preferito un formato compatibile e vengono esclusi AVIF, SVG e HEIC.
Il DNS resta quello del dispositivo. Nessun errore DNS rilevato richiede un resolver integrato; gli errori DNS e HTTPS sono ora diagnosticati separatamente. La verifica dei certificati rimane attiva.
L’auto skip degli episodi resta rimosso.

## Sorgenti
StreamIt-GitHub.zip contiene i sorgenti; build_repository.py alla radice è usato da GitHub Actions per generare i pacchetti e pubblicare Pages.
Incrementare le versioni quando cambia il contenuto dei pacchetti. Richiede Kodi 19 o successivo.
