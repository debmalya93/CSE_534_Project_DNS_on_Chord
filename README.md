# DNS_on_Chord

# Contributors
1. Debmalya Kundu
2. Dinker Goel
3. Dheeraj Nuthalapati

# Guide
1. Install Anaconda
2. conda create -n venv python=3.6
3. conda activate venv
4. pip install certifi==2020.11.8 cffi==1.14.4 joblib==0.17.0 numpy==1.19.4 pycparser==2.20 pydistalgo==1.0.12 threadpoolctl==2.1.0 wincertstore==0.2
5. python -m da --message-buffer-size 1000000 -F output --logfile --logfilename test.log src/chord_resolver/main.da

