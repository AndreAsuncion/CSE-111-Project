CREATE TABLE Trader (
    id SERIAL PRIMARY KEY,
    t_traderKey INTEGER NOT NULL,
    t_traderName VARCHAR(100)
);

CREATE TABLE Loadout (
    id SERIAL PRIMARY KEY,
    l_loadoutKey INTEGER NOT NULL,
    l_loadoutName VARCHAR(100) UNIQUE NOT NULL,
    l_ArmorKey INTEGER NOT NULL,
    l_WeaponName VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE Armor (
    id SERIAL PRIMARY KEY,
    a_armorKey INTEGER NOT NULL,
    a_armorName VARCHAR(100) UNIQUE NOT NULL,
    a_traderKey INTEGER NOT NULL,
    a_maxDur INTEGER NOT NULL,
    a_currDur INTEGER NOT NULL,
    a_slots INTEGER,
    a_price INTEGER NOT NULL,
    a_zone VARCHAR(100) NOT NULL,
    a_materialKey INTEGER NOT NULL,
    a_enchancementKey INTEGER NOT NULL,
    a_penaltieKey INTEGER NOT NULL
);

CREATE TABLE Material (
    id SERIAL PRIMARY KEY,
    m_materialKey INTEGER NOT NULL,
    m_materialName VARCHAR(100) UNIQUE NOT NULL,
    m_repairRate INTEGER NOT NULL
);

CREATE TABLE Enhancement (
    id SERIAL PRIMARY KEY,
    e_enhanceKey INTEGER NOT NULL,
    e_enhanceName VARCHAR(100) UNIQUE NOT NULL,
    e_percent INTEGER NOT NULL,
    e_level INTEGER NOT NULL
);

CREATE TABLE Penalty (
    id SERIAL PRIMARY KEY,
    p_penaltyKey INTEGER NOT NULL,
    p_penaltyName VARCHAR(100) UNIQUE NOT NULL,
    p_movement INTEGER NOT NULL,
    p_turning INTEGER NOT NULL,
    p_ergo INTEGER NOT NULL,
    p_weight INTEGER NOT NULL
);
