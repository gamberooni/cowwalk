# cowwalk

Take your cow for a walk! When you specify how long your cow should finish the walk, it acts as a timer. Otherwise, it simply just shows the elapsed time.

## How to use
1. git clone this project
2. Create a virtual enviroment and do `pip install -r requirements.txt`
3. Activate the virtual environment:
4. If using `cowwalk` as a timer (e.g. 1 minute), do `python /path/to/cowwalk/main.py --m=1`. Turn up your audio for a surprise at the end of the timer! If using it just to show elapsed time, do `python /path/to/cowwalk/main.py`.

## Example Output
### Timer
```
     _______________________________
     < Ending walk in 0:56 minutes >
     -------------------------------
            ^__^   /
    _______/(oo)  /
\/\(       /(__)
    ||w----||
    |\     |\
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```

### Elapsed Time
```
       ___________________________
       < Walked for 0:08 minutes >
       ---------------------------
            ^__^   /
    _______/(oo)  /
/\/(       /(__)
    ||w----||
    /|     /|
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```