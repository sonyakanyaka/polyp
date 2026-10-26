-- ============================================================
--  БАЗА ДАННЫХ «ПОЛИПРАГМАЗИЯ-КОНТРОЛЬ»
--  Три таблицы: вещества, критерии Бирса, взаимодействия.
-- ============================================================

CREATE TABLE active_ingredients (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT    NOT NULL,
    name_lower  TEXT    NOT NULL UNIQUE,
    rxcui       TEXT
);

CREATE TABLE beers_criteria (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    ingredient_id   INTEGER NOT NULL,
    category        TEXT    NOT NULL,
    rationale       TEXT    NOT NULL,
    recommendation  TEXT    NOT NULL,
    source          TEXT,
    FOREIGN KEY (ingredient_id) REFERENCES active_ingredients(id)
);

CREATE TABLE drug_interactions (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    ingredient_id_1 INTEGER NOT NULL,
    ingredient_id_2 INTEGER NOT NULL,
    severity        TEXT    NOT NULL,
    description     TEXT    NOT NULL,
    source          TEXT,
    FOREIGN KEY (ingredient_id_1) REFERENCES active_ingredients(id),
    FOREIGN KEY (ingredient_id_2) REFERENCES active_ingredients(id),
    UNIQUE (ingredient_id_1, ingredient_id_2)
);

CREATE INDEX idx_beers_ingredient    ON beers_criteria(ingredient_id);
CREATE INDEX idx_interaction_first   ON drug_interactions(ingredient_id_1);
CREATE INDEX idx_interaction_second  ON drug_interactions(ingredient_id_2);