--productions
CREATE TABLE IF NOT EXISTS productions (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY key,
    order_name text NOT NULL unique,
    format text NOT NULL unique,
    profile text NOT NULL unique,
    material_outer text NOT NULL,
    material_corrugation text NOT NULL,
    material_inside text NOT NULL,
    quantity INTEGER NOT NULL
);
