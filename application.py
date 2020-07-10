from flask import Flask, jsonify, Response
from flask_cors import CORS
from summary_parser import get_json
from summary_plotters import get_cartoon_heatmap, get_png_bytes
from werkzeug.contrib.cache import SimpleCache


app = Flask(__name__,
            static_folder = "./dist/assets",
            template_folder = "./dist")
app.config['JSON_SORT_KEYS'] = False
application = app  # for AWS EB
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

summary_json_cache = SimpleCache()
summary_heatmap_cache = SimpleCache()

def get_json_cache(accession):
    response = summary_json_cache.get(accession)
    if response is None:
        print("cached json")
        response = get_json(accession)
        summary_json_cache.set(accession, response, timeout=24 * 60 * 60)
    return response


def get_heatmap_cache(accession):
    heatmap_png = summary_heatmap_cache.get(accession)
    if heatmap_png is None:
        summary = get_json_cache(accession)
        fig = get_cartoon_heatmap(summary)
        heatmap_png = get_png_bytes(fig).getvalue()
        summary_heatmap_cache.set(accession, heatmap_png, timeout=24 * 60 * 60)
    return heatmap_png


@app.route('/api/summary/<accession>')
def summary_json(accession):
    summary = get_json_cache(accession)
    return jsonify(summary)


@app.route('/api/summary/<accession>/coverage_heatmap.png')
def plot_heatmap(accession):
    png = get_heatmap_cache(accession)
    return Response(png, mimetype='image/png')
