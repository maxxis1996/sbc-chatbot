import io
import json
import snips_nlu
from snips_nlu import SnipsNLUEngine
from snips_nlu.default_configs import CONFIG_ES


with io.open('dataset.json') as file:
    dataset = json.load(file)
snips_nlu.load_resources("es")
engine = SnipsNLUEngine()
engine.fit(dataset)
parsing = engine.parse(u"Informacion de animales en kitchwua y ingles")
print(json.dumps(parsing, indent=2))
temp=json.dump(parsing, indent=2)