import requests
import argparse
import json

def run_margot(text):
  data = {'text': text}
  headers = {'content-type': 'application/json'}
  response = requests.post('https://penelope.vub.be/margot-api/track-arguments', json=data, headers=headers)
  return response.text

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_file')
    parser.add_argument('-o', '--output_file')

    args = parser.parse_args()

    with open(f'{args.input_file}', 'r') as f, open(args.output_file, 'w') as o:
        count = 0
        for line in f:
            line_json = json.loads(line)
            text = line_json['review']

            try:
                margot_json = json.loads(run_margot(text))
                line_json['margot'] = margot_json['document']

                json.dump(line_json, o)
                o.write('\n')
            except:
                print(text)

            print(count)
            count += 1



if __name__ == '__main__':
    main()