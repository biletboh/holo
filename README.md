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
python run.py -p data/istpravda.csv -l ua
```

Aggregate statistics for ukrainian sources by year:
```
python run.py -l ua -a True
```

Gather statistics for polish sources:
```
python run.py -p data/rpospolyta.csv -l pl
```

Aggregate statistics for ukrainian sources by year:
```
python run.py -l pl -a True
```
