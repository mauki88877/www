import random

adjectives = [
    "adhesive",
    "adorable",
    "adversarial",
    "affectionate",
    "aggravated",
    "anal",
    "atrocious",
    "awkward",
    "baby",
    "bewildered",
    "bighuge",
    "black",
    "blazed",
    "bloodshot",
    "brown",
    "cheeky",
    "childish",
    "cold",
    "constipated",
    "corrupted",
    "cosmic",
    "crafty",
    "crazed",
    "creamy",
    "crispy",
    "crumbly",
    "crunchy",
    "cryptic",
    "cuddly",
    "cute",
    "dark",
    "dastardly",
    "deep",
    "demonic",
    "depressed",
    "depraved",
    "derogatory",
    "despicable",
    "devilish",
    "devious",
    "diabolic",
    "diabolical",
    "difficult",
    "dismal",
    "disturbed",
    "dramatic",
    "drunk",
    "effeminate",
    "embarrassed",
    "enigmatic",
    "enlightened",
    "esoteric",
    "ethereal",
    "euphoric",
    "evil",
    "exquisite",
    "extreme",
    "feathery",
    "ferocious",
    "fiendish",
    "fierce",
    "fleecy",
    "flirtatious",
    "frenetic",
    "frothy",
    "furry",
    "fuzzy",
    "gay",
    "gentle",
    "giddy",
    "glutinous",
    "grievous",
    "gummy",
    "hallucinogenic",
    "hammered",
    "harmful",
    "heated",
    "hectic",
    "heightened",
    "heinous",
    "hellish",
    "hideous",
    "hysterical",
    "immoral",
    "incomprehensible",
    "inebriated",
    "inexplicable",
    "infernal",
    "ingenious",
    "inquisitive",
    "insecure",
    "insidious",
    "insightful",
    "insolent",
    "intelligent",
    "intensified",
    "intensive",
    "intoxicated",
    "inventive",
    "large",
    "loveable",
    "malevolent",
    "malicious",
    "manic",
    "masochistic",
    "medicated",
    "mediocre",
    "melodramatic",
    "moist",
    "monstrous",
    "mushy",
    "mysterious",
    "naughty",
    "nefarious",
    "negligent",
    "normal",
    "nihilistic",
    "overcompensating",
    "overmedicated",
    "overwhelming",
    "overzealous",
    "paranoid",
    "pasty",
    "pedantic",
    "pernicious",
    "perturbed",
    "perverted",
    "philosophical",
    "pillowy",
    "pink",
    "pixilated",
    "plastered",
    "playful",
    "plump",
    "powerful",
    "premature",
    "profound",
    "promiscuous",
    "psychic",
    "psychedelic",
    "puffy",
    "pure",
    "queer",
    "questionable",
    "rabid",
    "raging",
    "raving",
    "rambunctious",
    "reckless",
    "ripped",
    "sadistic",
    "satanic",
    "savvy",
    "scheming",
    "schizophrenic",
    "secretive",
    "sedated",
    "senile",
    "severe",
    "shaggy",
    "sinful",
    "sinister",
    "slippery",
    "sly",
    "sneaky",
    "soft",
    "sophisticated",
    "spiteful",
    "squishy",
    "steamy",
    "sticky",
    "stoned",
    "strained",
    "strenuous",
    "stuffed",
    "stumped",
    "subtle",
    "suggestive",
    "suicidal",
    "sudden",
    "sunburned",
    "surreal",
    "suspicious",
    "sycophantic",
    "sweet",
    "tense",
    "terrible",
    "terrific",
    "thick",
    "thoughtful",
    "ticklish",
    "tiny",
    "tortured",
    "tricky",
    "tufty",
    "twitchy",
    "ugly",
    "unabated",
    "unexplained",
    "unholy",
    "unmedicated",
    "unmelted",
    "unmitigated",
    "unrestrained",
    "unworthy",
    "utmost",
    "vehement",
    "vicious",
    "vigorous",
    "vile",
    "violent",
    "vivid",
    "wasted",
    "wet",
    "whimsical",
    "white",
    "wicked",
    "wild",
    "wispy",
    "witty",
    "woolly",
]

names = [
    "aaron",
    "abigail",
    "adam",
    "alan",
    "albert",
    "alex",
    "alexander",
    "alexis",
    "alice",
    "allen",
    "allison",
    "alyssa",
    "amanda",
    "amber",
    "amy",
    "andrea",
    "andrew",
    "angela",
    "ann",
    "anna",
    "anne",
    "annie",
    "anthony",
    "antonio",
    "aragorn",
    "arthur",
    "arwen",
    "ashley",
    "audrey",
    "austin",
    "baggins",
    "barbara",
    "bellatrix",
    "benjamin",
    "betty",
    "beverly",
    "bilbo",
    "billy",
    "bobby",
    "bombadil",
    "bonnie",
    "boromir",
    "bradley",
    "brandon",
    "brandybuck",
    "brenda",
    "brian",
    "brianna",
    "brittany",
    "bruce",
    "bryan",
    "caleb",
    "cameron",
    "carl",
    "carlos",
    "carol",
    "carolyn",
    "carrie",
    "catherine",
    "charles",
    "charlotte",
    "cheryl",
    "christian",
    "christina",
    "christine",
    "christopher",
    "cindy",
    "clara",
    "clarence",
    "cody",
    "connie",
    "courtney",
    "craig",
    "crystal",
    "curtis",
    "cynthia",
    "dale",
    "daniel",
    "danielle",
    "danny",
    "david",
    "dawn",
    "deborah",
    "debra",
    "deckard",
    "denethor",
    "denise",
    "dennis",
    "diana",
    "diane",
    "dobby",
    "donald",
    "donna",
    "dooku",
    "doris",
    "dorothy",
    "douglas",
    "draco",
    "dumbledore",
    "dylan",
    "earl",
    "edith",
    "edna",
    "edward",
    "elaine",
    "eleanor",
    "elendil",
    "elijah",
    "elizabeth",
    "ella",
    "ellen",
    "elrond",
    "emily",
    "emma",
    "eomer",
    "eomund",
    "eothain",
    "eowyn",
    "eric",
    "erin",
    "ernest",
    "esther",
    "ethan",
    "ethel",
    "eugene",
    "eva",
    "evan",
    "evelyn",
    "faramir",
    "florence",
    "frances",
    "francis",
    "frank",
    "fred",
    "frederick",
    "frodo",
    "gabriel",
    "galadriel",
    "gandalf",
    "gary",
    "george",
    "gerald",
    "gimli",
    "gladys",
    "glenn",
    "glorfindel",
    "gloria",
    "goldberry",
    "gollum",
    "grace",
    "gregory",
    "hagrid",
    "hannah",
    "harold",
    "harry",
    "hazel",
    "heather",
    "helen",
    "henry",
    "hermione",
    "howard",
    "irene",
    "isaac",
    "isabella",
    "isildur",
    "jack",
    "jacob",
    "jacqueline",
    "james",
    "jamie",
    "jane",
    "janet",
    "janice",
    "jasmine",
    "jason",
    "jean",
    "jeffrey",
    "jennifer",
    "jeremy",
    "jerry",
    "jesse",
    "jessica",
    "jimmy",
    "joan",
    "joe",
    "joel",
    "john",
    "johnny",
    "jonathan",
    "jordan",
    "jose",
    "joseph",
    "josephine",
    "josh",
    "joyce",
    "juan",
    "judith",
    "judy",
    "julia",
    "julie",
    "justin",
    "karen",
    "katherine",
    "kathleen",
    "kathryn",
    "kathy",
    "kayla",
    "keith",
    "kelly",
    "kenneth",
    "kenobi",
    "kevin",
    "kimberly",
    "kyle",
    "lantern",
    "larry",
    "laura",
    "lauren",
    "lawrence",
    "legolas",
    "leia",
    "leonard",
    "leslie",
    "lillian",
    "linda",
    "lisa",
    "logan",
    "lois",
    "lori",
    "louis",
    "louise",
    "luis",
    "luke",
    "lupin",
    "madison",
    "margaret",
    "maria",
    "marie",
    "marilyn",
    "marjorie",
    "mark",
    "martha",
    "martin",
    "marvin",
    "mary",
    "mason",
    "matthew",
    "megan",
    "melissa",
    "melvin",
    "merry",
    "michael",
    "michelle",
    "mildred",
    "monica",
    "nancy",
    "natalie",
    "nathan",
    "nathaniel",
    "nazgul",
    "nicholas",
    "nicole",
    "noah",
    "norma",
    "norman",
    "obama",
    "olivia",
    "padme",
    "pamela",
    "patricia",
    "patrick",
    "paul",
    "paula",
    "peggy",
    "peter",
    "philip",
    "phillip",
    "phyllis",
    "pippin",
    "rachel",
    "radagast",
    "ralph",
    "randy",
    "raymond",
    "rebecca",
    "richard",
    "rita",
    "robert",
    "robin",
    "rodney",
    "roger",
    "ron",
    "ronald",
    "rose",
    "roy",
    "ruby",
    "russell",
    "ruth",
    "ryan",
    "samantha",
    "samuel",
    "samwise",
    "sandra",
    "sara",
    "sarah",
    "saruman",
    "sauron",
    "scott",
    "sean",
    "shannon",
    "sharon",
    "shawn",
    "shelob",
    "shirley",
    "sirius",
    "skywalker",
    "snape",
    "sophia",
    "stanley",
    "stephanie",
    "stephen",
    "steven",
    "susan",
    "tammy",
    "taylor",
    "teresa",
    "terry",
    "theoden",
    "theresa",
    "thomas",
    "tiffany",
    "timothy",
    "tina",
    "todd",
    "tony",
    "tracy",
    "travis",
    "treebeard",
    "tyler",
    "tyrell",
    "vader",
    "valerie",
    "vanessa",
    "victor",
    "victoria",
    "vincent",
    "virginia",
    "voldemort",
    "wallace",
    "walter",
    "wanda",
    "wayne",
    "wendy",
    "william",
    "willie",
    "wormtongue",
    "yoda",
    "zachary",
]


def random_name():
    name = f"{random.choice(adjectives)}_{random.choice(names)}"
    if name == "white_lantern":
        name = "black_lantern"
    return name
