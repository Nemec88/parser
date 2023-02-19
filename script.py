import requests


def check_sum(value):
    t = ''
    if '+' in value:
        v_1 = value.split('+')[0]
        v_2 = value.split('+')[1]
        t = str(int(v_1) + int(v_2))
    else:
        t = value
    return t


def check_second_value(t, event, player):
    l = len(event)
    # print(player)
    if l == 2 and event[1] == 'Red Card':                                                                               # Для YELLOW - RED CARDS
        player = player[0]
        return [t, '-', player]
    elif l == 2 and event[0] == 'Yellow Card':                                                                          # Для YELLOW CARDS, поле 'REASON'
        return [t, event[1]]
    elif l == 1 and event[0] in 'Yellow Card':                                                                          # Для YELLOW CARDS,
        return [t, '-']
    elif l == 1 and event[0] == 'Red Card':                                                                             # Red cards
        player = player[0]
        return [t, '-', player]
    elif event[0] in ['Substitution - Out', 'Substitution - In']:                                                       # Замены
        players = player[1] + '|' + player[0]
        return [t, players]
    elif event[0] == 'Own goal':
        player = player[0]
        return [t, player]
    elif event[0] == 'Penalty Kick':
        player = player[0]
        return [t, player]
    else:
        return [t]


def pars_summary(id):
    half = 0
    mark = 0
    summary_list = [{}]
    list_event = [['1Disallowed3'] * 5, ['2Goal1'] * 5,
                  ['MIT2'] * 4,
                  ['1Yellow Card2'] * 10,
                  ['1Yellow Card:Red Card3'] * 4,
                  ['1Red Card3'] * 4,
                  ['1Substitution2'] * 10,
                  ['1Own goal2'] * 4,
                  ['1Penalty Kick2'] * 4,
                  ['1Disallowed3'] * 4,                                                                                 # VAR
                  ]
    list_event_2 =[['2Yellow Card2'] * 10,
                  ['2Yellow Card:Red Card3'] * 4,
                  ['2Red Card3'] * 4,
                  ['2Substitution2'] * 10,
                  ['2Own goal2'] * 4,
                  ['2Penalty Kick2'] * 4,
                  ['2Disallowed3'] * 4,                                                                                 # VAR
                  ]
    result_summary_list = []
    result_summary_list_2 = []
    url_symmary = f'https://d.flashscore.com/x/feed/df_sui_1_{id}'
    response = requests.get(url_symmary, headers={
        "x-fsign": "SW9D1eZo"})  # Передаем ключь
    res = (response.text).split('¬')

    # print(res)

    for i in res[:-2]:
        key = i.split('÷')[0]
        value = i.split('÷')[1]
        if 'AC' in key:
            half += 1
        elif '~' in key:
            summary_list.append({key: [value, half]})
        elif summary_list[-1].get(key):
            summary_list[-1][key].append(value)
        else:
            summary_list[-1].update({key: [value]})

    # for q in summary_list:
    #     print(q)


    for el in list_event:
        count_2 = 0
        for i in el:                                                                                                    # 'Goal'
            count = -1
            mark_2 = 0
            for e in summary_list:                                                                                      # Ключи (строкой события)
                count += 1                                                                                              # Счетчик для удаления словаря в котором забрали событие
                if len(e.get('IK', 'No')) == 1 and i[1:-2] in e.get('IK', 'No')[0] and e.get('IA') == [i[0]] or\
                    len(e.get('IK', 'No')) == 2 and i[1:-2] in e.get('IK', 'No')[0] and e.get('IK', 'No')[1] != 'Red Card' and e.get('IA') == [i[0]] or \
                    len(e.get('IK', 'No')) == 2 and e.get('IK', 'No')[0] in i and e.get('IK', 'No')[1] in i and e.get('IA') == [i[0]]:    # Условие для события Goal (IK - событие, IA - номер команды)
                    # commanda = e.get('IA')
                    event = e.get('IK', 0)
                    t = check_sum(e.get('IB', 0)[0][:-1])
                    player = e.get('IF', 0)
                    # number_time = e.get('~III', 0)[1]
                    reason = check_second_value(t, event, player)
                    result_summary_list.append(reason)
                    del summary_list[count]
                    mark_2 += 1
                    break
                elif i[1:-2] in e.get('IKX', 'No')[0][4:] and e.get('IAX', 0) == [i[0]]:
                    var_reason = e.get('ILX', 0)[0]
                    player = e.get('IFX', 0)[0]
                    t = check_sum(e.get('IBX', 0)[0][:-1])
                    result_summary_list.append([t, var_reason, player])
                    del summary_list[count]
                    mark_2 += 1
                elif i[:-1] in list(e.keys()):                                                                          # Условие для события Referee
                    ref = e.get('MIV')[0]
                    country_ref = e.get('MIV')[3]
                    result_summary_list.append([ref, country_ref])
                    del summary_list[count]
                    mark_2 += 1
            if mark_2 == 0:
                result_summary_list.append(['-'] * int(i[-1]))



    for el in list_event_2:
        for i in el:     # 'Goal'
            count = -1
            mark_2 = 0
            for e in summary_list: # Ключи (строкой события)
                count += 1
                if len(e.get('IK', 'No')) == 1 and i[1:-2] in e.get('IK', 'No')[0] and e.get('IA') == [i[0]] or \
                    len(e.get('IK', 'No')) == 2 and i[1:-2] in e.get('IK', 'No')[0] and e.get('IK', 'No')[1] != 'Red Card' and e.get('IA') == [i[0]] or \
                    len(e.get('IK', 'No')) == 2 and e.get('IK', 'No')[0] in i and e.get('IK', 'No')[1] in i and e.get('IA') == [i[0]]:
                    # commanda = e.get('IA')
                    event = e.get('IK', 0)
                    t = check_sum(e.get('IB', 0)[0][:-1])
                    player = e.get('IF', 0)
                    # number_time = e.get('~III', 0)[1]
                    reason = check_second_value(t, event, player)
                    result_summary_list_2.append(reason)
                    del summary_list[count]
                    mark_2 += 1
                    break
                elif i[1:-2] in e.get('IKX', 'No')[0][4:]:                                                              # Обработка события VAR
                    var_reason = e.get('ILX', 0)[0]
                    player = e.get('IFX', 0)[0]
                    t = check_sum(e.get('IBX', 0)[0][:-1])
                    result_summary_list_2.append([t, var_reason, player])
                    del summary_list[count]
                    mark_2 += 1
                elif i[:-1] in list(e.keys()):
                    ref = e.get('MIV')[0]
                    country_ref = e.get('MIV')[3]
                    result_summary_list_2.append_2([ref, country_ref])
                    del summary_list[count]
                    mark_2 += 1
            if mark_2 == 0:
                result_summary_list_2.append(['-'] * int(i[-1]))

    # print(result_summary_list_2, result_summary_list_2)

    return result_summary_list, result_summary_list_2



if __name__ == '__main__':
    pars_summary('pCftMa15')
