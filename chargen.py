'''
Created on Feb 6, 2026

@author: tim
'''
import random
import re

debug_level = 0

ability_list = {"STR":0, "DEX":0, "CON":0, "INT":0, "WIS":0, "CHA":0}

race_list = {
        "dwarf" :       {
                            "ability_adjustments": {"CON":1,"CHA":-1}, 
                            "classes" : ["assassin","cleric","fighter","thief","fighter/thief"],
                            "languages" : ["common","dwarfish","gnomish","goblin","kobold","orcish","alignment tongue"],
                            "min ability scores" : {"STR":8, "DEX":3, "CON":12, "INT":3, "WIS":3, "CHA":3},
                            "max ability scores" : {"STR":18, "DEX":17, "CON":19, "INT":18, "WIS":18, "CHA":16},
                            "movement" : "90ft",
                            "height" : {"base":4.0,  "mod die":"3d4"},
                            "weight" : {"base":150.0, "mod die":"5d10"},
                            "age": {"cleric": "2d20+250","fighter":"5d4+40","thief":"3d6+75","assassin":"3d6+75"}
                        },
        "elf" :         {
                            "ability_adjustments": {"DEX":1,"CON":-1}, 
                            "classes": ["assassin","cleric","fighter","magic-user","thief","fighter/magic-user", "fighter/thief", "magic-user/thief", "fighter/magic-user/thief"],
                            "languages": ["common","elven","gnoll","gnomish","goblin","halfling","hobgoblin","orcish","alignment tongue"],
                            "min ability scores" : {"STR":3, "DEX":7, "CON":6, "INT":8, "WIS":3, "CHA":8},
                            "max ability scores" : {"STR":18, "DEX":19, "CON":18, "INT":18, "WIS":18, "CHA":18},
                            "movement" : "120ft",
                            "height" : {"base":4.5,  "mod die":"3d4"},
                            "weight" : {"base":70.0, "mod die":"5d10"},
                            "age":{"cleric":"10d10+500","fighter":"5d6+130","magic-user":"5d6+150","thief":"5d6+100","assassin":"5d6+100"}
                            
                        },
        "gnome" :       {
                            "classes": ["assassin","cleric", "fighter","illusionist", "thief", "fighter/illusionist", "fighter/thief", "illusionist/thief"],
                            "languages" : ["common","dwarfish","gnomish","goblin","halfling","kobold","burrowing animals","alignment tongue"],
                            "min ability scores" : {"STR":6, "DEX":7, "CON":8, "INT":7, "WIS":3, "CHA":3},
                            "max ability scores" : {"STR":18, "DEX":18, "CON":18, "INT":18, "WIS":18, "CHA":18},
                            "movement" : "90ft",
                            "height" : {"base":2.83,  "mod die":"3d4"},
                            "weight" : {"base":45.0, "mod die":"4d10"},
                            "age": {"cleric":"3d12+300","fighter":"5d4+60","illusionist":"2d12+100","thief":"5d4+80","assassin":"5d4+80"}
                        },
        "half-elf" :    {
                            "classes": ["assassin", "cleric", "druid", "fighter", "magic-user", "ranger", "thief", "cleric/fighter", "cleric/ranger", "cleric/magic-user", "fighter/magic-user", "fighter/thief", "cleric/fighter/magic-user", "fighter/magic-user/thief"],
                            "languages" : ["common","elven","gnoll","gnomish","goblin","halfling","hobgoblin","orcish","alignment tongue"],
                            "min ability scores" : {"STR":3, "DEX":6, "CON":8, "INT":4, "WIS":3, "CHA":3},
                            "max ability scores" : {"STR":18, "DEX":18, "CON":18, "INT":18, "WIS":18, "CHA":18},
                            "movement" : "120ft",
                            "height" : {"base":5.0,  "mod die":"4d4"},
                            "weight" : {"base":90.0, "mod die":"5d10"},
                            "age" : {"cleric":"2d4+40","druid":"2d4+40","fighter":"3d4+22","ranger":"3d4+22","magic-user":"2d8+30","thief":"3d8+22","assassin":"3d8+22"}
                        },
        "halfling" :    {
                            "ability_adjustments": {"DEX":1,"STR":-1}, 
                            "classes" : ["fighter", "druid", "thief", "fighter/thief"],
                            "languages" : ["common","dwarfish","gnomish","goblin","halfling","orcish","alignment tongue"],
                            "min ability scores" : {"STR":6, "DEX":8, "CON":10, "INT":6, "WIS":3, "CHA":3},
                            "max ability scores" : {"STR":17, "DEX":18, "CON":19, "INT":18, "WIS":17, "CHA":18},
                            "movement" : "90ft",
                            "height" : {"base":2.83,  "mod die":"3d4"},
                            "weight" : {"base":45.0, "mod die":"4d10"},
                            "age" : {"fighter":"3d4+20","druid":"3d4+40","thief":"2d4+40"}
                        },
        "half-orc" :    {
                            "ability_adjustments": {"STR":1,"CON":1},"CHA":-2, 
                            "classes" : ["assassin", "cleric", "fighter", "thief", "cleric/fighter", "cleric/thief", "cleric/assassin", "fighter/thief", "fighter/assassin"],
                            "languages" : ["common","orcish","alignment tongue"],
                            "min ability scores" : {"STR":6, "DEX":3, "CON":13, "INT":3, "WIS":3, "CHA":3},
                            "max ability scores" : {"STR":18, "DEX":17, "CON":19, "INT":17, "WIS":14, "CHA":12},
                            "movement" : "120ft",
                            "height" : {"base":5.5,  "mod die":"3d4"},
                            "weight" : {"base":150.0, "mod die":"5d10"},
                            "age" : {"cleric":"1d4+20","fighter":"1d4+13","thief":"2d4+20","assassin":"2d4+20"}
                        },
        "human" :       {
                            "classes": ["assassin","cleric","druid","fighter","illusionist","magic-user","monk","paladin","ranger","thief"],
                            "languages" : ["common","alignment tongue"],
                            "movement" : "120ft",
                            "height" : {"base":5.33,  "mod die":"3d4"},
                            "weight" : {"base":140.0, "mod die":"6d10"},
                            "age" : {"cleric":"1d4+20","druid":"1d4+20","monk":"1d4+20","fighter":"1d4+15","paladin":"1d4+15","ranger":"1d4+15","magic-user":"2d8+24","illusionist":"2d8+24","thief":"1d4+20","assassin":"1d4+20"}
                        }
    }

class_specs = {
        "assassin":     {
                            "min_scores" : {"STR":12,  "DEX":12,   "CON":6,    "INT":11,   "WIS":6},
                            "max level": 15,
                            "hit_die":["1d6","2d6","3d6","4d6","5d6","6d6","7d6","8d6","9d6","10d6","11d6","12d6","13d6","14d6","15d6"],
                            "hit_die_max":15,
                            "xp levels":[0,1500,3000,6000,12000,25000,50000,100000,200000,300000,450000,600000,750000,1000000,1500000],
                            "alignment": {"lnc": "any", "gne": "evil"},
                            "prime_req":"none",
                            "shields_allowed":"any",
                            "armor_allowed": ["leather","studded leather"],
                            "weapons_allowed": "any",
                            "weapon_proficiencies":3,
                            "nonproficiency_penalty":-3,
                            "weapon_specialization":"no",
                            "gold":{"die":"2d6","multiplier":10},
                            "saving throws": [
                                                {"aimed magic items": 14, "breath weapons": 16, "death/paralysis/poison" : 13, "petrification/polymorph": 12, "spells": 15},
                                            ],
                            "to-hit table" : [#  10  9  8  7  6  5  4  3  2  1 0  -1 -2 -3 -4 -5 -6 -7 -8 -9 -10
                                                [11,12,13,14,15,16,17,18,19,20,20,20,20,20,20,21,22,23,24,25,26]
                                            ]
                        },
                            
        "cleric":       {
                            "min_scores" : {"STR":6,               "CON":6,    "INT":6,    "WIS":9,    "CHA":6},
                            "max level": 20,
                            "hit_die":["1d8","2d8","3d8","4d8","5d8","6d8","7d8","8d8","9d8","9d8+2","9d8+4","9d8+6","9d8+8","9d8+10","9d8+12","9d8+14","9d8+16","9d8+18","9d8+20","9d8+22"],
                            "hit_die_max":9,
                            "xp levels":[0,1500,3000,6000,13000,27000,55000,110000,220000,450000,675000,900000,1125000,1350000,1575000,1800000,2050000,2300000,2550000,2700000],
                            "alignment": {"lnc": "any", "gne": "any"},
                            "prime_req":{"xp_bonus":0.1, "min_stats": {"WIS":16}},
                            "shields_allowed":"any",
                            "armor_allowed": "any",
                            "weapons_allowed": ["club","flail","hammer","mace","staff","torch","flaming oil (special)"],
                            "weapon_proficiencies":2,
                            "nonproficiency_penalty":-3,
                            "weapon_specialization":"no",
                            "gold":{"die":"3d6","multiplier":10},
                            "saving throws": [
                                                {"aimed magic items": 14, "breath weapons": 16, "death/paralysis/poison" : 10, "petrification/polymorph": 13, "spells": 15},
                                            ],
                            "to-hit table" : [#  10  9  8  7  6  5  4  3  2  1  0 -1 -2 -3 -4 -5 -6 -7 -8 -9 -10
                                                [10,11,12,13,14,15,16,17,18,19,20,20,20,20,20,20,21,22,23,24,25]
                                            ]
                        },
        
        "druid":        
                        {
                            "min_scores" : {"STR":6,               "CON":6,    "INT":6,    "WIS":12,   "CHA":15},
                            "max level":14,
                            "hit_die":["1d8","2d8","3d8","4d8","5d8","6d8","7d8","8d8","9d8","10d8","11d8","12d8","13d8","14d8"],                            
                            "hit_die_max":14,
                            "xp levels":[0,2000,4000,8000,12000,20000,35000,60000,90000,125000,200000,300000,750000,1500000],
                            "alignment": {"lnc": "any", "gne": "neutral"},
                            "prime_req":{"xp_bonus":0.1, "min_stats": {"WIS":16,"CHA":16}},
                            "shields_allowed":"wooden shields",
                            "armor_allowed": "leather",
                            "weapons_allowed": ["club","dagger","dart","hammer","scimitar","sling","spear","staff","torch","flaming oil (special)"],
                            "weapon_proficiencies":2,
                            "nonproficiency_penalty":-4,
                            "weapon_specialization":"no",
                            "gold":{"die":"3d6","multiplier":10},
                            "saving throws": [
                                                {"aimed magic items": 14, "breath weapons": 16, "death/paralysis/poison" : 10, "petrification/polymorph": 13, "spells": 15},
                                            ],
                            "to-hit table" : [#  10  9  8  7  6  5  4  3  2  1  0 -1 -2 -3 -4 -5 -6 -7 -8 -9 -10
                                                [10,11,12,13,14,15,16,17,18,19,20,20,20,20,20,20,21,22,23,24,25]
                                            ]
                        },
                        
        "fighter":      
                        {
                            "min_scores" : {"STR":9,   "DEX":6,    "CON":7,    "INT":3,    "WIS":6,    "CHA":6},
                            "max level": 20,
                            "hit_die":["1d10","2d10","3d10","4d10","5d10","6d10","7d10","8d10","9d10","9d10+3","9d10+3","9d10+6","9d10+9","9d10+12","9d10+15","9d10+18","9d10+21","9d10+24","9d10+27","9d10+30","9d10+33"],                            
                            "hit_die_max":9,
                            "xp levels" : [0,2000,4000,8000,17000,35000,70000,125000,250000,500000,750000,1000000,1250000,1500000,1750000,2000000,2250000,2500000,2750000,3000000],
                            "alignment": {"lnc": "any", "gne": "any"},
                            "prime_req":{"xp_bonus":0.1, "min_stats": {"STR":16}},
                            "shields_allowed":"any",
                            "armor_allowed": "any",
                            "weapons_allowed": "any",
                            "weapon_proficiencies":4,
                            "nonproficiency_penalty":-2,
                            "weapon_specialization":"optional",
                            "gold":{"die":"5d4","multiplier":10},
                            "saving throws": [
                                                {"aimed magic items": 18, "breath weapons": 20, "death/paralysis/poison" : 16, "petrification/polymorph": 17, "spells": 19},
                                            ],
                            "to-hit table" : [#  10  9  8  7  6  5  4  3  2  1  0 -1 -2 -3 -4 -5 -6 -7 -8 -9 -10
                                                [10,11,12,13,14,15,16,17,18,19,20,20,20,20,20,20,21,22,23,24,25]
                                            ]                        
                        },
        "illusionist":  
                        {
                            "min_scores": {"STR":6,   "DEX":16,               "INT":15,   "WIS":6,    "CHA":6},
                            "max level": 20,
                            "hit_die": ["1d4","2d4","3d4","4d4","5d4","6d4","7d4","8d4","9d4","10d4","10d4+1","10d4+2","10d4+3","10d4+4","10d4+5","10d4+6","10d4+7","10d4+8","10d4+9","10d4+10"],
                            "hit_die_max":10,
                            "xp levels": [0,2500,4750,9000,18000,35000,60000,95000,145000,220000,440000,660000,880000,1100000,1320000,1540000,1760000,1980000,2200000,2420000],
                            "alignment": {"lnc": "any", "gne": "any"},
                            "prime_req": "none",
                            "shields_allowed":"none",
                            "armor_allowed": "none",
                            "weapons_allowed": ["dagger","dart","oil","staff"],
                            "weapon_proficiencies":1,
                            "nonproficiency_penalty":-5,
                            "weapon_specialization":"no",
                            "gold":{"die":"2d4","multiplier":10},
                            "saving throws": [
                                                {"aimed magic items": 11, "breath weapons": 15, "death/paralysis/poison" : 14, "petrification/polymorph": 13, "spells": 12},
                                            ],
                            "to-hit table" : [#  10  9  8  7  6  5  4  3  2  1  0 -1 -2 -3 -4 -5 -6 -7 -8 -9 -10
                                                [11,12,13,14,15,16,17,18,19,20,20,20,20,20,20,21,22,23,24,25,26]
                                            ]    
                        },
        "magic-user":   
                        {
                            "min_scores" : {           "DEX":6,    "CON":6,    "INT":9,    "WIS":6,    "CHA":6},
                            "max level" : 20,
                            "hit_die": ["1d4","2d4","3d4","4d4","5d4","6d4","7d4","8d4","9d4","10d4","11d4","11d4+1","11d4+2","11d4+3","11d4+4","11d4+5","11d4+6","11d4+7","11d4+8","11d4+9"],
                            "hit_die_max":10,
                            "xp levels": [0,2400,4800,10250,22000,40000,60000,80000,140000,250000,375000,750000,1125000,1500000,1875000,2250000,2625000,3000000,3375000,3750000],
                            "alignment": {"lnc": "any", "gne": "any"},
                            "prime_req": {"xp_bonus":0.1, "min_stats": {"INT":16}},
                            "shields_allowed":"none",
                            "armor_allowed": "none",
                            "weapons_allowed": ["dagger","dart","oil","staff"],
                            "weapon_proficiencies":1,
                            "nonproficiency_penalty":-5,
                            "weapon_specialization":"no",
                            "gold":{"die":"2d4","multiplier":10},
                            "saving throws": [
                                                {"aimed magic items": 11, "breath weapons": 15, "death/paralysis/poison" : 14, "petrification/polymorph": 13, "spells": 12},
                                            ],
                            "to-hit table" : [#  10  9  8  7  6  5  4  3  2  1  0 -1 -2 -3 -4 -5 -6 -7 -8 -9 -10
                                                [11,12,13,14,15,16,17,18,19,20,20,20,20,20,20,21,22,23,24,25,26]
                                            ]                                
                        },
        "monk":         
                        {
                            "min_scores" : {"STR":10,  "DEX":15,                           "WIS":10,},
                            "max level": 17,
                            "hit_die":["2d4","3d4","4d4","5d4","6d4","7d4","8d4","9d4","10d4","11d4","12d4","13d4","14d4","15d4","16d4","17d4","18d4"],
                            "hit_die_max":18,
                            "xp levels" : [0,2000,5000,10000,21250,45000,100000,200000,350000,500000,700000,950000,1250000,1750000,2250000,1750000,3250000],
                            "alignment": {"lnc": "lawful", "gne": "any"},
                            "prime_req": "none",
                            "shields_allowed":"none",
                            "armor_allowed": "none",
                            "weapons_allowed": ["club","crossbow","dagger","hand axe","javelin","pole arm","spear","staff"],
                            "weapon_proficiencies":1,
                            "nonproficiency_penalty":-3,
                            "weapon_specialization":"no",
                            "gold":{"die":"5d4","multiplier":1},
                            "saving throws": [
                                                {"aimed magic items": 14, "breath weapons": 16, "death/paralysis/poison" : 13, "petrification/polymorph": 12, "spells": 15},
                                            ],
                            "to-hit table" : [#  10  9  8  7  6  5  4  3  2  1  0 -1 -2 -3 -4 -5 -6 -7 -8 -9 -10
                                                [10,11,12,13,14,15,16,17,18,19,20,20,20,20,20,20,21,22,23,24,25]
                                            ]                                 
                        },
        "paladin":      
                        {
                            "min_scores" : {"STR":12,  "DEX":6,    "CON":9,    "INT":9,    "WIS":13,   "CHA":17},
                            "max level": 20,
                            "hit_die":["1d10","2d10","3d10","4d10","5d10","6d10","7d10","8d10","9d10","9d10+3","9d10+3","9d10+6","9d10+9","9d10+12","9d10+15","9d10+18","9d10+21","9d10+24","9d10+27","9d10+30","9d10+33"],                            
                            "hit_die_max":9,
                            "xp levels" : [0,2550,5500,12500,25000,45000,95000,175000,325000,600000,1000000,1350000,1700000,2050000,2400000,2750000,3100000,3450000,3800000,4150000],
                            "alignment": {"lnc": "lawful", "gne": "good"},
                            "prime_req": {"xp_bonus":0.1, "min_stats": {"STR":16,"WIS":16}},
                            "shields_allowed":"any",
                            "armor_allowed": "any",
                            "weapons_allowed": "any",
                            "weapon_proficiencies":3,
                            "nonproficiency_penalty":-2,
                            "weapon_specialization":"optional",
                            "gold":{"die":"5d4","multiplier":10},
                            "saving throws": [
                                                {"aimed magic items": 14, "breath weapons": 15, "death/paralysis/poison" : 12, "petrification/polymorph": 13, "spells": 15},
                                            ],
                            "to-hit table" : [#  10  9  8  7  6  5  4  3  2  1  0 -1 -2 -3 -4 -5 -6 -7 -8 -9 -10
                                                [10,11,12,13,14,15,16,17,18,19,20,20,20,20,20,20,21,22,23,24,25]
                                            ]                                 
                        },
        "ranger":       
                        {
                            "min_scores" : {"STR":13,  "DEX":6,    "CON":14,   "INT":13,   "WIS":14,   "CHA":6},
                            "max level": 20,
                            "hit_die":["2d8","3d8","4d8","5d8","6d8","7d8","8d8","9d8","10d8","11d8","11d8+2","11d8+4","11d8+6","11d8+8","11d8+10","11d8+12","11d8+14","11d8+16","11d8+18","11d8+20"],                            
                            "hit_die_max":11,
                            "xp levels": [0,2250,4500,9500,20000,40000,90000,150000,225000,325000,650000,975000,1300000,1625000,1950000,2275000,2600000,2925000,3250000,3575000],
                            "alignment": {"lnc": "any", "gne": "good"},
                            "prime_req": {"xp_bonus":0.1, "min_stats": {"STR":16,"INT":16,"WIS":16}},
                            "shields_allowed":"any",
                            "armor_allowed": "any",
                            "weapons_allowed": "any",
                            "weapon_proficiencies":3,
                            "nonproficiency_penalty":-2,
                            "weapon_specialization":"optional",
                            "gold":{"die":"5d4","multiplier":10},
                            "saving throws": [
                                                {"aimed magic items": 16, "breath weapons": 17, "death/paralysis/poison" : 14, "petrification/polymorph": 15, "spells": 17},
                                            ],
                            "to-hit table" : [#  10  9  8  7  6  5  4  3  2  1  0 -1 -2 -3 -4 -5 -6 -7 -8 -9 -10
                                                [11,12,13,14,15,16,17,18,19,20,20,20,20,20,20,21,22,23,24,25,26]
                                            ]                                 
                        },
        "thief":        
                        {
                            "min_scores" : {"STR":6,   "DEX":9,    "CON":6,    "INT":6,                "CHA":6},
                            "max level": 20,
                            "hit_die":["1d6","2d6","3d6","4d6","5d6","6d6","7d6","8d6","9d6","10d6","10d6+2","10d6+4","10d6+6","10d6+8","10d6+10","10d6+12","10d6+14","10d6+16","10d6+18","10d6+20"],                            
                            "hit_die_max":10,
                            "xp levels":[0,1250,2500,5000,10000,20000,40000,70000,110000,160000,220000,440000,660000,880000,1100000,1320000,1540000,1760000,1980000,2200000],
                            "alignment": {"lnc": "any", "gne": "neutral/evil"},
                            "prime_req": {"xp_bonus":0.1, "min_stats": {"STR":16,"INT":16,"WIS":16}},
                            "shields_allowed":"any",
                            "armor_allowed": "any",
                            "weapons_allowed": "any",
                            "weapon_proficiencies":3,
                            "nonproficiency_penalty":-2,
                            "weapon_specialization":"optional",
                            "gold":{"die":"5d4","multiplier":10},
                            "saving throws": [
                                                {"aimed magic items": 14, "breath weapons": 16, "death/paralysis/poison" : 13, "petrification/polymorph": 12, "spells": 15},
                                            ],
                            "to-hit table" : [#  10  9  8  7  6  5  4  3  2  1  0 -1 -2 -3 -4 -5 -6 -7 -8 -9 -10
                                                [11,12,13,14,15,16,17,18,19,20,20,20,20,20,20,21,22,23,24,25,26]
                                            ]                               
                        }
    }

score_gen_method = 1

MAGIC_USER_SPELLS = [
        # Level 1
        ["affect normal fires","burning hands","charm person","comprehend languages","dancing lights","detect magic","enlarge","erase","feather fall","find familiar","friends","hold portal","identify","jump","light","niam's magic aura","magic missile","mending","message","protection from evil","push","read magic","shield","shocking grasp","sleep","spider climb","tanzur's floating disk","unseen servant","ventriloquism","write"],
    ]

ILLUSIONIST_SPELLS = [
        # Level 1
        ["audible glamour","change self","colour spray","dancing lights","darkness","detect illusion","detect invisibility","gaze reflection","hypnotism","light","phantasmal force","wall of fog"]
    ]

def is_integer(val):
    try:
        val=int(val)
    except:
        pass
    return isinstance(val, int)

def select_ability_generation_method():
    
    while True:
        print("Select rolling method:")
        print("0. Pre-defined")
        print("1. Hard mode")
        print("2. Difficult mode")
        print("3. Normal mode")
        print("4. Flexible mode")
    
        score_gen_method = input("select> ")
        
        if is_integer(score_gen_method):
            score_gen_method = int(score_gen_method)
            if score_gen_method >= 0 and score_gen_method <= 4:
                return score_gen_method

def select_desired_race():
    # gather all races
    r_list = []
    for r,_ in race_list.items():
        r_list.append(r)

    r_list.append("any")
    r_list.sort()

    while True:
        for i,r in enumerate(r_list):
            print(f"{i:>2} {r}")
        
        choice = input("select desired race>")
        if is_integer(choice) and int(choice) >= 0 and int(choice) < len(r_list):
            desired_race = r_list[int(choice)]
            break
        else:
            print("Invalid selection {int(choice)}.  Try again.")
    
    return desired_race            

def select_desired_class(desired_race):
    # gather all available classes across all races
    c_list = []
    if desired_race == "any":
        for _,v in race_list.items():
            for c in v['classes']:
                if c not in c_list:
                    c_list.append(c)
    else:
        for c in race_list[desired_race]['classes']:
            if c not in c_list:
                c_list.append(c) 
    
    c_list.append("any")
    c_list.sort()

    while True:
        for i,c in enumerate(c_list):
            print(f"{i:>2} {c}")
            
        choice = input("select desired class>")
        if is_integer(choice) and int(choice) >= 0 and int(choice) < len(c_list):
            desired_class = c_list[int(choice)]
            break
        else:
            print("Invalid selection {int(choice)}.  Try again.")

    return desired_class

def generate_ability_scores(method):
    char_abilities = ability_list.copy()
    
    if method == 0:
        for ability in char_abilities:
            while True:
                new_score=input(f"{ability}: >")
                if is_integer(new_score):
                    new_score = int(new_score)
                    if new_score >= 3 and new_score <= 18:
                        char_abilities[ability] = new_score
                        break
                    else:
                        print("*** INVALID VALUE, enter 3-18 ***")
        return char_abilities
    elif method == 1:
        for ability in char_abilities:
            die_list=[]
            for _ in range(0,3):
                die = random.randint(1,6)
                die_list.append(die)
            char_abilities[ability] = sum(die_list)
        return char_abilities
    elif method == 3:
        for ability in ability_list:
            die_list=[]
            for _ in range(0,4):
                die = random.randint(1,6)
                die_list.append(die)
                
            min_val = min(die_list)
            die_list.remove(min_val)
            char_abilities[ability] = sum(die_list)
        return char_abilities
    else:
        raise Exception("Not yet implemented")
        
def get_available_race_and_classes(abilities,desired_race,desired_class):
    available_race_and_class = {}
    for race,race_val in race_list.items():
        
        if desired_race == "any":
            pass
        elif desired_race == race:
            pass
        else:
            # skip this race
            continue
        
        # update the character's ability scores based on race
        tmp_abilities = abilities.copy()
        if "ability_adjustments" in race_val:
            for k,v in race_val["ability_adjustments"].items():
                tmp_abilities[k] = tmp_abilities[k] + v
        
        # verify that race meets the required ability score criteria
        illegal_race = False
        if "min ability scores" in race_val:
            for k,v in tmp_abilities.items():
                if v < race_val["min ability scores"][k]:
                    illegal_race = True
                    if debug_level > 0:
                        print(f"*** ILLEGAL RACE: {race}")
                        print(f"    ability score {k} is {v}, min required is {race_val['min ability scores'][k]}")
                    break
                
        if illegal_race:
            continue # short-circuit back to the for race loop above

        # clamp any values that exceed the max allowable ability score
        if "max ability scores" in race_val:
            for k,v in tmp_abilities.items():
                if v > race_val["max ability scores"][k]:
                    #print(f"*** Clamping racial ability score for {race}")
                    #print(f"    ability score {k} was {tmp_abilities[k]} and is now {race_val['max ability scores'][k]}")
                    tmp_abilities[k] = race_val["max ability scores"][k]
        
        # for each class the race has available
        cls_list = []
        for cls in race_val["classes"]:
            # if this is a standard class
            #if cls in class_specs:
                
            cls_allowed = True # assume the class is okay
            
            # use split() so we can validate multi-class options
            for test_cls in cls.split('/'):
                # check if the class's ability requirements are met
                ability_reqs = class_specs[test_cls]["min_scores"]
                for k,v in ability_reqs.items():
                    if tmp_abilities[k] < v:
                        cls_allowed = False
                        break

            # if nothing disallowed the class...
            if cls_allowed:
                # then it's good to go!
                if desired_class == "any" or desired_class == cls:
                    cls_list.append(cls)

        # if a class list was defined...
        if len(cls_list) > 0:
            # add it to the dictionary
            available_race_and_class[race] = cls_list

    return available_race_and_class

def select_available_race_and_classes(pi,available_race_and_class,abilities,random_sel=False):
    if available_race_and_class:
        race_and_class_list = []
        for race,cls_list in available_race_and_class.items():
            for cls in cls_list:
                race_and_class_list.append({"race": race, "class": cls}) 
        
        while True:
            if random_sel == False:
                i = 1            
                for rc in race_and_class_list:
                    print(f"{i}: {rc['race']} {rc['class']}")
                    i = i + 1
                    
                choice = input("select> ")
            else:
                choice = random.randint(1,len(race_and_class_list))
                i = len(race_and_class_list) + 1

            if is_integer(choice):
                choice = int(choice)
                if (choice < 1) or (choice >= i):
                    print(f"*** INVALID.  Select between 1 and {i-1}")
                else:
                    # apply racial stats to abilities and return race and class for further processing
                    race = race_and_class_list[choice-1]["race"]
                    cls = race_and_class_list[choice-1]["class"]
                    
                    pi["race"] = race
                    pi["class"] = cls
                    
                    if "ability_adjustments" in race_list[race]:
                        for k,v in race_list[race]["ability_adjustments"].items():
                            abilities[k] = abilities[k] + v
                              
                    # clamp any values that exceed the max allowable ability score
                    for k,v in abilities.items():
                        if "max ability scores" in race_list[race]:
                            if abilities[k] > race_list[race]["max ability scores"][k]:
                                #print(f"*** Clamping racial ability score for {race}")
                                #print(f"    ability score {k} was {abilities[k]} and is now {race_list[race]['max ability scores'][k]}")
                                abilities[k] = race_list[race]["max ability scores"][k]                                              

                    pi["ability_scores"] = abilities.copy()
                    break

def is_fighter_paladin_ranger(cls):
    if cls == "fighter" or cls == "paladin" or cls == "ranger":
        return True
    else:
        return False
    
def is_magic_user(cls):
    for c in cls.split('/'):
        if c == "magic-user":
            return True
    return False

def is_illusionist(cls):
    for c in cls.split('/'):
        if c == "illusionist":
            return True
    return False
        

def roll_die(val):
    # converts "d6" or "2d4" or "3d8+9" etc. into a random roll and returns the value rolled
    
    # pre-pend a 1 for simplicity
    if val[0] == 'd':
        val = '1' + val
    
    roll_specs = re.split(r"[d+]",val)
    
    if len(roll_specs) < 2 or len(roll_specs) > 3:
        raise Exception (f"Invalid die notation: {val}")
    
    res = 0
    die_rolls = int(roll_specs[0])
    die_max = int(roll_specs[1])
    
    for _ in range(0,die_rolls):
        res = res + random.randint(1,die_max)

    if len(roll_specs) == 3:
        res = res + int(roll_specs[2])
    
    if debug_level > 1:
        print(f"rolling {val} => {res}")
    
    return res

def get_max_roll(val):
    
    max_roll = 0
    
    if val[0] == 'd':
        val = '1' + val
    
    roll_specs = re.split(r"[d+]",val)
    
    if len(roll_specs) >= 2:
        die_rolls = int(roll_specs[0])
        die_max = int(roll_specs[1])
        max_roll = die_rolls * die_max
        
    return max_roll

def generate_player_hp(pi,level):

    multi_class_divider = len(pi["class"].split('/'))
    val = 0
    
    # get player's con bonus
    con = pi['ability_scores']["CON"]
    
    # loop on player's class since multi-classing affects the Hit Die used for hit point generation
    for cls in pi["class"].split('/'):
        
        hp_modifier = 0
        
        if con <= 3:
            hp_modifier = -2
        elif con <= 6:
            hp_modifier = -1
        elif con == 15:
            hp_modifier = 1
        elif con == 16:
            hp_modifier = 2
        elif con == 17:
            hp_modifier = 2
            if is_fighter_paladin_ranger(cls):
                hp_modifier = 3
        elif con == 18:
            hp_modifier = 2
            if is_fighter_paladin_ranger(cls):
                hp_modifier = 4
        elif con == 19:
            hp_modifier = 2
            if is_fighter_paladin_ranger(cls):
                hp_modifier = 5
        
        # get hit-die
        hd = class_specs[cls]["hit_die"][level-1]
        roll = int((roll_die(hd) + hp_modifier) / multi_class_divider)
        if roll <= 0:
            roll = 1
        val = val + roll
    
    # generate hp based on class & con bonus
    pi["hp"] = val
    
def generate_player_alignment(pi):
    
    # assume any alignment for law/chaos, good/evil
    lnc = set("lawful/neutral/chaotic".split('/'))
    gne = set("good/neutral/evil".split('/'))
    
    for cls in pi["class"].split('/'):
        if class_specs[cls]["alignment"]["lnc"] != "any":
            # remove the non-listed alignments
            lnc = set(class_specs[cls]["alignment"]["lnc"].split("/")) & lnc
        if class_specs[cls]["alignment"]["gne"] != "any":
            # remove the non-listed alignments
            gne = set(class_specs[cls]["alignment"]["gne"].split("/")) & gne

    lnc = random.choice(list(lnc))
    gne = random.choice(list(gne))
    
    if lnc == "neutral" and gne == "neutral":
        pi["alignment"] = "true neutral"
    else:   
        pi["alignment"] = lnc + " " + gne

def generate_spell_book_spells(pi):
    if is_magic_user(pi["class"]):
        spell_list = MAGIC_USER_SPELLS[0].copy()
    
        # ensure first spell is read magic
        pi["spell book"] = []
        pi["spell book"].append("read magic")
        spell_list.remove("read magic")
        
        for _ in range(0,3):
            spell = spell_list[random.randint(0,len(spell_list)-1)]
            pi["spell book"].append(spell)
            spell_list.remove(spell)
    elif is_illusionist(pi['class']):
        spell_list = ILLUSIONIST_SPELLS[0].copy()
        
        pi["spell book"] = []
        for _ in range(0,3):
            spell = spell_list[random.randint(0,len(spell_list)-1)]
            pi["spell book"].append(spell)
            spell_list.remove(spell)

def generate_starting_funds(pi):
    # select the class that can generate the most gold
    
    max_gold = 0
    for cls in pi["class"].split('/'):
        class_max_gold = get_max_roll(class_specs[cls]["gold"]["die"]) * class_specs[cls]["gold"]["multiplier"]
        if class_max_gold > max_gold:
            max_gold = class_max_gold
            gold_die = class_specs[cls]["gold"]["die"]
            gold_multiplier = class_specs[cls]["gold"]["multiplier"]
            
    gold = roll_die(gold_die) * gold_multiplier
    
    pi["gold"] = gold
        
def generate_weight_and_height(pi):
    race = pi['race']
    
    height = race_list[race]["height"]
    height_val = height["base"]*12.0 + (roll_die(height["mod die"]))
    if int(height_val % 12.0) == 0:
        pi["height"] = f"{int(height_val/12.0)}ft"
    else:
        pi["height"] = f"{int(height_val/12.0)}ft {int(height_val%12.0)}in"
        
    weight = race_list[race]["weight"]
    weight_val = weight["base"] + (roll_die(weight["mod die"]))
    pi["weight"] = f"{int(weight_val)}lbs"
    
def generate_age(pi):
    race = pi['race']
    cls = pi['class']
    
    age = race_list[race]["age"]
    
    # by fiat: grab the oldest age for multi-class characters
    cur_age = 0
    for c in cls.split('/'):
        r = roll_die(age[c])
        if r > cur_age:
            cur_age = r
            
    pi["age"] = f"{cur_age} yrs"
    
def generate_gender(pi):
    # flip a coin
    if roll_die("1d2") == 1:
        pi["gender"] = "male"
    else:
        pi["gender"] = "female"
    
def display_player_info(pi):
    # name / xp / age
    print(f"     name: {'':<25} {'xp:':>7} {0:<7} {'age:':>7} {pi['age']:<4}")
    
    # class / hp / height
    print(f"    class: {pi['class']:<25} {'hp:':>7} {pi['hp']:<7} {'height:':>7} {pi['height']}")
    
    # alignment / AC / weight
    print(f"alignment: {pi['alignment']:<25} {'AC:':>7} {'':<7} {'weight:':>7} {pi['weight']}")
    
    # race / lvl / gender
    print(f"     race: {pi['race']:<25} {'level:':>7} {pi['level']:<7} {'gender:':>7} {pi['gender']}")
    
    # MC / MC / MC
    
    # abilities
    print("\nAbility scores")
    for k,v in pi["ability_scores"].items():
        print(f"{k}: {v}")
    
    # print(f"\nAdditional ability info TBD")
    # str, to-hit, damage, encumbrance, minor test, major test
    # dex, surprise, missile to-hit, ac, agility save bonus, missile initiative bonus
    # con, hp, resurrection success, system shock
    # int, add'l languages
    # wis, mental save
    # cha, max henchman, loyalty, reaction
    # movement rate - determined via race and armor
    
    # save vs
    # aimed magic items / breath weapons / death, paralysis, poison / petrification, polymorph / spells
    # pick best saving throws for multi-classes
    saves = None
    for cls in pi["class"].split("/"):
        tmp_saves = class_specs[cls]["saving throws"][0]
        if saves:
            for k,v in tmp_saves.items():
                if saves[k] > v:
                    saves[k] = v
        else:
            saves = tmp_saves.copy()
    print("\nSaving Throws")
    for k,v in saves.items():
        print(f"{k:>23}: {v}")
    
    # weapons & armor
    
    # roll to hit AC
    to_hit_table = None
    for cls in pi["class"].split("/"):
        tmp_to_hit_table = class_specs[cls]["to-hit table"][0]
        if to_hit_table:
            i = 0
            for i,v in enumerate(tmp_to_hit_table):
                if to_hit_table[i] > v:
                    to_hit_table[i] = v
        else:
            to_hit_table = tmp_to_hit_table.copy()
    print("\nTo-hit Table")
    for i in range(10,-11,-1):
        print(f"{i:>4}",end="")
    print()
    for v in to_hit_table:
        print(f"{v:>4}",end="")
    print()
    
    # equipment
    
    # wealth
    
    # special abilities (race)
    # languages
    
    # special abilities (class)
    #print("\nClass abilities")
    if is_magic_user(pi['class']) or is_illusionist(pi['class']):
        print()
        print(f"spell book:")
        for spell in pi['spell book']:
            print(f"  {spell}")
    
    # notes
        
    print(f"\ngold: {pi['gold']}")

def main():
    print("Welcome to verderog's OSRIC 3.0 chargen!")
    
    while True:
        char_count = input("# of characters to generate>")
        if is_integer(char_count) >= 1:
            char_count = int(char_count)
            break
        else:
            print("Invalid entry: {char_count}.  Enter 1 or more.")
    
    desired_race = select_desired_race()
    desired_class = select_desired_class(desired_race)
             
    if debug_level > 2:
        print(f"desired race: {desired_race}")
        print(f"desired class: {desired_class}")
        
    score_gen_method = select_ability_generation_method()
    
    print("--------------------------------------------------------------------------------------")
    i = 0
    
    while i < char_count:
        #pi = player_info.copy()
        pi = {}
        pi['level'] = 1
        abilities = generate_ability_scores(score_gen_method)
        available_race_and_classes = get_available_race_and_classes(abilities,desired_race,desired_class)
        
        if not available_race_and_classes:
            if debug_level > 0:
                print("*** NO LEGAL RACES+CLASSES, REROLL!!! ***")
            continue
        else:
            select_available_race_and_classes(pi,available_race_and_classes,abilities,(char_count > 1))
        
        generate_player_hp(pi,1)
        generate_player_alignment(pi)
        generate_spell_book_spells(pi)
        generate_starting_funds(pi)
        generate_weight_and_height(pi)
        generate_age(pi)
        # apply age to ability scores
        generate_gender(pi)
        #generate_starting_equipment()
        
        display_player_info(pi)
        
        i = i + 1
        
        print("--------------------------------------------------------------------------------------")

    
if __name__ == '__main__':
    main()
    print("Done!")
