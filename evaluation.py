import os, glob
import time


def eval_sis():

    files = glob.glob('./graphs_sis/graphfile*0.txt')
    files = sorted(files, key=lambda x: int(x.split('_')[-1].replace('.txt', '')))

    for juliacode in ['sis_reject', 'sis_baseline']:
        for graphfile in files:
            name = 'EXPSIS_' + graphfile.split('/')[-1]
            julianame = '_baseline.txt' if 'base' in juliacode else '_rejection.txt'
            julianame = name.replace('.txt', julianame)

            try:
                os.system("julia {}.jl 10 {} {}".format(juliacode, graphfile, julianame))
                os.system("pkill -9 julia")
            except:
                pass

            time.sleep(.1)


def eval_voter():
    files = glob.glob('./graphs_voter/graphfile*0.txt')
    files = sorted(files, key=lambda x: int(x.split('_')[-1].replace('.txt', '')))

    for juliacode in ['voter_reject', 'voter_baseline']:
        for graphfile in files:
            name = 'EXPVoter_' + graphfile.split('/')[-1]
            julianame = '_baseline.txt' if 'base' in juliacode else '_rejection.txt'
            julianame = name.replace('.txt', julianame)

            try:
                os.system("julia {}.jl 10 {} {}".format(juliacode, graphfile, julianame))
                os.system("pkill -9 julia")
            except:
                pass

            time.sleep(.1)


def eval_neural():
    files = glob.glob('./graphs_neural/graphfile*0.txt')
    files = sorted(files, key=lambda x: int(x.split('_')[-1].replace('.txt', '')))

    for juliacode in ['expTPPneural_reject', 'expTPPneural_baseline']:
        for graphfile in files:
            name = 'EXPNeural_' + graphfile.split('/')[-1]
            julianame = '_baseline.txt' if 'base' in juliacode else '_rejection.txt'
            julianame = name.replace('.txt', julianame)

            try:
                os.system("julia {}.jl 10 {} {}".format(juliacode, graphfile, julianame))
                os.system("pkill -9 julia")
            except:
                pass

            time.sleep(.1)


os.system('julia setup.jl')
time.sleep(0.1)

eval_sis()
eval_voter()
eval_neural()