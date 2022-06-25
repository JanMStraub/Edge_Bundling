import json

# Opening JSON file
with open("extract_metrics/miserables.json") as json_file:
	miserables = json.load(json_file)

connections = {}

for entry in miserables["links"][:10]:
    if entry["source"] in connections.keys():
        connections[entry["source"]] = entry["target"]
    print(entry)

for entry in connections:
    print(entry)

print(connections)