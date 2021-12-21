# IMDb Dataset Gathering

The first step is to run `python get_imdb_data.py -c config.json -o output.json` or pass whatever output file name in the -o field. This will generate an json file
with the same style as `output.json`.

Next, run `python get_margot_values.py -i output.json -o margot_output.json` or pass whatever output file name in the -o filed. This will generate a json file
with the same style as `margot.json` in the main folder. Warning, this will take a long time as each entry will take approximately 30-45 seconds to run.
