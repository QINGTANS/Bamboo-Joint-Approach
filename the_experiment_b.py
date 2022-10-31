import Footprint
import os
#from HeuristicMiner import HeuristicMiner
from FodinaMiner import FodinaMiner
from pm4py.objects.log.importer.xes import importer as xes_importer
from lxml import etree
import subprocess
import re

def xes_to_list(log):
    list1 = []
    for i in range(len(log)):
        list2 = []
        for j in range(len(log[i])):
            list2.append(log[i][j]['concept:name'])
        list1.append(list2)
    return list1

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

def get_precision_recall(file_path_name, long_distance_map):
    s1 = 'java -jar /Users/apple/Desktop/codebase/jbpt-pm/entropia/jbpt-pm-entropia-1.6.jar -emp -rel='
    s2 = 'java -jar /Users/apple/Desktop/codebase/jbpt-pm/entropia/jbpt-pm-entropia-1.6.jar -emr -rel='
    e1 = ' -ret=/Users/apple/Desktop/research_project/fodina_code/that_fodina2.pnml | grep "Precision:"'
    e2 = ' -ret=/Users/apple/Desktop/research_project/fodina_code/that_fodina2.pnml | grep "Recall:"'
    precison_test = s1 + file_path_name + e1
    recall_test = s2 + file_path_name + e2

    the_log = []
    log = xes_importer.apply(file_path_name)
    for i in log:
        the_log.append(i)

    logs = xes_to_list(the_log)
    sample_miner = FodinaMiner(logs)
    sample_miner.count_frequency()
    sample_miner.normal_condition()
    sample_miner.mine_long_distances()

    if long_distance_map != None:
        sample_miner.reset_long_distance_dependency(long_distance_map)

    sample_miner.whole_part()
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
                one_one.append(tuple([l1[j], l2[j]]))
            elif len(l1[j]) > 1 and len(l2[j][0]) == 1 and len(l2[j]) == 1:
                more_one.append(tuple([l1[j], l2[j]]))
            else:
                one_more.append(tuple([l1[j], l2[j]]))

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

    # measurement for simplicity
    arc_num = len(tup_list)
    t_list = []
    for i in range(len(tup_list)):
        if tup_list[i][1][0] == 't' and tup_list[i][1] not in t_list:
            t_list.append(tup_list[i][1])
        if tup_list[i][2][0] == 't' and tup_list[i][2] not in t_list:
            t_list.append(tup_list[i][2])
    t_num = len(t_list)

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

    try:
        sub1 = subprocess.Popen(
            precison_test,
            shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf-8')
        m = sub1.communicate()
        m1 = re.sub(r'\D', '', m[0])
        precision = int(m1[0:6]) / 100000
    except:
        precision = 'mistake'
    print(precision)

    try:
        sub2 = subprocess.Popen(
            recall_test,
            shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf-8')
        n = sub2.communicate()
        n1 = re.sub(r'\D', '', n[0])
        recall = int(n1[0:6]) / 100000
    except:
        recall = 'mistake'
        os._exit()
    print(recall)
    print('next one')

    return [precision, recall, sample_miner.long_dependency, t_num, p_num, arc_num]

def get_test_result(file_path_name, long_distance_map):
    s1 = 'java -jar /Users/apple/Desktop/codebase/jbpt-pm/entropia/jbpt-pm-entropia-1.6.jar -emp -rel='
    s2 = 'java -jar /Users/apple/Desktop/codebase/jbpt-pm/entropia/jbpt-pm-entropia-1.6.jar -emr -rel='
    e1 = ' -ret=/Users/apple/Desktop/research_project/fodina_code/that_fodina2.pnml | grep "Precision:"'
    e2 = ' -ret=/Users/apple/Desktop/research_project/fodina_code/that_fodina2.pnml | grep "Recall:"'
    precison_test = s1 + file_path_name + e1
    recall_test = s2 + file_path_name + e2

    the_log = []
    log = xes_importer.apply(file_path_name)
    for i in log:
        the_log.append(i)

    logs = xes_to_list(the_log)
    sample_miner = FodinaMiner(logs)
    sample_miner.count_frequency()
    sample_miner.normal_condition()
    sample_miner.mine_long_distances()

    if long_distance_map != None:
        sample_miner.reset_long_distance_dependency(long_distance_map)

    sample_miner.whole_part()
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
                one_one.append(tuple([l1[j], l2[j]]))
            elif len(l1[j]) > 1 and len(l2[j][0]) == 1 and len(l2[j]) == 1:
                more_one.append(tuple([l1[j], l2[j]]))
            else:
                one_more.append(tuple([l1[j], l2[j]]))

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

    # measurement for simplicity
    arc_num = len(tup_list)
    t_list = []
    for i in range(len(tup_list)):
        if tup_list[i][1][0] == 't' and tup_list[i][1] not in t_list:
            t_list.append(tup_list[i][1])
        if tup_list[i][2][0] == 't' and tup_list[i][2] not in t_list:
            t_list.append(tup_list[i][2])
    t_num = len(t_list)

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

    try:
        sub1 = subprocess.Popen(
            precison_test,
            shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf-8')
        m = sub1.communicate()
        m1 = re.sub(r'\D', '', m[0])
        precision = int(m1[0:6]) / 100000
    except:
        precision = 'mistake'
    print(precision)

    try:
        sub2 = subprocess.Popen(
            recall_test,
            shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf-8')
        n = sub2.communicate()
        n1 = re.sub(r'\D', '', n[0])
        recall = int(n1[0:6]) / 100000
    except:
        recall = 'mistake'
        os._exit()
    print(recall)
    print('next one')

    return [precision, recall]


def pass_long_distance_map(basic_list, next_ld):
    next_result = get_precision_recall(training_path, next_ld)

    precision = basic_list[0]
    recall = basic_list[1]
    long_distance_map = basic_list[2]
    t_num = basic_list[3]
    p_num = basic_list[4]
    arc_num = basic_list[5]

    if recall > 1:
        recall = 1

    next_precision = next_result[0]
    next_recall = next_result[1]
    next_long_distance_map = next_result[2]
    next_t_num = next_result[3]
    next_p_num = next_result[4]
    next_arc_num = next_result[5]

    if next_recall > 1:
        next_recall = 1
    print('new_value')
    print(next_precision + next_recall)
    print('old_value')
    print(precision + recall)
    if (next_precision + next_recall) - (precision + recall) > - 0.01:
        return (next_precision, next_recall, next_long_distance_map, next_t_num, next_p_num, next_arc_num)
    else:
        return [precision, recall, long_distance_map, t_num, p_num, arc_num]

    #if next_precision + next_recall == 0:
        #f1 = 0
    #else:
        #f1 = 2 * next_precision * next_recall / (next_precision + next_recall)

    #if precision + recall == 0:
        #f2 = 0
    #else:
        #f2 = 2 * precision * recall / (precision + recall)

    #if f1 >= f2:
        #return (next_precision, next_recall, next_long_distance_map, next_t_num, next_p_num, next_arc_num)
    #else:
        #return [precision, recall, long_distance_map, t_num, p_num, arc_num]

def delete_node(ld, node):
    new_list = []
    for i in ld:
        if i[0] != node:
            new_list.append(i)
    return new_list

old_result = []
new_result = []
old_test_result = []
new_test_result = []
path = '/Users/apple/Desktop/Training_Logs/'
path_test = '/Users/apple/Desktop/Test_Logs/'
file_name_list_1 = ['pdc_2020_0000000.xes']
file_name_list = ['pdc_2020_0000000.xes', 'pdc_2020_0000001.xes', 'pdc_2020_0000010.xes', 'pdc_2020_0000011.xes', 'pdc_2020_0000100.xes',
                  'pdc_2020_0000101.xes', 'pdc_2020_0000110.xes', 'pdc_2020_0000111.xes', 'pdc_2020_0001000.xes', 'pdc_2020_0001001.xes',
                  'pdc_2020_0001010.xes', 'pdc_2020_0001011.xes', 'pdc_2020_0001100.xes', 'pdc_2020_0001101.xes', 'pdc_2020_0001110.xes',
                  'pdc_2020_0001111.xes', 'pdc_2020_0010000.xes', 'pdc_2020_0010001.xes', 'pdc_2020_0010010.xes', 'pdc_2020_0010011.xes',
                  'pdc_2020_0010100.xes', 'pdc_2020_0010101.xes', 'pdc_2020_0010110.xes', 'pdc_2020_0010111.xes', 'pdc_2020_0011000.xes',
                  'pdc_2020_0011001.xes', 'pdc_2020_0011010.xes', 'pdc_2020_0011011.xes', 'pdc_2020_0011100.xes', 'pdc_2020_0011101.xes',
                  'pdc_2020_0011110.xes', 'pdc_2020_0011111.xes'
                  ]

file_name_list = ['pdc_2020_0011100.xes', 'pdc_2020_0011101.xes',
                  'pdc_2020_0011110.xes', 'pdc_2020_0011111.xes']
file_name_list1 = ['pdc_2020_0200001.xes', 'pdc_2020_0200010.xes', 'pdc_2020_0200011.xes', 'pdc_2020_0200100.xes',
                  'pdc_2020_0200101.xes', 'pdc_2020_0200110.xes', 'pdc_2020_0200111.xes', 'pdc_2020_0201000.xes', 'pdc_2020_0201001.xes',
                  'pdc_2020_0201010.xes', 'pdc_2020_0201011.xes', 'pdc_2020_0201100.xes', 'pdc_2020_0201101.xes', 'pdc_2020_0201110.xes',
                  'pdc_2020_0201111.xes', 'pdc_2020_0210000.xes', 'pdc_2020_0210001.xes', 'pdc_2020_0210010.xes', 'pdc_2020_0210011.xes',
                  'pdc_2020_0210100.xes', 'pdc_2020_0210101.xes', 'pdc_2020_0210110.xes', 'pdc_2020_0210111.xes', 'pdc_2020_0211000.xes',
                  'pdc_2020_0211001.xes', 'pdc_2020_0211010.xes', 'pdc_2020_0211011.xes', 'pdc_2020_0211100.xes',
                  'pdc_2020_0211101.xes', 'pdc_2020_0211110.xes', 'pdc_2020_0211111.xes']


file_name_list_1 = ['pdc_2020_0000000.xes']
for file_name in file_name_list_1:
    precision = 0
    recall = 0
    t_num = 0
    p_num = 0
    arc_num = 0
    training_path = path + str(file_name)
    test_path = path_test + str(file_name)
    the_result = get_precision_recall(training_path, None)
    old_result.append((the_result[0], the_result[1], the_result[3], the_result[4], the_result[5]))

    o_test_result = get_test_result(test_path, the_result[2])
    old_test_result.append(o_test_result)

    basic_ld = the_result[2]
    ld_nodes = []
    for i in range(len(basic_ld)):
        if basic_ld[i][0] not in ld_nodes:
            ld_nodes.append(basic_ld[i][0])

    basic_value = [the_result[0], the_result[1], the_result[2], the_result[3], the_result[4], the_result[5]]
    for node in ld_nodes:
        print('node')
        print(node)
        next_ld = delete_node(basic_value[2], node)
        print('basic ld')
        print(basic_value[2])
        print('next ld')
        print(next_ld)
        #result = pass_long_distance_map(basic_ld, next_ld)
        #precision = result[0]
        #recall = result[1]
        #basic_ld = result[2]
        result = pass_long_distance_map(basic_value, next_ld)
        precision = result[0]
        recall = result[1]
        long_distance_map = result[2]
        t_num = result[3]
        p_num = result[4]
        arc_num = result[5]
        basic_value = [precision, recall, long_distance_map, t_num, p_num, arc_num]

        print('next')
        print(precision)
        print(recall)
        print(basic_ld)

    n_test_result = get_test_result(test_path, basic_value[2])
    new_test_result.append(n_test_result)
    new_result.append((precision, recall, t_num, p_num, arc_num))
    print('old_result')
    print(old_result)
    print('old test result')
    print(old_test_result)
    print('new_result')
    print(new_result)
    print('new test result')
    print(new_test_result)
#for file_name in file_name_list1:
    #training_path = path + str(file_name)
    #the_result = get_precision_recall(training_path)
    #result.append(the_result)
#for file_name in file_name_list2:
    #training_path = path + str(file_name)
    #the_result = get_precision_recall(training_path)
    #result.append(the_result)
#for file_name in file_name_list3:
    #training_path = path + str(file_name)
    #the_result = get_precision_recall(training_path)
    #result.append(the_result)
#for file_name in file_name_list4:
    #training_path = path + str(file_name)
    #the_result = get_precision_recall(training_path)
    #result.append(the_result)

#print(result)