import re
from textwrap import wrap

def get_handcards(string):
    '''
    检查输入是否合法，并读取手牌内容.
    若输入不合法，输出错误提示并返回None.
    '''
    fullmatch = re.fullmatch(r'(\d+[mps]|[1-7]+z)+', string)
    if not fullmatch:
        print('无效的输入！')
        return None
    match = re.findall(r'\d+[mps]|[1-7]+z', string)
    carddict = {
        'm':[], 'p':[], 's':[], 'z':[]
    }
    for cards in match:
        type_ = cards[-1]
        for i in cards[:-1]:
            if i == '0':# 红宝牌
                carddict[type_].append(5)
            else:
                carddict[type_].append(int(i))
        carddict[type_].sort()
    num = sum(len(carddict[tp]) for tp in 'mpsz')
    if num != 14:
        print('牌数量错误！手牌数必须为14张！')
        return None
    for tp in 'mpsz':
        for i in set(carddict[tp]):
            if carddict[tp].count(i) > 4:
                break
        else:
            continue
        print('牌数量错误！单种牌不得多于4张！')
        break
    else:
        return carddict
    return None

class HandCards:
    def __init__(self, carddict):
        self.carddict = carddict
        self.num = sum(len(carddict[tp]) for tp in 'mpsz')

    def taatsucount(self):
        '''计算手牌中的面子、搭子、对子数，并返回一个三元元组'''
        toitsu, taatsu, mentsu = (0, 0, 0)
        carddict_cpy = {
            'm':self.carddict['m'].copy(),
            'p':self.carddict['p'].copy(),
            's':self.carddict['s'].copy(),
            'z':self.carddict['z'].copy()
        }
    
        for tp in 'mps':
            for i in range(1, 8):
                if i in carddict_cpy[tp]:
                    if i + 1 in carddict_cpy[tp] and i + 2 in carddict_cpy[tp]:
                        carddict_cpy[tp].remove(i)
                        carddict_cpy[tp].remove(i + 1)
                        carddict_cpy[tp].remove(i + 2)
                        mentsu += 1
        for tp in 'mpsz':
            for i in range(1, 10):#不存在的89z不影响
                if carddict_cpy[tp].count(i) >= 3:
                    carddict_cpy[tp].remove(i)
                    carddict_cpy[tp].remove(i)
                    carddict_cpy[tp].remove(i)
                    # 4张字牌额外删除1张以便step5的检验
                    if tp == 'z' and carddict_cpy[tp].count(i) == 1:
                        carddict_cpy[tp].remove(i)
                    mentsu += 1

        toitsu_dict = {'m':[], 'p':[], 's':[]}
        for tp in 'mps':
            for i in range(1, 10):
                if carddict_cpy[tp].count(i) == 2:
                    carddict_cpy[tp].remove(i)
                    carddict_cpy[tp].remove(i)
                    toitsu_dict[tp].append(i)
                    toitsu += 1
        for i in range(1, 8):
            if carddict_cpy['z'].count(i) == 2:
                carddict_cpy['z'].remove(i)
                carddict_cpy['z'].remove(i)
                toitsu += 1
        
        for tp in 'mps':
            for i in toitsu_dict[tp]:
                if toitsu == 0:
                    break
                neighbor = [i - 2, i - 1, i + 1, i + 2]
                if sum(carddict_cpy[tp].count(j) for j in neighbor) >= 2:
                    # 删除其中的两个，改为搭子
                    count = 2
                    for j in neighbor:
                        if count == 0:
                            break
                        if j in carddict_cpy[tp]:
                            carddict_cpy[tp].remove(j)
                            count -= 1
                    toitsu -= 1
                    taatsu += 2
        for tp in 'mps':
            for i in range(1, 9):
                if i in carddict_cpy[tp]:
                    if i + 1 in carddict_cpy[tp]:
                        carddict_cpy[tp].remove(i)
                        carddict_cpy[tp].remove(i + 1)
                        taatsu += 1
                    elif i + 2 in carddict_cpy[tp]:
                        carddict_cpy[tp].remove(i)
                        carddict_cpy[tp].remove(i + 2)
                        taatsu += 1
        if mentsu + toitsu + taatsu + sum(len(carddict_cpy[tp]) for tp in 'mpsz') < 5:
            taatsu -= 1# 对函数本身而言这会导致搭子数计算错误，但能让向听数计算正确
        return (toitsu, taatsu, mentsu)

    def shanten(self):
        '''计算手牌的向听数'''
        st_kokushi = 13
        if self.num == 14:
            carddict_cpy = {
                'm':self.carddict['m'].copy(),
                'p':self.carddict['p'].copy(),
                's':self.carddict['s'].copy(),
                'z':self.carddict['z'].copy()
            }
            for tp in 'mps':
                if 1 in carddict_cpy[tp]:
                    st_kokushi -= 1
                    carddict_cpy[tp].remove(1)
                if 9 in carddict_cpy[tp]:
                    st_kokushi -= 1
                    carddict_cpy[tp].remove(9)
            for i in range(1,8):
                if i in carddict_cpy['z']:
                    st_kokushi -= 1
                    carddict_cpy['z'].remove(i)
            if carddict_cpy['z']:
                st_kokushi -= 1
            else:
                for tp in 'mps':
                    if 1 in carddict_cpy[tp] or 9 in carddict_cpy[tp]:
                        st_kokushi -= 1
                        break

        toitsu = 0
        dragon = 0 # 
        if self.num == 14:
            for tp in 'mpsz':
                for i in range(1,10):
                    if i in self.carddict[tp] and self.carddict[tp].count(i) == 4:
                        dragon += 1
                    elif i in self.carddict[tp] and self.carddict[tp].count(i) >= 2:
                        toitsu += 1

        if toitsu + 2 * dragon == 7:
            st_chitoi = 2 * dragon - 1
        else:
            st_chitoi = 6 - toitsu - dragon

        tuple_ = self.taatsucount()
        block = sum(tuple_)
        toitsu, taatsu, mentsu = tuple_
        if toitsu == 0:
            st_ippan = 8 - 2 * mentsu - taatsu + max(0, block - 4)
        else:
            st_ippan = 8 - 2 * mentsu - taatsu - toitsu + max(0, block - 5)

        return min(st_kokushi, st_chitoi, st_ippan)
    
    def jinzhang(self, card_num, card_tp):
        '''
        计算打某张牌的具体的进张以及进张数.
        '''
        ret_str = ''
        num = 0
        carddict_cpy = {
            'm':self.carddict['m'].copy(),
            'p':self.carddict['p'].copy(),
            's':self.carddict['s'].copy(),
            'z':self.carddict['z'].copy()
        }
        handcards_cpy = HandCards(carddict_cpy)
        for tp in 'mpsz':
            handcards_cpy.carddict[card_tp].remove(card_num)
            for i in range(1,10):
                if tp == 'z' and i > 7:
                    break
                if self.carddict[tp].count(i) == 4:
                    continue
                handcards_cpy.carddict[tp].append(i)
                handcards_cpy.carddict[tp].sort()
                if handcards_cpy.shanten() < self.shanten():
                    ret_str += str(i)
                    ret_str += tp
                    num += 4 - self.carddict[tp].count(i)
                handcards_cpy.carddict[tp].remove(i)
            handcards_cpy.carddict[card_tp].append(card_num)
        return (ret_str, num)

    def print_jinzhang(self):
        strlist = []
        for tp in 'mpsz':
            set_ = set(self.carddict[tp])
            for card_num in set_:
                drawcard, num = self.jinzhang(card_num, tp)
                if num > 0:
                    discard = str(card_num) + tp
                    strlist.append((discard, drawcard, num))
        # 将输出按一定顺序排列
        global output
        output = []

        strlist.sort(key = lambda tuple_: tuple_[0][0])
        strlist.sort(key = lambda tuple_: tuple_[0][1])
        strlist.sort(key = lambda tuple_: tuple_[2], reverse = True)
        for tuple_ in strlist:
            output.append([tuple_[0], wrap(tuple_[1],2), tuple_[2]])
        return output

def call(string):
    if string:
        if get_handcards(string):
            handcards = HandCards(get_handcards(string))
            if handcards.shanten() < 0:
                output = handcards.print_jinzhang()
                x = ['聽牌']
                x.extend(output)
                return x
            elif handcards.shanten() == 0:
                output = handcards.print_jinzhang()
                x = ['聽牌']
                x.extend(output)
                return x
            else:
                output = handcards.print_jinzhang()
                x = ['{}向聽'.format(handcards.shanten())]
                x.extend(output)
                return x

if __name__ == '__main__':
    print('欢迎使用麻将向听计算器！')
    print('输入格式：数字+字母，数字为牌的点数，字母为牌的种类，m为万，p为饼，s为索，z为字牌')
    while True:
        string = input('请输入您的手牌: ')
        if string:
            if get_handcards(string):
                handcards = HandCards(get_handcards(string))
                if handcards.shanten() < 0:
                    print('胡了')
                elif handcards.shanten() == 0:
                    output = handcards.print_jinzhang()
                    x = ['聽牌', output]
                    print(x)
                else:
                    output = handcards.print_jinzhang()
                    x = ['{}向聽'.format(handcards.shanten()), output]
                    print(x)
        else:
            break