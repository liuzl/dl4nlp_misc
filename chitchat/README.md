
```sh
cat ~/dl4nlp_misc/s2s/data.txt | awk -F'\t' '{print $1}' | ./mathsolver -eval | grep "nf.math"
```
