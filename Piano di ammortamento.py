#Piano di ammortamento
#importazione librerie
import numpy as np
import math
import matplotlib.pyplot as plt
import pandas as pd
from tabulate import tabulate

#selezionare: stile di ammortamento , se calcolare in anni o rate , il numero di anni o rate  
stile_ammortamento='francese'
anni_o_rate='anni'
n=30

def ammortamento(debito,j_pagamenti,tasso_annuo,):
    if anni_o_rate=='rate':
        rate=math.trunc(j_pagamenti*n/j_pagamenti)
    elif anni_o_rate=='anni':
        rate=math.trunc(j_pagamenti*n)

    tempo= np.arange(1,rate+1)
    tasso_equivalente=(1+tasso_annuo)**(1/j_pagamenti)-1
    
    #Colonne del piano : R,QC,I,DR,DE
    if stile_ammortamento=='francese':
        R= np.full(rate,debito/((1-(1+tasso_equivalente)**-rate)/tasso_equivalente))
        QC= R*((1+tasso_equivalente)**-(rate-tempo+1))
        I=  R*((1-(1+tasso_equivalente)**-(rate-tempo+1)))
        DR= R*((1-(1+tasso_equivalente)**(-rate+tempo))/tasso_equivalente)
        DE= debito-DR
    elif stile_ammortamento=='italiano':
        QC= np.full(rate,(debito/rate))
        DR= ((rate-tempo)/rate)*debito
        DE= tempo*(debito/rate)
        I= (rate-tempo+1)*(debito/rate)*tasso_equivalente
        R=  QC+I
    #Tabella
    T=pd.DataFrame(zip(tempo,R,QC,I,DR,DE),
    columns=["N°Rate","Rata","Quote Capitale","Interessi","Debito Residuo","Debito Estinto"])
    
    #Restituisci tabella
    print(tabulate(T,headers="keys",tablefmt="fancy_grid",floatfmt=[".0f", ".2f", ".2f", ".2f", ".2f", ".2f"],showindex="never"))
    debito_finale=(debito+sum(I)).round(2)
    totale_interessi=(sum(I)).round(2)
    incidenza_int= ((totale_interessi/debito)*100).round(2)
    #Grafico
    fig, ax=plt.subplots()
    ax.hlines(y=debito,xmin=0,xmax=rate,color='black',label='debito iniziale=' + str(debito))
    ax.plot(tempo,np.cumsum(I),color='firebrick',linestyle='--',label='Interessi=' + str(totale_interessi))
    ax.hlines(y=debito+sum(I).round(2),xmin=0,xmax=rate,color='blue',label='debito finale=' + str(debito_finale))
    ax.set_facecolor('floralwhite')
    ax.set_xlabel('N° Rate',fontweight='bold',fontsize=14)
    ax.grid(linestyle='--',linewidth=0.5)
    ax.plot([], [], ' ', label='incidenza interessi/debito =' + str(incidenza_int)+'%')
    ax.legend(ncol=2, loc='center', bbox_to_anchor=(0.55,1.085))
    plt.show()            
ammortamento(10000,1,0.03)                  


