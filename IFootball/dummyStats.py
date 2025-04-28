# Complete Football Statistics Dataset 24/25 Season

COMPETITION_IDS = {
    "UEFA Champions League": 2001,
    "Premier League": 2021,
    "La Liga": 2014,
    "Bundesliga": 2002,
    "Serie A": 2019,
    "Ligue 1": 2015
}

FOOTBALL_DATA = {
    # UEFA Champions League Data
    "UEFA Champions League": {
        "competition_id": 2001,
        "goals": [
            {"player": "Guirassy", "team": "Borussia Dortmund", "total": 13, "penalties": 5},
            {"player": "Raphinha", "team": "Barcelona", "total": 12},
            {"player": "Lewandowski", "team": "Barcelona", "total": 11, "penalties": 3},
            {"player": "Kane", "team": "Bayern Munich", "total": 11, "penalties": 4},
            {"player": "Lautaro", "team": "Internazionale", "total": 8, "penalties": 1},
            {"player": "Haaland", "team": "Manchester City", "total": 8, "penalties": 2},
            {"player": "Vinicius", "team": "Real Madrid", "total": 8, "penalties": 1},
            {"player": "Dembélé", "team": "Paris Saint-Germain", "total": 7},
            {"player": "Mbappé", "team": "Real Madrid", "total": 7},
            {"player": "Alvarez", "team": "Atletico Madrid", "total": 7},
            {"player": "Vangelis Pavlidis", "team": "Benfica", "total": 7, "penalties": 2},
            {"player": "Jonathan David", "team": "Lille", "total": 7, "penalties": 2},
            {"player": "Griezmann", "team": "Atletico Madrid", "total": 6}
        ],
        "assists": [
            {"player": "Mac Allister", "team": "Liverpool", "total": 5},
            {"player": "Álvaro Carreras", "team": "Benfica", "total": 5},
            {"player": "Vazquez", "team": "Real Madrid", "total": 4},
            {"player": "Goretzka", "team": "Bayern Munich", "total": 4},
            {"player": "Gimenez", "team": "Atletico Madrid", "total": 4},
            {"player": "Bensebaini", "team": "Borussia Dortmund", "total": 4},
            {"player": "Julien Le Cardinal", "team": "Stade Brestois", "total": 4},
            {"player": "Vinicius", "team": "Real Madrid", "total": 4},
            {"player": "Éderson", "team": "Atalanta", "total": 4},
            {"player": "Stuani", "team": "Girona", "total": 3},
            {"player": "André", "team": "Lille", "total": 3},
            {"player": "Gross", "team": "Borussia Dortmund", "total": 3},
            {"player": "Meunier", "team": "Lille", "total": 3}
        ],
        "clean_sheets": [
            {"player": "Yann Sommer", "team": "Inter Milan", "total": 7},
            {"player": "David Raya", "team": "Arsenal FC", "total": 6},
            {"player": "Marco Carnesecchi", "team": "Atalanta BC", "total": 5},
            {"player": "Emiliano Martinez", "team": "Aston Villa", "total": 5},
            {"player": "Manuel Neuer", "team": "Bayern Munich", "total": 4},
            {"player": "Gianluigi Donnarumma", "team": "Paris Saint-Germain", "total": 4},
            {"player": "Anatoly Trubin", "team": "SL Benfica", "total": 4},
            {"player": "Gregor Kobel", "team": "Borussia Dortmund", "total": 4},
            {"player": "Caoimhín Kelleher", "team": "Liverpool FC", "total": 3}
        ]
    },

    # Premier League Data
    "Premier League": {
        "competition_id": 2021,
        "goals": [
            {"player": "Salah", "team": "Liverpool", "total": 27, "penalties": 9},
            {"player": "Isak", "team": "Newcastle Utd", "total": 21, "penalties": 2},
            {"player": "Haaland", "team": "Manchester City", "total": 21, "penalties": 2},
            {"player": "Wood", "team": "Nottingham Forest", "total": 19, "penalties": 3},
            {"player": "Bryan Mbeumo", "team": "Brentford", "total": 18, "penalties": 5},
            {"player": "Yoane Wissa", "team": "Brentford", "total": 16},
            {"player": "Ollie Watkins", "team": "Aston Villa", "total": 15, "penalties": 2},
            {"player": "Jean-Philippe Mateta", "team": "Crystal Palace", "total": 14, "penalties": 2},
            {"player": "Matheus Cunha", "team": "Wolverhampton", "total": 14},
            {"player": "Cole Palmer", "team": "Chelsea", "total": 14, "penalties": 3},
            {"player": "Jørgen Strand Larsen", "team": "Wolverhampton", "total": 12},
            {"player": "Kluivert", "team": "AFC Bournemouth", "total": 12, "penalties": 6},
            {"player": "Liam Delap", "team": "Ipswich Town", "total": 12, "penalties": 2}
        ],
        "assists": [
            {"player": "Lukic", "team": "Fulham", "total": 12},
            {"player": "Hughes", "team": "Crystal Palace", "total": 11},
            {"player": "Joelinton", "team": "Newcastle", "total": 10},
            {"player": "Flynn Downes", "team": "Southampton", "total": 10},
            {"player": "Caicedo", "team": "Chelsea", "total": 10},
            {"player": "Sam Morsy", "team": "Ipswich Town", "total": 9},
            {"player": "Burn", "team": "Newcastle", "total": 9},
            {"player": "Ryan Christie", "team": "Bournemouth", "total": 9},
            {"player": "Ugarte", "team": "Man Utd", "total": 9},
            {"player": "Ryan Yates", "team": "Nottingham Forest", "total": 9},
            {"player": "Daniel Muñoz", "team": "Crystal Palace", "total": 9},
            {"player": "Morgan Rogers", "team": "Aston Villa", "total": 9},
            {"player": "Antoine Semenyo", "team": "Bournemouth", "total": 9}
        ],
        "clean_sheets": [
            {"player": "Matz Sels", "team": "Nottingham Forest", "total": 13},
            {"player": "David Raya", "team": "Arsenal FC", "total": 12},
            {"player": "Alisson", "team": "Liverpool FC", "total": 10},
            {"player": "Jordan Pickford", "team": "Everton FC", "total": 10},
            {"player": "Dean Henderson", "team": "Crystal Palace", "total": 10},
            {"player": "André Onana", "team": "Manchester United", "total": 9},
            {"player": "Ederson", "team": "Manchester City", "total": 7},
            {"player": "Kepa Arrizabalaga", "team": "AFC Bournemouth", "total": 7},
            {"player": "Robert Sánchez", "team": "Chelsea FC", "total": 7},
            {"player": "Nick Pope", "team": "Newcastle", "total": 6}
        ],
        "discipline": [
            {"player": "Bruno Fernandes", "team": "Man Utd", "yellow_cards": 2},
            {"player": "Lewis-Skelly", "team": "Arsenal", "red_cards": 2},
            {"player": "Joelinton", "team": "Newcastle", "red_cards": 10},
            {"player": "Flynn Downes", "team": "Southampton", "yellow_cards": 10},
            {"player": "Caicedo", "team": "Chelsea", "yellow_cards": 10},
            {"player": "Sam Morsy", "team": "Ipswich Town", "yellow_cards": 9},
            {"player": "Burn", "team": "Newcastle", "yellow_cards": 9},
            {"player": "Ryan Christie", "team": "Bournemouth", "yellow_cards": 9},
            {"player": "Ugarte", "team": "Man Utd", "yellow_cards": 9},
            {"player": "Ryan Yates", "team": "Nottingham Forest", "yellow_cards": 9},
            {"player": "Daniel Muñoz", "team": "Crystal Palace", "yellow_cards": 9},
            {"player": "Morgan Rogers", "team": "Aston Villa", "yellow_cards": 9},
            {"player": "Antoine Semenyo", "team": "Bournemouth", "yellow_cards": 9}
        ]
    },

    # La Liga Data
    "La Liga": {
        "competition_id": 2014,
        "goals": [
            {"player": "Lewandowski", "team": "Barcelona", "total": 25, "penalties": 3},
            {"player": "Mbappé", "team": "Real Madrid", "total": 22, "penalties": 6},
            {"player": "Budimir", "team": "Osasuna", "total": 18, "penalties": 8},
            {"player": "Raphinha", "team": "Barcelona", "total": 15, "penalties": 2},
            {"player": "Alvarez", "team": "Atletico Madrid", "total": 15, "penalties": 4},
            {"player": "Oihan Sancet", "team": "Athletic Club", "total": 15, "penalties": 3},
            {"player": "Ayoze Perez", "team": "Villarreal", "total": 14},
            {"player": "Sorloth", "team": "Atletico Madrid", "total": 13, "penalties": 1},
            {"player": "Kike", "team": "Deportivo Alaves", "total": 12, "penalties": 2},
            {"player": "Dodi Lukébakio", "team": "Sevilla", "total": 11, "penalties": 1},
            {"player": "Vinicius", "team": "Real Madrid", "total": 11, "penalties": 2},
            {"player": "Puado", "team": "Espanyol", "total": 11, "penalties": 4},
            {"player": "Ferran Torres", "team": "Barcelona", "total": 10}
        ],
        "assists": [
            {"player": "Yamal", "team": "Barcelona", "total": 13},
            {"player": "Raphinha", "team": "Barcelona", "total": 9},
            {"player": "I.Williams", "team": "Athletic Club", "total": 8},
            {"player": "Dani Rodriguez", "team": "RCD Mallorca", "total": 7},
            {"player": "Berenguer", "team": "Athletic Club", "total": 7},
            {"player": "Álex Baena", "team": "Villarreal", "total": 7},
            {"player": "Sergi Cardona", "team": "Villarreal", "total": 7},
            {"player": "Bellingham", "team": "Real Madrid", "total": 7},
            {"player": "Griezmann", "team": "Atletico Madrid", "total": 6},
            {"player": "Saul", "team": "Sevilla", "total": 6},
            {"player": "McBurnie", "team": "Las Palmas", "total": 6},
            {"player": "Óscar Mingueza", "team": "Celta", "total": 6},
            {"player": "Giuliano Simeone", "team": "Atletico Madrid", "total": 6}
        ],
        "clean_sheets": [
            {"player": "Jan Oblak", "team": "Atlético de Madrid", "total": 13},
            {"player": "Alex Remiro", "team": "Real Sociedad", "total": 12},
            {"player": "Thibaut Courtois", "team": "Real Madrid", "total": 11},
            {"player": "David Soria", "team": "Getafe CF", "total": 9},
            {"player": "Marko Dmitrovic", "team": "CD Leganés", "total": 8},
            {"player": "Wojciech Szczesny", "team": "FC Barcelona", "total": 7},
            {"player": "Oijan Nyland", "team": "Sevilla FC", "total": 7},
            {"player": "Antonio Sivera", "team": "Deportivo Alavés", "total": 7},
            {"player": "Vicente Guaita", "team": "Celta de Vigo", "total": 7},
            {"player": "Giorgi Mamardashvili", "team": "Valencia CF", "total": 7}
        ],
        "discipline": [
            {"player": "Mario Martín", "team": "Valladolid", "yellow_cards": 3},
            {"player": "Vedat Muriqi", "team": "RCD Mallorca", "yellow_cards": 2},
            {"player": "Pape Gueye", "team": "Villarreal", "yellow_cards": 2},
            {"player": "Dário Essugo", "team": "Las Palmas", "yellow_cards": 2},
            {"player": "Christantus Uche", "team": "Getafe", "yellow_cards": 2},
            {"player": "Aspas", "team": "Celta", "yellow_cards": 1},
            {"player": "Kike", "team": "Alaves", "yellow_cards": 1},
            {"player": "Alonso", "team": "Celta", "yellow_cards": 1},
            {"player": "Juan Carlos", "team": "Girona", "yellow_cards": 1},
            {"player": "Saul", "team": "Sevilla", "yellow_cards": 1},
            {"player": "Chimy Ávila", "team": "Betis", "yellow_cards": 1},
            {"player": "Antonio Rafilo", "team": "RCD Mallorca", "yellow_cards": 1},
            {"player": "Mascarell", "team": "RCD Mallorca", "yellow_cards": 1}
        ]
    },

    # Bundesliga Data
    "Bundesliga": {
        "competition_id": 2002,
        "goals": [
            {"player": "Kane", "team": "Bayern Munich", "total": 24, "penalties": 9},
            {"player": "Schick", "team": "Bayer Leverkusen", "total": 18},
            {"player": "Guirassy", "team": "Borussia Dortmund", "total": 16, "penalties": 2},
            {"player": "Kleindienst", "team": "Borussia M'gladbach", "total": 15, "penalties": 1},
            {"player": "Omar Marmoush", "team": "Eintracht Frankfurt", "total": 15, "penalties": 2},
            {"player": "Jonathan Burkardt", "team": "Mainz 05", "total": 15, "penalties": 1},
            {"player": "Hugo Ekitiké", "team": "Eintracht Frankfurt", "total": 14, "penalties": 1},
            {"player": "Ermedin Demirovi?", "team": "Stuttgart", "total": 13},
            {"player": "Musiala", "team": "Bayern Munich", "total": 12},
            {"player": "Benjamin Sesko", "team": "RB Leipzig", "total": 12, "penalties": 2},
            {"player": "Kramari?", "team": "Hoffenheim", "total": 11, "penalties": 3},
            {"player": "Plea", "team": "Borussia M'gladbach", "total": 10, "penalties": 1},
            {"player": "Mohamed Amoura", "team": "Wolfsburg", "total": 10, "penalties": 2}
        ],
        "assists": [
            {"player": "Kohr", "team": "Mainz", "total": 11},
            {"player": "Matus Bero", "team": "Bochum", "total": 10},
            {"player": "Gouweleeuw", "team": "Augsburg", "total": 9},
            {"player": "Benedikt Gimber", "team": "1.FC Heidenheim", "total": 9},
            {"player": "Senne Lynen", "team": "Bremen", "total": 9},
            {"player": "Jens Stage", "team": "Bremen", "total": 9},
            {"player": "Nicolai Remberg", "team": "Holstein Kiel", "total": 9},
            {"player": "Maximilian Wittek", "team": "Bochum", "total": 8},
            {"player": "Atakan Karazor", "team": "Stuttgart", "total": 8},
            {"player": "Ibrahima Sissoko", "team": "Bochum", "total": 8},
            {"player": "Cédric Zesiger", "team": "Augsburg", "total": 8},
            {"player": "Jeff Chabot", "team": "Stuttgart", "total": 8},
            {"player": "Frank Onyeka", "team": "Augsburg", "total": 8}
        ],
        "clean_sheets": [
            {"player": "Peter Gulácsi", "team": "RB Leipzig", "total": 13},
            {"player": "Manuel Neuer", "team": "Bayern Munich", "total": 11},
            {"player": "Noah Atubolu", "team": "SC Freiburg", "total": 10},
            {"player": "Finn Dahmen", "team": "FC Augsburg", "total": 9},
            {"player": "Robin Zentner", "team": "1.FSV Mainz 05", "total": 9},
            {"player": "Frederik Rönnow", "team": "1.FC Union Berlin", "total": 8},
            {"player": "Nikola Vasilj", "team": "FC St. Pauli", "total": 8},
            {"player": "Michael Zetterer", "team": "SV Werder Bremen", "total": 8},
            {"player": "Kevin Trapp", "team": "Eintracht Frankfurt", "total": 6},
            {"player": "Lukas Hradecky", "team": "Bayer 04 Leverkusen", "total": 6},
            {"player": "Kevin Müller", "team": "1.FC Heidenheim", "total": 6}
        ],
        "discipline": [
            {"player": "Orban", "team": "Leipzig", "yellow_cards": 2},
            {"player": "Amiri", "team": "Mainz", "yellow_cards": 2},
            {"player": "Friedl", "team": "Bremen", "yellow_cards": 2},
            {"player": "Schlotterbeck", "team": "Dortmund", "yellow_cards": 2},
            {"player": "Holtby", "team": "Holstein Kiel", "yellow_cards": 1},
            {"player": "Gross", "team": "Dortmund", "yellow_cards": 1},
            {"player": "Weiser", "team": "Bremen", "yellow_cards": 1},
            {"player": "Emre Can", "team": "Dortmund", "yellow_cards": 1},
            {"player": "Grimaldo", "team": "Leverkusen", "yellow_cards": 1},
            {"player": "Kohr", "team": "Mainz", "yellow_cards": 1},
            {"player": "N. Stark", "team": "Bremen", "yellow_cards": 1},
            {"player": "Adam Dzwigala", "team": "FC St. Pauli", "yellow_cards": 1},
            {"player": "Gerhardt", "team": "Wolfsburg", "yellow_cards": 1}
        ]
    },

    # Serie A Data
    "Serie A": {
        "competition_id": 2019,
        "goals": [
            {"player": "Mateo Retegui", "team": "Atalanta", "total": 23, "penalties": 3},
            {"player": "Kean", "team": "Fiorentina", "total": 17, "penalties": 1},
            {"player": "Thuram", "team": "Internazionale", "total": 14},
            {"player": "Lookman", "team": "Atalanta", "total": 13, "penalties": 1},
            {"player": "Lukaku", "team": "Napoli", "total": 12, "penalties": 3},
            {"player": "Lautaro", "team": "Internazionale", "total": 12},
            {"player": "Orsolini", "team": "Bologna", "total": 12, "penalties": 3},
            {"player": "Artem Dovbyk", "team": "Roma", "total": 11, "penalties": 2},
            {"player": "Krstovic", "team": "Lecce", "total": 10, "penalties": 2},
            {"player": "Taty Castellanos", "team": "Lazio", "total": 10, "penalties": 2},
            {"player": "Reijnders", "team": "Milan", "total": 10},
            {"player": "Lorenzo Lucca", "team": "Udinese", "total": 10, "penalties": 1},
            {"player": "Adams", "team": "Torino", "total": 9}
        ],
        "assists": [
            {"player": "Rovella", "team": "Lazio", "total": 13},
            {"player": "Izzo", "team": "Monza", "total": 12},
            {"player": "Jaka Bijol", "team": "Udinese", "total": 10},
            {"player": "Saúl Coco", "team": "Torino", "total": 10},
            {"player": "Liam Henderson", "team": "Empoli", "total": 9},
            {"player": "Goldaniga", "team": "Como", "total": 9},
            {"player": "Zaccagni", "team": "Lazio", "total": 9},
            {"player": "Isak Hien", "team": "Atalanta", "total": 9},
            {"player": "Diego Coppola", "team": "Verona", "total": 9},
            {"player": "A.Grassi", "team": "Empoli", "total": 8},
            {"player": "Duda", "team": "Verona", "total": 8},
            {"player": "Pedro Pereira", "team": "Monza", "total": 8},
            {"player": "Lorenzo Lucca", "team": "Udinese", "total": 8}
        ],
        "clean_sheets": [
            {"player": "Mile Svilar", "team": "Roma", "goals_conceded": 32},
            {"player": "Alex Meret", "team": "Napoli", "goals_conceded": 23},
            {"player": "Michele Di Gregorio", "team": "Monza", "goals_conceded": 28},
            {"player": "Marco Carnesecchi", "team": "Atalanta", "goals_conceded": 29},
            {"player": "Yann Sommer", "team": "Inter Milan", "goals_conceded": 29},
            {"player": "David De Gea", "team": "Roma", "goals_conceded": 30},
            {"player": "Nicola Leali", "team": "Lazio", "goals_conceded": 25},
            {"player": "Vanja Milinkovic-Savic", "team": "Torino", "goals_conceded": 34},
            {"player": "Mike Maignan", "team": "Milan", "goals_conceded": 36},
            {"player": "Lorenzo Montipo", "team": "Verona", "goals_conceded": 59}
        ],
        "discipline": [
            {"player": "Guilbert", "team": "Lecce", "yellow_cards": 2},
            {"player": "Tommaso Pobega", "team": "Bologna", "yellow_cards": 2},
            {"player": "S. Touré", "team": "Udinese", "yellow_cards": 2},
            {"player": "Reda Belahyane", "team": "Lazio", "yellow_cards": 2},
            {"player": "D'Ambrosio", "team": "Monza", "yellow_cards": 1},
            {"player": "De Sciglio", "team": "Empoli", "yellow_cards": 1},
            {"player": "Mari", "team": "Fiorentina", "yellow_cards": 1},
            {"player": "Rebic", "team": "Lecce", "yellow_cards": 1},
            {"player": "Alli", "team": "Como", "yellow_cards": 1},
            {"player": "Kempf", "team": "Como", "yellow_cards": 1},
            {"player": "Romagnoli", "team": "Lazio", "yellow_cards": 1},
            {"player": "Maripán", "team": "Torino", "yellow_cards": 1},
            {"player": "Hassane Kamara", "team": "Udinese", "yellow_cards": 1}
        ]
    },

    # Ligue 1 Data
    "Ligue 1": {
        "competition_id": 2015,
        "goals": [
            {"player": "Dembélé", "team": "Paris Saint-Germain", "total": 21, "penalties": 1},
            {"player": "Greenwood", "team": "Olympique Lyon", "total": 18, "penalties": 6},
            {"player": "Jonathan David", "team": "Lille", "total": 16, "penalties": 6},
            {"player": "Muinga", "team": "Rennes", "total": 14, "penalties": 5},
            {"player": "Barcola", "team": "Paris Saint-Germain", "total": 13},
            {"player": "Emanuel Emegha", "team": "Strasbourg", "total": 13},
            {"player": "Lacazette", "team": "Olympique Lyon", "total": 12, "penalties": 4},
            {"player": "Ludovic Ajorque", "team": "Stade Brestois", "total": 12},
            {"player": "Mika Biereth", "team": "Monaco", "total": 12, "penalties": 1},
            {"player": "Lucas Stassin", "team": "Saint-Étienne", "total": 12},
            {"player": "Keito Nakamura", "team": "Stade de Reims", "total": 11},
            {"player": "Evann Guessand", "team": "Nice", "total": 11},
            {"player": "Hamed Junior Traorè", "team": "Auxerre", "total": 10}
        ],
        "assists": [
            {"player": "André", "team": "Lille", "total": 11},
            {"player": "Facundo Medina", "team": "Lens", "total": 10},
            {"player": "Modibo Sagnan", "team": "Montpellier", "total": 10},
            {"player": "Rabby Nzingoula", "team": "Montpellier", "total": 10},
            {"player": "Cristian Cásseres Jr.", "team": "Toulouse", "total": 9},
            {"player": "Hicham Boudaoui", "team": "Nice", "total": 9},
            {"player": "Alexsandro", "team": "Lille", "total": 9},
            {"player": "Pallois", "team": "Nantes", "total": 8},
            {"player": "Caleta-Car", "team": "Lyon", "total": 8},
            {"player": "Lorenz Assignon", "team": "Rennes", "total": 8},
            {"player": "Lamine Camara", "team": "Monaco", "total": 8},
            {"player": "Jonathan Clauss", "team": "Nice", "total": 7},
            {"player": "Aliou Baldé", "team": "Angers", "total": 7}
        ],
        "clean_sheets": [
            {"player": "Brice Samba", "team": "Lens", "total": 11},
            {"player": "Djordje Petrovic", "team": "RC Strasbourg Alsace", "total": 10},
            {"player": "Lucas Chevalier", "team": "LOSC Lille", "total": 10},
            {"player": "Guillaume Restes", "team": "FC Toulouse", "total": 9},
            {"player": "Lucas Perri", "team": "Olympique Lyon", "total": 9},
            {"player": "Donovan Leon", "team": "AJ Auxerre", "total": 8},
            {"player": "Marco Bizot", "team": "Stade Brestois 29", "total": 8},
            {"player": "Philipp Köhn", "team": "AS Monaco", "total": 7},
            {"player": "Steve Mandanda", "team": "Stade Rennais FC", "total": 6}
        ],
        "discipline": [
            {"player": "Barcola", "team": "PSG", "yellow_cards": 1},
            {"player": "Moses Simon", "team": "Nantes", "yellow_cards": 9},
            {"player": "Cherki", "team": "Lyon", "yellow_cards": 9},
            {"player": "Dilane Bakwa", "team": "Strasbourg", "yellow_cards": 9},
            {"player": "Gaëtan Perrin", "team": "Auxerre", "yellow_cards": 8},
            {"player": "Maghnes Akliouche", "team": "Monaco", "yellow_cards": 8},
            {"player": "João Neves", "team": "PSG", "yellow_cards": 8},
            {"player": "Jonathan Clauss", "team": "Nice", "yellow_cards": 7},
            {"player": "L.Blas", "team": "Rennes", "yellow_cards": 7},
            {"player": "Mathias Pereira Lage", "team": "Stade Brestois", "yellow_cards": 7},
            {"player": "Zuriko Davitashvili", "team": "Saint-Étienne", "yellow_cards": 7},
            {"player": "Evann Guessand", "team": "Nice", "yellow_cards": 7},
            {"player": "Gabriel Suazo", "team": "Toulouse", "yellow_cards": 6}
        ]
    }
}