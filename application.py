from flask import Flask, jsonify, Response
from flask_cors import CORS
from summary_parser import get_json
from summary_plotters import get_cartoon_heatmap, get_png_bytes

app = Flask(__name__,
            static_folder = "./dist/assets",
            template_folder = "./dist")
app.config['JSON_SORT_KEYS'] = False
application = app  # for AWS EB
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/api/summary/<accession>')
def summary_json(accession):
    response = get_json(accession)
    return jsonify(response)

@app.route('/api/summary/<accession>/coverage_heatmap.png')
def plot_png(accession):
    summary = get_json(accession)
    fig = get_cartoon_heatmap(summary)
    output = get_png_bytes(fig)
    return Response(output.getvalue(), mimetype='image/png')
