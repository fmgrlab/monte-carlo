import math
from collections import OrderedDict
import numpy as np
from app import utils
from app.objects import HwStep, Node

# coding: utf-8

# In[1]:


rates = []
rates.append(0.05)
rates.append(0.0575)
rates.append(0.0625)
rates.append(0.0675)
rates.append(0.07)

print(rates)

# In[35]:


import math
import numpy as np


### I CREATED FUNCTIONAL PROBABILITY MATRIX ###

def compute_value2(alpha, sig, dt, maturity, R):
    # precalculate constants
    N = int(maturity / dt)
    dr = sig * math.sqrt(3 * dt)
    M = -alpha * dt
    jmax = int(math.ceil(-0.1835 / M))

    row = N + 1
    column = 1 + jmax * 2

    # initialize yield curve

    # P = premium
    P = []
    P.append(1)
    for i in range(1, len(R) + 1):
        P.append(math.exp(-R[i - 1] * i * dt))
    print(P)

    # declare the matrices
    r = np.zeros((row, column))
    Q = np.zeros((row, column))
    p = [[] for y in range(row)]

    d = np.zeros((row, column))

    a = []

    # initialise first node for simplified process
    Q[0][jmax] = 1
    d[0][jmax] = math.exp(-R[0] * dt)

    # print(Q)

    graph = {'(0,0)': ['(0,0)']}

    # BEGIN# calculate tree for simplified process
    for i in range(0, N + 1):

        top_node = int(min(i, jmax))

        # create rate nodes at time step i
        for j in range(-top_node, top_node + 1):
            r[i, j + jmax] = j * dr  # adding top_node will set the first postion as zero

        # calculate probabilities - first central to top nodes

        for j in range(0, top_node + 1):

            # here I define which type of branching

            if j == jmax:
                pu = 7.0 / 6.0 + (j * j * M * M + 3 * j * M) / 2
                pm = -1.0 / 3.0 - j * j * M * M - 2 * j * M
                pd = 1.0 / 6.0 + (j * j * M * M + j * M) / 2

                # branching B
                # positive
                actual_point = '(' + str(i) + ',' + str(j) + ')'
                graph[actual_point] = ['(' + str(i + 1) + ',' + str(j - 2) + ')']
                graph[actual_point].append('(' + str(i + 1) + ',' + str(j - 1) + ')')
                graph[actual_point].append('(' + str(i + 1) + ',' + str(j) + ')')

                # branching C
                # negative
                actual_point = '(' + str(i) + ',' + str(-j) + ')'
                graph[actual_point] = ['(' + str(i + 1) + ',' + str(-j) + ')']
                graph[actual_point].append('(' + str(i + 1) + ',' + str(-j + 1) + ')')
                graph[actual_point].append('(' + str(i + 1) + ',' + str(-j + 2) + ')')

            # branching A
            else:
                pu = 1.0 / 6.0 + (j * j * M * M + j * M) / 2
                pm = 2.0 / 3.0 - (j * j * M * M)
                pd = 1.0 / 6.0 + (j * j * M * M - j * M) / 2

                # positive
                actual_point = '(' + str(i) + ',' + str(j) + ')'
                graph[actual_point] = ['(' + str(i + 1) + ',' + str(j - 1) + ')']
                graph[actual_point].append('(' + str(i + 1) + ',' + str(j) + ')')
                graph[actual_point].append('(' + str(i + 1) + ',' + str(j + 1) + ')')

                # negative
                if j != 0:
                    actual_point = '(' + str(i) + ',' + str(-j) + ')'
                    graph[actual_point] = ['(' + str(i + 1) + ',' + str(-j - 1) + ')']
                    graph[actual_point].append('(' + str(i + 1) + ',' + str(-j) + ')')
                    graph[actual_point].append('(' + str(i + 1) + ',' + str(-j + 1) + ')')

            p_temp_pos = []
            p_temp_pos.append(pd)
            p_temp_pos.append(pm)
            p_temp_pos.append(pu)

            p[i].append(p_temp_pos)

            # calculate the other probabilities by reflection
            if i > 0 and j > 0:
                p_temp_neg = p_temp_pos[::-1]
                p[i].insert(0, p_temp_neg)

        p[i] = p[i][::-1]

    # END# calculate tree for simplified process

    # sorting the graph nodes
    graph_sorted = []
    for k1 in graph:
        graph_sorted.append(k1)

    graph_sorted = sorted(graph_sorted)

    # at the origin of the tree a0 reduces to the simpler form
    a.append((-math.log(P[1])) / dt)

    # BEGIN# update state prices, find time-varying drift and displace nodes
    for i in range(1, N + 1):
        top_node = int(min(i, jmax))

        sum_a = 0
        sum_temp = 0

        # update pure security prices
        for j in range(-top_node, top_node + 1):

            list_connexions = []

            fixed = '(' + str(i) + ',' + str(j) + ')'
            print("i: %d, j: %d" % (i, j))

            # create rate nodes at time step i
            top_node_p = int(min(i - 1, jmax))
            for j_p in range(-top_node_p, top_node_p + 1):

                position = '(' + str(i - 1) + ',' + str(j_p) + ')'

                for item in graph_sorted:
                    if item == position:
                        for connect in graph[item]:
                            if connect == fixed:
                                list_connexions.append(position)

            # by here, I have the list of nodes that connect to the actual node

            u_m_d = 0
            sum_temp = 0

            for link in list_connexions:
                i_link = int(link[1])
                if link[3] == '-':
                    j_link = int(link[3:5])
                else:
                    j_link = int(link[3])

                if j == jmax:
                    u_m_d = 0
                elif j == -jmax:
                    u_m_d = 2
                elif j == 0:
                    if j_link < 0:
                        u_m_d = 0
                    elif j_link > 0:
                        u_m_d = 2
                    else:
                        u_m_d = 1
                elif j > 0 and j != jmax:
                    if (j - j_link) <= 0:
                        u_m_d = 1
                    else:
                        u_m_d = 0
                elif j < 0 and j != -jmax:
                    if (j_link - j) <= 0:
                        u_m_d = 1
                    else:
                        u_m_d = 2

                        # by here, I know which probability I should use for each node connection

                # print("i_link: %d" % i_link)
                # print("j_link: %d" % j_link)
                # print("u_m_d: %d" % u_m_d)

                print("i_link: %d, j_link: %d" % (i_link, j_link))

                if i_link == 0:
                    # print(Q[i_link][j_link+jmax])
                    # print(p[i_link][j_link][u_m_d])
                    # print(d[i_link][j_link+jmax])

                    sum_temp = sum_temp + (
                    Q[i_link][j_link + jmax] * p[i_link][j_link][u_m_d] * d[i_link][j_link + jmax])
                else:
                    top_node_temp = int(min(i_link, jmax))
                    # print(Q[i_link][j_link+jmax])
                    # print(p[i_link][j_link+top_node_temp][u_m_d])
                    # print(d[i_link][j_link+jmax])

                    sum_temp = sum_temp + (
                    Q[i_link][j_link + jmax] * p[i_link][j_link + top_node_temp][u_m_d] * d[i_link][j_link + jmax])

                    # print(sum_temp)

            Q[i][j + jmax] = sum_temp

        # find a[i]
        for j in range(-top_node, top_node + 1):
            sum_a = sum_a + Q[i][j + jmax] * math.exp(-j * dr * dt)

        a.append((math.log(sum_a) - math.log(P[i + 1])) / dt)

        # displace nodes to obtain r[i] and d[i]
        for j in range(-top_node, top_node + 1):
            r[i][j + jmax] = r[i][j + jmax] + a[i]

            d[i][j + jmax] = math.exp(-r[i][j + jmax] * dt)

        r[0][0 + jmax] = R[0]
    # PRINT PROBABILITIES
    # for element in p:
    #    for vec in element:
    #        print(vec)
    #    print(len(element))

    # PRINT GRAPH
    # l_ = []
    # for k1 in graph:
    #    l_.append(k1)

    # l_ = sorted(l_)

    # for item in l_:
    #    print(item)
    #    print(graph[item])

    for element in Q:
        print(element)

    for element in r:
        print(element)

    return graph, r, p


# In[39]:


graph, r, p = compute_value2(0.1, 0.01, 1, 3, rates)

# # Plotting the r matrix

# In[138]:


import matplotlib.pyplot as plt


# In[196]:


i = 0
matriz = []
names = []
names_set = set()

for k1 in graph:
    names.append(k1)
names = sorted(names)

for line in r:
    j = 0
    if i < len(r) - 1:
        for element in line:
            if element != 0:
                if j == 1 or j == 2 or j == 3:
                    matriz.append([(i, r[i, j]), (i + 1, r[i + 1, j + 1])])
                    matriz.append([(i, r[i, j]), (i + 1, r[i + 1, j])])
                    matriz.append([(i, r[i, j]), (i + 1, r[i + 1, j - 1])])
                    names_set.add()

                elif j == 0:
                    matriz.append([(i, r[i, j]), (i + 1, r[i + 1, j + 2])])
                    matriz.append([(i, r[i, j]), (i + 1, r[i + 1, j + 1])])
                    matriz.append([(i, r[i, j]), (i + 1, r[i + 1, j])])

                elif j == 4:
                    matriz.append([(i, r[i, j]), (i + 1, r[i + 1, j])])
                    matriz.append([(i, r[i, j]), (i + 1, r[i + 1, j - 1])])
                    matriz.append([(i, r[i, j]), (i + 1, r[i + 1, j - 2])])

            # names_set.add((i, r[i,j]))

            j += 1

    else:
        for element in line:
            # names_set.add((i, r[i,j]))

            j += 1

    i += 1
#
# names_set.remove((0,0))
# names_set.remove((1,0))
fig = plt.figure()
ax = fig.add_subplot(111)

for l in matriz:
    d = [[p[0] for p in l], [p[1] for p in l]]
    ax.plot(d[0], d[1], 'k-*')
    for p in l:
        names_set.add(p)
print(names_set)

i_names = 0
for p in names_set:
    print(names[i_names])
    ax.annotate(names[i_names], xy=p)
    i_names += 1

plt.xlim([0, 4])
plt.ylim([0, .15])
fig.set_size_inches(11, 8)
plt.show()

