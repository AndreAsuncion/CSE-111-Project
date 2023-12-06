from flask import Flask, render_template, jsonify, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__, template_folder='templates', static_url_path='/static', static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tarkov.db' 
app.config['SECRET_KEY'] = 'She_Jerry_On_My_Wang'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Trader(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    t_traderKey = db.Column(db.Integer, nullable=False) 
    t_traderName = db.Column(db.String(100), unique=True, nullable=False)
    t_repairRate = db.Column(db.Integer)
    t_repairDescription = db.Column(db.String(100))

    def __init__(self, t_traderKey, t_traderName):
        self.t_traderKey = t_traderKey
        self.t_traderName = t_traderName

class Loadout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    l_loadoutKey = db.Column(db.Integer, nullable=False)
    l_loadoutName = db.Column(db.String(100), unique=True, nullable=False)
    l_ArmorKey = db.Column(db.Integer, nullable=False)
    l_traderKey = db.Column(db.Integer, nullable=False)
    l_WeaponName = db.Column(db.String(100), unique=True, nullable=False)

    def __init__(self, l_loadoutKey, l_loadoutName, l_ArmorKey, l_traderKey, l_WeaponName):
        self.l_loadoutKey = l_loadoutKey
        self.l_loadoutName = l_loadoutName
        self.l_ArmorKey = l_ArmorKey
        self.l_traderKey = l_traderKey
        self.l_WeaponName = l_WeaponName

class Armor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    a_armorKey = db.Column(db.Integer, nullable=False)
    a_armorName = db.Column(db.String(100), unique=True, nullable=False)
    a_traderKey = db.Column(db.Integer, nullable=False)
    a_maxDur = db.Column(db.Integer, nullable=False)
    a_currDur = db.Column(db.Integer, nullable=False)
    a_slots = db.Column(db.Integer, nullable=True)
    a_price = db.Column(db.Integer, nullable=False)
    a_zone = db.Column(db.String(100), nullable=False)
    a_materialKey = db.Column(db.Integer, nullable=False)
    a_enchancementKey = db.Column(db.Integer, nullable=False)
    a_penaltieKey = db.Column(db.Integer, nullable=False)

    def __init__(self, a_armorKey, a_armorName, a_traderKey, a_maxDur, a_currDur, a_slots, a_price, a_zone, a_materialKey, a_enchancementKey, a_penaltieKey):
        self.a_armorKey = a_armorKey
        self.a_armorName = a_armorName
        self.a_traderKey = a_traderKey
        self.a_maxDur = a_maxDur
        self.a_currDur = a_currDur
        self.a_slots = a_slots
        self.a_price = a_price
        self.a_zone = a_zone
        self.a_materialKey = a_materialKey
        self.a_enchancementKey = a_enchancementKey
        self.a_penaltieKey = a_penaltieKey

class Material(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    m_materialKey = db.Column(db.Integer, nullable=False)
    m_materialName = db.Column(db.String(100), unique=True, nullable=False)
    m_repairRate = db.Column(db.Integer, nullable=False)

    def __init__(self, m_materialKey, m_materialName, m_repairRate):
        self.m_materialKey = m_materialKey
        self.m_materialName = m_materialName
        self.m_repairRate = m_repairRate

class Enhancement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    e_enhanceKey = db.Column(db.Integer, nullable=False)
    e_enhanceName = db.Column(db.String(100), unique=True, nullable=False)
    e_percent = db.Column(db.Integer, nullable=False)
    e_level = db.Column(db.Integer, nullable=False)

    def __init__(self, e_enhanceKey, e_enhanceName, e_percent, e_level):
        self.e_enhanceKey = e_enhanceKey
        self.e_enhanceName = e_enhanceName
        self.e_percent = e_percent
        self.e_level = e_level

class Penalty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    p_penaltyKey = db.Column(db.Integer, nullable=False)
    p_penaltyName = db.Column(db.String(100), unique=True, nullable=False)
    p_movement = db.Column(db.Integer, nullable=False)
    p_turning = db.Column(db.Integer, nullable=False)
    p_ergo = db.Column(db.Integer, nullable=False)
    p_weight = db.Column(db.Integer, nullable=False)

    def __init__(self, p_penaltyKey, p_penaltyName, p_movement, p_turning, p_ergo, p_weight):
        self.p_penaltyKey = p_penaltyKey
        self.p_penaltyName = p_penaltyName
        self.p_movement = p_movement
        self.p_turning = p_turning
        self.p_ergo = p_ergo
        self.p_weight = p_weight

with app.app_context():
    db.create_all()

@app.route('/style.css')
def serve_style():
    return app.send_static_file('style.css')

@app.route('/script.js')
def serve_script():
    return app.send_static_file('script.js')

@app.route('/')
def index():
    distinct_armors = db.session.query(Armor.a_armorKey, Armor.a_armorName) \
        .join(Loadout, Loadout.l_ArmorKey == Armor.a_armorKey) \
        .distinct().all()
    
    distinct_traders = db.session.query(Loadout.l_traderKey, Trader.t_traderName) \
        .join(Trader, Loadout.l_traderKey == Trader.t_traderKey) \
        .distinct().all()
    
    weapons = Loadout.query.with_entities(Loadout.l_WeaponName).distinct().all()
    weapon_names = [weapon[0] for weapon in weapons]
    
    return render_template('index.html', armors=distinct_armors, traders=distinct_traders, weapons=weapon_names)

@app.route('/filter_loadouts', methods=['POST'])
def filter_loadouts():
    selected_armor = request.form['armor']
    selected_trader = request.form['trader']
    selected_weapon = request.form['weapon']

    distinct_armors = db.session.query(Armor.a_armorKey, Armor.a_armorName) \
        .join(Loadout, Loadout.l_ArmorKey == Armor.a_armorKey) \
        .distinct().all()
    
    distinct_traders = db.session.query(Loadout.l_traderKey, Trader.t_traderName) \
        .join(Trader, Loadout.l_traderKey == Trader.t_traderKey) \
        .distinct().all()
    
    weapons = Loadout.query.with_entities(Loadout.l_WeaponName).distinct().all()
    weapon_names = [weapon[0] for weapon in weapons]

    filters = []

    if selected_armor:
        filters.append(Loadout.l_ArmorKey == selected_armor)
    if selected_trader:
        filters.append(Loadout.l_traderKey == selected_trader)
    if selected_weapon:
        filters.append(Loadout.l_WeaponName == selected_weapon)

    if filters:
        filtered_loadouts = Loadout.query.filter(*filters).all()
    else:
        filtered_loadouts = Loadout.query.all()

    loadout_info = []
    for loadout in filtered_loadouts:
        armor_name = Armor.query.filter_by(a_armorKey=loadout.l_ArmorKey).first().a_armorName
        trader_name = Trader.query.filter_by(t_traderKey=loadout.l_traderKey).first().t_traderName
        weapon_name = loadout.l_WeaponName
        loadout_info.append({
            'loadout_name': loadout.l_loadoutName,
            'armor_name': armor_name,
            'trader_name': trader_name,
            'weapon_name': weapon_name
        })

    return render_template(
        'index.html',
        armors=distinct_armors,
        traders=distinct_traders,
        weapons=weapon_names,
        loadout_info=loadout_info,
    )

@app.route('/armor')
def armor():
    distinct_traders = db.session.query(Trader.t_traderKey, Trader.t_traderName).distinct().all()

    materials = db.session.query(Material.m_materialKey, Material.m_materialName).distinct().all()
    enhancements = db.session.query(Enhancement.e_enhanceKey, Enhancement.e_enhanceName).distinct().all()
    penalties = db.session.query(Penalty.p_penaltyKey, Penalty.p_penaltyName).distinct().all()

    return render_template('armor.html', traders=distinct_traders, materials=materials,
                           enhancements=enhancements, penalties=penalties)

@app.route('/filter_armors', methods=['POST'])
def filter_armors():
    selected_trader = request.form['trader']
    min_durability = request.form['min_durability']
    max_durability = request.form['max_durability']
    min_slots = request.form['min_slots']
    max_slots = request.form['max_slots']
    min_price = request.form['min_price']
    max_price = request.form['max_price']
    selected_zones = request.form.getlist('zones[]')
    selected_material = request.form['material_key']
    selected_enhancement = request.form['enhancement_key']
    selected_penalty = request.form['penalty_key']

    filters = []

    if selected_trader:
        filters.append(Armor.a_traderKey == selected_trader)

    if min_durability:
        filters.append(Armor.a_maxDur >= int(min_durability))
    if max_durability:
        filters.append(Armor.a_maxDur <= int(max_durability))

    if min_slots:
        filters.append(Armor.a_slots >= int(min_slots))
    if max_slots:
        filters.append(Armor.a_slots <= int(max_slots))

    if min_price:
        filters.append(Armor.a_price >= int(min_price))
    if max_price:
        filters.append(Armor.a_price <= int(max_price))

    if selected_zones:
        zone_filters = [Armor.a_zone.contains(zone) for zone in selected_zones]
        filters.append(db.or_(*zone_filters))

    if selected_material:
        filters.append(Armor.a_materialKey == selected_material)
    if selected_enhancement:
        filters.append(Armor.a_enchancementKey == selected_enhancement)
    if selected_penalty:
        filters.append(Armor.a_penaltieKey == selected_penalty)

    if filters:
        filtered_armors = Armor.query.filter(*filters).all()
    else:
        filtered_armors = Armor.query.all()

    armor_info = []
    for armor in filtered_armors:
        trader_name = Trader.query.filter_by(t_traderKey=armor.a_traderKey).first().t_traderName

        material_name = Material.query.filter_by(m_materialKey=armor.a_materialKey).first().m_materialName
        enhancement_name = Enhancement.query.filter_by(e_enhanceKey=armor.a_enchancementKey).first().e_enhanceName
        penalty_name = Penalty.query.filter_by(p_penaltyKey=armor.a_penaltieKey).first().p_penaltyName
        
        armor_info.append({
            'armor_name': armor.a_armorName,
            'trader_name': trader_name,
            'max_durability': armor.a_maxDur,
            'slots': armor.a_slots,
            'price': armor.a_price,
            'zone': armor.a_zone,
            'material_name': material_name,
            'enhancement_name': enhancement_name,
            'penalty_name': penalty_name
        })

    distinct_traders = db.session.query(Trader.t_traderKey, Trader.t_traderName).distinct().all()
    materials = db.session.query(Material.m_materialKey, Material.m_materialName).distinct().all()
    enhancements = db.session.query(Enhancement.e_enhanceKey, Enhancement.e_enhanceName).distinct().all()
    penalties = db.session.query(Penalty.p_penaltyKey, Penalty.p_penaltyName).distinct().all()

    return render_template(
        'armor.html',
        traders=distinct_traders,
        armor_info=armor_info,
        materials=materials,
        enhancements=enhancements,
        penalties=penalties,
        selected_material=selected_material,  # Include the selected values
        selected_enhancement=selected_enhancement,
        selected_penalty=selected_penalty
    )

@app.route('/attribute')
def attribute():
    return render_template('attribute.html')

@app.route('/filter_penalties', methods=['POST'])
def filter_penalties():
    min_movement = request.form.get('min_movement')
    max_movement = request.form.get('max_movement')
    min_turning = request.form.get('min_turning')
    max_turning = request.form.get('max_turning')
    min_ergo = request.form.get('min_ergo')
    max_ergo = request.form.get('max_ergo')
    min_weight = request.form.get('min_weight')
    max_weight = request.form.get('max_weight')

    filters = []

    if min_movement:
        filters.append(Penalty.p_movement >= int(min_movement))
    if max_movement:
        filters.append(Penalty.p_movement <= int(max_movement))

    if min_turning:
        filters.append(Penalty.p_turning >= int(min_turning))
    if max_turning:
        filters.append(Penalty.p_turning <= int(max_turning))

    if min_ergo:
        filters.append(Penalty.p_ergo >= int(min_ergo))
    if max_ergo:
        filters.append(Penalty.p_ergo <= int(max_ergo))

    if min_weight:
        filters.append(Penalty.p_weight >= int(min_weight))
    if max_weight:
        filters.append(Penalty.p_weight <= int(max_weight))

    if filters:
        filtered_penalties = Penalty.query.filter(*filters).all()
    else:
        filtered_penalties = Penalty.query.all()

    return render_template('attribute.html', filtered_penalties=filtered_penalties)


@app.route('/filter_enhancements', methods=['POST'])
def filter_enhancements():
    min_percent = request.form['min_percent']
    max_percent = request.form['max_percent']
    min_level = request.form['min_level']
    max_level = request.form['max_level']

    filters = []

    if min_percent:
        filters.append(Enhancement.e_percent >= int(min_percent))
    if max_percent:
        filters.append(Enhancement.e_percent <= int(max_percent))

    if min_level:
        filters.append(Enhancement.e_level >= int(min_level))
    if max_level:
        filters.append(Enhancement.e_level <= int(max_level))

    if filters:
        filtered_enhancements = Enhancement.query.filter(*filters).all()
    else:
        filtered_enhancements = Enhancement.query.all()

    return render_template('attribute.html', filtered_enhancements=filtered_enhancements)

def calculate_repair_costs(a_currDur, a_maxDur, a_price, m_repairRate, t_repairRate):
    missing_dur = a_maxDur - a_currDur
    repaired_dur = m_repairRate * missing_dur * (t_repairRate / 125)
    total_cost = repaired_dur * (a_price/missing_dur)
    fixed_durr = a_currDur + repaired_dur
    adj_cost = total_cost * (t_repairRate / 100)
    return adj_cost, fixed_durr

@app.route('/calculator', methods=['GET', 'POST'])
def calculator():

    distinct_armors = db.session.query(Armor.a_armorKey, Armor.a_armorName, Armor.a_maxDur).distinct().all()
    
    distinct_traders = db.session.query(Trader.t_traderKey, Trader.t_traderName, Trader.t_repairDescription) \
        .filter(Trader.t_repairRate.isnot(None)) \
        .distinct() \
        .all()
    
    if request.method == 'POST':
        error = []
        trader_key = request.form['trader']
        armor_key = request.form['armor']
        current_durability = request.form['durability']

        # Checking all the fields
        if not trader_key:
            error.append('Please select trader')
        if not armor_key:
            error.append('Please select armor')
        if not current_durability.isdigit():
            current_durability = 0
        
        if error:
            flash(error)
        else:
            armor = Armor.query.filter_by(a_armorKey=armor_key).first()
            
            material = Material.query.filter_by(m_materialKey=armor.a_materialKey).first()

            trader = Trader.query.filter_by(t_traderKey=trader_key).first()

            current_durability = int(current_durability)

            if current_durability == armor.a_maxDur:
                error.append('Cannot repair full armor')
            
            if current_durability > armor.a_maxDur:
                error.append('Durability over max')

            if error:
                flash(error)
            else:
                

                # Calculation
                calculation = calculate_repair_costs(current_durability, armor.a_maxDur, armor.a_price, material.m_repairRate, trader.t_repairRate)
                # calculation = calculate_repair_costs(1,2,3,4)

                repair_info = [trader.t_traderName, armor.a_armorName, material.m_materialName, calculation[1], armor.a_maxDur]
                # repair_info = [armor.a_armorName, material,3,4,5]

                return render_template(
                    'calculator.html',
                    armors=distinct_armors,
                    traders=distinct_traders,
                    repair_info = repair_info,
                    cost = calculation[0],
                )

    return render_template('calculator.html', armors=distinct_armors, traders=distinct_traders)

if __name__ == '__main__':
    app.run(debug=True)
