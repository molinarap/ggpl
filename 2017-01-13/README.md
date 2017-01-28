# WORKSHOP 10

## Descrizione
Obiettivo del progetto è la costruzione di una casa a due piani data una piantina andando a utilizzare i progetti precedenti svolti con la possibilità di migliorarli

####Requisiti:
- muri interni 
- muri esterni
- porte
- finestre
- scale con righiera
- tetto

![alt text](https://github.com/molinarap/ggpl/blob/master/2017-01-13/images/model.jpg "all")

##Creazione dei livelli
Si sono andati a creare per i prima cosa dei file SVG di tutta la struttura per poi ottenere tramite il plugin *svg2lines/* i file lines con tutte le coordinate che servivano

Nella cartella params sono stati inseriti tutti i file utili:
- params/[directory]/ai/file.ai per la lavorazione della piantina
- params/[directory]/svg/file.svg per la costruzione del file lines
- params/[directory]/lines/file.lines per la lettura dei punti della struttura

I livelli sono divisi in:
- base ---> file lines per la costruzione della base della casa e del pavimento di ogni piano
- external ---> file lines per la costruzione di tutti i muri esterni della casa (senza porte e finestre)
- internal ---> file lines per la costruzione di tutti i muri interni della casa (senza porte)
- doors ---> file lines per la costruzione di tutte le porte di ogni piano sia interne che esterne. È stata creata una funziona che dati i parametri di una porta crea una maniglia andandola a posizionare precisamente a metà altezza e 3/4 di larghezza di quest'ultima
- windows ---> file lines per la costruzione di tutte le finestre di ogni piano. È stata utilizzata la libreria MATERIAL per la trasparenza dei vetri
- stair ---> file lines per la costruzione delle scale che portano dal primo al secondo piano e della righiera nel corridoio del secondo piano

#Screenshot della casa
##Esterno della casa
![alt text](https://github.com/molinarap/ggpl/blob/master/2017-01-13/images/img7.png "all")
![alt text](https://github.com/molinarap/ggpl/blob/master/2017-01-13/images/img6.png "all")
![alt text](https://github.com/molinarap/ggpl/blob/master/2017-01-13/images/img2.png "all")
![alt text](https://github.com/molinarap/ggpl/blob/master/2017-01-13/images/img3.png "all")

##Porte e finestre
![alt text](https://github.com/molinarap/ggpl/blob/master/2017-01-13/images/img5.png "all")

##Scale dal primo al secondo piano
![alt text](https://github.com/molinarap/ggpl/blob/master/2017-01-13/images/img4.png "all")
![alt text](https://github.com/molinarap/ggpl/blob/master/2017-01-13/images/img1.png "all")
