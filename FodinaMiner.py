from Footprint import Footprint as footprint

class FodinaMiner:
    def __init__(self, log):
        self.log = log
        self.unique_activity_tasks = self.get_activity_tasks()
        self.dependency_map = []
        self.long_dependency = []
        self.length_one_loop = []
        self.length_two_loops = []
        self.two_loops_freq = {}
        self.event_frequency = self.get_event_frequency()
        self.frequency = []
        self.significance = []
        self.start_event = self.find_start_element()
        self.end_event = self.find_end_element()
        self.split_and_join_in = {}
        self.split_and_join_out = {}
        self.threshold_l1l = 0.9
        self.threshold_d = 0.8
        self.threshold_l2l = 0.8
        self.threshold_ld = 0.9
        self.threshold_tpat = 0.8
        self.nol2lwithl1l = False
        self.no_binary_conflicts = True
        self.connect_net = False
        self.mine_long_dependences = True

    def get_activity_tasks(self):
        activity_tasks = []
        for trace in self.log:
            for event in trace:
                if event not in activity_tasks:
                    activity_tasks.append(event)
        return activity_tasks

    def get_event_frequency(self):
        dict = {}
        for unique_task in self.unique_activity_tasks:
            num = 0
            for trace in self.log:
                for event in trace:
                    if event == unique_task:
                        num += 1
            dict[unique_task] = num
        return dict

    def count_frequency(self):
        for i in self.unique_activity_tasks:
            self.frequency.append([i, dict.fromkeys([w for w in self.unique_activity_tasks], 0)])
        for trace in self.log:
            for i, event in enumerate(trace):
                if i != len(trace) - 1:
                    self.increment_freq(event, trace[i+1], self.frequency)

    def increment_freq(self, event, value, dicts):
        for dict in dicts:
            if dict[0] == event:
                dict[1][value] += 1

    #def step2_one_loop(self):
        #for i in self.frequency:
            #first_event = i[0]
            #event_times = i[1][first_event]
            #if event_times / (event_times + 1) > self.threshold_l1l:
                #self.dependency_map.append([first_event, first_event])

    # step2 and step3 together
    def normal_condition(self):
        self.count_frequency()
        for i in self.unique_activity_tasks:
            self.significance.append([i, dict.fromkeys([w for w in self.unique_activity_tasks], 0)])
            for freq_dict in self.frequency:
                event = freq_dict[0]
                for value in freq_dict[1]:
                    a = self.return_dict_value(event, value, self.frequency)
                    b = self.return_dict_value(value, event, self.frequency)
                    for sign_dict in self.significance:
                        if sign_dict[0] == event:
                            if event == value:
                                sign_dict[1][value] = a / (a + 1)
                                if a / (a + 1) > self.threshold_l1l:
                                    if [event, event] not in self.dependency_map:
                                        self.dependency_map.append([event, event])
                                        self.length_one_loop.append([event, event])
                            else:
                                #sign_dict[1][value] = (a - b) / (a + b + 1)
                                #if (a - b) / (a + b + 1) > self.threshold_d:
                                sign_dict[1][value] = a / (a + b + 1)
                                if a / (a + b + 1) > self.threshold_d:
                                    if [event, value] not in self.dependency_map:
                                        self.dependency_map.append([event, value])

    def return_dict_value(self, event, value, dicts):
        for freq_dict in dicts:
            if freq_dict[0] == event:
                return freq_dict[1][value]

    #step4
    def find_length_two_loops(self):
        two_loops = []
        for trace in self.log:
            for index, event in enumerate(trace):
                if index < len(trace) - 2:
                    if trace[index] == trace[index + 2]:
                        two_loops.append([event, trace[index+1]])
        for list in two_loops:
            list1, list2 = list[0], list[1]
            if self.calculate_two_loops(list, two_loops) > self.threshold_l2l:
                if list not in self.length_two_loops:
                    if self.nol2lwithl1l == False and [list1, list1] not in self.length_one_loop \
                            and [list2, list2] not in self.length_two_loops:
                        self.length_two_loops.append(list)
                        if self.reverse(list) not in self.length_two_loops:
                            self.length_two_loops.append(self.reverse(list))
                if list not in self.dependency_map:
                    if self.nol2lwithl1l == False and [list1, list1] not in self.length_one_loop \
                            and [list2, list2] not in self.length_two_loops:
                        self.dependency_map.append(list)
                        if self.reverse(list) not in self.dependency_map:
                            self.dependency_map.append(self.reverse(list))

    def calculate_two_loops(self, list, two_loops):
        m1 = 0
        for two_loop in two_loops:
            if list == two_loop:
                m1 += 1
        if self.dictkey_not_has_list(list, self.two_loops_freq):
            self.two_loops_freq[tuple(list)] = m1
        m2 = 0
        for two_loop in two_loops:
            if self.reverse(list) == two_loop:
                m2 += 1
        if self.dictkey_not_has_list(self.reverse(list), self.two_loops_freq):
            self.two_loops_freq[tuple(self.reverse(list))] = m2
        return (m1 + m2) / (m1 + m2 + 1)

    def reverse(self, list):
        result = []
        result.append(list[1])
        result.append(list[0])
        return result

    def dictkey_not_has_list(self, list, dict):
        if dict == {}:
            return True
        for i in dict.keys():
            if list == i:
                return False
        return True

    #step5 and step9, we have only one start element and one end element
    def delete_first_end(self):
        start_element = self.find_start_element()
        end_element = self.find_end_element()
        for depend_relation in self.dependency_map:
            if depend_relation[1] == start_element and depend_relation[0] != depend_relation[1]:
                self.dependency_map.remove(depend_relation)
        for depend_relation in self.dependency_map:
            if depend_relation[0] == end_element and depend_relation[0] != depend_relation[1]:
                self.dependency_map.remove(depend_relation)

    def find_start_element(self):
        start_dict = {}
        for trace in self.log:
            if trace[0] not in start_dict.keys():
                start_dict[trace[0]] = 1
            else:
                start_dict[trace[0]] += 1
        return self.find_most_fre_event(start_dict)

    def find_end_element(self):
        end_dict = {}
        for trace in self.log:
            if trace[len(trace)-1] not in end_dict.keys():
                end_dict[trace[len(trace)-1]] = 1
            else:
                end_dict[trace[len(trace)-1]] += 1
        return self.find_most_fre_event(end_dict)

    def find_most_fre_event(self, dict):
        max_value = 0
        max_event = 0
        for i in dict.keys():
            if dict[i] > max_value:
                max_value = dict[i]
                max_event = i
        return max_event

    # control with binary conflicts
    # from step10 to step17
    def binary_conflicts(self):
        pairs_list = []
        if self.no_binary_conflicts == True:
            for pairs in self.dependency_map:
                if self.reverse(pairs) in self.dependency_map and pairs[0] != pairs[1]:
                    pairs_list.append(pairs)
                    pairs_list.append(self.reverse(pairs))
                    self.dependency_map.remove(pairs)
                    self.dependency_map.remove(self.reverse(pairs))
        for pairs in pairs_list:
            if tuple(pairs) in self.two_loops_freq.keys():
                if self.two_loops_freq[tuple(pairs)] > 0:
                    if [pairs[0], pairs[0]] not in self.dependency_map:
                        self.dependency_map.append([pairs[0], pairs[0]])
        for pair in pairs_list:
            for event in self.unique_activity_tasks:
                if event != pair[0] and event != pair[1] and pair[0] != pair[1]:
                    if [event, pair[0]] in self.dependency_map and [event, pair[1]] not in self.dependency_map:
                        self.dependency_map.append([event, pair[1]])
                    if [event, pair[0]] not in self.dependency_map and [event, pair[1]] in self.dependency_map:
                        self.dependency_map.append([event, pair[0]])
                    if [pair[0], event] in self.dependency_map and [pair[1], event] not in self.dependency_map:
                        self.dependency_map.append([pair[1], event])
                    if [pair[0], event] not in self.dependency_map and [pair[1], event] in self.dependency_map:
                        self.dependency_map.append([pair[0], event])

    # consider unconnected nodes
    def operate_unconnect_nodes(self):
        without_start = []
        without_end = []
        if self.connect_net == True:
            for i in self.unique_activity_tasks:
                if i != self.start_event and i != self.end_event:
                    # the function means we have a list, we want to find whether the first position of the elements of the list has i
                    if not self.key_position_dict(i, self.dependency_map, 1):
                        without_start.append(i)
                    if not self.key_position_dict(i, self.dependency_map, 0):
                        without_end.append(i)
            if without_start is not None:
                #value1 = 0
                #connect1 = []
                for event in without_start:
                    #if value1 < self.find_best_start_connection(event)[0]:
                        #value1 = self.find_best_start_connection(event)[0]
                        #event1 = self.find_best_start_connection(event)[1]
                        #connect1 = [event1, event]
                #self.dependency_map.append(connect1)
                    self.find_best_start_connection(event)
            if without_end is not None:
                #value2 = 0
                #connect2 = []
                for event in without_end:
                    self.find_best_end_connection(event)
                    #if value2 < self.find_best_end_connection(event)[0]:
                        #value2 = self.find_best_end_connection(event)[0]
                        #event2 = self.find_best_end_connection(event)[1]
                        #connect2 = [event, event2]
                #self.dependency_map.append(connect2)

    def key_position_dict(self, event, dependency_map, index):
        for pair in dependency_map:
            if event == pair[index]:
                return True
        return False

    def find_best_start_connection(self, event):
        best_event = 0
        best_value = 0
        for i in self.frequency:
            for j in i[1].keys():
                if j == event:
                    a_b_value = i[1][j]
                    for k in self.frequency:
                        if k[0] == event:
                            b_a_value = k[1][i[0]]
                            if best_value < a_b_value / (a_b_value + b_a_value + 1) and i[0] != event:
                                best_value = a_b_value / (a_b_value + b_a_value + 1)
                                best_event = i[0]
        if not self.key_position_dict(event, self.dependency_map, 1):
            self.dependency_map.append([best_event, event])

    def find_best_end_connection(self, event):
        best_event = 0
        best_value = 0
        for i in self.frequency:
            if i[0] == event:
                for j in i[1].keys():
                    end_part = i[1][j]
                    for k in self.frequency:
                        if k[0] == j:
                            start_part = k[1][i[0]]
                            if best_value < end_part / (end_part + start_part + 1) and event != j:
                                best_value = end_part / (end_part + start_part + 1)
                                best_event = j
        if not self.key_position_dict(event, self.dependency_map, 0):
            self.dependency_map.append([event, best_event])

    # step line 30-36
    # mine_long_distances
    def mine_long_distances(self):
        for event_a in self.unique_activity_tasks:
            for event_b in self.unique_activity_tasks:
                if event_a != event_b:
                    ab_value = self.calculate_long_value(event_a, event_b)
                    num_event_a = self.event_frequency[event_a]
                    num_event_b = self.event_frequency[event_b]
                    long_distance_value = 2*ab_value/(num_event_a+num_event_b+1)-2*abs(num_event_a-num_event_b)/(num_event_a+num_event_b+1)
                    if long_distance_value >= self.threshold_ld:
                        if self.path_exists_from_to_without_visiting(self.start_event, self.end_event, event_a) and self.path_exists_from_to_without_visiting(self.start_event, self.end_event, event_b) and self.path_exists_from_to_without_visiting(event_a, self.end_event, event_b):
                            if [event_a, event_b] not in self.dependency_map:
                                self.dependency_map.append([event_a, event_b])
                                self.long_dependency.append([event_a, event_b])

    def calculate_long_value(self, event_a, event_b):
        num = 0
        for trace in self.log:
            event_a_index = []
            event_b_index = []
            for index, event in enumerate(trace):
                if event == event_a:
                    event_a_index.append(index)
                if event == event_b:
                    event_b_index.append(index)
            if event_a_index != [] and event_b_index != []:
                if len(event_a_index) > 1:
                    for i, index_a in enumerate(event_a_index):
                        if i != len(event_a_index)-1:
                            if self.element_exist_between_two_indexes(event_b_index, event_a_index[i]+1, event_a_index[i+1]):
                                num += 1
                        else:
                            if event_a_index[len(event_a_index)-1]+1 < event_b_index[len(event_b_index)-1]:
                                num += 1
                else:
                    if len(event_a_index) == 1 and event_a_index[0]+1 < event_b_index[len(event_b_index)-1]:
                        num += 1
        return num

    def element_exist_between_two_indexes(self, list, start_index, end_index):
        for element in list:
            if element > start_index and element < end_index:
                return True
        return False

    def path_exists_from_to_without_visiting(self, start_event, end_event, middle_event):
        for trace in self.log:
            start_event_index = []
            end_event_index = []
            middle_event_index = []
            for index, event in enumerate(trace):
                if event == start_event:
                    start_event_index.append(index)
            for index, event in enumerate(trace):
                if event == end_event:
                    end_event_index.append(index)
            for index, event in enumerate(trace):
                if event == middle_event:
                    middle_event_index.append(index)

            if start_event_index != [] and end_event_index != []:
                start = start_event_index[0]
                end = end_event_index[len(end_event_index)-1]
                if self.element_exist_between_two_indexes(middle_event_index, start, end):
                    return True
        return False

    def reset_long_distance_dependency(self, dependency):
        for element in self.long_dependency:
            if element not in dependency:
                self.dependency_map.remove(element)
        self.long_dependency = dependency

    # Algorithm 2

    # line1 to line3
    def whole_part(self):
        for t in self.unique_activity_tasks:
            self.find_patterns(t, 'input')
            self.find_patterns(t, 'output')

    def find_patterns(self, the_event, statues):
        PS = {}
        if statues == 'input':
            ps_input = self.get_dependency_element(the_event, 1)
        if statues == 'output':
            ps_output = self.get_dependency_element(the_event, 0)

        # consider input
        if statues == 'input':
            for trace in self.log:
                for index, event in enumerate(trace):
                    if event == the_event:
                        P = []
                        for c in ps_input:
                            CO = self.get_dependency_element(c, 0)
                            # return an max_index
                            cp = self.most_near_input(trace, index-1, c)
                            if cp != -1 and self.cp_fit_input_conditions(trace, the_event, c, CO, cp, index-1):
                                P.append(c)
                        if P != []:
                            if tuple(P) not in PS.keys():
                                PS[tuple(P)] = 1
                            else:
                                PS[tuple(P)] += 1
            return self.filter_patterns(the_event, PS, ps_input, 'input')

        # consider output
        if statues == 'output':
            for trace in self.log:
                for index, event in enumerate(trace):
                    if event == the_event:
                        P = []
                        for c in ps_output:
                            CI = self.get_dependency_element(c, 1)
                            # return an max_index
                            cp = self.most_near_output(trace, index + 1, c)
                            if cp != -1 and self.cp_fit_output_conditions(trace, the_event, c, CI, cp, index + 1):
                                P.append(c)
                        if P != []:
                            if tuple(P) not in PS.keys():
                                PS[tuple(P)] = 1
                            else:
                                PS[tuple(P)] += 1
            return self.filter_patterns(the_event, PS, ps_output, 'output')

        #if statues == 'input':
            #return self.filter_patterns(the_event, PS, ps_input, 'input')
        #else:
            #return self.filter_patterns(the_event, PS, ps_output, 'output')



    def cp_fit_input_conditions(self, trace, the_event, c, CO, cp, upper_index):
        for index, event in enumerate(trace):
            if index > cp and index <= upper_index:
                if event == the_event:
                    return False
                if event in CO and [c, the_event] not in self.long_dependency:
                    return False
        return True

    def cp_fit_output_conditions(self, trace, the_event, c, CI, cp, lower_index):
        for index, event in enumerate(trace):
            if index >= lower_index and index < cp:
                if event == the_event:
                    return False
                if event in CI and [the_event, c] not in self.long_dependency:
                    return False
        return True

    def most_near_input(self, trace, up_index, the_event):
        result = -1
        for index, event in enumerate(trace):
            if index <= up_index and event == the_event:
                result = index
        return result

    def most_near_output(self, trace, low_index, the_event):
        result = -1
        for index, event in enumerate(trace):
            if index >= low_index and event == the_event:
                return index
        return result



    def get_dependency_element(self, event, position):
        map_list = []
        for i in self.dependency_map:
            if i[position] == event:
                map_list.append(i[1-position])
        return map_list

    def filter_patterns(self, the_event, PS, C, statues):
        PF = []
        total_event = 0
        for trace in self.log:
            for event in trace:
                if event == the_event:
                    total_event += 1

        if len(PS.keys()) > 0:
            total_p_num = 0
            total_ps_num = 0
            for i in PS.keys():
                total_p_num += PS[i]
                total_ps_num += 1
            tr = total_p_num / (total_event * total_ps_num)
            if self.threshold_tpat <= 0:
                tr = tr + tr * self.threshold_tpat
            else:
                tr = tr + (1 - tr) * self.threshold_tpat
            for p in PS.keys():
                if PS[p] / total_event >= tr:
                    PF.append(p)
        #for c in C:
            #if tuple([c]) not in PS.keys():
                #PF.append(tuple([c]))
        for c in C:
            m = False
            for i in PS.keys():
                for j in i:
                    if c == j:
                        m = True
            if m == False:
                PF.append(tuple([c]))

        if statues == 'input':
            self.split_and_join_in[the_event] = PF
            #if self.split_and_join_in[the_event] == [] and the_event != self.start_event:
                #self.split_and_join_in[the_event] = tuple(self.start_event)
        else:
            self.split_and_join_out[the_event] = PF
            #if self.split_and_join_out[the_event] == [] and the_event != self.end_event:
                #self.split_and_join_out[the_event] = tuple(self.end_event)




