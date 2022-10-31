import Footprint
import os
#from HeuristicMiner import HeuristicMiner
from FodinaMiner import FodinaMiner
from pm4py.objects.log.importer.xes import importer as xes_importer


# for a total big list, get the first/second/third element to create a new list
def get_first_list(l):
    if l == '':
        return None
    else:
        output = []
        for each_row in l:
            if each_row != '':
                output.append(each_row[0])
        return output


def get_second_list(l):
    if l == '':
        return None
    else:
        output = []
        for each_row in l:
            if len(each_row) >= 2:
                output.append(each_row[1])
        return output


def get_third_list(l):
    if l == '':
        return None
    else:
        output = []
        for each_row in l:
            if len(each_row) == 3:
                output.append(each_row[2])
        return output


def get_order_num(element, lis):
    for i in range(len(lis)):
        if lis[i] == element:
            return i
    return None


def new_double_list(list1, list2):
    if len(list1) == len(list2):
        l = []
        for i in range(len(list1)):
            l.append([list1[i], list2[i]])
        return l
    return None

s1 = 'java -jar /Users/apple/Desktop/codebase/jbpt-pm/entropia/jbpt-pm-entropia-1.6.jar -emp -rel=/Users/apple/Desktop/Training_Logs/'
e1 = ' -ret=/Users/apple/Desktop/research_project/fodina_code/that_fodina2.pnml | grep "Precision:"'
e2 = ' -ret=/Users/apple/Desktop/research_project/fodina_code/that_fodina2.pnml | grep "Recall:"'
path = '/Users/apple/Desktop/Training_Logs/'
file_name_list = os.listdir(path)
for file_name in file_name_list:
    training_path = path + str(file_name)



log1 = xes_importer.apply('/Users/apple/Desktop/Training_Logs/pdc_2020_0000001.xes')
#log2 = xes_importer.apply('/Users/apple/Desktop/Training_Logs/pdc_2020_0000001.xes')
#log3 = xes_importer.apply('/Users/apple/Desktop/Training_Logs/pdc_2020_0000111.xes')
#log4 = xes_importer.apply('/Users/apple/Desktop/Training_Logs/pdc_2020_0000011.xes')
together = [log1]
log = []
for the_log in together:
    for i in the_log:
        log.append(i)


def xes_to_list(log):
    list1 = []
    for i in range(len(log)):
        list2 = []
        for j in range(len(log[i])):
            list2.append(log[i][j]['concept:name'])
        list1.append(list2)
    return list1

logs = xes_to_list(log)

#log = [['a','a','a','a','b','a','c','b','c','d','e'], ['a','b','c','b','c','e','d','e'], ['g','a']]
#log1 = [['a','b','a','b','c'], ['a','c','d','c','d','e']]
#log2 = [['a','c','d','f','e'], ['a','d','c','f','e']]
#log3 = [['a','c','d','f','e'],['a','c','m','f','c','h','f','e'],['a','c','g','f','e'],['a','c','g','k','e']]
sample_miner = FodinaMiner(logs)
sample_miner.count_frequency()
#print(sample_miner.event_frequency)
sample_miner.normal_condition()
#print(sample_miner.frequency)
#print(sample_miner.dependency_map)
#sample_miner.find_length_two_loops()

#sample_miner.operate_unconnect_nodes()
#print(sample_miner.dependency_map)
#sample_miner.delete_first_end()
#print(sample_miner.length_two_loops)
#print(sample_miner.end_event)
#print(sample_miner.significance)
#sample_miner.binary_conflicts()
#print(sample_miner.dependency_map)
#sample_miner.operate_unconnect_nodes()

print(len(sample_miner.dependency_map))
sample_miner.mine_long_distances()
print(len(sample_miner.long_dependency))
#ld = [['t54', 't76'], ['t54', 't82'], ['t51', 't81'], ['t51', 't91']]
# change the long distance dependency map
# ld = [['t11', 't41'], ['t11', 't51'], ['t11', 't54'], ['t11', 't82'], ['t11', 't71'], ['t11', 't81'], ['t11', 't91'], ['t26', 't54'], ['t26', 't82'], ['t26', 't71'], ['t26', 't81'], ['t26', 't91'], ['t41', 't71'], ['t41', 't81'], ['t41', 't91'], ['t51', 't81'], ['t51', 't91'], ['t54', 't82'], ['t71', 't91']]
#origin_ld = [['t26', 't44'], ['t26', 't54'], ['t26', 't71'], ['t26', 't81'], ['t26', 't76'], ['t26', 't82'], ['t21', 't41'], ['t21', 't51'], ['t21', 't71'], ['t21', 't81'], ['t21', 't76'], ['t21', 't82'], ['t44', 't81'], ['t44', 't76'], ['t44', 't82'], ['t41', 't71'], ['t41', 't81'], ['t41', 't82'], ['t54', 't76'], ['t54', 't82'], ['t51', 't71'], ['t51', 't81']]
#next ld
#ld = [['t44', 't81'], ['t44', 't76'], ['t44', 't82'], ['t41', 't71'], ['t41', 't81'], ['t41', 't82'], ['t54', 't76'], ['t54', 't82'], ['t51', 't71'], ['t51', 't81']]
#sample_miner.reset_long_distance_dependency(ld)

print(len(sample_miner.long_dependency))
print('ld long dependency')
print(sample_miner.long_dependency)
print(sample_miner.dependency_map)
sample_miner.whole_part()
print("IN")
print(sample_miner.split_and_join_in)
print('OUT')
print(sample_miner.split_and_join_out)
print('FINISH')
print(sample_miner.start_event)
print(sample_miner.end_event)

from lxml import etree
the_input = sample_miner.split_and_join_in
the_output = sample_miner.split_and_join_out

output_elements = []
for i in the_output.keys():
    output_elements.append(i)

output_dict = {}
for i in the_output:
    output_dict[tuple([i])] = the_output[i]

for i in the_input.keys():
    for j in the_input[i]:
        if j in output_dict.keys():
            if tuple([i]) not in output_dict[j]:
                # change tuple to list
                output_dict[j].append(tuple([i]))
        else:
            output_dict[j] = []
            output_dict[j].append(tuple([i]))

print(output_dict)
start_event = []
end_event = []
for i in output_elements:
    m = True
    for j in output_dict.keys():
        if output_dict[j] != []:
            for j1 in j:
                if j1 == i:
                    m = False
    if m == True:
        end_event.append(i)
print(end_event)

for i in output_elements:
    m = True
    for j in output_dict.keys():
        if output_dict[j] != []:
            for k in output_dict[j]:
                for k1 in k:
                    if k1 == i:
                        m = False
    if m == True:
        start_event.append(i)

n_start_event = []
n_end_event = []
for s_event in start_event:
    if s_event not in end_event:
        n_start_event.append(s_event)

for e_event in end_event:
    if e_event not in start_event:
        n_end_event.append(e_event)

start_event = n_start_event
end_event = n_end_event

total_element = []
for i in the_input.keys():
    if i not in total_element:
        total_element.append(i)
for j in the_output.keys():
    if j not in total_element:
        total_element.append(j)

# divide into three parts: (1,1),(1,more),(more,1)
l1, l2 = [], []
for i in output_dict:
    l1.append(i)
    l2.append(output_dict[i])

one_one = []
one_more = []
more_one = []

for j in range(len(l1)):
    if l2[j] != []:
        if len(l1[j]) == 1 and len(l2[j][0]) == 1 and len(l2[j]) == 1:
            one_one.append(tuple([l1[j],l2[j]]))
        elif len(l1[j]) > 1 and len(l2[j][0]) == 1 and len(l2[j]) == 1:
            more_one.append(tuple([l1[j],l2[j]]))
        else:
            one_more.append(tuple([l1[j],l2[j]]))

# consider (more, 1) firstly
total_check_list = []
place_dict = {}
m = 1

more_one_l = []
unique_sec = []
sec_l = []
for i in more_one:
    for j in i[0]:
        l = []
        l.append(j)
        more_one_l.append((tuple(l), i[1][0]))
        sec_l.append(i[1][0][0])

for i in sec_l:
    if i not in unique_sec:
        unique_sec.append(i)

for i in unique_sec:
    for j in range(len(sec_l)):
        if sec_l[j] == i:
            l = []
            l.append(i)
            m_str = m
            new_list = new_double_list(get_first_list(total_check_list), get_second_list(total_check_list))
            place_dict[(more_one_l[j][0], tuple(l))] = m_str
            total_check_list.append([more_one_l[j][0][0], tuple(l)[0], m_str])
            m += 1

# consider the conditions of (1, more)
one_to_one = []
fir_element = []
one_more_l = []
unique_fir = []
for i in one_more:
    for j in i[1]:
        one_more_l.append((i[0], j))

for i in one_more_l:
    # has more than one element like (E1, E2)
    if len(i[1]) > 1:
        for j in i[1]:
            str_l = []
            str_l.append(j)
            m_str = m
            new_list = new_double_list(get_first_list(total_check_list), get_second_list(total_check_list))
            if [i[0][0], tuple(str_l)[0]] not in new_list:
                place_dict[(i[0], tuple(str_l))] = m_str
                total_check_list.append([i[0][0], tuple(str_l)[0], m_str])
                m = m + 1
            # elif j in get_second_list(total_check_list):
            # queue_num = get_order_num(j, get_second_list(total_check_list))
            # p_num = get_third_list(total_check_list)[queue_num]
            # place_dict[(i[0], tuple(str_l))] = p_num
            # total_check_list.append([i[0][0], tuple(str_l)[0], p_num])

    # has element saparatedly, like (E1), (E2)
    if len(i[1]) == 1:
        one_to_one.append(i)
        fir_element.append(i[0][0])

for i in fir_element:
    if i not in unique_fir:
        unique_fir.append(i)

for i in unique_fir:
    for j in range(len(fir_element)):
        if fir_element[j] == i:
            m_str = m
            new_list = new_double_list(get_first_list(total_check_list), get_second_list(total_check_list))
            if [one_to_one[j][0][0], one_to_one[j][1][0]] not in new_list:
                place_dict[(one_to_one[j][0], one_to_one[j][1])] = m_str
                total_check_list.append([one_to_one[j][0][0], one_to_one[j][1][0], m_str])
    m = m + 1

# for (1, 1) condition
sec_element = []
for i in one_one:
    print(i)
    sec_element.append(i[1][0][0])

unique_sec = []
for j in sec_element:
    if j not in unique_sec:
        unique_sec.append(j)

for i in range(len(unique_sec)):
    val = unique_sec[i]
    for j in range(len(sec_element)):
        if sec_element[j] == val:
            new_list = new_double_list(get_first_list(total_check_list), get_second_list(total_check_list))
            if [one_one[j][0][0], one_one[j][1][0][0]] not in new_list:
                m_str = m
                place_dict[(one_one[j][0], one_one[j][1][0])] = m_str
                total_check_list.append([one_one[j][0][0], one_one[j][1][0][0], m_str])
    m = m + 1

dict_list = []
for i in place_dict.keys():
    dict_list.append(place_dict[i])

dict_max = max(dict_list)

the_startest = sample_miner.start_event
the_endest = sample_miner.end_event
start_eve = []
for i in start_event:
    if i != the_startest:
        start_eve.append(i)

eles = []
for i in start_eve:
    ele = []
    for line in total_check_list:
        if line[0] == i:
            ele.append(line[2])
    eles.append(ele)

same_ones = []
for i in range(len(eles)):
    for j in range(len(eles) - i - 1):
        if eles[i] == eles[i + j + 1]:
            same_ones.append([start_eve[i], start_eve[i + j + 1]])

k = []
for line in same_ones:
    for j in line:
        k.append(j)

for eve in start_eve:
    if eve not in k:
        same_ones.append(eve)

used_list = []
tup_list = []
# input the start arcs
m = 0
m_id = 'm' + str(m)
m += 1
tup_list.append((m_id, 'p0', the_startest))
the_num = 0

total_p_list = []
for i in place_dict.keys():
    if place_dict[i] not in total_p_list:
        total_p_list.append(place_dict[i])

for i in place_dict:
    for i_first in i[0]:
        if [i_first, 'p' + str(place_dict[i])] not in used_list:
            m_id = 'm' + str(m)
            m = m + 1
            tup_list.append((m_id, i_first, 'p' + str(place_dict[i])))
            used_list.append([i_first, 'p' + str(place_dict[i])])
    for i_second in i[1]:
        if ['p' + str(place_dict[i]), i_second] not in used_list:
            m_id = 'm' + str(m)
            m = m + 1
            tup_list.append((m_id, 'p' + str(place_dict[i]), i_second))
            used_list.append(['p' + str(place_dict[i]), i_second])

p_num = dict_max + 1

for i in same_ones:
    m_id = 'm' + str(m)
    m = m + 1
    tup_list.append((m_id, the_startest, 'p' + str(p_num)))
    total_p_list.append(p_num)
    m_id = 'm' + str(m)
    m = m + 1
    if (isinstance(i, list)) == True:
        for part_i in i:
            tup_list.append((m_id, 'p' + str(p_num), part_i))
            m_id = 'm' + str(m)
            m = m + 1
        m = m - 1
        p_num += 1
    else:
        tup_list.append((m_id, 'p' + str(p_num), i))
        p_num += 1

if the_endest in end_event:
    m_id = 'm' + str(m)
    tup_list.append((m_id, the_endest, 'p' + str(p_num)))
if the_endest not in end_event:
    p_num -= 1

total_p_list.append(p_num)

# initial input for XML
pnml = etree.Element('pnml')
net = etree.SubElement(pnml, 'net')
name = etree.SubElement(net, 'name')
wr = etree.SubElement(name, 'text')
wr.text = 'model'
page = etree.SubElement(net, 'page', {'id': 'page0'})

# add initial p0 for XML
place_ini = etree.SubElement(page, 'place', {'id': 'p0'})
name = etree.SubElement(place_ini, 'name')
wr = etree.SubElement(name, 'text')
wr.text = 'p0'
ini_marking = etree.SubElement(place_ini, 'initialMarking')
ini_test = etree.SubElement(ini_marking, 'text')
ini_test.text = str(1)

# add other places for XML
for i in total_p_list:
    point_mark = 'p' + str(i)
    place = etree.SubElement(page, 'place', {'id': point_mark})
    name = etree.SubElement(place, 'name')
    wr = etree.SubElement(name, 'text')
    wr.text = point_mark

# add end places for XML
# point_end_mark = 'p' + str(len(place_dict)+1)
# place_end = etree.SubElement(page, 'place', {'id':point_end_mark})
# name = etree.SubElement(place_end, 'name')
# wr = etree.SubElement(name, 'text')
# wr.text = point_end_mark

# add transitions for XML
for i in total_element:
    trans = etree.SubElement(page, 'transition', {'id': i})
    name = etree.SubElement(trans, 'name')
    wr = etree.SubElement(name, 'text')
    wr.text = i

# add initial arcs for XML
for i in tup_list:
    arc = etree.SubElement(page, 'arc', {'id': i[0], 'source': i[1], 'target': i[2]})

# arc = etree.SubElement(page, 'arc', {})

doc = etree.ElementTree(pnml)
doc.write(open('that_fodina2.pnml', 'wb'), encoding='utf-8', pretty_print=True)
print(tup_list)

import subprocess
import re
sub1 = subprocess.Popen('java -jar /Users/apple/Desktop/codebase/jbpt-pm/entropia/jbpt-pm-entropia-1.6.jar -emp -rel=/Users/apple/Desktop/Test_Logs/pdc_2020_0000111.xes -ret=/Users/apple/Desktop/research_project/fodina_code/that_fodina2.pnml | grep "Precision:"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
m = sub1.communicate()
m1 = re.sub(r'\D', '', m[0])
precision = int(m1[0:6])/100000
print(precision)

sub2 = subprocess.Popen('java -jar /Users/apple/Desktop/codebase/jbpt-pm/entropia/jbpt-pm-entropia-1.6.jar -emr -rel=/Users/apple/Desktop/Test_Logs/pdc_2020_0000111.xes -ret=/Users/apple/Desktop/research_project/fodina_code/that_fodina2.pnml | grep "Recall:"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
n = sub2.communicate()
n1 = re.sub(r'\D', '', n[0])
recall = int(n1[0:6])/100000
print(recall)

