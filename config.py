class Config:
    def __init__(self):
        self.configPath = 'config.txt'
    
    def getName(self):
        with open(self.configPath, 'r', encoding='utf-8') as file:
            for i in file.readlines():
                if 'name' in i:
                    return str(i.replace('name', '').replace('-', '').strip())