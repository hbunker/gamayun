'''
Contains classes relevant to the QEMs to HTML class
Author: Harris Bunker
Updated: August 2, 2019
'''

import numpy as np
import pandas as pd
import re #regex

class Tossup():
    '''Tossup'''
    def __init__(self,q_text = 'No text', answer = 'No Answer', author = 'No Author', q_id = 9999, packet = 0):
        self.text = q_text
        self.answer = answer
        self.author = author
        self.q_id = q_id
        self.packet = packet
        self.category = None #important to fix
        
    def __repr__(self):
        '''Packet-like representation of a tossup'''
        return '{}\nANSWER: {} <{}>'.format(self.text, self.answer, self.author)
    
    def power(self):
        '''Returns an html formmated question text'''
        splits = self.text.split('(*)')
        power_str = "<b>" + splits[0] + '(*)</b>' + splits[1]
        self.text = power_str
        return self.text
    
    def bold_pg(self):
        '''adds pronounciation guides with bold formatting'''
        temp = self.text.replace('(', '(<b>')
        temp = temp.replace(')', '</b>)')
        temp = temp.replace('(<b>*','(*') #fixes for power marks
        temp = temp.replace('*</b>)','*)')
        self.text = temp
        return self.text
    
    def answer_bold_u(self):
        '''
        Returns answerline formatting including prompts
        '''
        regex_answer = r'(?<=\_)(.*)(?=\_)'
        pattern_answer = r'<b><u>\1</u></b>'
        regex_prompt = r'(?<=\__)(.*)(?=\__)'
        pattern_prompt = r'<u>\1</u>'
        tokens = self.answer.split()

        temp_list = [re.sub(regex_prompt, pattern_prompt,t) for t in tokens]
        no_prompts = " ".join(temp_list).replace('__','') #double 'prompt' underscore
        tokens = no_prompts.split() #remake new tokens for no prompts list

        cleaned_list = [re.sub(regex_answer, pattern_answer, t) for t in tokens] #each word in the answerline
        self.answer = " ".join(cleaned_list).replace('_','')
        return self.answer
    
    def clean_html(self):
        def italicize(mytext):
            '''returns italicized text'''
            regex = r'(?<=\~)(.*)(?=\~)'
            pattern = r"<i>\1</i>"
            splits = mytext.split('.') #split on period
            temp_list = [re.sub(regex, pattern, sent) for sent in splits]
            return '.'.join(temp_list).replace('~','')
        
        #Question TEXT
        powered = self.power()
        pg = self.bold_pg()
        italicized = italicize(pg)
        self.text = italicized
        
        #ANSWER
        self.answer = self.answer_bold_u()
        self.answer = italicize(self.answer)
        #add #<br>tag for new line in printing
        return self
    
class Bonus():
    '''Bonus'''
    
    def __init__(self, lead_in = 'Blank', q_list = ['No text','No text', 'No text'], answer_list = ['No Answer', 'No Answer', 'No Answer'],
                author = 'No Author', q_id = 9999, packet = 0):
        self.lead_in = lead_in
        self.q_list = q_list
        self.answer_list = answer_list
        self.author = author
        self.q_id = q_id
        self.packet = packet
        self.category = None #important to fix
    
    def __repr__(self):
        print_str = '{}\n[10]{}\nANSWER: {}\n[10]{}\nANSWER: {}\n[10]{}\nANSWER: {} <{}>'.format(self.lead_in, 
                                                                 self.q_list[0], self.answer_list[0],
                                                                 self.q_list[1], self.answer_list[1],
                                                                 self.q_list[2], self.answer_list[2], self.author)
        return print_str
    
    def answer_bold_u(self):
        '''
        Returns answerline formatting including prompts
        '''
        regex_answer = r'(?<=\_)(.*)(?=\_)'
        pattern_answer = r'<b><u>\1</u></b>'
        regex_prompt = r'(?<=\__)(.*)(?=\__)'
        pattern_prompt = r'<u>\1</u>'
        temp_list = []
        
        for answer in self.answer_list:
            tokens_answer = answer.split()
            no_prompts_list = [re.sub(regex_prompt, pattern_prompt,t) for t in tokens_answer]
            no_prompts = " ".join(no_prompts_list).replace('__','') #double 'prompt' underscore
            #print('no prompts',no_prompts)
            tokens = no_prompts.split() #remake new tokens for no prompts list

            cleaned_list = [re.sub(regex_answer, pattern_answer, t) for t in tokens] #each word in the answerline
            temp = " ".join(cleaned_list).replace('_','')
            temp_list.append(temp)
        self.answer_list = temp_list #reassign answers to have prompt and answerline formatting
        return self
    
    def bold_pg(self):
        '''adds pronounciation guides with bold formatting'''
        #lead-in
        temp = self.lead_in.replace('(', '(<b>')
        temp = temp.replace(')', '</b>)')
        self.lead_in = temp
        #rest of bonus:
        temp_list = []
        for text in self.q_list:
            temp = text.replace('(', '(<b>')
            temp = temp.replace(')', '</b>)')
            temp_list.append(temp)
        self.q_list = temp_list    
        return self
    
    def clean_html(self):
        '''returns text optimized for html'''
        def italicize(mytext):
            '''returns italicized text'''
            regex = r'(?<=\~)(.*)(?=\~)'
            pattern = r"<i>\1</i>"
            splits = mytext.split('.') #split on period
            temp_list = [re.sub(regex, pattern, sent) for sent in splits]
            return '.'.join(temp_list).replace('~','')
        #QUESTIONS
        self.bold_pg()
        self.lead_in = italicize(self.lead_in) #italics
        temp_list = []
        for q in self.q_list:
            temp = italicize(q)
            temp_list.append(temp)
        self.q_list = temp_list
        #ANSWERS
        self.answer_bold_u()
        temp_list2 = []
        for answer in self.answer_list:
            temp = italicize(answer)
            temp.replace('/(','(') #fix parens
            temp_list2.append(temp)
        self.answer_list = temp_list2    
        return self

class Packet(): #possibly add a way to load in the preamble from a markup file of .txt
    '''Packet with comes with its template and a list of its tossups, bonuses'''
    
    def __init__(self, tu_list, b_list, p_num = 0, 
                 template_tu = np.zeros((20,2), dtype = str), template_b = np.zeros((20,2), dtype = str),
                 size = 20, preamble = ''):
        '''tu_list is made up of Tossup objects, b_list is made up of Bonus objects
        size only works for 20 for now
        preamble is printed at the front of each packet'''
        
        self.number = p_num
        self.template_tu = template_tu #need to make for tossups and bonuses
        self.template_b = template_b
        self.tu_list = tu_list
        self.b_list = b_list
        self.max_size = size #number of tossups or bonuses (e.g. for 20/20 -> 20)   
        #self.ordered = [[],[]] #ordered list of tossups and bonus
        self.preamble = preamble #printed before Tossup 1 for each packet
        
    def __len__(self):
        '''Prints many questions in packets'''
        return len(self.tu_list) + len(self.b_list)
    
    def __repr__(self):
        return 'Packet {} consisting of {} Tossups and {} Bonuses'.format(self.number, len(self.tu_list), 
                                                                          len(self.b_list))
    def __getitem__(self, param): #need to fix
        '''Input: param1 is in {'tossup', 'bonus'} and param2 is a number in {1, ..., max_size}
        Returns: a tossup or bonus
        '''
        #error handling
        if len(param) != 2:
            raise ValueError('Must be a pair of format ("tossup",num) or ("tossup",num)')
        if param[0].lower() not in ["tossup", 'bonus']:
            raise ValueError('First argument must be either "tossup" or "bonus"')
        if param[0].lower() == 'tossup':
            #print('tossup')
            return self.tu_list[param[1] - 1] #support of 1-indexing
        if param[0].lower() == 'bonus':
            #print('bonus')
            return self.b_list[param[1] - 1] #support of 1-indexing
            
        else: #outside the values that currently exist
            raise ValueError('{} is not a valid index'.format(param[1]))
        
    def add(self, item, clean = False):
        #cleaning for HTML formatting
        '''Add tossups and bonuses to a packet'''
        if isinstance(item, Tossup) == True:
                #print('tossup')
            if len(self.tu_list) != self.max_size:
                self.tu_list.append(item)
            else:
                print('Packet {} full of tossups'.format(self.number))
                return self
        elif isinstance(item, Bonus) == True:
            #print('bonus')
            if len(self.b_list) != self.max_size:
                self.b_list.append(item)
            else:
                print('Packet {} full of bonuses'.format(self.number))
                return self
        else:
            raise TypeError("Can't add object of {} type".format(type(item)))
        return self
    
    def to_txt(self):
        fname = './Packet' + str(self.number) + '.txt'
        wp = open(fname, 'w')
        wp.write(self.preamble)
        #wp.write('') #blank line
        wp.write('\nPacket ' + str(self.number) + '\n\n')
        #Tossups
        wp.write('\nTossups:\n\n')
        count = 0
        for t in self.tu_list:
            count += 1 
            wp.write(str(count) + '. ' + str(t))
            wp.write('\n\n')
        #Bonuses    
        wp.write('Bonuses:\n\n')
        count = 0
        for b in self.b_list:
            count += 1
            wp.write(str(count) + '. ' + str(b))
            wp.write('\n\n')
        wp.close()
        return 'file saved at {}'.format(fname)
    
    def to_html(self):
        #lead-in
        fname = './Packet' + str(self.number) + '.html'
        wp = open(fname,'w')
        wp.write('<html>\n<head>\n<title>' + 'Packet' + str(self.number) + '</title>\n') #title
        wp.write('<br><p><font size="6">' + 'Packet' + str(self.number) + '</font></p>')
        wp.write('<body>')
        wp.write('<p>' + self.preamble + '</p>')
        wp.write('<br><p>Tossups:</p><br>')
        count = 0
        for t in self.tu_list:
            count += 1
            wp.write('<p>' + str(count) + '. ' + str(t).replace('\n','<br>') + '</p>')
            #wp.write('<br>')
        count = 0
        wp.write('<br><p>Bonues:</p><br>')
        for b in self.b_list:
            count += 1
            wp.write('<p>' + str(count) + '. ' + str(b).replace('\n','<br>') + '</p>')
            #wp.write('<br>')
        wp.write("</body>\n</html>")                            
        wp.close()
        return 'file saved at' + fname
    
    def randomize(self, random = True):
        if random == True:
            #uses np.random.shuffle() on tossup and bonus lists
            np.random.seed(328)
            np.random.shuffle(self.tu_list)
            np.random.shuffle(self.b_list)
        if random == False:
            #use a pre-built template #need to build-out
            if self.template_tu.size != (self.max_size,2):
                raise ValueError('Template is not of correct size or is empty.\n It should be of (max_length, 2) size (e.g. 20 x 2)')
            else:
                pass #need to build out
        
        print('randomized')
        return self