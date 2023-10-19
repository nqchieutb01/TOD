import json
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--synthetic_data', help='synthetic data path')
parser.add_argument('--version', help='version', default="2.1",
                    choices=["2.1", "2.2"])

args = parser.parse_args()

print(args)

data_ori = json.load(open(f'MultiWOZ_{args.version}/processed/train_data.json'))
data_pred = json.load(open(args.synthetic_data))


def remove_spe_token(text):
    text = text.split()[1:-1]
    return ' '.join(text)


res = {}
for key in data_ori:
    if key not in data_pred:
        continue
    res[f"{key}_syn"] = data_ori[key]

    for i in range(len(data_ori[key]['log'])):
        res[f"{key}_syn"]['log'][i]['bspn_gen'] = remove_spe_token(data_pred[key][i]['bspn_gen'])
        res[f"{key}_syn"]['log'][i]['dbpn_gen'] = remove_spe_token(data_pred[key][i]['dbpn_gen'])
        res[f"{key}_syn"]['log'][i]['aspn_gen'] = remove_spe_token(data_pred[key][i]['aspn_gen'])
        res[f"{key}_syn"]['log'][i]['resp_gen'] = remove_spe_token(data_pred[key][i]['resp_gen'])

with open(f"MultiWOZ_{args.version}/processed/mttod_no_aux/train_synthetic_data_t5_small.json", "w") as outfile:
    json.dump(res, outfile, indent=4)
