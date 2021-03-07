import string
import random
import os

def list_flattener(item):
    temp = []
    for i in item:
        if type(i) != list:
            temp.append(i)
        else:
            for x in list_flattener(i):
                temp.append(x)
    return temp

def list_to_coord(list):
    coord = ''
    for pos in list:
        coord += '[{}]'.format(pos)
    return coord

def list_flattener(item):
    temp = []
    for i in item:
        if type(i) == str:
            temp.append(i)
        else:
            for x in list_flattener(i):
                temp.append(x)
    return temp

class PositionsTree:
    def __init__(self,depth, length):
        self.depth = depth
        self.length = length
        self.root = TreeNode(None,None,False)
        self.gen_main()

    def gen_main(self):
        self.generate_children_recursive(self.depth, self.root)

    def generate_children_recursive(self, depth, target):
        if depth > 1:
            target.generate_children(self.length)
            for child in target.children:
                self.generate_children_recursive(depth - 1, child)
        else:
            target.generate_children(self.length, True)

    def get_pos_main(self):
        if self.root.children != []:
            return self.get_pos_recursive(self.root,[])

    def get_pos_recursive(self,target,pos):
        if not target.base:
            # print(target.number,[i.number for i in target.children])
            chosen = random.choice(target.children)
            chosen.check_filled()
            pos.append(chosen.number)
            return self.get_pos_recursive(chosen, pos)
        else:
            return pos

    def remove_position(self,position):
        target = self.root
        for coord in position:
            target = target.children[coord]
            target.check_filled()

class TreeNode:
    def __init__(self,number,parent,base = False):
        self.number = number
        self.parent = parent
        self.base = base
        self.children = []

    def generate_children(self,length,base = False):
        for i in range(length):
            new = TreeNode(i,self,base)
            self.children.append(new)

    def check_filled(self):
        # print('self = {}, children = {}'.format(self.number,','.join(str(child.number) for child in self.children)))
        if self.parent is None:
            return
        elif self.base or len(self.children) == 0:
            self.parent.children.remove(self)
            self.parent.check_filled()

class EncryptFile:
    ### address obsfucation ---> len(self.lookuptable) / self.grid_size
    ### after address chosen then random.choice(limited range representing same position)
    def __init__(self,**kwargs):

        self.lookuptable = string.ascii_letters + ' \n\t' + string.digits + string.punctuation

        if 'chunk_length' in kwargs:
            self.chunk_length = kwargs['chunk_length']
        else:
            self.chunk_length = 3

        if 'grid_size' in kwargs:
            self.grid_size = kwargs['grid_size']
        else:
            self.grid_size = len(self.lookuptable)

        if 'deciphering' in kwargs:
            self.deciphering = kwargs['deciphering']
        else:
            self.deciphering = False

        if 'file' in kwargs:
            if os.path.exists(kwargs['file']):
                with open(kwargs['file'],'r') as file:
                    lines = file.readlines()
                    self.text = ''.join(lines)
        elif 'text' in kwargs:
            self.text = kwargs['text']
        else:
            print('Enter Text')
            return

        self.input_text()

        if 'password' in kwargs:
            self.format_password(kwargs['password']) #create attribute self.password_variables
            self.reorder_table_key(self.password_values[1])
            self.password_authentication()
        else:
            print('Enter Password')
            return

        self.text_to_chunk()
        if self.deciphering:
            self.fill_grid_main()
            self.decrypt_main()
        else:
            self.chunk_to_grid()

    def generate_possible_positions(self,num_coords = 2):
        self.possible_positions = PositionsTree(num_coords,self.grid_size)
        self.grid = ['']*self.grid_size
        self.generate_grid_recursive(self.grid, num_coords - 1)

    def generate_grid_recursive(self,grid,num_coords = 2):
        if num_coords > 0:
            for x in range(self.grid_size):
                grid[x] = ['']*self.grid_size
            for x in range(self.grid_size):
                self.generate_grid_recursive(grid[x],num_coords-1)

    def format_password(self,password):
        password = str(password)
        if password.isnumeric():
            password_values = []
            for i in range(0,len(password),2):
                password_values.append(str(int(password[i:i + 2]) % len(self.lookuptable)))
            for index,value in enumerate(password_values):
                password_values[index] = self.lookuptable[int(value)]
            password_values = password,''.join(password_values)
        elif password.isalnum():
            password_values = []
            for char in password:
                password_values.append(self.lookuptable.index(char))
            password_values = ''.join([str(i) for i in password_values]),password
        self.password_values = password_values

    def password_authentication(self):
        # from password to starting position
        key = self.password_values[0]
        section_length = len(key)//self.num_coords
        sections = [key[i:i+section_length] for i in range(0,len(key),section_length)]
        if len(sections) > self.num_coords:
            sections[-2] += sections[-1]
            sections.pop(-1)
        key_pos = [int(section) % self.grid_size for section in sections]
        self.key_pos = key_pos

    def reorder_table_key(self,key_string):
        temp = list(key_string + self.lookuptable)
        temp = ''.join(list(dict.fromkeys(temp)))
        self.lookuptable = temp

    def input_text(self):
        length_text = len(self.text)

        if not self.deciphering:
           self.text = self.text + 'eot_one' + str(length_text) + 'eot_two' #eot = endoftext
           length_text = len(self.text)

        self.num_coords = 2
        if not self.deciphering:
            max_in_grid = (self.grid_size ** self.num_coords) * self.chunk_length
            while length_text > max_in_grid:
                print('Text too large')
                self.num_coords += 1
                max_in_grid = (self.grid_size ** self.num_coords) * self.chunk_length
        else:
            max_in_grid = (self.grid_size ** self.num_coords) * (self.chunk_length + self.num_coords)
            while length_text > max_in_grid:
                print('Text too large')
                self.num_coords += 1
                max_in_grid = (self.grid_size ** self.num_coords) * (self.chunk_length + self.num_coords)
        self.generate_possible_positions(self.num_coords)

    def text_to_chunk(self):
        if not self.deciphering:
            chunk_length = self.chunk_length
        else:
            chunk_length = self.chunk_length + self.num_coords

        temp_string = ''
        self.chunks = []

        # split text into chunks
        for char in self.text:
            if len(temp_string) < chunk_length:
                temp_string += char
            else:
                self.chunks.append(temp_string)
                temp_string = ''
                temp_string += char
        if len(temp_string) == chunk_length:
            self.chunks.append(temp_string)
            temp_string = ''

        if not self.deciphering:
            # fill in remainder of temp_string with gibberish
            if len(temp_string) < chunk_length:
                while len(temp_string) < chunk_length:
                    random_char = random.choice(list(self.lookuptable))
                    temp_string += random_char
                self.chunks.append(temp_string)
            else:
                self.chunks.append(temp_string)

            # fill in remainder of break_up_text with gibberish
            while len(self.chunks) < (self.grid_size ** 2):
                temp_add = []
                for i in range(chunk_length):
                    temp_add.append(random.choice(list(self.lookuptable)))
                temp_string = ''.join(temp_add)
                self.chunks.append(temp_string)

    def chunk_to_grid(self):
        ##does coordinate lookup intefere with postions?
        for i in range(len(self.chunks)):
            if i == 0:
                # if first iteration
                # input encrypted text there @ key position
                # random next position
                # first_row,first_column = key_row,key_column
                self.possible_positions.remove_position(self.key_pos)
                curr_pos = self.key_pos
                next_pos = self.possible_positions.get_pos_main()
                pointer = ''.join([self.lookuptable[coord] for coord in next_pos])
                str_curr_pos = list_to_coord(curr_pos)
                result_chunk = self.chunks[i]+pointer
                ciphered_chunk = self.cipher(self.key_pos,result_chunk)
                exec('self.grid{} = {}'.format(str_curr_pos, repr(ciphered_chunk)))

            elif i == len(self.chunks) - 1:
                # if grid is filled
                prev_pos = curr_pos
                curr_pos = next_pos
                pointer = ''.join([self.lookuptable[coord] for coord in self.key_pos])
                str_curr_pos = list_to_coord(curr_pos)
                result_chunk = self.chunks[i] + pointer
                ciphered_chunk = self.cipher(prev_pos, result_chunk)

                exec('self.grid{} = {}'.format(str_curr_pos, repr(ciphered_chunk)))
            else:
                # all other cases
                prev_pos = curr_pos
                curr_pos = next_pos
                next_pos = self.possible_positions.get_pos_main()
                pointer = ''.join([self.lookuptable[coord] for coord in next_pos])
                str_curr_pos = list_to_coord(curr_pos)
                result_chunk = self.chunks[i] + pointer
                ciphered_chunk = self.cipher(prev_pos, result_chunk)
                exec('self.grid{} = {}'.format(str_curr_pos, repr(ciphered_chunk)))

    def cipher(self,prev_pos,chunk):
        new_chunk = ''
        shift = sum(prev_pos)
        for index, char in enumerate(chunk):
            shift += index
            current_pos = self.lookuptable.index(char)
            new_pos = (current_pos + shift) % len(self.lookuptable)
            new_chunk += self.lookuptable[new_pos]
        self.lookuptable = ''.join(dict.fromkeys(list(chunk + self.lookuptable)).keys())
        return new_chunk

    def reorder_lookup(self,pos1,pos2):
        first = min(pos1, pos2)
        last = max(pos1, pos2)
        self.lookuptable = self.lookuptable[last:] + \
                           self.lookuptable[:first+1] + \
                           self.lookuptable[last:first:-1]

    def fill_grid_main(self):
        self.fill_grid_recursive(self.grid)

    def fill_grid_recursive(self,target):
        switch = False
        for index,value in enumerate(target):
            if type(value) == list:
                switch = True
                self.chunks = self.fill_grid_recursive(target[index])
            else:
                target[index] = self.chunks[index]
        if not switch:
            return self.chunks[index+1:]
        else:
            return self.chunks

    def decrypt_main(self):
        str_key_pos = list_to_coord(self.key_pos)
        self.full_message = ''

        result_chunk = self.decipher(self.key_pos,eval('self.grid{}'.format(str_key_pos)))
        message_text,pointer = result_chunk[:-self.num_coords],result_chunk[-self.num_coords:]
        self.full_message += message_text
        prev_pos = self.key_pos
        next_pos = [self.lookuptable.index(pos) for pos in pointer]
        str_next_pos = list_to_coord(next_pos)
        self.lookuptable = ''.join(dict.fromkeys(list(result_chunk + self.lookuptable)).keys())
        while 'eot_one' not in self.full_message or 'eot_two' not in self.full_message:
            result_chunk = self.decipher(prev_pos, eval('self.grid{}'.format(str_next_pos)))
            message_text, pointer = result_chunk[:-self.num_coords], result_chunk[-self.num_coords:]
            self.full_message += message_text
            prev_pos = next_pos
            next_pos = [self.lookuptable.index(pos) for pos in pointer]
            self.lookuptable = ''.join(dict.fromkeys(list(result_chunk + self.lookuptable)).keys())
            str_next_pos = list_to_coord(next_pos)
        self.full_message = self.full_message[:self.full_message.find('eot_one')]

    def decipher(self,prev_pos,chunk):
        new_chunk = ''
        shift = sum(prev_pos)
        for index,char in enumerate(chunk):
            shift += index
            current_pos = self.lookuptable.index(char)
            new_pos = (current_pos - shift) % len(self.lookuptable)
            new_chunk += self.lookuptable[new_pos]
        return new_chunk

    def grid_to_text(self):
        output = ''.join(list_flattener(self.grid))
        return output

    def output_encrypted(self):
        return self.chunk_length,self.grid_size,self.grid_to_text()

def main(**kwargs):
    new = EncryptFile(**kwargs)
    if 'deciphering' not in kwargs or not kwargs['deciphering']:
        return (new.output_encrypted())
    else:
        return (new.full_message)

test = main(chunk_length=4,grid_size=5,password='4356535457',text='test')


