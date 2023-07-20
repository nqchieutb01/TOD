# TOD
```
{
  "dial_id": "mul2499",
  "turn_num": 0,
  "user": "i am looking for a cheap restaurant in the center of the city .",
  "bspn": "[restaurant] pricerange cheap area centre",
  "bsdx": "[restaurant] pricerange area",
  "aspn": "[restaurant] [request] food",
  "bspn_reform": "[restaurant] pricerange is cheap , area is centre",
  "bsdx_reform": "[restaurant] pricerange , area",
  "aspn_reform": "[restaurant] [request] food",
  "resp": "do you have any specific type of food you would like ?",
  "dspn_gen": "[restaurant]",
  "dspn": "[restaurant]",
  "db": "[db_3]",
  "pointer": "restaurant: >3; ",
  "turn_domain": [
    "[restaurant]"
  ],
 "resp_gen": "there are [value_choice] restaurant -s that meet your criteria . do you have a food type preference ?",
  "bspn_gen": "[restaurant] pricerange cheap area centre",
  "aspn_gen": ""
}
{
  "dial_id": "mul2499",
  "turn_num": 1,
  "user": "no , i am not picky as long as the price -s are low .",
  "bspn": "[restaurant] pricerange cheap area centre",
  "bsdx": "[restaurant] pricerange area",
  "aspn": "[restaurant] [inform] price name food area [offerbook]",
  "bspn_reform": "[restaurant] pricerange is cheap , area is centre",
  "bsdx_reform": "[restaurant] pricerange , area",
  "aspn_reform": "[restaurant] [inform] price name food area [offerbook]",
  "resp": "there is a [value_price] [value_food] restaurant called the [value_name] located in the [value_area] of town . would you like to book a table ?",
  "dspn_gen": "[restaurant]",
  "dspn": "[restaurant]",
  "db": "[db_3]",
  "pointer": "restaurant: >3; ",
  "turn_domain": [
    "[restaurant]"
  ],
  "resp_gen": "[value_name] is a [value_food] restaurant in the [value_area] . would you like me to book a table for you ?",
  "bspn_gen": "[restaurant] pricerange cheap area centre food dontcare",
  "aspn_gen": ""
}
```
Multiwoz 2.1
```
dst_small:           Join: 53.80 F1: 91.79 Acc: 97.05
report in paper:     Join: 53.33 F1: 91.68

dst_small_reinforce: Join: 53.19 F1: 91.61 Acc: 96.95
report in paper:     Join: 54.97 F1: 92.01

nlg_small:         : inform: 85.49 success: 75.88 BLEU: 18.99 combine: 99.67
Report in paper:     inform: 88.90 success: 81.40 BLEU: 18.73 combine: 103.88

nlg_small_reinforce: inform: 98.50 success: 61.76 BLEU: 07.58 combine: 87.71
Report in paper:     inform: 97.00 success: 87.40 BLEU: 17.12 combine: 109.32

```

