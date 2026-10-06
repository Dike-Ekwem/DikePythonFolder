#BUILD AN RPG CHARACTER

full_dot = '●'
empty_dot = '○'

def create_character(character_name, strength, intelligence, charisma):
    
    #name
    if not isinstance(character_name, str):
        return 'The character name should be a string'
    if character_name =='':
        return 'The character should have a name'
    if len(character_name) > 10:
        return 'The character name is too long'
    if ' ' in character_name:
        return 'The character name should not contain spaces'
    
    #stats
    stats = [strength, intelligence, charisma]
    if not all(isinstance(stat, int) for stat in stats):
        return 'All stats should be integers'
    if any(stat < 1 for stat in stats):
        return 'All stats should be no less than 1'
    if any(stat > 4 for stat in stats):
        return 'All stats should be no more than 4'
    if sum(stats) != 7:
        return 'The character should start with 7 points'

    #After every other thing has been validated...
    labels = ["STR", "INT", "CHA"]
    output = [character_name]
    for label, stat in zip(labels, stats):
        output.append(f'{label} {full_dot * stat}{empty_dot * (10 - stat)}')
    return '\n'.join(output)  

print(create_character('ren', 4, 2, 1))