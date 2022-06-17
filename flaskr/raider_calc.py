import numpy as np
import pandas as pd
import requests

def GetScore(region, realm, char_name):
    response = requests.get(f"https://raider.io/api/v1/characters/profile?region={region}&realm={realm}&name={char_name}&fields=mythic_plus_best_runs%2Cmythic_plus_alternate_runs")
    data = response.json()

    best = pd.DataFrame(data['mythic_plus_best_runs'])
    alternate = pd.DataFrame(data['mythic_plus_alternate_runs'])

    # List of current S3 dungeons
    dungeon_shorthands = ['NW', 'STRT', 'SOA', 'PF', 'MISTS', 'HOA', 'DOS', 'TOP', 'SD', 'GMBT']
    dungeon_full_names = [  "The Necrotic Wake",
                            "Tazavesh: Streets of Wonder",
                            "Spires of Ascension",
                            "Plaguefall",
                            "Mists of Tirna Scithe",
                            "Halls of Atonement",
                            "De Other Side",
                            "Theater of Pain",
                            "Sanguine Depths",
                            "Tazavesh: So'leah's Gambit"]

    assert data['name'] == char_name, "Wrong character data collected from API call."

    char_name = data['name']

    # Reindex the data to use dungeon shorthands
    best.index = best.short_name
    alternate.index = alternate.short_name

    del best['short_name']
    del alternate['short_name']

    # Rename column
    best = best.rename(columns={'num_keystone_upgrades' : 'upgrade'})
    alternate = alternate.rename(columns={'num_keystone_upgrades' : 'upgrade'})

    # Clean up both of the data frames by seperating out the affixes and removing unnecessary columns
    best['affix1'] = [best.loc[i, ('affixes')][0]['name'] for i in best.index]
    best['affix2'] = [best.loc[i, ('affixes')][1]['name'] for i in best.index]
    best['affix3'] = [best.loc[i, ('affixes')][2]['name'] for i in best.index]
    del best['affixes']
    del best['zone_id']
    del best['map_challenge_mode_id']

    alternate['affix1'] = [alternate.loc[i, ('affixes')][0]['name'] for i in alternate.index]
    alternate['affix2'] = [alternate.loc[i, ('affixes')][1]['name'] for i in alternate.index]
    alternate['affix3'] = [alternate.loc[i, ('affixes')][2]['name'] for i in alternate.index]
    del alternate['affixes']
    del alternate['zone_id']
    del alternate['map_challenge_mode_id']

    # Check for any dungeons missing in either dataset, if they are, add them to the pandas array
    for i in range(len(dungeon_shorthands)):
        index = dungeon_shorthands[i]
        if not index in best.index:
            # print(f"No best run found for {dungeon_full_names[i]}.")
            best = pd.concat([best, pd.DataFrame([{'dungeon' : dungeon_full_names[i]}], index=[index])], verify_integrity=True)

    for i in range(len(dungeon_shorthands)):
        index = dungeon_shorthands[i]
        if not index in alternate.index:
            # print(f"No alternate run found for {dungeon_full_names[i]}.")
            alternate = pd.concat([alternate, pd.DataFrame([{'dungeon' : dungeon_full_names[i]}], index=[index])], verify_integrity=True)

    best=best.fillna(0)
    alternate=alternate.fillna(0)

    # Calculate adjusted score
    best['adjusted_score'] = best['score']*1.5
    alternate['adjusted_score'] = alternate['score']*0.5

    # Calculate time remaining on key (negative time_left_ms means an untimed key)
    best['time_left_ms'] = best['par_time_ms'] - best['clear_time_ms']
    alternate['time_left_ms'] = alternate['par_time_ms'] - alternate['clear_time_ms']

    best = best[['dungeon','mythic_level', 'score', 'adjusted_score', 'upgrade','clear_time_ms','par_time_ms', 'time_left_ms','affix1','affix2','affix3','url']]
    alternate = alternate[['dungeon','mythic_level', 'score', 'adjusted_score', 'upgrade','clear_time_ms','par_time_ms', 'time_left_ms','affix1','affix2','affix3','url']]

    # ### Present data ###
    # print("############# \n")
    # print(char_name)
    # print(f"Total Score: {best.adjusted_score.sum() + alternate.adjusted_score.sum():.2f}")

    score=best.adjusted_score.sum() + alternate.adjusted_score.sum()
    return score
