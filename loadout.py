from Model import Loadout
from flask import request, render_template

def filter_loadouts():
    armors = Loadout.query.with_entities(Loadout.l_ArmorKey).distinct().all()
    traders = Loadout.query.with_entities(Loadout.l_traderKey).distinct().all()
    weapons = Loadout.query.with_entities(Loadout.l_WeaponName).distinct().all()

    if request.method == 'POST':
        selected_armor = request.form['armor']
        selected_trader = request.form['trader']
        selected_weapon = request.form['weapon']

        loadouts = Loadout.query.filter_by(
            l_ArmorKey=selected_armor,
            l_traderKey=selected_trader,
            l_WeaponName=selected_weapon
        ).all()

        return render_template('filtered_loadouts.html', loadouts=loadouts)

    return render_template(
        'loadout.html',
        armors=armors,
        traders=traders,
        weapons=weapons
    )