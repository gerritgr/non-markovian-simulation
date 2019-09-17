import os, glob
import time

files = glob.glob('./rust-configuration-model/model/graphfile*0.txt')

files = sorted(files, key=lambda x: int(x.split('_')[-1].replace('.txt','')))

files = [files[0]] + files # this is to avaoid performance artefacts, julia needs some time to get peak performance

def exp1():
    for juliacode in ['exp1_reject', 'exp1_baseline']:
        for graphfile in files:


            if "100000" in graphfile:
                continue

            #if juliacode != "exp1_reject":
            #    continue

            if "3.0"  in graphfile:
                continue

            name = 'EXP1_'+ graphfile.split('/')[-1]
            #print(graphfile)
            #print(name)

            julianame = '_baseline.txt' if 'base' in juliacode else '_rejection.txt'
            julianame = name.replace('.txt', julianame)

            try:
                os.system("julia {}.jl 5 {} {}".format(juliacode, graphfile,julianame))
                print('os.system("julia {}.jl 5 {} {}")'.format(juliacode, graphfile,julianame))
                os.system("pkill -9 julia")
            except:
                pass

            time.sleep(.1)


def exp2():
    files = glob.glob('./rust-configuration-model/modelV/graphfile*0.txt')
    files = sorted(files, key=lambda x: int(x.split('_')[-1].replace('.txt', '')))
    files = [files[0]] + files  # this is to avaoid performance artefacts, julia needs some time to get peak performance



    for juliacode in ['exp2_reject', 'exp2_baseline']:
        for graphfile in files:


            if "100000"  in graphfile:
                continue

            if "3.0" in graphfile:
                continue
            #if juliacode == "exp2_reject":
            #    continue

            #if "2.5" not in graphfile:
            #    continue


            #if "1000000" not in graphfile or juliacode != "exp2_reject" or "3.0" in graphfile:
            #    continue

            name = 'EXP2e_'+ graphfile.split('/')[-1]
            #print(graphfile)
            #print(name)

            julianame = '_baseline.txt' if 'base' in juliacode else '_rejection.txt'
            julianame = name.replace('.txt', julianame)

            try:
                print('os.system("julia {}.jl 2 {} {}")'.format(juliacode, graphfile, julianame))
                os.system("julia {}.jl 8 {} {}".format(juliacode, graphfile,julianame))
                os.system("pkill -9 julia")
            except:
                pass

            time.sleep(.1)


def exp3():
    files = glob.glob('./rust-configuration-model/modelV/graphfile*0.txt')
    files = sorted(files, key=lambda x: int(x.split('_')[-1].replace('.txt', '')))
    files = [files[0]] + files  # this is to avaoid performance artefacts, julia needs some time to get peak performance

    for juliacode in ['exp3_nmga']:#, 'exp3_reject', 'exp3_baseline']:
        for graphfile in files:

            if "100000"  in graphfile:
                continue

            if "3.0"  in graphfile:
                continue

            name = 'EXP3x_'+ graphfile.split('/')[-1]
            #print(graphfile)
            #print(name)

            julianame = '_baseline.txt'
            if juliacode == 'exp3_reject':
                julianame = '_rejection.txt'
            if juliacode == 'exp3_nmga':
                julianame = '_nmga.txt'


            julianame = name.replace('.txt', julianame)


            try:
                print('os.system("julia {}.jl 3.0 {} {}")'.format(juliacode, graphfile, julianame))
                os.system("julia {}.jl 3.0 {} {}".format(juliacode, graphfile,julianame))
                os.system("pkill -9 julia")
            except:
                pass

            time.sleep(.1)


def exp4():
    for juliacode in ['exp4_nmga']:#, 'exp4_reject', 'exp4_baseline']:
        for graphfile in files:


            if "10000." not in graphfile:
                continue


            if "2.0" not  in graphfile:
                continue

            name = 'EXP4x_'+ graphfile.split('/')[-1]
            #print(graphfile)
            #print(name)

            julianame = '_baseline.txt'
            if juliacode == 'exp4_reject':
                julianame = '_rejection.txt'
            if juliacode == 'exp4_nmga':
                julianame = '_nmga.txt'


            julianame = name.replace('.txt', julianame)

            try:
                os.system("julia {}.jl 5.0 {} {}".format(juliacode, graphfile,julianame))
                print('os.system("julia {}.jl 5.0 {} {}")'.format(juliacode, graphfile,julianame))
                os.system("pkill -9 julia")
            except:
                pass

            time.sleep(.1)




exp4()


#exp1()

x=x/0


#todo
# add 1m to exp1
# exp2


# def exp1():
#     for graphfile in files:
#         name = 'EXP1_'+ graphfile.split('/')[-1]
#         print(graphfile)
#         print(name)
#         name_reject = name.replace('.txt','_reject.txt')
#         name_baseline = name.replace('.txt', '_baseline.txt')
#
#         try:
#             os.system("julia exp1_reject.jl 5 {} {}".format(graphfile,name_reject))
#         except:
#             pass
#
#         time.sleep(1)
#
#         try:
#             os.system("julia exp1_baseline.jl 5 {} {}".format(graphfile, name_baseline))
#         except:
#             pass
#
#         time.sleep(1)


x=x/0
os.system("julia exp1_reject.jl 5 ./rust-configuration-model/model/graphfile_2.0_100.txt EXP1_graphfile_2.0_100_rejection.txt")
os.system("julia exp1_reject.jl 5 ./rust-configuration-model/model/graphfile_2.0_100.txt EXP1_graphfile_2.0_100_rejection.txt")
os.system("julia exp1_reject.jl 5 ./rust-configuration-model/model/graphfile_3.0_100.txt EXP1_graphfile_3.0_100_rejection.txt")
os.system("julia exp1_reject.jl 5 ./rust-configuration-model/model/graphfile_2.0_1000.txt EXP1_graphfile_2.0_1000_rejection.txt")
os.system("julia exp1_reject.jl 5 ./rust-configuration-model/model/graphfile_3.0_1000.txt EXP1_graphfile_3.0_1000_rejection.txt")
os.system("julia exp1_reject.jl 5 ./rust-configuration-model/model/graphfile_3.0_10000.txt EXP1_graphfile_3.0_10000_rejection.txt")
os.system("julia exp1_reject.jl 5 ./rust-configuration-model/model/graphfile_2.0_10000.txt EXP1_graphfile_2.0_10000_rejection.txt")


os.system("julia exp1_baseline.jl 5 ./rust-configuration-model/model/graphfile_2.0_100.txt EXP1_graphfile_2.0_100_baseline.txt")
os.system("julia exp1_baseline.jl 5 ./rust-configuration-model/model/graphfile_2.0_100.txt EXP1_graphfile_2.0_100_baseline.txt")
os.system("julia exp1_baseline.jl 5 ./rust-configuration-model/model/graphfile_3.0_100.txt EXP1_graphfile_3.0_100_baseline.txt")
os.system("julia exp1_baseline.jl 5 ./rust-configuration-model/model/graphfile_2.0_1000.txt EXP1_graphfile_2.0_1000_baseline.txt")
os.system("julia exp1_baseline.jl 5 ./rust-configuration-model/model/graphfile_3.0_1000.txt EXP1_graphfile_3.0_1000_baseline.txt")
os.system("julia exp1_baseline.jl 5 ./rust-configuration-model/model/graphfile_3.0_10000.txt EXP1_graphfile_3.0_10000_baseline.txt")
os.system("julia exp1_baseline.jl 5 ./rust-configuration-model/model/graphfile_2.0_10000.txt EXP1_graphfile_2.0_10000_baseline.txt")


os.system("julia exp2_reject.jl 50 ./rust-configuration-model/model/graphfile_2.0_100.txt EXP2_graphfile_2.0_100_rejection.txt")
os.system("julia exp2_reject.jl 50 ./rust-configuration-model/model/graphfile_2.0_100.txt EXP2_graphfile_2.0_100_rejection.txt")
os.system("julia exp2_reject.jl 50 ./rust-configuration-model/model/graphfile_3.0_100.txt EXP2_graphfile_3.0_100_rejection.txt")
os.system("julia exp2_reject.jl 50 ./rust-configuration-model/model/graphfile_2.0_1000.txt EXP2_graphfile_2.0_1000_rejection.txt")
os.system("julia exp2_reject.jl 50 ./rust-configuration-model/model/graphfile_3.0_1000.txt EXP2_graphfile_3.0_1000_rejection.txt")
os.system("julia exp2_reject.jl 50 ./rust-configuration-model/model/graphfile_3.0_10000.txt EXP2_graphfile_3.0_10000_rejection.txt")
os.system("julia exp2_reject.jl 50 ./rust-configuration-model/model/graphfile_2.0_10000.txt EXP2_graphfile_2.0_10000_rejection.txt")


os.system("julia exp2_baseline.jl 50 ./rust-configuration-model/model/graphfile_2.0_100.txt EXP2_graphfile_2.0_100_baseline.txt")
os.system("julia exp2_baseline.jl 50 ./rust-configuration-model/model/graphfile_2.0_100.txt EXP2_graphfile_2.0_100_baseline.txt")
os.system("julia exp2_baseline.jl 50 ./rust-configuration-model/model/graphfile_3.0_100.txt EXP2_graphfile_3.0_100_baseline.txt")
os.system("julia exp2_baseline.jl 50 ./rust-configuration-model/model/graphfile_2.0_1000.txt EXP2_graphfile_2.0_1000_baseline.txt")
os.system("julia exp2_baseline.jl 50 ./rust-configuration-model/model/graphfile_3.0_1000.txt EXP2_graphfile_3.0_1000_baseline.txt")



os.system("julia exp1_reject.jl 5 ./rust-configuration-model/model/graphfile_3.0_100000.txt EXP1_graphfile_3.0_100000_rejection.txt")
os.system("julia exp1_reject.jl 5 ./rust-configuration-model/model/graphfile_2.0_100000.txt EXP1_graphfile_2.0_100000_rejection.txt")
os.system("julia exp1_reject.jl 5 ./rust-configuration-model/model/graphfile_2.0_1000000.txt EXP1_graphfile_2.0_1000000_rejection.txt")
os.system("julia exp1_reject.jl 5 ./rust-configuration-model/model/graphfile_3.0_1000000.txt EXP1_graphfile_3.0_1000000_rejection.txt")


os.system("julia exp1_baseline.jl 5 ./rust-configuration-model/model/graphfile_3.0_100000.txt EXP1_graphfile_3.0_100000_baseline.txt")
os.system("julia exp1_baseline.jl 5 ./rust-configuration-model/model/graphfile_2.0_100000.txt EXP1_graphfile_2.0_100000_baseline.txt")
os.system("julia exp1_baseline.jl 5 ./rust-configuration-model/model/graphfile_2.0_1000000.txt EXP1_graphfile_2.0_1000000_baseline.txt")
os.system("julia exp1_baseline.jl 5 ./rust-configuration-model/model/graphfile_3.0_1000000.txt EXP1_graphfile_3.0_1000000_baseline.txt")


os.system("julia exp2_reject.jl 50 ./rust-configuration-model/model/graphfile_3.0_100000.txt EXP2_graphfile_3.0_100000_rejection.txt")
os.system("julia exp2_reject.jl 50 ./rust-configuration-model/model/graphfile_2.0_100000.txt EXP2_graphfile_2.0_100000_rejection.txt")
os.system("julia exp2_reject.jl 50 ./rust-configuration-model/model/graphfile_2.0_1000000.txt EXP2_graphfile_2.0_1000000_rejection.txt")
os.system("julia exp2_reject.jl 50 ./rust-configuration-model/model/graphfile_3.0_1000000.txt EXP2_graphfile_3.0_1000000_rejection.txt")


os.system("julia exp2_baseline.jl 50 ./rust-configuration-model/model/graphfile_3.0_10000.txt EXP2_graphfile_3.0_10000_baseline.txt")
os.system("julia exp2_baseline.jl 50 ./rust-configuration-model/model/graphfile_2.0_10000.txt EXP2_graphfile_2.0_10000_baseline.txt")
os.system("julia exp2_baseline.jl 50 ./rust-configuration-model/model/graphfile_3.0_100000.txt EXP2_graphfile_3.0_100000_baseline.txt")
os.system("julia exp2_baseline.jl 50 ./rust-configuration-model/model/graphfile_2.0_100000.txt EXP2_graphfile_2.0_100000_baseline.txt")
os.system("julia exp2_baseline.jl 50 ./rust-configuration-model/model/graphfile_2.0_1000000.txt EXP2_graphfile_2.0_1000000_baseline.txt")
os.system("julia exp2_baseline.jl 50 ./rust-configuration-model/model/graphfile_3.0_1000000.txt EXP2_graphfile_3.0_1000000_baseline.txt")