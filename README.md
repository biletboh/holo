# Description

This project analyzes data about holocaust and holodomor from ukrainian and polish media.


## Dependencies
Install and run [api_nlp_uk](https://github.com/arysin/api_nlp_uk)


## Run script
Go to src directory:
```
cd src/
```

Gather statistics for ukrainian sources:
```
python run.py -p istpravda.csv -l ua
```

Aggregate statistics for ukrainian sources by year:
```
python run.py -l ua -a True
```

Gather statistics for polish sources:
```
python run.py -f rpospolyta.csv -l pl
```

Aggregate statistics for ukrainian sources by year:
```
python run.py -l pl -a True
```

Create a linear graphic for a timeline.csv:
```
python run.py -p True
```

Find most frequent words:
```
python run.py -f istpravda.csv -mc True
```
