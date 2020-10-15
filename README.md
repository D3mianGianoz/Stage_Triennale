# Stage_Triennale

# Using a set of Symptoms for non trivial diagnosis

The set (V) is not entailed by the Knowledge Base but the union beetewen the two is consistent.
We are interested in finding an answer, using a set of assertion D such as V follows from the union KB U D.

Thesis converted to markdown.

Università degli Studi di Torino

### Dipartimento di Informatica

### Corso di Laurea in Informatica

### Tesi di Laurea in Informatica

Diagnosis by Numbers:

Uno strumento basato su

logiche descrittive, "tipicalità" e probabilità

### Relatore:

### Prof. Gian Luca Pozzato

### Candidato:

### Damiano Gianotti

### Sessione Ottobre 2019

### a.a 2018/



#### Uno strumento basato sulle logiche descrittive, "tipicalità" e

#### probabilità

#### Damiano Gianotti

#### Abstract

Lo stage si pone l’obiettivo di realizzareDbN, un tool di supporto per ladiagnosi
differenziale, con applicazione ad un caso di studio in ambito medico, basato su una
logica descrittiva con tipicalità e probabilità di avere eccezioni. La logica in que-
stione consente di generare scenari plausibili ma “sorprendenti”, che consentiranno di
formulare diagnosi non ovvie (iter alternativi potenzialmente rilevanti) e di stimarne
la probabilità. Lo strumento potrebbe portare ad ulteriori ricerche, nel caso in cui
le spiegazioni più plausibili non siano quelle corrette e mostrare possibili scenari non
banali.

Il lavoro iniziale è stato lo studio delle Logiche Descrittive, una famiglia di linguaggi
formali utilizzati per esprimere (rappresentare) la conoscenza in un dominio specifico
(detto mondo). Sono quindi alla base dei linguaggi impiegati per lo sviluppo di
ontologie nel Web Semantico, come il Web Ontology Language (OWL).

In seguito, il progetto è partito come estensione della tesi “Logiche descrittive della
tipicalità: sviluppo di uno strumento per il ragionamento sulle probabilità di ecce-
zioni” [11]. Infatti, dopo averne studiato le caratteristiche importanti, si è cercato
di costruire sopra un diverso sistema di generazione degli scenari e di rafforzarne le
componenti di ragionamento, fortemente orientati all’implementazione dell’esempio
di “Typicalities and Probabilities of Exceptions in Nonmotonic Description Logics”
[8]. Raggiunto questo obiettivo, non banale, si è ottimizzato e pulito il codice e
sono state aggiunte ulteriori importanti funzionalità, come la creazione di grafici
interattivi e costi diagnostici.

Struttura della tesi

Di seguito, il piano di quest’opera.

- Il primo capitolo dà una breve infarinatura sulle fondamenta del progetto e
    descrive schematicamente il lavoro che è stato svolto.
- Il secondo capitolo invece fornisce alcune tra le nozioni teoriche più importanti
    che servono per comprendere i meccanismi su cui si basa DbN
- Il terzo tratta di quali librerie/linguaggi son state/i utilizzate/i e il perché
- Il quarto descrive, in dettaglio, le singole componenti delsoftware
- Il quinto racconta dei principali problemi presenti e delle possibili idee risolu-
    tive

##### 3


## Indice


- 1 Introduzione
   - 1.1 Ambiente e metodologie di studio
   - 1.2 Motivazioni del lavoro
   - 1.3 Obiettivi
- 2 Logiche Descrittive
   - 2.1 Informazioni iniziali
   - 2.2 Caratteristiche e limiti
      - 2.2.1 Tipologia ed Ingredienti
      - 2.2.2 Monotonicità
   - 2.3 Il linguaggio baseAL.
   - 2.4 Operatore T
      - 2.4.1 Premessa
      - 2.4.2 Definizione di T
   - 2.5 La logicaALC+T
   - 2.6 La logica non monotonaALC+TRaClR
      - 2.6.1 Traduzione dell’operatore T
   - 2.7 La logicaALC+TPR
      - 2.7.1 Modifiche alla semantica
      - 2.7.2 Estensione dell’Abox
      - 2.7.3 Dalla logica verso la "diagnosi"
- 3 Strumenti utilizzati
   - 3.1 OWL2
      - 3.1.1 Semantica
      - 3.1.2 Caratteristiche
      - 3.1.3 Sintassi e Modellazione di Base
      - 3.1.4 Classi complesse e implementazione diu,t,∃e∀
      - 3.1.5 OWL2VersusDB e considerazioni finali
   - 3.2 Owlready2
      - 3.2.1 Tabella di conversione
      - 3.2.2 Che cosa posso fare con OWLReady2?
      - 3.2.3 Architettura
      - 3.2.4 Paragone con precedenti approcci
   - 3.3 Plotly
      - 3.3.1 Perché usare Plotly.py?
      - 3.3.2 Che cosa posso fare con Plotly.py?
         -
- 4 Caso d’uso: Tool per il supporto diagnostico
   - 4.1 PEAR - Sintesi
   - 4.2 Visione complessiva
   - 4.3 Immissione dei dati
      - 4.3.1 I documenti in ingresso
      - 4.3.2 La classe dedicata alla traduzione
   - 4.4 L’ amministrazione dell’ontologia
   - 4.5 La creazione dei membri tipici e degli scenari
   - 4.6 L’inferenza
   - 4.7 Analisi del risultato
   - 4.8 Il file principaleMain.py
- 5 Conclusione e sviluppi futuri
- A Esempio completo
- INDICE Damiano Gianotti


# Capitolo 1

# Introduzione

### 1.1 Ambiente e metodologie di studio

La ricerca nel settore della rappresentazione della conoscenza si concentra da sempre
sulla possibilità di fornire descrizioni ad alto livello di fatti, gerarchie terminologiche
e reti concettuali necessarie ad software ‘intelligenti’, ossia a quelle applicazioni in
grado di ricavare conseguenze implicite (talvolta profonde o nascoste) di conoscenze
esplicitamente disponibili o facilmente accessibili.

In tal senso le Logiche Descrittive si pongono come miglior risposta per questo di
problema poiché riescono a coniugare in modo sapiente l’espressività ed efficien-
za: man mano che gli studi e le sperimentazioni relative alle Logiche Descrittive
progrediscono, le nostre conoscenze e capacità di classificare in modo sottile i vari
frammenti dei linguaggi logici si fanno sempre più profonde ed adeguate alle esigenze
dei vari ambiti applicativi.

Nel nostro caso, però, si trovano subito delle difficoltà, infatti si presuppone la con-
giunzione di due requisiti contrastanti : il bisogno composizioni sintattiche (tipiche
dei sistemi logici), e la necessità dell’utilizzo della "tipicalitá". Uno dei limiti di que-
ste logiche è che non sono in grado di rappresentare proprietà tipiche e di ragionare
sull’eredità rivedibile [8]. Richiamiamo dunque, in maniera informale, un classico
esempio proveniente dalla letteratura: immaginiamo di sapere che gli uccelli volano,
ma che i pinguini siano uccelli che non volano. Questa base di conoscenza sarebbe
consistente solo se non ci fosse neppure un pinguino. Per affrontare questo problema
fin dai primi anni ’90 sono state approfondite e studiate numerose estensioni non
monotone delle logiche descrittive.

Il programma oggetto delle tesi si basa sullaALC+TPR. Questa, oltre ad avere com-
plessità ExpTime-completa (come la sottostanteALC), combina diverse componenti
importanti:

- in primis la logicaALC+T dove le proprietà tipiche possono direttamente es-
    sere descritte dall’operatoreTdi “tipicalità“, grazie a cui è possibile esprimere
    che, per ogni concetto C,T(C) indica che le istanze di C sono considera-
    tetipicheonormali. Così unaTBox potrà contenere inclusioni della forma
    T(C)vD a rappresentare che “i tipiciC sono ancheD. A differenza del-
    la maggior parte delle altre logiche descrittive questa ci permetterà quindi di

##### 6


```
esprimere e ragionare sulle eccezioni mantenendo una consistenza della base
di conoscenza.[2];
```
- il secondo ingrediente necessario sarà una semantica distribuita, simile a quella
    utilizzata per le logiche descrittive probabilistiche, conosciuta come DISPON-
    TE. L’idea è quindi quella di aggiungere un’etichetta alle inclusioni che indichi
    la probabilità di tale fenomeno, per poter esprimere quanto sia possibile che
    un evento eccezionale si verifichi.
    Con questa estensione è possibile esprimere fatti del tipo:

```
T(C)vpD("abbiamo una probabilità p che un tipico C sia un D")
```
```
direttamente nella base di conoscenza oppure inferire e/o dedurre fatti del tipo
```
```
p:T(C)(m)("il membro m è un tipico C con una certa probabilità p")[8];
```
- il terzo riguarda il rafforzamento della semantica trattato nell’articolo [3] dove
    gli autori hanno ristretto la consequenzialità logica ad una classe di modelli
    minimi. L’idea intuitiva è quella di restringere la consequenzialità logica ai
    modelli che minimizzano le istanze atipiche di un concetto. La logica risultante
    èALC+TRaClR la cui semantica vedremo meglio in seguito.

Se opportunamente uniti otteniamo proprioALC+TPR che è caratterizzata dalla
probabilità di eccezionalitàdalla forma:

```
T(C)vpD
```
dovep∈(0,1)il cui significato intuitivo è:

```
"normalmente, gli elementiC sonoD
e la probabilità di avere elementiC che non sonoDè 1 −p.”
```
### 1.2 Motivazioni del lavoro

Sul fatto che un calcolatore possa trattare i dati statistici e fare predizioni proba-
bilistiche meglio di un essere umano non possono esserci dubbi: l’essere umano non
è tanto portato per il ragionamento statistico, che in genere appare controintuitivo.
In questo senso DbN potrebbe diventare un aiuto diagnostico prezioso, uno stru-
mento di consultazione del medico, più efficace di trattati e riviste, ma con il grande
limite di essere disumanizzante. Infatti il dato rilevante alla diagnosi si raccoglie nel
contesto del rapporto medico-paziente e il paziente non racconterebbe a DbN la sua
anamnesi come la racconterebbe ad un medico di sua fiducia.
Va sottolineato che, a causa della logica non standard utilizzata, DbN non è certo
allo stato dell’arte ma, al momento, un semplice ma efficace prototipo.

L’aspetto più interessante è il contesto in cui andrebbe ad inserirsi: in effetti già esi-
stono applicazioni per lo smartphone che dovrebbero aiutare il medico nelle decisioni
o, almeno, fornirgli spunti di riflessione e di esercizio. Contrariamente, supportare la
diagnostica medica è un problema privo di regole esatte e, in fondo, di ampiezza non
limitata che sembra molto al di là delle possibilità di una macchina, ma la presenza
di grandi aziende, comeIMBconWatson, ci fa chiedere per quanto tempo questo
rimarrà così.

1. Introduzione Damiano Gianotti 7


L’ultimo aspetto da considerare è relativo ai costi: per ora DbN è un embrione,
un piccolo prototipo e non è nemmeno immaginabile cosa costerebbe produrne e
renderne disponibile un numero sufficiente a soddisfare tutte le possibili richieste
di consulenza. D’altra parte la macchina ha delle potenzialità, e anche da sola
può rispondere a diverse richieste, ma sicuramente necessita di ulteriori sviluppi.
Il vantaggio nell’uso di un consulente elettronico risulterebbe molto grande, sia per
l’accuratezza delle diagnosi e delle terapie, sia per le implicazioni medico-legali come
elemento di buona prassi.

### 1.3 Obiettivi

Alle luce di queste motivazioni, introduciamo ora i sommi capi del sistema DbN.
Presa in esame un’ontologia (o base di conoscenza), più o meno vasta, scritta at-
traverso le logiche descrittive ed arricchita da espressioni di tipicalità e da sinto-
mi/prodromi riguardanti un paziente, l’obiettivo è quello di generare tutte le possibili
diagnosi (o spiegazioni), controllarne la veridicità (logicamente parlando) e presen-
tarle in forma grafica, evidenziandone la probabilità e il costo stimato. Va specificato
che, come diagnosi si intende un elenco di scenari, realtà "future" possibili, la cui
coerenza con laKBè stata verificata dallo strumento.

I risultati ottenuti e il lavoro svolto troveranno illustrazione in dettaglio nelle suc-
cessive sezioni.

8 1. Introduzione Damiano Gianotti


# Capitolo 2

# Logiche Descrittive

In questo capitolo iniziale forniremo una definizione diDL (Description Logics),
analizzeremo le sue componenti e verranno descritte brevemente le sue estensioni
più importanti, utilizzate negli ultimi anni.

### 2.1 Informazioni iniziali

Le logiche descrittive sono una famiglia di formalismi per la rappresentazione della
conoscenza, con la capacità di descrivere ciò che è noto in un dominio di applica-
zione (detto mondo). Tale rappresentazione si fonda su strutture importanti, come
grafi o frames, e ha una difficoltà variabile, che dipende dal linguaggio scelto, poi-
ché l’espressività e la complessità computazionale sono direttamente proporzionali.
Tipicamente i nodi rappresentano concetti (oggetti), che possono avere proprietà
(semplici o articolate) associate. È piuttosto semplice creare una corrispondenza tra
i grafi e leDL, perché queste ultime sono dotate di predicati facilmente equiparabili
alle strutture dei grafi: predicati unari corrispondo agli insiemi di individui,predi-
cati binari rappresentano relazioni tra singoli e infine un meccanismo di istruzioni
d’inclusione per esprimere proprietà appartenenti ai concetti, come, ad esempio,
ScimmiavMammifero.

Ecco alcuni esempi riguardanti individui:

- Volpe(foxy)
- Scappa(foxy)
- Gallina(coco)
- Ruba(foxy,coco)
- Uomo(jhon)
- Insegue(jhon,foxy)

È anche possibile utilizzare l’intersezione di concetti tramite la sintassiCane u
Taglia Grossaper cercare individui che appartengono ad entrambe le categorie.
Ricordiamo che questa tipologia di logiche ha alla base quella del prim’ordine, da
cui eredita la capacità di ragionamento attraverso inferenza, come ilmodus ponens.

##### 9


```
Figura 2.1: Un esempio di grafo
```
Infatti se all’insieme precedente aggiungessimo che:

```
MammiferovAnimale
```
allora da questo potremo inferire cheVolpevAnimale.

Per queste e altre caratteristiche peculiari le DL sono ampiamente utilizzate in
numerosi sistemi, proprio per il buon compromesso tra capacità di rappresentazione,
ragionamento e complessità.
Vediamo, in breve, alcuni dei principali domini applicativi:

Data mining Questo campo, da sempre al centro di molti dibattiti (anche etici),
ha come scopo "l’estrazione" di dati grezzi. Successivamente, al fine di classificarli,
viene fatto largo utilizzo delle logiche descrittive, per poi, in seguito, attraverso
tecniche di ragionamento, fare inferenza su di essi ed ottenere nuova conoscenza.

Medicina Fin dagli anni ’80 al centro di molte iniziative è stata la creazione di
una grande ontologia delle conoscenza medica, volta ad essere di supporto nelle
diagnosi. Per far fronte alla scalabilità della base di conoscenza, si sono spesso
utilizzate logiche descrittive basilari. Rappresenta l’ambito di maggiore interesse
per questo studio.

Configuration management È uno dei campi di maggior successo: esso include
applicazioni che supportano la progettazione di sistemi complessi grazie all’unione
di componenti multipli. In particolare attraverso la classificazione di concetti (che
possono anche essere basate su modelli object oriented) si può creare una tassono-
mia che, unita alla possibilità di ragionamento, intrinseca nelle logiche descrittive,
permette di trovare con facilità eventuali inconsistenze nel sistema.

Ingegneria del software Uno dei primi domini di applicazione: l’idea alla base
era di implementare, attraverso le logiche descrittive, un sistema che permettesse
allo sviluppatore di trovare facilmente informazioni rilevanti riguardo ad un sistema
particolarmente grande e/o complesso.

10 2. Logiche Descrittive Damiano Gianotti


### 2.2 Caratteristiche e limiti

#### 2.2.1 Tipologia ed Ingredienti

Ogni logica descrittiva è caratterizzata da una particolare capacità espressiva che
varia a seconda delle possibilità e delle restrizioni imposte nei seguenti elementi:

- AL:indica la logica degli attributi e introduce gli operatori di congiunzione
    e quantificazione universale ed esistenziale;
- C:descrive la possibilità di usare l’operatore di negazione;
- S:indica la capacità di definire la chiusura transitiva di un ruolo;
- H:fornisce la potenzialità di definire gerarchie tra ruoli;
- O:asserisce la presenza dell’operatore di enumerazione;
- I:permette di riferirsi al ruolo inverso;
- F N eQ:caratterizzano le disponibilità di definire, rispettivamente, la car-
    dinalità funzionale, semplice e qualificata (in ordine di espressività crescente);
- D:descrive la possibilità di riferirsi a domini concreti.

#### 2.2.2 Monotonicità

Caratteristica peculiare delleDLnella forma di

```
KB|=Q =⇒ KB∪{F}|=Q
```
ovvero, se da una base di conoscenzaKBsi può concludere un fattoQ, allora lo
stesso fattoQsi deduce dalla stessa base di conoscenza arricchita con un nuovo fatto
F.

Questa proprietà in sè è moltoimportante, tuttavia non sempre si rivela pratica,
anzi, esistono contesti (come il nostro) in cui, più che dare benefici, rende difficile
il ragionamento e la deduzione di nuove informazioni. Vediamone il perché con un
famoso esempio.
Consideriamo la seguente base di conoscenza oKnowledge Basetratta da [11]:

```
Piove =⇒ Prendo(ombrello)
```
```
Piove
```
si può banalmente concludere che:Prendo(ombrello)

Aggiungiamo ora la seguenteformula

```
Sono_Squattrinato
```
La conclusione precedente rimane lecita anche dopo l’arricchimento dellaKB.

Aggiungiamo, invece, questaespressione

```
Ho_Perso(ombrello)
```
2. Logiche Descrittive Damiano Gianotti 11


Contro le nostre aspettative/intuizioni la conclusione non cambia, poiché dalle due
premesse iniziali si giunge allo stessa conclusione senza che la nuova "conoscenza"
influisca sul risultato. Questo semplice modello ci mostra perché è importante, in
contesti specifici, avere dei linguaggi e degli automatismi in grado di tenere conto
della realtà dei fatti, cioè una logica che possegga unaeredità rivedibile.

### 2.3 Il linguaggio baseAL.

Un sistema di rappresentazione della conoscenza basato sulleDLpermette di creare,
manipolarle e ragionare su diverseKnowledge Base.
Ma cos’è formalmente unaKB? La base di conoscenza è composta principalmente da
una coppia(T,A)TBoxeABox. La prima introduce i concetti, insiemi di individui,
e ruoli, che denotano relazioni binarie tra i concetti.
Invece per quanto concerne la seconda, essa contiene asserzioni su singoli individui,
riguardanti concetti dellaTBox. Definiamo come descrizioni elementari i concetti
e ruoli atomici. Invece trattiamo come complesse le descrizioni che possono essere
costruite attraverso induzione. In notazione useremo le lettereAeBper indicare
concetti atomici, la lettera R per rappresentare i ruoli atomici e le lettere C e
D per le descrizioni dei concetti. Qui sotto daremo una definizione di AL [1],
linguaggio minimo di interesse pratico, su cui si basano tutti gli altri linguaggi di
questa famiglia.

Le descrizioni di concetti sono definite secondo le seguenti regole sintattiche:

```
C, D→
> (concetto atomico)
```
```
⊥ (top concept - generico)
```
```
¬A (negazione atomica)
CuD (intersezione)
```
```
∀R.C (restrizione di valore)
```
```
∃R.⊥ (quantificazione esistenziale limitata)
```
Per definire una semantica formale per i concetti diALponiamo alla base l’idea di
modello e l’idea di funzione d’interpretazione:

```
M=〈∆;f x〉 (2.1)
```
```
f x:A→∆ (2.2)
```
Definito che le interpretazioniIsono sottoinsiemi non vuoti di∆(dominio dell’inter-
pretazione), lo scopo di 2.1 è quello di fornire un significato alle formule, mentre, per
quanto riguarda 2.2, quello di permettere di assegnare a ogni concetto atomicoAun
insiemeAI⊆∆Ie per ogni ruolo atomicoRuna relazione binariaRI⊆∆I×∆I.
La funzione di interpretazione è estesa alla descrizione di concetti attraverso le
seguenti definizioni induttive :

```
>I =∆I
```
12 2. Logiche Descrittive Damiano Gianotti


##### (¬A)I =∆I\AI

```
(CuD)I =CIuDI
(∀R.C)I ={x∈∆|∀y.(x, y)∈RI→y∈CI}
```
```
(∃R.>)I ={x∈∆|∃y.(x, y)∈RI}
```
Diciamo che due concettiC, Dsono equivalenti, e scriviamoC =D, seCI=DI
per ogni interpretazioneI.

Aggiunta diC: l’operatore di negazione
A questo linguaggio, possiamo aggiungere l’estensione di negazione, un concetto
arbitrario:

```
¬C (concept negation)
```
La cui semantica risulta essere:

```
(¬C)I= ∆I\CI
```
Grazie a questa aggiunta il linguaggioALsi arricchisce, passando ad essere la logica
descrittivaALC.

Esempio
Vediamo un semplice caso che faccia uso di questa nuova sintassiABox

- V olpe(f oxy)
- Gallina(coco)
- U omo(jhon)

TBox

- ∀x, y|(V olpe(x)∧Affamata(x))∧Gallina(y) =⇒ Ruba(x, y)
- ∃x, y|U omo(x)∧Gallina(y)∧Ama(x, y) =⇒ ¬U ccide(x, y)∧P rotegge(x, y)

Per ogni volpe e gallina, se laVulpesè affamata allora ruba ilGallus domesticusDi
conseguenza se esiste una gallina e un uomo che la ama, questo non la ucciderà ma
la proteggerà (dalla volpe).

2. Logiche Descrittive Damiano Gianotti 13


### 2.4 Operatore T

#### 2.4.1 Premessa

L’obbiettivo dellaTBox è costruire una tassonomia di concetti (ossia un albero di
classificazione). Come rappresentare le proprietà dei prototipi e ragionare sulla loro
perdita a livelli inferiori?
Data una tassonomiaT, con AeB tali cheAè un concetto “padre“ diB, non
sempre tutte le proprietà diApossono essere ereditate daB.
L’approccio tradizionale a questo problema è di gestire le perdite di proprietà inte-
grando alcuni meccanismi di ragionamento non monotono, portando allo studio di
estensioni delle logiche descrittive in questo ambito e cercando di superare il limite.

#### 2.4.2 Definizione di T

Idealmente un’estensione possibile dovrebbe possedere almeno le seguenti caratteri-
stiche:

1. una chiara semantica, basata sulla stessa della logica sottostante;
2. la possibilità di specificare proprietà dei prototipi in maniera naturale e diretta;
3. mantenere la decidibilità (già ereditata) e dimostrabile attraverso il metodo
    convenzionale.

Vediamo dunque come nel lavori [2] e [7] si faccia uso dell’operatoreTdi tipicalità
per l’inferenze. La nostraKBha, in aggiunta, un insieme di asserzioni della forma
T(C)vDoT(C)(m)doveDè un concetto che non menzionaC.

Supponiamo che laTboxcontenga:

```
T(Student)v¬IncomeT axP ayer
T(StudentuW orker)vIncomeT axP ayer
```
```
T(StudentuW orkeruErasmus)v¬IncomeT axP ayer
```
InterpretandoTcome "tipico/i", questa corrisponde alle asserzioni:

```
(ITstudenti non sono tassati)
```
```
(ITstudenti-lavoratori sono tassati)
```
```
(ITstudenti-lavoratori in erasmus non sono tassati)
```
Ipotizziamo che laABox contenga, in alternativa, uno dei seguenti fatti:

1. Student(andrea)
2. Student(agnese), W orker(agnese)
3. Student(damiano), W orker(damiano), Erasmus(damiano)

Dunque possiamo inferire le aspettate conclusioni:

1. ¬IncomeT axP ayer(andrea)
2. IncomeT axP ayer(agnese)

14 2. Logiche Descrittive Damiano Gianotti


3. ¬IncomeT axP ayer(damiano)

SeABoxcontenesse l’espressione∃HasBrother.Student(davide)è possibile dedurre
proprietà di individui implicitamente introdotte dalla restrizione esistenziale, come:

```
∃HasBrother.¬IncomeT axP ayer(davide)
```
Infine, aggiungere informazioni irrilevanti non dovrebbe modificare le conclusioni.
Ammettendo, infatti, che laTBoxprecedente abbia la seguente forma:

```
T(StudentuShort)v¬IncomeT axP ayer
```
```
T(StudentuW orkeruShort)vIncomeT axP ayer
T(StudentuW orkeruErasmusuShort)v¬IncomeT axP ayer
```
possiamo concludere cheShort è un’informazione irrilevante rispetto all’essere tas-
sati. Per la stessa ragione, la conclusione che Andrea sia un’istanza di
¬IncomeT axP ayer(andrea)o meno, non è influenzata qualora si aggiunga l’espres-
sioneT all(andrea)allaABox.

2. Logiche Descrittive Damiano Gianotti 15


### 2.5 La logicaALC+T

Dato un alfabeto contenti nomi di ConcettiC, di RuoliRe costanti di individui
Oil linguaggioLappartenente alla logicaALC+Tviene definito a partire dalla
distinzione chiave traConcettieConcetti Estesi[2]

```
Concetti
```
```
A∈ C,>e⊥sonoconcettidi
L
```
```
seC, D ∈ LeR ∈ Rallora
CuD, CtD¬C,∀R.C,∃R.C
sono concetti diL
```
```
ConcettiEstesi
```
```
seCè unconcettodiL, allora
CeT(C)sonoconcetti estesi
diL
```
```
combinazioni booleane di con-
cetti estesi sono a loro volta
concetti estesidiL.
```
La base di conoscenzaKBconserva la coppia(Tbox, Abox)dove:

- T box: contiene asserzioniCvD, doveC∈Lè unconcetto estesodella forma
    C′oppureT(C′), mentreD∈Lè unconcetto
- Abox: composta da espressioniC(a)eaRbdoveC∈ Lè unconcetto esteso,
    R∈LeO

Estendiamo la definizione di Modello utilizzato nella terminologia logica sottostante,
al fine di fornire una semantica all’operatoreT

```
M=〈∆;I;<〉
```
∆è il domino.Iè la funzione di estensione. Ecco il nuovo elemento, una relazione
d’ordine, non riflessiva, transitiva e modulare, che ha la funzione di determinare,
all’interno dellaKnowledge Base, quali individui siano tipici e quali no.

16 2. Logiche Descrittive Damiano Gianotti


Intuitivamente un individuomètipicose non esiste alcun elemento piùnormale, vi-
ceversa, unnèatipicoquando esiste almeno un individuo piùnormale. Indichiamo
formalmente che l’espressione:

```
x < y (l’individuoxè piùnormalediy)
```
Consideriamo dunque l’esempio 2.5 della pagina precedente:
gli studenti tipici sonob, c, d, e, f, g, h, in particolare,eè tipico perché non è in al-
cuna relazione del tipox < y, per quanto riguarda la catenah, f, d, bsi evince ched
ebsiano piùnormalidifche a sua volta è piùnormaledih;
come conseguenzadebrisultano essere tipici poiché questa catena non prosegue
bensì termina con loro due. Invece non risulta corretto concludere chegsia uno stu-
dente tipico, infatti, nonostante sia più normale dic, è in relazione cona, tuttaviaa
appartiene ad un insieme diverso (Barista) e questo non influisce sulla sua "tipicità".
La relazione di preferenza ha limite di essere parziale, infatti non è sempre possibile
stabilire quale elemento sia più tipico degli altri.

In realtà l’estensione di questa sezione viene chiamataALC+TRdove il pedice R
indica il concetto di logica razionale sulle cui proprietà si basa la semantica di T. Tali
caratteristiche, come laspecificità, costituiscono le fondamenta del ragionamento non
monotono, permettendo modellare la situazione in questo modo:

```
Figura 2.2: Un esempio di modello
```
2. Logiche Descrittive Damiano Gianotti 17


Nella Figura 2.2 è possibile rappresentare Tux (unPinguino) come è un uccello che
non vola; graficamente quest’informazione è racchiusa nella zona verde dell’insieme
Uccello, ovvero, quella sezione popolata da tutti gli uccelli atipici, mentre la porzione
in blu rappresenta gli elementi tipici.

### 2.6 La logica non monotonaALC+TRaClR

Nonostante l’aggiunta dell’operatoreTla logica appena vista rimane monotona, nel
senso che se il fattoFsegue da una certa base di conoscenzaKB, allora lo stesso
fattoFsegue da una qualsiasiKB′⊆KB. Di conseguenza, a meno che una base
di conoscenza contenga delle assunzioni esplicite circa la tipicalità degli individui,
non esiste alcun modo per inferire proprietà rivedibili su di loro.
Un’altra limite riguarda l’intrattabilità dellairrilevanza.

```
LottatoreDiSumovAtleta
```
```
T(Atleta)v¬Grasso
```
```
T(LottatoreDiSumo)vGrasso
```
per via della monotonia diALC+TRnon si può derivare che:

```
T(LottatoreDiSumouOrientale)vGrasso
```
malgrado l’etnia sia totalmente irrilevante rispetto all’essere grassi o magri.

Con l’obbiettivo di creare inferenze non monotone utili gli autori in [3] hanno rin-
forzato la semantica precedente restringendo le assegnazioni ad una classe minimale
di modelli. L’idea è quella di restringere l’assegnazione a modelli minimi chemi-
nimizzino l’atipicalità dei concetti e dove le inclusioni implicate sono quelle che
appartengono alla chiusura razionale della base di conoscenza, estensione naturale
di [6].

Considerare solo i modelli che massimizzano le istanze tipiche di un concetto quan-
do sono consistenti con la base di conoscenza. Senza entrare troppo nei dettagli
la semanticaALC+TRaClR non monotona si basa su modelli razionali minimi che
riducono al minimo ilrankdegli elementi del dominio.

Intuitivamente, dati due modelli M∞,M∈ di una KB se è noto che inM 1 un
elementoxha rank 2 (a causa di istanzez < y < x) ed inM 2 xha rank 1 (a causa
diy < x), noi preferiamo il secondo, perché l’elemento x risulta più tipico che inM 1.
I modelli vengono quindi selezionati per il ragionamento scartando quelli grado più
elevato poiché in essi gli elementi sono meno "tipici" e quindi verrebbero dedotte
meno informazioni (vedi anche Figura a pagina 16).

18 2. Logiche Descrittive Damiano Gianotti


#### 2.6.1 Traduzione dell’operatore T

In alcuni contesti non è sempre possibile modificare l’intera struttura basata su
logiche consolidate. È sensato chiedersi quale sia il significato di questo operatore e
se esistano formulazioni equivalenti. Consideriamo laTBox:

```
T(P esce)vOviparo
```
Come sappiamo esprime il fatto che, tipicamente, gli uccelli sono ovipari (depositano
le uova).
Ecco la traduzione equipollente, vista in [11] e [7], senza far uso dell’operatoreTè
la seguente:

1. P esceuP esce 1 vOviparo
2. P esce 1 v∀R(¬P esceuP esce1)
3. ¬P esce 1 v∃R(P esceuP esce1)

Questa traduzione implementa la relazione d’ordine<precedentemente introdotta.
L’insiemeP esce 1 rappresenta i pesci tipici mentreP escecontiene tutti i possibili
pesci, compresi quelli atipici, e costituisce infatti un soprainsieme di Pesce1.
La suddivisione in questi due insiemi a 2.3 è fondamentale per poter tenere traccia
delle eccezioni, ottenendo così la possibilità di ragionare sia sull’individuo generico
sia sul tipico individuo.
Pertanto per inferire chenemosia un tipico P escecontrollerà che la seguente

```
Figura 2.3: Esempio traduzioneT(P esce)vOviparo
```
espressione sia vera:

```
T(P esce)(nemo) ⇐⇒ P esce(nemo)∧P esce1(nemo)
```
In caso di risposta affermativa sarà verificato che:

```
P esce(nemo)uP esce1(nemo)vOviparo(nemo)
```
2. Logiche Descrittive Damiano Gianotti 19


Ecco quindi verificata la condizione 1 di 2.6.1 Viceversa la definizione 2 e 3 esprimono
formalmente cosa significhi essere un individuo a/tipico.

P esce 1 v∀R.(¬P esceuP esce1) ¬P esce 1 v∃R.(P esceuP esce1)

Nell’esempio 2.6.1, i membrid, eedfsono pesci tipici. È evidente che l’intersezione
¬P esceuP esce 1 sia vuota. Dunque deduciamo che, dato l’insiemeA, se un elemento
m∈Aètipicoo non è in alcuna relazione del tipox < y()e quindi non esiste un
individuo più normale di lui) o è più ordinario di un genericox(m < x)conx∈A
oppure si trovi nella relazionex < mdove peròx /∈A.

Per quanto concerne i pesciatipici, come le istanzea, bec, per verificarne la tipicità
viene svolto un procedimento molto simile. Prendiamo in esempiob: viene verificato
inizialmente lo stato dell’elemento (se si trovi o meno in una o più relazioni) e
analizzato. In questo caso scopriamo che è più caratteristico diama meno dic
che, a sua volta, è più generico did, che scopriamo essere tipico. Per transitività
troviamo la relazioned < bche conferma a b la sua atipicità. In conclusione, un
membro è atipico quando esistealmeno unindividuo più normale di lui

### 2.7 La logicaALC+TPR

Dopo aver illustrato la logica di baseALCed introdotto l’estensione non monotona
ALC+Tcon i relativi concetti dichiusura e logica razionale, in questa sezione
verrà descritta l’estensione "accennata" nel capitolo introduttivo 1.1 che permette
di tenere in considerazione la probabilità di individui particolari [8].

#### 2.7.1 Modifiche alla semantica

L’inclusione di tipicalità si evolve e va ad assumere la forma:

```
T(C)vpD
```
con il significato intuitivo aggiuntivo: la probabilità di avere unCeccezionale (cioè
atipico) che non sia anche unDvale 1 −p.

La base di conoscenza (KB)(T Box, ABox)ha la seguente struttura

T Boxin cuip∈ep∈(0,1)

- CvpP
- T(C)vpP

```
ABoxin cuia, b∈′
```
- C(a)
- R(a, b)

È facilmente intuibile che più la probabilità p è alta più l’inclusione è "libera da ec-
cezioni" o, equivalentemente, è meno probabile avere un C speciale che non è anche
un D.
A tal proposito è importante sottolineare che la probabilitàpconp= 1non è consen-
tita in quanto l’inclusioneT(C)v 1 Dcorrisponde all’inclusione strettaT(C)vD
che esprime invece il fatto che l’elementoCè sicuramente anche unD.

20 2. Logiche Descrittive Damiano Gianotti


Data una seconda inclusioneT(C′)vp′D′, conp′< p, si assume che questa inclu-
sione sia meno "restrittiva" rispetto alla prima in quanto la possibilità di avere un
eccezionaleC′è più alta rispetto alla probabilità di avere un eccezionaleC, tenendo
rispettivamente conto delle proprietàD′eD.

Considerando, per esempio, la seguenteTBox

- T(Liceale)v 0. 80 Studioso
- T(Liceale)v 0. 60 P raticaDelloSport

si evince che il tipico scolare è studioso e che, normalmente, pratica dello sport;
entrambe sono proprietà del prototipo dello studente, tuttavia ci sono più eccezioni
di studenti che non fanno sport rispetto a quelli che non studiano.

Una cosa importante da tenere in considerazione è la possibilità di avereKnowledge
Basecontenenti inclusioni conp≤ 0. 5 , che se erroneamente interpretate, potrebbero
venir considerate contro-intuitive.

Ad esempio,l’inclusioneT(Liceale)v 0. 22 F umatore potrebbe venir erroneamente
interpretata come "normalmente, gli studenti non sono fumatori"; anche se la cor-
rispondente probabilità è bassa, la spiegazione corretta è che fare uso di sigarette è
in ogni caso una proprietà del prototipo dello studente liceale.
A differenza dell’espressioneT(Liceale)v 0. 80 Studioso, si ha che la probabilità di
trovare studenti eccezionali non fumatori è più alta rispetto a quella di trovare stu-
denti eccezionali che siano studiosi.
Ponendo il caso in cui si volesse formalizzare che il tipico studente non è una persona
giovane, bisogna semplicemente formulare l’inclusioneT(Liceale)v 0. 78 ¬F umatore
nella base di conoscenza.

#### 2.7.2 Estensione dell’Abox

Data una base di conoscenzaKB , viene definito l’insieme finitoTipdei concetti
che occorrono all’interno dell’operatore di tipicalità, formalmente

```
Tip={C|T(C)vpD∈KB}.
```
Dato un individuoaesplicitamente dichiarato nell’ABox, si definisce l’insieme delle
assunzioni di tipicalitàT(C)(a)che possono essere dedotte in maniera minimale
dallaKBnella logica non monotonaALC+TRaClR , conC∈Tip.

Quindi si considera un insieme ordinatoTipA(doveAsta perABox) di coppie(a, C)
di tutte le possibili assunzioniT(C)(a), per tutti i concettiC∈Tipe per tutti gli
individuianell’ABox.

In aggiunta si definisce il multi-insieme ordinatoPAtupla della forma[p 1 , p 2 , ..., pn]
dovepiè la probabilità dell’assunzioneT(C)(a)tale che(a, C)∈TipAalla posizione
i; inoltre rappresenta il prodotto di tutte le probabilitàpijdelle inclusioniT(C)vpij
DnellaTBox.

Seguendo le idee di [10], si considerano diverse estensioniA ̃idell’ABoxche vengono
equipaggiate con una probabilitàpi. Partendo dagli insiemi PA= [p 1 , p 2 , ..., pn]e

2. Logiche Descrittive Damiano Gianotti 21


TipA, il primo passo è quello di definire l’insiemeSdi tutte le stringhe di possibili as-
sunzioni, utilizzando lo 0 comepiper rappresentare che la corrispondente asserzione
di tipicalità non viene più assunta.

Successivamente, si definisce l’estensioneA ̃i diAcorrispondente ad una stringa
[s 1 , s 2 , ..., sn]∈Scosi ottenuta. In questo modo, la probabilità più alta viene asse-
gnata all’estensione dell’ABoxcorrispondente aPA, dove tutte le assunzioni di tipi-
calità vengono considerate. mentre diminuisce nelle altre estensioni, alcune assun-
zioni di tipicalità vengono scartate, così 0 viene usato al posto della corrispondente
pi.

La probabilità di una estensione quindiA ̃icorrispondente aPAi= [pi 1 , pi 2 , ..., pin]
è definita come il prodotto delle probabilitàpij quandopij 6 = 0( cioè la possibi-
lità della corrispondente assunzione di tipicalità nel momento in cui questa viene
selezionata per l’estensione) e 1 −pjquandopij= 0(cioè la corrispondente assun-
zione di tipicalità viene scartata, per segnalare che l’estensione contiene un’eccezione
all’inclusione).

Si può osservare che, inALC+TRaClR , l’insieme delle assunzioni di tipicalità che
possono essere inferite da unaKBcorrispondono all’estensioneAequivalenti alla
stringaPA(nel caso in nessun elemento sia impostato a 0); vengono considerate
tutte le assunzioni di tipicalità, degli individui presenti nell’ABox, consistenti con la
base di conoscenza.
Al contrario, inALC+TR, nessuna assunzione di tipicalità può esser dedotta da
unaKB, e questo equivale ad estendereAcon delle asserzioni corrispondenti alla
stringa[0, 0 , ...,0], ovvero l’insieme vuoto.

Otteniamo dunque una distribuzione di probabilità sulle estensioni diA)(se presen-
ti). Prendiamo come esempio unaKB(T,A)in cui le uniche inclusioni di tipicalità
inT siano le seguenti:

1. T(C)v 0. 60 D
2. T(E)v 0. 85 F

e ae bsiano gli unici individui presenti inA; supponiamo inoltre cheT(C)(a),
T(C)(b)eT(E)(b)siano dedotte dallaKBcon la logicaALC+TPR.

Il risultato è quindi:

TipA={(a, C),(b, C),(b, E)} PA= [0. 6 , 0. 6 , 0 ,85]

Tutte le possibili stringhe, tutte le corrispondenti estensioni diAe tutte le proba-
bilità sono illustrate nella seguente tabella 2.4

22 2. Logiche Descrittive Damiano Gianotti


```
Figura 2.4: Estensioni plausibili
```
#### 2.7.3 Dalla logica verso la "diagnosi"

Descriviamo formalmente cosa si intenda per diagnosi in questo contesto particolare,
aiutandoci con un esempio. Data la seguenteKBcon
ABox={M emoryLoss(P ietro)}eTBox:

- P aranoiavDepressed
- T(AlzheimerP atient)v 0. 85 M emoryLoss
- T(AlzheimerP atient)v 0. 65 P aranoia
- T(DiabetesP atient)v 0. 90 T hirst
- T(DiabetesP atient)v 0. 55 Depressed
- T(Depressed)v 0. 80 Insomnia
- T(Depressed)v 0. 70 Headache

consideriamo un setV, espresso nella formaC(a), che rappresenta i sintomi e i segni
nella forma:
V={P aranoia(P ietro), Headache(P ietro)}

sappiamo cheVnon è implicato dalla base di conoscenza, ma cheKBtVèconsi-
stente. Utilizzando la logicaALC+TPRsiamo interessati a trovare una diagnosi per
i sintomi diP ietro, cioè un insieme diasserzioni Dtali cheKBtD|=V.
Seguendo l’esempio:

- D 1 ={AlzheimerP atient(P ietro)}segue logicamente
- D 2 ={Depressed(P ietro)}non segue logicamente
- D 3 ={AlzheimerP atient(P ietro), Depressed(P ietro)}segue logicamente

che corrispondono a

- T(AlzheimerP atient)(P ietro)è implicato daKBtD 1 ∧KBtD 3
- T(Depressed)(P ietro) è implicato solo inKBtD 3
- T(DiabetesP atient)(P ietro) non è implicato da nessunaKB
2. Logiche Descrittive Damiano Gianotti 23


Possiamo ragionare sugli scenari, consideriamo, ad esempio,D 3 con

```
TipA= (P ietro, AlzheimerP atient),(P ietro, Depressed)
```
e conPA= [0. 525 , 0 .556]dove 0 .525 = 0. 85 × 0. 65 è la probabilità di equipaggiare
la proprietà tipica del concettoAlzheimerP atient, discorso analogo perDepressed.
Utilizzando quanto visto precedentemente si considerano le seguenti estensioni

- A ̃^31 ={T(AlzheimerP atient)(P ietro)}
    conPA ̃ 31 = 0. 525 × 0 .463 = 0. 243
- A ̃^33 ={T(AlzheimerP atient)(P ietro),T(Depressed)(P ietro)}
    conPA ̃ 33 = 0. 556 × 0 .557 = 0. 309

deduciamo, dunque, che:

```
KBtDi|= (ALC+TPR)(0,1)P aranoia(P ietro), Headache(P ietro)
```
coni= 1, 3 , vale a dire che tutte le asserzioni di cui sopra rappresentano una diagnosi
per i sintomiV

E con questo concludiamo la trattazione dei fondamenti di logica.
Questa capitolo altro non è che un sunto, a tratti informale, della storia di questa
branca matematica e non sostituisce certamente gli articoli e studi fatti nel corso
degli anni, da figure molto più autorevoli, della mia ma costituisce il corpo fondante
di tutta la tesi.

24 2. Logiche Descrittive Damiano Gianotti


# Capitolo 3

# Strumenti utilizzati

In questo capitolo descriveremo le componenti che utilizzeremo nella nostra archi-
tettura e, per ognuna di queste, introdurremo brevemente le caratteristiche chiave.

### 3.1 OWL2

L’OWL 2 Web Ontology Language, informalmente OWL 2, è un linguaggio onto-
logico, basato sulle logiche descrittive oDL, costruito per il Semantic Web con un
significato formale e definito in [9]. Le ontologie in OWL 2 vengono definite tramite
la specifica di classi, proprietà, individui e valori dei dati e sono memorizzate come
documenti del Semantic Web. Queste possono essere pubblicate sul web e riferite da
altre ontologie, per costruire basi di conoscenza più complesse. Inoltre sono spesso
utilizzate assieme insieme a documenti scritti nel formato RDF, ed stesse vengono
scambiate principalmente come documenti RDF.

#### 3.1.1 Semantica

La semantica è definitaformalmente, cioè permette di scrivere Knowledge Base
sulle quali è possibile applicare inferenze in modo automatico. OWl2 possiede due
semantiche:

```
Semantica diretta, basata sulle Logiche Descrittive (vedi pag.9)
```
- è applicabile a un frammento del linguaggio detto OWL2 DL;
- è sempre decidibile;
- ha una sintassi più ristretta.

```
Semantica Indiretta, basata sui grafi RDF
```
- estende la semantica formale di RDF
- ha la massima espressività
- la decibilità non è garantita

la semantica è basata suiff(se e solo se) quindi:

```
Cè sottoclasse di D ⇐⇒ istanze diC⊆istanze diD
```
##### 25


#### 3.1.2 Caratteristiche

Il linguaggio prevede tre componenti principali:

1. Entità: elementi atomici usati per riferirsi ad oggetti, categorie e relazioni del
    mondo reale; costituiscono gli assiomi
    Lara, donna, P ietro, Sof ia, essere_f idanzati
2. Assiomi: affermazioni (statement) di base espressi da un’ontologia OWL
    Laraè unadonna|P ietroeSof iasonof idanzati
3. Espressioni: combinazioni di entità che costituiscono descrizioni complesse,
    definite tramite l’utilizzo di costruttori.
    M edicoeDonnacombinate definisconoDonnaM edico

Ogni file.owlinizia con un preambolo:

```
Prefix(:=<http://example.com/owl/families/>)
Prefix(otherOnt:=<http://example.org/otherOntologies/families/>)
Prefix(xsd:=<http://www.w3.org/2001/XMLSchema#>)
Prefix(owl:=<http://www.w3.org/2002/07/owl#>)
Ontology(<http://example.com/owl/families>
Import( <http://example.org/otherOntologies/families.owl> )
```
Prefix(..)

permette di fare, sinteticamente, riferimento a elementi definiti in altre ontologie o in
altri file; il prefisso più l’etichetta sono composti nell’identificatore dell’elemento di
interesse, ad esempioowl:Thingdiventahttp://www.w3.org/2002/07/owl#Thing.

Ontology(..)

Specifica l’URI(Uniform Resource Identifier) del file contenente l’ontologia definita.

#### 3.1.3 Sintassi e Modellazione di Base

È possibile scrivere ontologie OWL utilizzando sintassi differenti:

- Functional-StyleClassAssertion(:Persona:Damiano)
- ManchesterIndividual: Damiano
- Turtle:Damiano rdf:type :Persona
- RDF/XML<Persona rdf:about="Damiano">
- OWL

```
<ClassAssertion>
<Class IRI="Person"/>
<NamedIndividual IRI="Damiano"/>
</ClassAssertion>
```
Ed esiste una chiara equivalenza tra le varie terminologie utilizzate, vediamola:

26 3. Strumenti utilizzati Damiano Gianotti


Ing. della conoscenza

- Oggetti
- Categorie
- Relazioni

```
Description Logic
```
- Costanti
- Predicati Unari
- Predicati Binari

```
Termini OWL
```
- Individui
- Classi
- Proprietà

Dopo queste considerazioni generali, entriamo ora nei dettagli della modellazione con
OWL2. Nei paragrafi successivi introdurremo le funzionalità essenziali per produrre
una base di conoscenza. Queste saranno condite con esempi, semplici dimostrazioni
delle varie funzionalità di OWL. Per semplicità useremo ilFunctional-Style.

Ecco come si esprimono gli Assiomi:

- dichiarazioni di individuo: Declaration(Name Individual(:Dario))
- dichiarazioni di classe: Declaration(Class(:Persona))
- dichiarazioni di proprietà: Declaration(ObjectProperty(:Uomo))

E alcune delle relazioni chiave:

ClassAssertion(:Persona :Dario)) lega un’istanza ad una classe;
SubClassOf(:Persona :Uomo)) relazione di sottoclasse (v);
EquivalentClasses(:Persona :Umano) equivalenza di due classi;
DisjointClasses(:Donna :Uomo) classi disgiunte.

Permette di legare due individui tramite una proprietà.

ObjectPropertyAssertion(:haMoglie :Donna :Uomo)

#### 3.1.4 Classi complesse e implementazione diu,t,∃e∀

Tramite opportuni costrutti è possibile specificare classi complicate e relazionarle,
anche grazie all’operatore di intersezioneue disgiunzionet.

```
EquivalentClasses(:Padre
ObjectIntersectionOf(:Uomo :Genitore))
EquivalentClasses(:Genitore
ObjectIntersectionOf(:Madre :Padre))
```
Nonna è sottoclasse dell’intersezione fraDonna e Genitore.

```
SubClassOf(:Nonna
ObjectIntersectionOf(:Donna :Genitore))
```
L’individuoMarcoè unaPersona(e) nonGenitore.

```
ClassAssertion(
ObjectIntersectionOf(:Persona
ObjectComplementOf(:Genitore))
:Marco)
```
Vediamo, infine, come si possano utilizzare i quantificatori∃e∀con qualche esempio.
La classeGenitoreè l’insieme di quegli individui che possiedono almeno un’istanza

3. Strumenti utilizzati Damiano Gianotti 27


diPersonache è loro Figlio; una persona èFelicequanto tutti i suoi figli sono felici.
Le persone che non hanno figli, vengono correttamente considerati felici.

Quantificatore esistenziale∃

```
EquivalentClasses(
:Genitore
ObjectSomeValuesFrom
(:haFiglio :Persona))
```
```
Quantificatore universale∀
EquivalentClasses(
:PersonaFelice
ObjectAllValuesFrom
(:haFiglio :PersonaFelice))
```
Questo conclude la nostra visione sintetica del linguaggio.

#### 3.1.5 OWL2VersusDB e considerazioni finali

I file.owlconservano informazioni ma nonostante ciò OWL2nonè un framework per
basi di dati; Nonostante parte della terminologia evochi assonanze con iDataBase,
la semantica di base ha delle differenze sostanziali.

In primis l’assunzione di mondo: un fatto non contenuto in unDBè considerato
falso (mondo chiuso) mentre nel mondo logico viene considerato mancante (mondo
aperto). In secondo luogo, classi e proprietà possono avere definizioni multiple e
OWL non richiede che le uniche proprietà di un individuo siano quelle della classe a
cui appartiene. Come terzo punto, ci teniamo a sottolineare un ulteriore differenza
sostanziale: con iDBnon faccio ragionamento, non esplicito informazioni implicite,
con OWL sì. Infine ricordiamo ciò che abbiamo visto a 3.1.2 : le informazioni
riguardanti un singolo individuo possono essere distribuite su più documenti diversi,
contrariamente ad un classico database.

In conclusione vogliamo ricordare che OWLnonè un linguaggio di programmazione,
bensì un linguaggiodichiarativo, in grado di rappresentare della conoscenza. Diversi
sono gli strumenti a disposizione per trattare le ontologie: ragionatori automatici,
API, validatori, editor e ambienti di sviluppo. Nella sezione successiva tratteremo
alcuni di questi tool che fanno parte di DbN.

### 3.2 Owlready2

Lavorare direttamente con OWL è impegnativo e tedioso, ma, in nostro soccorso,
arrivano le API (Application Programming Interface). Tra le più recenti e interes-
santi spicca Owlready2 [5], pratica libreria ontology-oriented, scritta in Python3.
Owlready versione 2 permette un accesso trasparente alle ontologie, contrariamen-
te alle API basate su Java. Può caricare ontologie OWL2 come oggetti Python,
modificarli, salvarli e, appoggiandosi adHermiTePellet(reasoner scritti in Java),
eseguire veri e propri ragionamenti. Vediamo alcune caratteristiche chiave.

#### 3.2.1 Tabella di conversione

Se dovessimo "convertire" le formule tra Description Logics, Owlready2 e/o Protegè,
potrebbe essere di interesse la sottostante tabella.

28 3. Strumenti utilizzati Damiano Gianotti


Molti di questi simboli ci sono familiari e, di conseguenza, il salto rappresentazio-
nale è molto basso. Utilizzare la semantica di questo pacchetto non risulta troppo
impegnativo, poiché coerente con le Logiche Descrittive.

3. Strumenti utilizzati Damiano Gianotti 29


#### 3.2.2 Che cosa posso fare con OWLReady2?

from owlready2 import *

# Caricare un ontologia da una repostiory locale o da Internet:
onto = get_ontology("http://www.lesfleursdunormal.fr/.. .../pizza_onto.owl")
onto.load()

# Creare nuove classi nell'ontologia
# mischiando costrutti OWL e metodi Python:
class NonVegeterianPizza(onto.Pizza):
equivalent_to = [onto.Pizza &
(onto.has_topping.some(onto.MeatTopping) |
onto.has_topping.some(onto.FishTopping)
)]

```
def eat(self) : print ("Yuuum! So good!")
```
with onto:
class Pizza (Thing):
def eat(self) : print ("I love pizza !")
pass

# Accedere le classi dell'ontologia e creare nuovi Individui/instanze:
test_pizza = onto.Pizza("test_pizza_owl_identifier")
test_pizza.has_topping = [onto.CheeseTopping(),onto.TomatoTopping()]
print(test_pizza.has_topping)
''' [pizza_onto.cheesetopping1, pizza_onto.tomatotopping1] '''

# In questo pacchetto quasi ogni lista può essere modificata sul posto,
# per esempio aggiungendo/rimuovendo elementi dalla lista.
# Owlready2 aggiornerà in automatico il quadstore RDF.
test_pizza.has_topping.append(onto.MeatTopping())
print(test_pizza.has_topping)
''' [pizza_onto.cheesetopping1, pizza_onto.tomatotopping1,
pizza_onto.meattopping1]'''
test_pizza.eat() ''' I love pizza! '''

# Effeturare "reasoning" e classificare le istanze e le classi
print(test_pizza.__class__) ''' pizza_onto.Pizza '''
sync_reasoner()
print(test_pizza.__class__) ''' pizza_onto.NonVegeterianPizza '''
test_pizza.eat() ''' Yuuum! So good! '''

# Esportare l'ontologia in un file .owl
onto.save("Demo")

30 3. Strumenti utilizzati Damiano Gianotti


#### 3.2.3 Architettura

Le RDF Quadruple giocano un ruolo importante, diamone una definizione : SiaSun
insieme di fonti di dati, che è un sottoinsieme delIRIsset (cioeS⊆I. Una coppia
ordinata(t, g)della triplat= (s, p, o)e del grafog∈S et∈get(c)è una tripla
nel grafog, dovegetè una richiesta HTTP get request, e il risultato della richiesta
non può essere un insieme vuoto (get(s) 6 =. La quadrupla(s, p, o, g)è chiamata una
RDF quadrupla (RDF quad).

Owlready2 mantiene, quindi, un quadstore (DBdi quadruple) RDF in un database
ottimizzatoSQLite3, sia in memoria che, opzionalmente, su disco.
Fornisce, inoltre, un accesso di alto livello alle classi e agli oggetti presenti nell’onto-
logia. Classi e Individui vengono caricati dinamicamente dalDBsecondo necessità,
salvati in memoria e poi eliminati quando non più necessari.

#### 3.2.4 Paragone con precedenti approcci

```
Figura 3.1: Paragone di Owlready con altri approci di programmazione.
```
La tabella 3.1 confronta diverse tecnologie precedenti con Owlready2. Owlready
si distingue come uno degli approcci più avanzati. In particolare, è in grado di
classificare automaticamente (non solo gli individui ma anche le classi), compiere
"reasoning" sul mondo locale chiuso e non e proporre una sintassi ad alto livello
per definire i vincoli "role-fillers". Queste ed altre caratteristiche risultano cruciali
quando si lavora utilizzando ontologie mediche, ma, certamente, non sfigurano anche
in altri domini applicativi.

Ecco, quindi, quali sono le componenti chiavi di un sistema capace di adattarsi a
differenti casi d’uso, in maniera decisamente flessibile e dinamica.

3. Strumenti utilizzati Damiano Gianotti 31


### 3.3 Plotly

Plotly.py è una delle migliori librerieOpen Source di plotting: supporta oltre 40
tipi di grafici unici, interattivi e ricchi di funzionalità, andando a coprire una vasta
gamma di casi d’uso: statistico, finanziario, geografico, scientifico e tridimensionale.
Non mancano i classici grafici a linee, a barre, a bolle e a punti. [4]

#### 3.3.1 Perché usare Plotly.py?

Costruita sopra la più celebre libreria Javascript (Plotly.js, composta da d3.js e
stack.gl), Ploty.py permette di creare bellissime realizzazioni interattive basate sul
web, che possono essere salvate come file HTML o utilizzate come parte di web-app
scritte in Python. Tutti i grafici di Plotly.py sono completamente costumomizzabili.
Tutto, dai colori e dalle etichette alle linee della griglia e alle legende, può essere
personalizzato utilizzando una serie di attributi dedicati. I diagrammi, inoltre, sono
dotati di funzionalità interessanti come lo zoom, il panning, il ridimensionamento
automatico, ecc.
Grazie all’integrazione profonda con Orca, utility per l’esportazione di immagini,
Plotly.py fornisce un notevole supporto anche per i contesti al di fuori del web,
inclusi gli IDE (PyCharm, Spyder) e la pubblicazione di documenti cartacei, come
questo testo.

L’obiettivo era quello di rendere gradevoli ed esplicativi i risultati "diagnostici"
prodotti dal tool DbN.

#### 3.3.2 Che cosa posso fare con Plotly.py?

# Esistono principalmente due modi per rappresentare le figure:
# usando i dict di python
import plotly.io as pio

fig_dict = {
"data": [{"type": "bar",
"x": [1, 2, 3],
"y": [1, 3, 2]}],
"layout": {"title": {"text": "A Bar Chart"}}
}
pio.show(fig)

# usando la gerarichia delle classi chiamata "graph objects".
import plotly.graph_objects as go
fig_graph = go.Figure(
data=[go.Bar(x=[1, 2, 3], y=[1, 3, 2])],
layout=go.Layout(
title=go.layout.Title(text="A Bar Chart")
)
)
fig.show()

32 3. Strumenti utilizzati Damiano Gianotti


# Si possono salvare i diagrammi in singoli file HTML:
fig.write_html('first_figure.html', auto_open=True)

# Esiste anche la possibilità di creare sottografici
from plotly.subplots import make_subplots

# Creiamo un grafico da una riga e due colonne:
fig = make_subplots(rows=1, cols=2)

# Aggiungiamo un grafico a dispersione e un istogramma:
fig.add_scatter(y=[4, 2, 1], mode="lines", row=1, col=1)
fig.add_bar(y=[2, 1, 3], row=1, col=2)
fig.show()

3. Strumenti utilizzati Damiano Gianotti 33


# Capitolo 4

# Caso d’uso: Tool per il supporto

# diagnostico

In questo capitolo verrà descritto il programma oggetto della tesi DbN (Diagnosis
by Numbers) che altro non è che un’estensione diPEAR(Probability of Exceptions
and typicAlity Reasoner) [11]. Inizialmente si fornirà un breve riassunto del lavoro di
Soriano; successivamente cosa sia stato preso o meno. Poi obiettivi posti e aggiunte
ed infine il progetto completo con annesso esempio. Come linguaggio per lo sviluppo
è stato sceltoPython(in particolare la sua versionePython3.7) per diversi motivi,
eccone alcuni:

- continuità con il lavoro precedente;
- la presenza di nuove API (vedi 3.2 pag. 28);
- tipicamente richiede meno codice rispetto ad altre soluzioni;
- è uno dei linguaggi più popolari per l’elaborazione scientifica.

### 4.1 PEAR - Sintesi

Struttura Questo tool, basato sulla logicaALC+TPR, è strumento che permette
di ragionare e dedurre informazioni, di definire precisamente chi siano gli individui
tipici, atipici e quali siano le caratteristiche peculiari di una data categoria. Il
funzionamento dell’intero strumento è riassumibile in questi passi:

1. dopo aver letto le informazioni costituenti la KB, presenti in un file a parte,
    viene creata l’ontologia;
2. vengono combinate le probabilità delle assunzioni di tipicalità e generati tutti
    gli scenari (possibili realtà dei fatti);
3. di ogni scenario viene calcolata la probabilità complessiva;
4. viene verificata o meno la consequenzialità logica del fattoFdato in input per
    ogni scenario;
5. infine vengono mostrati i risultati dell’interrogazione.

##### 34


Questo è possibile anche grazie alla seguente architettura (vedi Figura 4.1), dove i
singoli file richiamano, spesso, i concetti teorici associati, precedentemente illustrati.

```
Figura 4.1: Archittetura di Pear
```
Limiti Le conclusioni così prodotte sono certamente interessanti, ma la procedura
di ragionamento in se è vincolata, di volta in volta, dalla query iniziale.
Intuitivamente, ci si chiede se un determinato eventoFsia conseguenza logica nel-
la possibili diramazioni (scenari)B 1 , B 2 , ...., Bndella base di conoscenzaB. Questo
procedimento non è applicabile in un contesto realistico, poiché chiederebbe all’uten-
te di comprendere la logica anche solo per capire come effettuare un’interrogazione
significativa. Inoltre sono presenti dei difetti tecnici, come, ad esempio, la necessi-
tà, durante la verifica di conseguenza logica, di effettuare una copia dell’istanza del
manager dell’ontologia per ogni scenario.

Alla luce di quanto detto in precedenza ecco la necessità di ottimizzazione ed
espansione diPEARin una naturale evoluzione:Diagnosis by Numbers

### 4.2 Visione complessiva

L’idea di questa tesi, introdotta nel primo capitolo e ribadita più volte, finalmente
inizia a prender forma. Data un’ontologia, più o meno vasta, arricchita da espressio-
ni di tipicalità e dai sintomi/prodromi riguardanti un paziente, l’obiettivo è quello
di generare tutte le possibili diagnosi (o spiegazioni), controllarne la veridicità (lo-
gicamente parlando) e presentarle in forma grafica, evidenziandone la probabilità e
il costo stimato.

4. Caso d’uso Damiano Gianotti 35


Ovviamente il focus principale rimane la correttezza di esecuzione, non tanto la
complessità dell’ontologia medica o dei costi diagnostici reali. Questo non toglie che
in futuro possa avere delle applicazioni concrete.

Struttura del progetto Il progetto è composto da 12 File; questi, a volte,
verranno indicati con un intuitiva abbreviazione, così da rendere la lettura più
scorrevole:

- Main.pyfile principale, contenente l’ordine d’esecuzione delle operazioni.
- Due file di testo, di input:
    - OntologyInput.txtcontiene classi, relazioni tra classi, fatti tipici ed indi-
       vidui;
    - PatientSetOfSymptoms.txtcomposto da coppie individuo-classe.
- Quattro file chiave:
    - OntologyManager.pygestisce tutto ciò che riguarda l’ontologia;
    - InputFromFile.pysi occupa della traduzione del file OntoInput tramite
       OntoManager;
    - IncreasedOntology.pycalcola le probabilità di ogni membro tipico e genera
       tutti gli scenari;
    - ReasoningOnScenarios.pycalcola le probabilità per ogni scenario ed ef-
       fettua il ragionamento per ogni scenario arricchito con gli scenari.
- Cinque file di supporto:
    - AboxMember.pycorrispettivo dell’ABox;
    - TypicalFact.pyassieme alla classe TypicalMember
       corrispettivo dell’TBox;
    - TypicalMember.pyassieme alla classe TypicalFact
       corrispettivo dell’TBox;
    - Scenario.pyrappresenta il singolo scenario;
    - QueryResult.pymemorizza i risultati e genera il grafico associato.

Le successive sezioni del capitolo andranno ad illustrare le funzionalità chiave dello
strumento organizzate per file.

### 4.3 Immissione dei dati

#### 4.3.1 I documenti in ingresso

Partiamo dall’illustrare come vengano memorizzate le informazioni relative all’on-
tologia dallo strumento e quale sia il corrispettivo del file in termini di logiche
descrittive.

36 4. Caso d’uso Damiano Gianotti


Classes:
Bipolar Depressed MoodReactivity ProstateCancerPatient Nocturia
Set_as_sub_class:
Bipolar,Depressed
Add_members_to_class:
Greg;Depressed | Luca;ProstateCancerPatient
....
Set_typical_facts:
Typical(ProstateCancerPatient),Nocturia,0.8
Typical(Depressed),Not(MoodReactivity),0.85
......

Il fileOntologyInput.txtè composto da 4 parti:

1. Classes: altro non è che un elenco di tutte le classi che si andranno ad
    utilizzare;
2. Set_as_sub_class: è una lista composta da coppie sottoclasse e classe, vedi
    il sottoparagrafo 3.1.3;
3. Add_members_to_class: contiene gli individui e le relative classi di apparte-
    nenza;
4. Set_typical_facts: contiene l’elenco delle inclusioni di tipicalità.

La stessa ontologia espressa in termini diKB(T,A):

- T Box
    - Bipolar@Depressed
    - T(P rostateCancerP atient)v 0. 80 N octuria
    - T(Depressed)v 0. 85 ¬M oodReactivity
- ABox
    - Depressed(Greg)
    - P rostateCancerP atient(Luca)

In fondo al documento troviamo un nuovo elemento, i costi diagnostici; ogni malattia
tipica avrà un costo associato e, alla fine dell’elaborazione, verranno elaborati e
combinati per assegnare al singolo scenario un costo indicativo, al fine di dare un
ulteriore criterio di preferenza al medico. Allo stato attuale i costi sono puramente
d’esempio e non realistici.

Set_cost_of:
ProstateCancerPatient: 10000
Depressed: 3000

SottoSet_cost_ofvi sono le coppie malattia-costo stimato (in€)

Infine il filePatientSetOfSymptoms.txtin confronto è più basilare

```
Luca;Not(Bipolar) | Greg;Nocturia
```
4. Caso d’uso Damiano Gianotti 37


Questi fatti verranno manipolati e poi aggiunti all’Aboxin ogni scenario, solo se
consistenti con l’ontologia di base.

#### 4.3.2 La classe dedicata alla traduzione

Il fileInputFromFile.pycontiene due metodi: build_ontologyeread_symptoms.
Ogni metodo si occupano del rispettivo file, rispettivamente OntologyInput.txt e
PatientSetOfSymptoms.txt. Infatti, dopo aver letto il contenuto del file di testo, le
stringhe vengono elaborate e successivamente data in input ai metodi della classe
OntologyManagerqualicreate_class, add_sub_class_, add_member_to_class
ecc. Come ulteriore ottimizzazione, l’esecuzione diread_symptomsviene effettuata
una sola volta, poiché si è preferito salvare i dati letti indict()(coppie chiave-valore)
dedicato tramite il metodostore_for_reasoning, che vedremo più in dettaglio
nella prossima sezione.

Rispetto alla versione precedente il codice è stato ottimizzato e reso più leggibile
anche grazie all’introduzione di due funzioni ausiliarestrip_notestrip_typical.
Come si intuisce dal nome lo scopo di queste 1-line-function è di rimuovere le stringhe
"Not"e"Typical"che son superflue e vanno diversamente gestite.

### 4.4 L’ amministrazione dell’ontologia

Nel fileOntologyManager.py, contenente l’omonima classe, sono presenti numerosi
metodi per la creazione e la gestione dei mondi e delle ontologie. Focalizziamo la
nostra attenzione sul costruttore:

def __init__(self, iri="http://www.example.org/onto.owl"):
self.typical_facts_list = list()
self.a_box_members_list = list()
self.scenarios_list = list()
self.typical_members_list = list()
self.cost_dict = dict()
self.symptoms_dict = dict()
self.my_world = World()
self.big_world = World()
self.onto = self.my_world.get_ontology(iri)

notiamo, oltre alla presenza dell’iri 3.1.3, l’utilizzo di una variabile, dal nome espli-
cativo, per ogni lista necessaria. La novità più importante riguarda l’utilizzo dei
mondi. Owlready2 3.2 può supportare numerosi mondi isolati, e questo ci aiu-
ta, poiché siamo interessati a caricare diverse versioni della stessa ontologia. Ecco
quindi spiegate le due differenti variabili. my_worldè utilizzata per contenere l’on-
tologia di base, mentrebig_worldha lo scopo di racchiudere l’ontoBase arricchita
con lo scenario selezionato. Se non si capisce ora quale sia l’utilità di questa scelta,
successivamente verrà illustrata in maniera più approfondita.

Passiamo ora ad analizzare i metodi di istanza incaricati della gestione dell’ontolo-
gia; la maggior parte sono semplici wrapper delle risorse fornite dalla libreria e non
richiedono ulteriori spiegazioni. Tuttavia, tra questi spiccano i metodi per la gestio-
ne deifatti tipicie deimembri tipici, operatori non conosciuti dalla nostraAPIdi

38 4. Caso d’uso Damiano Gianotti


Python. La soluzione migliore, già adotta in PEAR, consiste nell’eliminare l’opera-
toreTtramite una particolare traduzione, vista nella sezione 2.6.1 e implementata
nel metodoadd_typical_fact. Ricordiamo, brevemente, che un paziente è atipico
quando esistealmeno unindividuo più normale di lui. Per, invece, esprimere il
concetto di membromè un tipicoCbisogna dire chemappartiene sia alla classe
C (tutti gli elementi) sia alla classeC 1 (elementi tipici). Questa idea trova la sua
realizzazione nel metodoset_as_typical_member.

Per ridurre i tempi di lettura e manipolazione da file si è voluto introdurre una
mappa dedicata ai sintomi con due funzioni manipolative associate, vediamole:

def store_for_reasoning(self, member_name: str, class_id: object):
self.symptoms_dict.update({class_id: member_name})

def add_symptoms_to_kb(self):
for class_sy, pname, in self.symptoms_dict.items():
class_c = self.create_class(class_sy.name)
not_class_c = self.create_class("Not(" + class_sy.name + ")")
class_c.equivalent_to = [Not(not_class_c)]
self.add_member_to_class(pname, not_class_c, symp=True)
print("Sintomo aggiunto: " + pname + ": " + class_c.name)

la prima ha il compito di aggiungere valori al "dizionario" le coppie:
nome-paziente: classe-sintomo.
La seconda, invece, per ogni coppia presente nella struttura, crea le classi appro-
priate e poi aggiunge un membro all’ABoxall’ontologia corrente tramite la funzione
add_member_to_class.

È altrettanto importante focalizzarci sulla gestione dei mondi, effettuata dai metodi:

```
def save_base_world(self):
self.onto.save("ontoBase.owl", format="ntriples")
```
```
def create_new_world(self):
self.onto.destroy()
self.big_world = World()
self.onto = self.big_world.get_ontology(
"file://" + PATH_TO_ONTO + "//ontoBase.owl").load()
```
il primo possiede l’incarico di esportare l’ontologia, creata nell’omonimo mondo nel
punto 4.3.2 Il secondo assume la funzione di distruggere l’ontologia contenuta nella
variabileonto, di creare un nuovo mondo e di caricare l’ontologia salvata preceden-
temente sul file. Vedremo meglio più avanti quale sia stata la strategia dietro lo
sviluppo di questi metodi.
Analogamente a questo concetto citiamo la seguente funzione:

def consistency(self, condition: bool = False):
try:
with self.onto:
if condition:
sync_reasoner(self.my_world)
classi_incosistenti = list(

4. Caso d’uso Damiano Gianotti 39


```
self.my_world.inconsistent_classes())
if not len(classi_incosistenti) == 0:
return classi_incosistenti
else:
sync_reasoner(self.big_world)
return "The ontology is consistent"
except OwlReadyInconsistentOntologyError:
return "The ontology is inconsistent"
```
I ragionatoreHermit è in grado di controllare la consistenza di un ontologia e de-
durre nuovi fatti, riclassificando individui e classi in base alle loro relazioni. In
caso di inconsistenza viene lanciata l’eccezione appropriata. È possibile avere classi
inconsistenti senza rendere l’intera ontologia inconsistente ,a patto che queste non
abbiano individui. In nostro aiuto il reasoner inferisce tali classi come equivalenti
toNothing(elemento primitivo di OWL) ed è quindi possibile interrompere l’ese-
cuzione del tool prima che l’intera ontologia sia inconsistente! Vediamo un esempio.
Se avessi unaKB:

TBox

- ¬AvB
- BvA
- T(C)v 0. 80 D

```
ABox
```
- D(Giovanni)

La classe¬A, nonostante non abbia elementi, è inconsistente poiché in contraddi-
zione con l’assiomaBvA. Questo chiude la trattazione del manager.

### 4.5 La creazione dei membri tipici e degli scenari

Il fileIncreasedOntology.pyè un modulo che fornisce i metodi necessari per la ge-
nerazione di tutti i membri tipici e gli scenari possibili e per il calcolo delle relative
probabilità. I metodi incaricati del valutazione delle "percentuali" sono:

def compute_probability_for_typical_members(onto_manager):
facts_list = onto_manager.typical_facts_list
abox_members_list = onto_manager.a_box_members_list
facts_list.sort(key=lambda x: x.t_class_identifier.name)
abox_members_list.sort(key=lambda x: x.class_identifier.name)
......
__set_probability( prob_to_assign_to_typical_member, onto_manager,
facts_list[i].t_class_identifier,
facts_list[i].class_identifier)
....

def __set_probability(prob_to_assign, onto_mng, t_class_id, class_id):
for aboxMember in onto_mng.a_box_members_list:
if aboxMember.isSymptom is True and
aboxMember.class_identifier.name == class_id.name:

40 4. Caso d’uso Damiano Gianotti


```
onto_mng.typical_members_list.
append(TypicalMember(
t_class_id,
aboxMember.member_name,
prob_to_assign
))
```
Il primo processo è il più complicato e si avvale del secondo come supporto. In
sintesi per computare la probabilità da associare ad ogni membro tipico si vanno a
moltiplicare tra loro le probabilità di ogni inclusione di tipicalità avente la medesima
classe argomento dell’operatoreT(ovverot_class_identifier) e, a quel punto, il
metodo di supporto,viene invocato per creare il membro tipico.

Ricordiamo chem è tipico se è nella formap: T(C)(m). Tale funzione, quindi,
scansionando tutti i membri dell’ABox, cerca quello che è un sintomo e ha come
classe di appartenenzaC. Una volta trovato, passa alla creazione Membro tipico,
con la probabilità calcolata precedentemente.

La seconda parte della classe ha la responsabilità degli scenari, realtà possibili dei
fatti. Il numero totale cambia al variare deiTypicalMembere del numero di Sintomi,
in particolare, conn membri tipici è 2 n. Considerando, ad esempio, mt 1 e mt 2
l’insieme risultante sarà la combinazione:

```
{{∅},{mt 1 },{mt 2 },{mt 1 , mt 2 }}
```
dove∅rappresenta lo scenario vuoto, in cui non si fa alcuna assunzione,{mt 1 }in
cui si assume solomt 1 ,{mt 2 }in cui si assume solomt 2 e infine l’ultimo dove si
assumono entrambi.

Per quanto riguarda la probabilità da associare ad ogni scenario, essa è data dal
prodotto dikfattori, conkpari al numero di membri tipici generati (nell’esempio
precedente avendo dueTypicalMember, la probabilità di ognuno dei quattro scenari
è data dal prodotto dik= 2fattori) dove ogni fattore è una probabilità che coincide
con lapappartenente al membro tipico se assunto, altrimenti vale 1 −pse questo,
nello scenario, non viene assunto.
Riprendendo l’esempio precedente, supponendo chemt 1 abbia come probabilità il
valorep 1 e chemt 2 abbia il valorep 2 , la probabilità dello scenario vuoto vale(1−
p1) (1−p2), quella dello scenario in cui si assume solomt 1 valep 1 ×(1−p2), quella
in cui si assume solomt 2 vale(1−p1)×p 2 ed infine l’ultimo scenariop 1 ×p 2.

I metodi che si occupano di questa traduzione sono 4, 1 principale e 3 di supporto
"privati":

def set_probability_for_each_scenario(ontology_manager):
def __generate_scenario(ontology_manager):
def __difference(scenario, typical_members_list):
def __get_typical_member(key, ontology_manager):

Per prima cosa il metodoset_probability_for_each_scenariogenera tutti gli
scenari tramite il metodo__generate_scenario(determinando l’insieme delle par-
ti), successivamente gli scenari vengono così processati: viene moltiplicata la pro-
babilità dei membri tipici assunti e non assunti (grazie a__difference) in modo

4. Caso d’uso Damiano Gianotti 41


da calcolare la probabilità per ogni scenario. Questo verrà memorizzato nell’oggetto
dedicatoScenarioovviamente gestito dall’OntologyManager.

In particolare il metodo __differenceeffettua una differenza insiemistica tra i
due insiemi: membri tipici: assunti e generati. __get_typical_member, invece,
calcola la probabilità del membro tipico non assunto nello scenario corrente grazie
alla presenza delle chiavi identificativekey: cerca all’interno dell’ontology_manager
l’oggettoTypicalMembercorrispondente a quella chiave.

Abbiamo deciso di ignorare lo scenario∅poiché è il più banale, già scartato in altri
contesti. Infatti è corretto logicamente generare tale scenario ma, verificato o meno
se sia conseguenza logica della KB, non ha molto senso dare una diagnosi del tipo:
con una probabilità X non ha niente, o, comunque, per arrivare a questo non è
necessario utilizzare tutta questa tecnologia.

### 4.6 L’inferenza

Il fileReasoningOnScenarios.pysi occupa di verificare se i sintomi in input seguano
logicamente dalla base di conoscenza, arricchita con l’aggiunta di un determinato
scenario. Questo per ogni oggettoScenariopresente. Per verificare l’implicazione
logica, in simboloA|=B, bisogna verificare che in tutti i modelli in cuiAèT rue,
ancheBè vera. Nel nostro caso dobbiamo provare cheKB∪S|=V doveS è un
determinato scenario eV è un set di formule che rappresenta i sintomi del paziente.
Possiamo dimostrare ciò grazie alla dimostrazione perrefutazione, che permette
di rispondereT rue se si dimostra l’equivalenza(KB∪S∧¬V)≡ F alse. DbN
utilizzerà proprio questa strategia, vediamo come.

def __translate_scenario(scenario, ontology_manager):
for tm in scenario.list_of_typical_members:
ontology_manager.set_as_typical_member(
tm.member_name, tm.t_class_identifier,
ontology_manager.
onto[tm.t_class_identifier.name + "1"])
def is_logical_consequence(ontology_manager,
lower_probability_bound=0, higher_probability_bound=1):

Il metodo, di supporto,translate_scenariosha il compito di tradurre ogni mem-
bro tipico presente all’interno dello scenario. Il metodois_logical_consequence
gestisce l’intera fase di verifica, opzionalmente esaminando solo gli scenari in un de-
terminato intervallo di probabilità, tramite gli argomenti facoltativi lower and higher
_bound. I risultati verranno salvati all’interno diquery_result = QueryResult().
Una volta selezionati gli scenari, questi vengono esaminati uno per volta nel seguente
modo:

1. viene creato un nuovomondo, un’universo isolato, in cui si carica l’ontologia di
    base creata in precedenza;
2. a questa vengono aggiunti i sintominegatie lo scenario corrente, tramite i
    metodiadd_symptoms_to_kb()e__translate_scenario();
3. quindi si verifica la consistenza dell’ontologia:

42 4. Caso d’uso Damiano Gianotti


- se è consistente, cioè≡T rue, alloraKB∪S6|=V e quindi lo scenario
    viene ignorato e il ciclo riparteloop.
4. In caso contrario, si salva l’oggettoScenarioall’interno diquery_result;
5. e si accumula la probabilità dello scenario, appena verificato,
nella vartotal_probability, riparte illoop;

Alla fine del ciclo si salva la probabilità totale così all’interno della variabile
query_result. L’ esecuzione quindi termina.

### 4.7 Analisi del risultato

Alla luce di quanto detto prima, vediamo ora la struttura del fileQueryResult.pye,
in particolare, delle sue operazioni.

def show_query_result(self):
.....
def create_and_show_plot(self, patient_symptoms: str, disease_cost: dict):
# Crea una figura con un secondo asse y
self.fig = make_subplots(specs=[[{"secondary_y": True}]])
# Crea l'istogramma, come asse y la probabilità degli scenari
trace1 = go.Bar(...)
# Aggiunge quest'ultimo alla figura
self.fig.add_trace(trace1)
# Crea il grafico a dispersione, come asse y il costo degli scenari €
trace2 = go.Scatter(...)
# Viene unito alla figura, specificando della presenza del diverso asse y
self.fig.add_trace(trace2, secondary_y=True)
self.fig.show()

La prima funzione ha il compito di stampare, sullo standar output, gli scenari possi-
bili. Più interessante ècreate_and_show_plot, questa, grazie all’utilizzo di Plotly
(vedi 3.3 a pag. 32), permette la realizzazione di un grafico interattivo, contente
tutte le informazioni significative e facilmente esplorabile. L’idea è stata quella di
utilizzare due grafici distinti per rappresentare la probabilità e i costi dei singoli sce-
nari, vedi la Figura 4.2. Successivamente si è pensato di unire i due grafici, poiché
accomunati dagli stessi valori sull’asse delle x, semplicemente il numero dello scena-
rio generato; il risultato è stato, all’incirca, questo è mostrato nella Figura 4.3. Per
migliorare il risultato finale sono stati aggiunti ulteriori metadati, così da rendere
il grafico il più auto-esplicativo possibile. Vale la pena menzionare la possibilità di
esportare e salvare i risultati in due formati distinti. Html per una visione dinamica,
mentre pdf per una statica.

def save_query_result(self,name=None):
if name is not None:
# self.fig.write_html(name + ".html")
self.fig.write_image(name + ".pdf")

4. Caso d’uso Damiano Gianotti 43


```
Figura 4.2: Grafico a dispersione e Istogramma separati
```
```
Figura 4.3: Grafico a dispersione e Istogramma uniti
```
44 4. Caso d’uso Damiano Gianotti


### 4.8 Il file principaleMain.py

Composto dal omonimo__name__ == '__main__'e dalla nuova funzione di sup-
portoentailed_knowledge().

def entailed_knowledge():
patient_sym = read_symptoms(ontology_manager, result=True)
result = ontology_manager.consistency(condition=True)
if not result == "The ontology is consistent":
# Ontologia inconsistente o classi inconsitenti
print(result)
ontology_manager.show_classes_iri_my()
ontology_manager.show_members_in_classes_my()
# Termina
sys.exit(5)
return patient_sym

In quest’ultima effettua la lettura dei sintomi (vedi 4.3.2) e salvato il valore di
ritorno si verifica la consistenza dellaKB. In caso negativo si effettuano delle stampe
esplicative e si termina l’esecuzione; altrimenti si ritorna i sintomi, sotto forma di
stringa.

Il'__main__'altro non è che la corretta sequenza di chiamate che permette al tool
di funzionare:

if __name__ == '__main__':
ontology_manager = OntologyManager()
build_ontology(ontology_manager)
sym: str = entailed_knowledge()
IncreasedOntology.
compute_probability_for_typical_members(ontology_manager)
IncreasedOntology.
set_probability_for_each_scenario(ontology_manager)
ontology_manager.show_scenarios()
query_result = is_logical_consequence(ontology_manager)
query_result.show_query_result()
query_result.create_and_show_plot(sym, ontology_manager.cost_dict)

in primis viene istanziata la classeOntologyManager, dopodichè viene invocato il
metodobuild_ontologytramite cui viene costruita l’ontologia ed ecco quindi la
chiamata all’attività di supporto. Calcolata le probabilità necessarie per i membri ti-
pici e per gli scenari generati, si passa alla fase di inferenza e successivamente a quella
di analisi dei risultati e generazione dei grafici. Questo conclude la simulazione.

Abbiamo trattato lo strumento nel modo più completo possibile, cercando, però,
di evitare dettagli o piccolezze trascurabili, focalizzando l’attenzione il più possibile
sugli elementi importanti e peculiari.

4. Caso d’uso Damiano Gianotti 45


# Capitolo 5

# Conclusione e sviluppi futuri

Questo breve capitolo finale serve come resoconto di tutto quello presentato fin’ora e
cerca di dare un’idea su come questo tool potrebbe essere impiegato, e sulle possibili
future evoluzioni che potrà assumere.

Il focus del progetto è il supporto alle decisioni del medico, l’affiancamento, non la
sostituzione di tale figura professionale,

Il considerare i sintomi, normalmente catalogati come atipici, per una certa malattia,
sotto una diversa luce potrebbe permettere di scoprire che, in realtà, sono indiret-
tamente collegati ad altre patologie. Per rendere l’idea si pensi ad una persona che
soffre di obesità; tendenzialmente un obeso ha problemi di metabolismo, scarsa au-
tostima e alti livelli di colesterolo. L’utilizzo di smartphone durante i pasti è stato
riscontrato essere un fattore incidente sull’aumento di peso, poiché i pazienti testati,
tendono a prestare meno attenzione a quello che mangiano e, come conseguenza,
ingeriscono maggiori quantità di cibo. Questo fatto, indirettamente collegato con
l’obesità, potrebbe essere, in alcuni soggetti, un fattore decisivo. Come conseguen-
za, questa situazione, se ben rappresentata nella KB, potrebbe esser modellata nello
strumento come uno scenario poco probabile, ma sempre possibile; la chiave è avere
sottomano lo spettro completo delle alternative.

Per quanto riguarda possibili migliorie, le strade percorribili sono numerose; a par-
tire dall’interfaccia utente: la creazione di una GUI e la semplificazione del processo
di immissione dati rappresenterebbe un notevole passo avanti per quanto riguarda
l’usabilità e abbasserebbe la curva di apprendimento del software. Pensando, invece,
all’effettivo test ed utilizzo sul campo, è necessario un lavoro di studio, modifica e
creazione di ontologie realistiche o semi-realistiche per dare una parvenza di veri-
dicità alle diagnosi prodotte, soprattutto per quanto riguarda le probabilità delle
relazioni e i costi delle diagnosi. Un altro possibile percorso potrebbe essere quello
di computare e aggiungere ulteriori metadati ai singoli scenari, come, ad esempio,
tempistiche indicative e/o un elenco di esami/visite necessarie alla verifica della
"diagnosi". Se dovessimo pensare a delle ottimizzazioni e perfezionamenti, una delle
prime idee possibili è l’utilizzodi super-classi OWLpiù significative del generico
Thing; classi comePatient,MedicalIllnessoSymptomscritte in un ontologia di
supporto.

##### 46


# Appendice A

# Esempio completo

In questa appendice mostreremo un esempio completo di utilizzo diDbN, in par-
ticolare l’esempio n.6 dell’articolo “Typicalities and Probabilities of Exceptions in
Nonmotonic Description Logics” [8] con la seguenteKB= (T,A)

TBox:

```
BipolarvDepressed
T(Depressed)v 0. 85 ¬∃hasSymptom.M oodReactivity
```
```
T(Bipolar)v 0. 70 ∃hasSymptom.M oodReactivity
```
```
T(P rostateCancerP atient)v 0. 60 ∃hasSymptom.M oodReactivity
T(P rostateCancerP atient)v 0. 80 ∃hasSymptom.N octuria
```
```
T(Depressed)v 0. 60 ∃Smart
```
ABox:
{Depressed(Greg),¬Smart(Greg)}

Set ofSymptomsV:

```
{∃hasSymptom.M oodReactivity(Greg)}
```
Set of Cost of Disease withTipicality:

```
{Bipolar: 1000, P rostateCancerP atient: 10000, Depressed: 3000}
```
Output dello strumento con la seguente ontologia; passo 1, verifica della condizione
KB∪V ≡consistente:

========== Adding a set of Symptoms to the KB ==========
Sintomo aggiunto: Greg MoodReactivity
========== Checking consistency ==========
========== The ontology is consistent ==========

passo 2, generazione scenari possibili:

##### 47


##### INIZIO SCENARIO 1

Typical(Bipolar),Greg,0.7
Probabilità scenario: 0.364
FINE SCENARIO 1

##### INIZIO SCENARIO 2

Typical(ProstateCancerPatient),Greg,0.48
Probabilità scenario: 0.144
FINE SCENARIO 2

##### INIZIO SCENARIO 3

Typical(Bipolar),Greg,0.7
Typical(ProstateCancerPatient),Greg,0.48
Probabilità scenario: 0.3356
FINE SCENARIO 3

passo 3, per ogni scenario si effettua l’inferenza, viene mostrato il primo come
esempio:

ONTOLOGIA PRIMA DELLA LETTURA DELLA QUERY
Greg member_of Depressed
Greg member_of Not(Smart)
Bipolar is_a [ontoBase.Depressed, owl.Thing]
Depressed is_a [owl.Thing]
MoodReactivity is_a [owl.Thing]
ProstateCancerPatient is_a [owl.Thing]
Nocturia is_a [owl.Thing]
Smart is_a [owl.Thing]
Not(Smart) is_a [owl.Thing]
Not(MoodReactivity) is_a [owl.Thing]
Depressed1 is_a [owl.Thing, ontoBase.r1.only ...
IntersectionDepressedDepressed1 is_a [ontoBase ...
NotDepressed1 is_a [owl.Thing, ontoBase.r1.some( ...
Bipolar1 is_a [owl.Thing, ontoBase.r1.only(Not( ...
IntersectionBipolarBipolar1 is_a [ontoBase ...
NotBipolar1 is_a [owl.Thing, ontoBase.r1.some( ...
ProstateCancerPatient1 is_a [owl.Thing, ontoBase.r1.only ...
IntersectionProstateCancerPatientProstateCancerPatient1 is_a ...
NotProstateCancerPatient1 is_a [owl.Thing, ontoBase.r1.some( ...
FINE ONTOLOGIA PRIMA DELLA LETTURA DELLA QUERY

##### LETTURA SINTOMI

Sintomo aggiunto: Greg: Not(MoodReactivity)

##### TRADUCENDO LO SCENARIO:

##### INIZIO SCENARIO

Bipolar,Greg,0.7;
ProbabilitÓ scenario: 0.364
FINE SCENARIO

48 A. Esempio completo Damiano Gianotti


Membro tipico:
Greg is_a Bipolar
Greg is_a Bipolar1
Greg is_a IntersectionBipolarBipolar1
FINE TRADUZIONE SCENARIO

##### ONTOLOGIA CON SCENARIO E SINTOMI

Bipolar is_a [ontoBase.Depressed, owl.Thing]
Depressed is_a [owl.Thing]
MoodReactivity is_a [owl.Thing]
ProstateCancerPatient is_a [owl.Thing]
Nocturia is_a [owl.Thing]
Smart is_a [owl.Thing]
Not(Smart) is_a [owl.Thing]
Not(MoodReactivity) is_a [owl.Thing]
Depressed1 is_a [owl.Thing, ontoBase.r1.only ...
IntersectionDepressedDepressed1 is_a [ontoBase ...
NotDepressed1 is_a [owl.Thing, ontoBase.r1.some( ...
Bipolar1 is_a [owl.Thing, ontoBase.r1.only(Not( ...
IntersectionBipolarBipolar1 is_a [ontoBase ...
NotBipolar1 is_a [owl.Thing, ontoBase.r1.some( ...
ProstateCancerPatient1 is_a [owl.Thing, ontoBase.r1.only ...
IntersectionProstateCancerPatientProstateCancerPatient1 is_a ...
NotProstateCancerPatient1 is_a [owl.Thing, ontoBase.r1.some( ...
Greg member_of Depressed
Greg member_of MoodReactivity
Greg member_of Not(Smart)
Greg member_of Not(MoodReactivity)
Greg member_of Bipolar1
Greg member_of IntersectionBipolarBipolar1
FINE ONTOLOGIA CON SCENARIO E SINTOMI
=====================
Il fatto segue logicamente nel seguente scenario:
INIZIO SCENARIO
Bipolar,Greg,0.7;
ProbabilitÓ scenario: 0.364
FINE SCENARIO
=====================
ONTOLOGIA PRIMA DELLA LETTURA DELLA QUERY
Greg member_of Depressed
Greg member_of Not(Smart)
Bipolar is_a [ontoBase.Depressed, owl.Thing]
Depressed is_a [owl.Thing]
MoodReactivity is_a [owl.Thing]
ProstateCancerPatient is_a [owl.Thing]
Nocturia is_a [owl.Thing]
Smart is_a [owl.Thing]

A. Esempio completo Damiano Gianotti 49


Not(Smart) is_a [owl.Thing]
Not(MoodReactivity) is_a [owl.Thing]
Depressed1 is_a [owl.Thing, ontoBase.r1.only ...
IntersectionDepressedDepressed1 is_a [ontoBase ...
NotDepressed1 is_a [owl.Thing, ontoBase.r1.some( ...
Bipolar1 is_a [owl.Thing, ontoBase.r1.only(Not( ...
IntersectionBipolarBipolar1 is_a [ontoBase ...
NotBipolar1 is_a [owl.Thing, ontoBase.r1.some( ...
ProstateCancerPatient1 is_a [owl.Thing, ontoBase.r1.only ...
IntersectionProstateCancerPatientProstateCancerPatient1 is_a ...
NotProstateCancerPatient1 is_a [owl.Thing, ontoBase.r1.some( ...
FINE ONTOLOGIA PRIMA DELLA LETTURA DELLA QUERY

##### LETTURA SINTOMI

Sintomo aggiunto: Greg: Not(MoodReactivity)

##### TRADUCENDO LO SCENARIO:

##### INIZIO SCENARIO

ProstateCancerPatient,Greg,0.48;
ProbabilitÓ scenario: 0.14400000000000002
FINE SCENARIO
Membro tipico:
Greg is_a ProstateCancerPatient
Greg is_a ProstateCancerPatient1
Greg is_a IntersectionProstateCancerPatientProstateCancerPatient1

##### FINE TRADUZIONE SCENARIO

##### ONTOLOGIA CON SCENARIO E SINTOMI

Bipolar is_a [ontoBase.Depressed, owl.Thing]
Depressed is_a [owl.Thing]
MoodReactivity is_a [owl.Thing]
ProstateCancerPatient is_a [owl.Thing]
Nocturia is_a [owl.Thing]
Smart is_a [owl.Thing]
Not(Smart) is_a [owl.Thing]
Not(MoodReactivity) is_a [owl.Thing]
Depressed1 is_a [owl.Thing, ontoBase.r1.only ...
IntersectionDepressedDepressed1 is_a [ontoBase ...
NotDepressed1 is_a [owl.Thing, ontoBase.r1.some( ...
Bipolar1 is_a [owl.Thing, ontoBase.r1.only(Not( ...
IntersectionBipolarBipolar1 is_a [ontoBase ...
NotBipolar1 is_a [owl.Thing, ontoBase.r1.some( ...
ProstateCancerPatient1 is_a [owl.Thing, ontoBase.r1.only ...
IntersectionProstateCancerPatientProstateCancerPatient1 is_a ...
NotProstateCancerPatient1 is_a [owl.Thing, ontoBase.r1.some( ...
Greg member_of Depressed
Greg member_of MoodReactivity

50 A. Esempio completo Damiano Gianotti


Greg member_of ProstateCancerPatient
Greg member_of Nocturia
Greg member_of Not(Smart)
Greg member_of Not(MoodReactivity)
Greg member_of ProstateCancerPatient1
Greg member_of IntersectionProstateCancerPatientProstateCancerPatient1

##### FINE ONTOLOGIA CON SCENARIO E SINTOMI

##### =====================

Il fatto segue logicamente nel seguente scenario:
INIZIO SCENARIO
ProstateCancerPatient,Greg,0.48;
ProbabilitÓ scenario: 0.14400000000000002
FINE SCENARIO
=====================
ONTOLOGIA PRIMA DELLA LETTURA DELLA QUERY

Greg member_of Depressed
Greg member_of Not(Smart)
Bipolar is_a [ontoBase.Depressed, owl.Thing]
Depressed is_a [owl.Thing]
MoodReactivity is_a [owl.Thing]
ProstateCancerPatient is_a [owl.Thing]
Nocturia is_a [owl.Thing]
Smart is_a [owl.Thing]
Not(Smart) is_a [owl.Thing]
Not(MoodReactivity) is_a [owl.Thing]
Depressed1 is_a [owl.Thing, ontoBase.r1.only ...
IntersectionDepressedDepressed1 is_a [ontoBase ...
NotDepressed1 is_a [owl.Thing, ontoBase.r1.some( ...
Bipolar1 is_a [owl.Thing, ontoBase.r1.only(Not( ...
IntersectionBipolarBipolar1 is_a [ontoBase ...
NotBipolar1 is_a [owl.Thing, ontoBase.r1.some( ...
ProstateCancerPatient1 is_a [owl.Thing, ontoBase.r1.only ...
IntersectionProstateCancerPatientProstateCancerPatient1 is_a ...
NotProstateCancerPatient1 is_a [owl.Thing, ontoBase.r1.some( ...
FINE ONTOLOGIA PRIMA DELLA LETTURA DELLA QUERY

##### LETTURA SINTOMI

Sintomo aggiunto: Greg: Not(MoodReactivity)

##### TRADUCENDO LO SCENARIO:

##### INIZIO SCENARIO

Bipolar,Greg,0.7; ProstateCancerPatient,Greg,0.48;
ProbabilitÓ scenario: 0.33599999999999997
FINE SCENARIO
Membro tipico:

A. Esempio completo Damiano Gianotti 51


Greg is_a Bipolar
Greg is_a Bipolar1
Greg is_a IntersectionBipolarBipolar1
Membro tipico:
Greg is_a ProstateCancerPatient
Greg is_a ProstateCancerPatient1
Greg is_a IntersectionProstateCancerPatientProstateCancerPatient1
FINE TRADUZIONE SCENARIO

##### ONTOLOGIA CON SCENARIO E SINTOMI

Bipolar is_a [ontoBase.Depressed, owl.Thing]
Depressed is_a [owl.Thing]
MoodReactivity is_a [owl.Thing]
ProstateCancerPatient is_a [owl.Thing]
Nocturia is_a [owl.Thing]
Smart is_a [owl.Thing]
Not(Smart) is_a [owl.Thing]
Not(MoodReactivity) is_a [owl.Thing]
Depressed1 is_a [owl.Thing, ontoBase.r1.only ...
IntersectionDepressedDepressed1 is_a [ontoBase ...
NotDepressed1 is_a [owl.Thing, ontoBase.r1.some( ...
Bipolar1 is_a [owl.Thing, ontoBase.r1.only(Not( ...
IntersectionBipolarBipolar1 is_a [ontoBase ...
NotBipolar1 is_a [owl.Thing, ontoBase.r1.some( ...
ProstateCancerPatient1 is_a [owl.Thing, ontoBase.r1.only ...
IntersectionProstateCancerPatientProstateCancerPatient1 is_a ...
NotProstateCancerPatient1 is_a [owl.Thing, ontoBase.r1.some( ...
Greg member_of Depressed
Greg member_of MoodReactivity
Greg member_of ProstateCancerPatient
Greg member_of Nocturia
Greg member_of Not(Smart)
Greg member_of Not(MoodReactivity)
Greg member_of Bipolar1
Greg member_of IntersectionBipolarBipolar1
Greg member_of ProstateCancerPatient1
Greg member_of IntersectionProstateCancerPatientProstateCancerPatient1
FINE ONTOLOGIA CON SCENARIO E SINTOMI

Il fatto segue logicamente nel seguente scenario:
INIZIO SCENARIO
Bipolar,Greg,0.7; ProstateCancerPatient,Greg,0.48;
ProbabilitÓ scenario: 0.33599999999999997
FINE SCENARIO

52 A. Esempio completo Damiano Gianotti


passo 4, elenco degli scenari verificati e relativo grafico:

RISULTATI DELL'INTERROGAZIONE:
SCENARI IN CUI LA QUERY SEGUE LOGICAMENTE
INIZIO SCENARIO 1
Bipolar,Greg,0.7;
Probabilità complessiva dello scenario: 0.364
FINE SCENARIO 1

##### INIZIO SCENARIO 2

ProstateCancerPatient,Greg,0.48;
Probabilità complessiva dello scenario: 0.14400000000000002
FINE SCENARIO 2

##### INIZIO SCENARIO 3

Bipolar,Greg,0.7; ProstateCancerPatient,Greg,0.48;
Probabilità complessiva dello scenario: 0.33599999999999997
FINE SCENARIO 3

##### PROBABILITÀ TOTALE: 0.844

Fine simulazione, tempo totale: 1.984983205795288 s

Analisi dei risultati

Possiamo vedere nelle figure A.1 ed A.2 una rappresentazione grafica dei risultati
finali. Iniziamo dunque descrivendo i tre assi cartesiani (due x e uno y) e il loro
significato magari non immediato. L’asse x contiene il numero della diagnosi (1,2,3)
con il suo corrispettivo istogramma e punto della funzione a dispersione, infatti ,sui
due assi y, troviamo raffigurata sia la probabilità della diagnosi (scenario)t, espressa
in percentuale ‘%‘, sia il costo stimato della stessa, espressa in€. Come rappre-
sentazione si è scelto nel primo caso un istogramma al cui interno troviamo la/le
malattia/e considerata/e come possibile spiegazione. Ogni rettangolo è identificato
con colore diverso per la variabile, per darne risalto, essendo un fattore importante
che facilità la scelta dell’eventuale iter terapeutico. Per quanto riguarda la spesa
medica si è preferito un grafico a dispersione in quanto questo criterio decisionale è
secondario alla salute del paziente e, soprattutto necessita ulteriori sviluppi.

In conclusione si fa notare al lettore la presenza della legenda riassuntiva e delle
etichette esplicative sui relativi assi, in particolare la probabilità complessiva delle
possibili diagnosi (escluso lo scenario vuoto, cioè nessuna spiegazione).

A. Esempio completo Damiano Gianotti 53


```
Figura A.1: Versione Web
```
```
Figura A.2: Versione documento
```
54 A. Esempio completo Damiano Gianotti


# Bibliografia

[1] Franz Baader et al.The Description Logic Handbook: Theory, Implementation,
and Applications. Gen. 2007.
[2] Laura Giordano et al. “ALC + T: a Preferential Extension of Description
Logics”. In:Fundam. Inform.96 (gen. 2009), pp. 341–372.doi:10.3233/FI-
2009-182.
[3] Laura Giordano et al. “Semantic characterization of rational closure: From
propositional logic to description logics”. In:Artificial Intelligence226 (mag.
2015), pp. 1–33.doi:10.1016/j.artint.2015.05.001.
[4] Plotly Technologies Inc.Collaborative data science. [Online; accessed 06-09-
2019]. 2015.url:https://plot.ly/python/.
[5] Jean-Baptiste Lamy. “Owlready: Ontology-oriented programming in Python
with automatic classification and high level constructs for biomedical onto-
logies”. In:Artificial Intelligence in Medicine80 (ago. 2017), pp. 1–18.doi:
10.1016/j.artmed.2017.07.002.
[6] Daniel Lehmann e Menachem Magidor. “What Does a Conditional Knowledge
Base Entail?” In:Artificial Intelligence 55 (mag. 1992), pp. 1–60.doi: 10.
1016/0004-3702(92)90041-U.
[7] Antonio Lieto, Gian Luca Pozzato e Alberto Valese. “COCOS: a typicality
based COncept COmbination System”. In: vol. 2214. 33rd Italian Conference
on Computational Logic, set. 2018, pp. 55–59.
[8] Gian Luca Pozzato. “Typicalities and Probabilities of Exceptions in Nonmo-
tonic Description Logics”. In:International Journal of Approximate Reasoning
107 (feb. 2019).doi:10.1016/j.ijar.2019.02.03.
[9] Bijan Parsia et al.OWL 2 Web Ontology Language Primer (Second Edition).
[http://www.w3.org/TR/2012/REC-owl2-primer-20121211/.](http://www.w3.org/TR/2012/REC-owl2-primer-20121211/.) W3C, dic. 2012.
[10] Gian Luca Pozzato. “Reasoning about surprising scenarios in description logics
of typicality”. In: Conference of the Italian Association for Artificial Intelligen-
ce, 2016, pp. 418–432.
[11] Gabriele Soriano e Gian Luca Pozzato. “Logiche descrittive della tipicalità:
sviluppo di uno strumento per il ragionamento sulle probabilità di eccezioni”.
Laurea in Informatica (triennale, DM270). UniTo, apr. 2019.

##### 55



