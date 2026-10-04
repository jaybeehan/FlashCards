"""Alberta (Canada) high school courses and units, by grade and subject.

Unit lists follow the Alberta Education programs of study (Math, Science, Social Studies, ELA).
Edit freely: any course or unit you add here shows up in the web page automatically.
"""

ELA_UNITS = [
    "Short Stories", "Novel Study", "Poetry", "Drama and Shakespeare",
    "Essay and Persuasive Writing", "Literary Devices and Analysis",
    "Grammar and Language Conventions", "Media and Visual Literacy",
]

CURRICULUM = {
    "9": {
        "Mathematics": {
            "Mathematics 9": [
                "Rational Numbers", "Exponents and Powers", "Square Roots and the Pythagorean Theorem",
                "Polynomials", "Linear Relations", "Linear Equations and Inequalities",
                "Similarity and Scale", "Surface Area and Volume", "Statistics and Probability",
            ],
        },
        "Science": {
            "Science 9": [
                "Biological Diversity", "Matter and Chemical Change", "Environmental Chemistry",
                "Electrical Principles and Technologies", "Space Exploration",
            ],
        },
        "Social Studies": {
            "Social Studies 9": [
                "Issues for Canadians: Governance and Rights",
                "Issues for Canadians: Economic Systems",
            ],
        },
        "English Language Arts": {"English Language Arts 9": ELA_UNITS},
    },
    "10": {
        "Mathematics": {
            "Mathematics 10C": [
                "Measurement (SI and Imperial)", "Trigonometry of Right Triangles", "Factors and Products",
                "Roots and Powers", "Relations and Functions", "Linear Functions and Graphs",
                "Systems of Linear Equations",
            ],
        },
        "Science": {
            "Science 10": [
                "Energy and Matter in Chemical Change", "Energy Flow in Technological Systems",
                "Cycling of Matter in Living Systems", "Energy Flow in Global Systems",
            ],
        },
        "Social Studies": {
            "Social Studies 10-1": ["Perspectives on Globalization"],
            "Social Studies 10-2": ["Living in a Globalizing World"],
        },
        "English Language Arts": {
            "English Language Arts 10-1": ELA_UNITS,
            "English Language Arts 10-2": ELA_UNITS,
        },
    },
    "11": {
        "Mathematics": {
            "Mathematics 20-1": [
                "Sequences and Series", "Trigonometry", "Quadratic Functions", "Quadratic Equations",
                "Radical Expressions and Equations", "Rational Expressions and Equations",
                "Absolute Value and Reciprocal Functions", "Systems of Equations and Inequalities",
            ],
            "Mathematics 20-2": [
                "Geometry and Measurement", "Logical Reasoning", "Probability", "Quadratic Functions",
                "Rational Expressions and Equations", "Statistics (Normal Distribution)",
                "Systems of Linear Inequalities",
            ],
            "Mathematics 20-3": [
                "Measurement", "Right Triangle Trigonometry", "Algebra and Number", "Linear Relations",
                "Statistics", "Financial Mathematics",
            ],
        },
        "Science": {
            "Science 20": [
                "Dynamics of Ecosystems", "Chemical Change", "Changes in Motion", "Changing Earth",
            ],
        },
        "Biology": {
            "Biology 20": [
                "Energy and Matter Exchange in the Biosphere", "Ecosystems and Population Change",
                "Photosynthesis and Cellular Respiration", "Human Systems",
            ],
        },
        "Chemistry": {
            "Chemistry 20": [
                "Diversity of Matter and Chemical Bonding", "Forms of Matter: Gases",
                "Matter as Solutions, Acids and Bases", "Quantitative Relationships in Chemical Changes",
            ],
        },
        "Physics": {
            "Physics 20": [
                "Kinematics", "Dynamics", "Circular Motion, Work and Energy",
                "Oscillatory Motion and Mechanical Waves",
            ],
        },
        "Social Studies": {
            "Social Studies 20-1": ["Perspectives on Nationalism"],
            "Social Studies 20-2": ["Understandings of Nationalism"],
        },
        "English Language Arts": {
            "English Language Arts 20-1": ELA_UNITS,
            "English Language Arts 20-2": ELA_UNITS,
        },
    },
    "12": {
        "Mathematics": {
            "Mathematics 30-1": [
                "Transformations of Functions", "Radical Functions", "Polynomial Functions",
                "Trigonometric Functions", "Exponential and Logarithmic Functions",
                "Rational Functions", "Function Operations", "Permutations, Combinations and Binomial Theorem",
            ],
            "Mathematics 30-2": [
                "Logic and Set Theory", "Probability", "Rational Expressions and Equations",
                "Polynomial Functions", "Exponential and Logarithmic Functions", "Sinusoidal Functions",
            ],
            "Mathematics 30-3": [
                "Algebra and Number", "Trigonometry", "Statistics and Probability",
                "Financial Mathematics", "Linear and Non-linear Relations",
            ],
        },
        "Science": {
            "Science 30": [
                "Living Systems Respond to their Environment", "Chemistry and the Environment",
                "Electromagnetic Energy", "Energy and the Environment",
            ],
        },
        "Biology": {
            "Biology 30": [
                "Nervous and Endocrine Systems", "Reproductive Systems and Development",
                "Cell Division, Genetics and Molecular Biology", "Population Dynamics",
            ],
        },
        "Chemistry": {
            "Chemistry 30": [
                "Thermochemical Changes", "Electrochemical Changes", "Organic Chemistry",
                "Chemical Equilibrium Focusing on Acid-Base Systems",
            ],
        },
        "Physics": {
            "Physics 30": [
                "Momentum and Impulse", "Forces and Fields", "Electromagnetic Radiation", "Atomic Physics",
            ],
        },
        "Social Studies": {
            "Social Studies 30-1": ["Perspectives on Ideology"],
            "Social Studies 30-2": ["Understandings of Ideology"],
        },
        "English Language Arts": {
            "English Language Arts 30-1": ELA_UNITS,
            "English Language Arts 30-2": ELA_UNITS,
        },
    },
}

CORE_SUBJECTS = ["Mathematics", "Science", "Social Studies", "English Language Arts"]
CORE_LABEL = "Core Subjects (mixed)"
ALL_UNITS = "All units"
