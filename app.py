from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='templates', static_url_path='/static', static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tarkov.db' 
db = SQLAlchemy(app)

class Trader(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    t_traderKey = db.Column(db.Integer, nullable=False) 
    t_traderName = db.Column(db.String(100), unique=True, nullable=False)

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
        
def calculate_repair_costs(a_currDur, a_maxDur, a_price, m_repairRate):
    missing_dur = a_maxDur - a_currDur
    repaired_dur = m_repairRate * missing_dur
    total_cost = repaired_dur * (a_price/missing_dur)
    fixed_durr = a_currDur + repaired_dur
    return total_cost, fixed_durr

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

@app.route('/calculator')
def calculator():
    distinct_armors = db.session.query(Armor.a_armorKey, Armor.a_armorName) \
        .join(Loadout, Loadout.l_ArmorKey == Armor.a_armorKey) \
        .distinct().all()
        
    distinct_materials = db.session.query(Material.m_materialKey, Material.m_materialName, Material.m_repairRate) \
        .join(Armor, Armor.a_materialKey == Material.m_materialKey) \
        .distinct().all()
    
    distinct_traders = db.session.query(Loadout.l_traderKey, Trader.t_traderName) \
        .join(Trader, Loadout.l_traderKey == Trader.t_traderKey) \
        .distinct().all()
    
    costs = calculate_repair_costs(Armor.a_currDur, Armor.a_maxDur, Armor.a_price, Material.m_repairRate)
    
    repair_info = []
    for repair in repair_info:
        armor_name = Armor.query.filter_by(a_materialKey=repair.m_materialKey).first().a_armorName
        trader_name = Trader.query.filter_by(t_traderKey=repair.a_traderKey).first().t_traderName
        repair.append({
            'trader_name': trader_name,
            'armor_name': armor_name,
            'material_name': Material.m_materialName,
            'curr_durr': Armor.a_currDur,
            'max_durr': Armor.a_maxDur,
        })
    
    return render_template('calculator.html', armors=distinct_armors, traders=distinct_traders, material = distinct_materials, cost = costs)

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

if __name__ == '__main__':
    app.run(debug=True)
