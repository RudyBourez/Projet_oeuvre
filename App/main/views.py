from django.shortcuts import render
import pandas as pd
import numpy as np
import json

def listing(request):
    df = pd.DataFrame(np.array([["0000000", "A", 3], ["0000001", "B", 6], ["0000002", "C", 9]]),
                   columns=['Matricule', 'Libellé', 'Nb_virements'])
    json_records = df.to_json(orient ='records')
    data = []
    data = json.loads(json_records)
    context = {'d': data}
    return render(request, 'listing.html', context)
