# serratus.io

Serratus website API built using Flask.

## Quickstart

Clone the repository and preview the site locally:

```
git clone https://github.com/serratus-bio/serratus-api.git
cd serratus-api
bash run.sh
```

Go to http://localhost:5000/

## API (in development)

- `/api/summary/<sra_accession>`: raw JSON of summary file
    - Example: https://dev.serratus.io/api/summary/ERR2756788
- `/api/summary/<sra_accession>/coverage_heatmap.png`: coverage heatmap constructed from coverage cartoons.
    - Example: https://dev.serratus.io/api/summary/ERR2756788/coverage_heatmap.png
