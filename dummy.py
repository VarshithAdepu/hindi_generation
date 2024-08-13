from collections import defaultdict

data = {
    "Ora": "samuccaya",
    # "ki": "pariNAma",
    "evaM": "samuccaya",
    "waWA": "samuccaya",
    # "agara": "AvaSyakawApariNAma",
    # "yaxi": "AvaSyakawApariNAma",
    "wo": "AvaSyakawApariNAma",
    "nahIM wo": "AvaSyakawApariNAma",
    "kyoMki": "kAryakAraNa",
    'cUzki': "kAryakAraNa",
    'cUMki': "kAryakAraNa",
    "isIlie": "pariNAma",
    "isalie": "pariNAma",
    "awaH": "pariNAma",
    "jabaki": "viroXI_xyowaka",
    "yaxyapi": "vyaBicAra",
    "waWApi": "vyaBicAra",
    "hAlAzki": "vyaBicAra",
    "Pira BI": "vyaBicAra",
    "lekina": "viroXI",
    "kiMwu": "viroXI",
    "paraMwu": "viroXI",
    "yA": "anyawra",
    "aWavA": "anyawra",
    'isake pariNAmasvarUpa': "pariNAma",
    'isI kAraNa': 'pariNAma',
    'isake viparIwa': "viroXI",
    "viparIwa": 'viroXI',
    "isake alAvA": 'samuccaya x',
    'isake awirikwa': 'samuccaya x',
    'isake sAWa-sAWa': 'samuccaya x',
    'isake sAWa sAWa': 'samuccaya x',
    'isa kAraNa': 'pariNAma',
    'isake kAraNa': 'kAryakAraNa',
    'isake bAvajZUxa': 'vavicAra',
    'nA kevala': 'samuccaya'
}

result = defaultdict(list)

for key, value in data.items():
    result[value].append(key)

# Convert to regular dictionary
result = dict(result)

print(result)
