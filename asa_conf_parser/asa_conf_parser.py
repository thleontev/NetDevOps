from ciscoconfparse import CiscoConfParse
parse = CiscoConfParse("/home/user/asa-inet", syntax='asa')
# asa-debug.conf

def get_type_object(obj_name):
    if obj_name == "object-group network":
        result = 1
    elif obj_name == "object network":
        result = 2       
    elif obj_name == "network-object host":
        result = 3
    elif obj_name == "network-object object":
        result = 4
    elif obj_name == "group-object":
        result = 5
    elif obj_name == "object-group service":
        result = 6
    elif obj_name == "object service":
        result = 7
    else:
        result = -1
    return(result);

# type 1 - object-group network, type 2 - object network, type 6 - object-group service, type 7 - object service
def parse_object(obj_type, obj_name, obj_list=[]):
    # type 1
    # object-group network
    try:
        result = -1               
        if obj_type == 1:
            obj = parse.find_objects(r"^object-group network %s$" %obj_name)
            if len(obj) == 0:
                return(-1)
            obj_list.append("["+obj_name+"]")
            for obj_child in obj[0].children:
                lst = obj_child.text.split()
                # type 3
                # network-object host
                if get_type_object(lst[0]+" "+lst[1]) == 3:
                    obj_list.append(lst[2])
                    result = 1
                # type 4
                # network-object object           
                elif get_type_object(lst[0]+" "+lst[1]) == 4:
                    result = parse_object(4,lst[2],obj_list)
                # type 5
                # group-object   
                elif get_type_object(lst[0]) == 5:
                    result = parse_object(5,lst[1],obj_list)
                # description
                elif lst[0] == "description":
                    continue
                # network-object n.n.n.n m.m.m.m
                else:
                    obj_list.append(lst[1]+" / "+lst[2])
                    result = 1
        # type 2
        # object network
        #   host/subnet
        if obj_type == 2:
            obj = parse.find_objects(r"^object network %s$" %obj_name)
            if len(obj) == 0:
                return(-1)
            for obj_child in obj[0].children:
                lst = obj_child.text.split()
                if lst[0] == "subnet":
                    obj_list.append("("+obj_name+") "+lst[1]+" / "+lst[2])
                    result = 1
                elif lst[0] == "range":
                    obj_list.append("("+obj_name+") "+lst[1]+" - "+lst[2])
                    result = 1
                elif lst[0] == "host":
                    obj_list.append("("+obj_name+") "+lst[1])
                    result = 1
                else:
                    continue
        # type 4
        # network-object object 
        if obj_type == 4:
            result = parse_object(2,obj_name,obj_list)
        # type 5
        # group-object
        if obj_type == 5:
            result = parse_object(1,obj_name,obj_list)

        # type 6
        # object-group service
        # object-group protocol
        if obj_type == 6:
            obj_list.append("["+obj_name+"]")
            # object-group service DM_INLINE_TCP_2 tcp
            obj = parse.find_objects(r"^object-group service %s " %obj_name)
            # object-group service DM_INLINE_SERVICE_178
            if len(obj) == 0:
                obj = parse.find_objects(r"^object-group service %s" %obj_name)
            # object-group protocol TCPUDP
            if len(obj) == 0:
                obj = parse.find_objects(r"^object-group protocol %s" %obj_name)
            olst = obj[0].text.split()
            for obj_child in obj[0].children:
                lst = obj_child.text.split()
                if lst[0] == "port-object":
                    if lst[1] == "object":
                        result = parse_object(7,lst[2],obj_list)
                    elif lst[1] == "range":
                        obj_list.append(olst[3]+"/"+lst[2]+"-"+lst[3])
                        result = 1
                    else:
                        obj_list.append(olst[3]+"/"+lst[2])
                        result = 1
                elif lst[0] == "service-object":
                    if lst[1] == "object":
                        result = parse_object(7,lst[2],obj_list)
                    elif lst[3] == "range":
                        obj_list.append(lst[1]+"/"+lst[4]+"-"+lst[5])
                        result = 1
                    else:
                        obj_list.append(lst[1]+"/"+lst[4])
                        result = 1
                elif lst[0] == "group-object":
                    result = parse_object(6,lst[1],obj_list)
                elif lst[0] == "protocol-object":
                    obj_list.append(lst[1])
                    result = 1
                else:
                    result = -1
        # type 7
        # object service
        if obj_type == 7:
            #obj_list.append("("+obj_name+")")
            obj = parse.find_objects(r"^object service %s" %obj_name)
            olst = obj[0].text.split()
            for obj_child in obj[0].children:
                lst = obj_child.text.split()
                if lst[0] == "service":
                    if lst[3] == "range":
                        obj_list.append("("+obj_name+") "+lst[1]+"/"+lst[4]+"-"+lst[5])
                        result = 1
                    else:
                        obj_list.append("("+obj_name+") "+lst[1]+"/"+lst[4])
                        result = 1
    except:
        result = -1
    return(result);

def write_list(file, obj_list=[]):
    f_tab = ""
    for i in range(len(obj_list)):
        file.write(f_tab+"%s\n" %obj_list[i])
        if obj_list[i].find("]") > 0:
            f_tab = f_tab+" "
    return

# main loop
f = open('/home/user/rules_file_inet', 'w')

# access-list
f_remark =  False
for obj in parse.find_objects(r"^access-list"):
    rules = obj.text.split()
    obj_index = 0

    if f_remark == True:
        print(obj.text)
        f.write(obj.text+'\n')
        f_remark = False
    else:
        print(obj.text)
        f.write('\n'+obj.text+'\n')
        
    if rules[2] == "remark":
        f_remark = True
        
    if rules[2] == "extended":
       for i in range(len(rules)):
        if rules[i] == "object":
            asa_object = []
            res = parse_object(2,rules[i+1], asa_object)
            if  res == -1:
                asa_object = []
                parse_object(7,rules[i+1], asa_object)
                print(asa_object)
                write_list(f,asa_object)
            else:
                print(asa_object)
                write_list(f,asa_object)
        if rules[i] == "object-group":
            asa_object = []
            res = parse_object(1,rules[i+1], asa_object)
            if res == -1:
                asa_object = []
                parse_object(6,rules[i+1], asa_object)
                print(asa_object)
                write_list(f,asa_object)
            else:
                print(asa_object)
                write_list(f,asa_object)

# nat()
for obj in parse.find_objects(r"^nat "):
    rules = obj.text.split()
    obj_index = 0
    print(obj.text)
    f.write(obj.text+'\n')
    f_beg = False
    for i in range(len(rules)):
        if rules[i].find(")") > 0:
            f_beg = True
            continue
        if f_beg == False:
            continue
        if rules[i] == "source" or rules[i] == "static" or rules[i] == "destination": 
            continue
        asa_object = []
        if parse_object(1,rules[i], asa_object) != -1:
            print(asa_object)
            write_list(f,asa_object)
            continue
        asa_object = []
        if parse_object(2,rules[i], asa_object) != -1:
            print(asa_object)
            write_list(f,asa_object)
            continue
        asa_object = []
        if parse_object(6,rules[i], asa_object) != -1:
            print(asa_object)
            write_list(f,asa_object)
            continue
        asa_object = []
        if parse_object(7,rules[i], asa_object) != -1:
            print(asa_object)
            write_list(f,asa_object)

    f.write('\n')
f.close()
