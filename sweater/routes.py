from flask import render_template, request, redirect, url_for
from sweater import app
from sweater.main import graph
import json


@app.route('/results', methods=['GET', 'POST'])
def results():
    data = json.load(open('options/response.json', ))['response']
    print(data)
    return render_template("results.html", data=data)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = request.form.to_dict()
    if 'algorithm' in form:
        sorts = {
            'dijkstra': graph.dijkstra.run,
            'floyd': graph.floyd.run,
            'johnson': graph.dijkstra.run,
            'bellman': graph.bellman.run
        }
        sorts[form['algorithm']](int(form['source']), int(form['target']))

        # FIXME: since the path search in each algorithm is unique,
        #        it is difficult to come up with a universal algorithm
        #        and I display the path on the screen using the dijkstra method.
        #        Need to figure out how to make another implementation

        graph.network.restore_path()
        _, parent = graph.dijkstra.dijkstra_algorithm(graph.dijkstra.matrix.weights, int(form['source']))
        graph.draw_path(parent, int(form['target']), int(form['source']))
        graph.draw_graph()
        print("HELLLO")
        return redirect(url_for('results'))

    return render_template("output.html")
