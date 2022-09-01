from flask import Flask, jsonify
from flask import request
import json

app = Flask(__name__)

seen_strings = {}


@app.route('/')
def root():
    return '''
    <pre>
    Welcome to the Stringinator 3000 for all of your string manipulation needs.

    GET / - You're already here!
    POST /stringinate - Get all of the info you've ever wanted about a string. Takes JSON of the following form: {"input":"your-string-goes-here"}
    GET /stats - Get statistics about all strings the server has seen, including the longest and most popular strings.
    </pre>
    '''.strip()


@app.route('/stringinate', methods=['POST'])
def Poststringinate():
    input = ''
    input = json.loads(request.data)['input']
    print(input)
    if input not in seen_strings.keys():
        seen_strings[input] = 1
        print(seen_strings)
    else:
        seen_strings[input] += 1
    resp={"input":input,"length":len(input),"number of occurrences":seen_strings[input]}
    return json.dumps(resp)


@app.route('/stringinate', methods=['GET'])
def Getstringinate():
    input = request.args.get('input', '')
    if input in seen_strings.keys():
        resp = {"input": input, "status": "Found"}
        return json.dumps(resp)
    else:
        resp = {"input": input, "status": "Not Found"}
        return json.dumps(resp)


@app.route('/stats')
def string_stats():
    most_popular_val=0
    most_popular_str =""
    longest_input_received=""
    for key in seen_strings:
        if len(key) > len(longest_input_received):
            longest_input_received=key
        if seen_strings[key] > most_popular_val:
            most_popular_str=key
    seen_strings["most_popular_str"]=  most_popular_str
    seen_strings["longest_input_received"]=longest_input_received
    return json.dumps(seen_strings)
