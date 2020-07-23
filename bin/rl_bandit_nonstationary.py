#!/usr/bin/python

import matplotlib.pyplot as plt
import numpy as np
import sys

def run(nruns=1, eps=0.1, nq=10, nsteps=10000, qstdinc=0.01, rstd=0.01):
    optPctAvgAlp = []
    RavgAvgAlp = []
    for alp in [None, 0.1]:
        optPctAvg = np.zeros(nsteps+1)
        RavgAvg = np.zeros(nsteps+1)
        for r in range(nruns):
            print('Run {}/{}'.format(r+1,nruns))
            q = [np.zeros(nq)]
            Q = [np.zeros(nq)+5]
            R = [0.0]
            Ravg = [0.0]
            optCnt = 0
            optPct = [0.0]
            if alp is None:
                Qn = np.zeros(nq)
        
            def chooseA(Qt):
                if np.random.random() < eps:
                    return np.random.randint(0, nq)
                return np.argmax(Qt)
        
            def updateQ(At, Rt):
                nonlocal Q
                Qt = Q[-1]
                Qnew = list(Qt)
                alpt = alp
                if alp is None:
                    Qn[At] = Qn[At] + 1
                    alpt = 1.0/Qn[At]
                Qnew[At] = Qt[At] + alpt*(Rt-Qt[At])
                Q.append(Qnew)
        
            def updateq():
                nonlocal q
                q.append(q[-1] + np.random.normal(scale=qstdinc, size=nq))
        
            for step in range(nsteps):
                qt = q[-1]
                Qt = Q[-1]
                At = chooseA(Qt)
                if At == np.argmax(qt):
                    optCnt = optCnt + 1
                Rt = np.random.normal(loc=qt[At], scale=rstd)
                updateQ(At, Rt)
                updateq()
                R += [Rt]
                Ravg += [Ravg[-1] + (1/(step+1))*(Rt-Ravg[-1])]
                optPct += [optCnt/(step+1)]
    
            RavgAvg = RavgAvg + (1/(r+1))*(np.array(Ravg)-RavgAvg)
            optPctAvg = optPctAvg + (1/(r+1))*(np.array(optPct)-optPctAvg)
        RavgAvgAlp += [RavgAvg]
        optPctAvgAlp += [optPctAvg]
    
    xsteps = list(range(nsteps+1))
    skip = 10
    plt.plot(xsteps[skip:], optPctAvgAlp[0][skip:], 'r-', label='sample avg')
    plt.plot(xsteps[skip:], optPctAvgAlp[1][skip:], 'b-', label='alpha=0.1')
    plt.xlabel('Steps')
    plt.ylabel('% Optimal action')
    plt.legend(loc='upper left')
    plt.grid()
    plt.savefig('optPct.png')
    plt.clf()
    plt.plot(xsteps[skip:],RavgAvgAlp[0][skip:], 'r-', label='sample avg')
    plt.plot(xsteps[skip:],RavgAvgAlp[1][skip:], 'b-', label='alpha=0.1')
    plt.xlabel('Steps')
    plt.ylabel('Average reward')
    plt.legend(loc='upper left')
    plt.grid()
    plt.savefig('R.png')

if __name__ == "__main__":
    if len(sys.argv) == 1:
        run()
    elif len(sys.argv) == 2:
        run(int(sys.argv[1]))
    elif len(sys.argv) == 3:
        run(int(sys.argv[1]), float(sys.argv[2]))
    elif len(sys.argv) == 4:
        run(int(sys.argv[1]), float(sys.argv[2]), int(sys.argv[3]))
    elif len(sys.argv) == 5:
        run(int(sys.argv[1]), float(sys.argv[2]), int(sys.argv[3]),
                float(sys.argv[4]))
    elif len(sys.argv) == 6:
        run(int(sys.argv[1]), float(sys.argv[2]), int(sys.argv[3]),
                float(sys.argv[4]), float(sys.argv[5]))
    else:
        sys.exit(1)
