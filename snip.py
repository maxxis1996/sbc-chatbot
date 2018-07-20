import io
import os
import json
from snips_nlu import load_resources
from snips_nlu import SnipsNLUEngine
from snips_nlu.default_configs import CONFIG_EN

BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_resources(u"es")

engine = SnipsNLUEngine(config=CONFIG_EN)
with io.open("dataset.json") as f:
    dataset = json.load(f)
engine.fit(dataset)
parsing = engine.parse(u"Hey, li")
print(json.dumps(parsing, indent=2))