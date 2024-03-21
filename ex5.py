import json

json_text = {"messages": [{"message":"This is the first message","timestamp":"2021-06-04 16:40:53"}, {"message": "And this is a second message", "timestamp": "2021-06-04 16:41:01"}]}
obj_json = json.dumps(json_text)

data = json.loads(obj_json)

print(data["messages"][1]['message'])



