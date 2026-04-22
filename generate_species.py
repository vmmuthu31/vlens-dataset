"""
Vlens-Trust: Species Annotations Dataset Generator
Generates 3,200 rows (1,600 plant + 1,600 animal) with real taxonomy
"""
import pandas as pd
import numpy as np
import json

np.random.seed(42)

# ─────────────────────────────────────────────────────────────
# REAL PLANT TAXONOMY
# ─────────────────────────────────────────────────────────────
MEDICINAL_PLANTS = [
    ("Ashwagandha",          "Withania somnifera",          "Withania",       "Solanaceae",      "Withania_somnifera"),
    ("Turmeric",             "Curcuma longa",               "Curcuma",        "Zingiberaceae",   "Turmeric"),
    ("Neem",                 "Azadirachta indica",          "Azadirachta",    "Meliaceae",       "Azadirachta_indica"),
    ("Holy Basil (Tulsi)",   "Ocimum tenuiflorum",          "Ocimum",         "Lamiaceae",       "Ocimum_tenuiflorum"),
    ("Brahmi",               "Bacopa monnieri",             "Bacopa",         "Plantaginaceae",  "Bacopa_monnieri"),
    ("Shatavari",            "Asparagus racemosus",         "Asparagus",      "Asparagaceae",    "Asparagus_racemosus"),
    ("Giloy (Guduchi)",      "Tinospora cordifolia",        "Tinospora",      "Menispermaceae",  "Tinospora_cordifolia"),
    ("Amla (Indian Gooseberry)", "Phyllanthus emblica",     "Phyllanthus",    "Phyllanthaceae",  "Phyllanthus_emblica"),
    ("Ginger",               "Zingiber officinale",         "Zingiber",       "Zingiberaceae",   "Zingiber_officinale"),
    ("Black Pepper",         "Piper nigrum",                "Piper",          "Piperaceae",      "Black_pepper"),
    ("Fenugreek",            "Trigonella foenum-graecum",   "Trigonella",     "Fabaceae",        "Fenugreek"),
    ("Moringa (Drumstick)",  "Moringa oleifera",            "Moringa",        "Moringaceae",     "Moringa_oleifera"),
    ("Haritaki",             "Terminalia chebula",          "Terminalia",     "Combretaceae",    "Terminalia_chebula"),
    ("Bibhitaki",            "Terminalia bellirica",        "Terminalia",     "Combretaceae",    "Terminalia_bellirica"),
    ("Senna",                "Senna alexandrina",           "Senna",          "Fabaceae",        "Senna_alexandrina"),
    ("Licorice (Mulethi)",   "Glycyrrhiza glabra",          "Glycyrrhiza",    "Fabaceae",        "Liquorice"),
    ("Cardamom",             "Elettaria cardamomum",        "Elettaria",      "Zingiberaceae",   "Cardamom"),
    ("Cinnamon",             "Cinnamomum verum",            "Cinnamomum",     "Lauraceae",       "Cinnamomum_verum"),
    ("Clove",                "Syzygium aromaticum",         "Syzygium",       "Myrtaceae",       "Clove"),
    ("Peppermint",           "Mentha x piperita",           "Mentha",         "Lamiaceae",       "Peppermint"),
    ("Valerian",             "Valeriana officinalis",       "Valeriana",      "Caprifoliaceae",  "Valerian"),
    ("Echinacea",            "Echinacea purpurea",          "Echinacea",      "Asteraceae",      "Echinacea_purpurea"),
    ("St. John's Wort",      "Hypericum perforatum",        "Hypericum",      "Hypericaceae",    "Hypericum_perforatum"),
    ("Chamomile",            "Matricaria chamomilla",       "Matricaria",     "Asteraceae",      "Matricaria_chamomilla"),
    ("Lavender",             "Lavandula angustifolia",      "Lavandula",      "Lamiaceae",       "Lavandula_angustifolia"),
    ("Ginseng",              "Panax ginseng",               "Panax",          "Araliaceae",      "Panax_ginseng"),
    ("Green Tea",            "Camellia sinensis",           "Camellia",       "Theaceae",        "Camellia_sinensis"),
    ("Aloe Vera",            "Aloe barbadensis",            "Aloe",           "Xanthorrhoeaceae","Aloe_vera"),
    ("Andrographis",         "Andrographis paniculata",     "Andrographis",   "Acanthaceae",     "Andrographis_paniculata"),
    ("Safed Musli",          "Chlorophytum borivilianum",   "Chlorophytum",   "Asparagaceae",    "Chlorophytum_borivilianum"),
    ("Punarnava",            "Boerhavia diffusa",           "Boerhavia",      "Nyctaginaceae",   "Boerhavia_diffusa"),
    ("Gurmar",               "Gymnema sylvestre",           "Gymnema",        "Apocynaceae",     "Gymnema_sylvestre"),
    ("Bitter Melon",         "Momordica charantia",         "Momordica",      "Cucurbitaceae",   "Momordica_charantia"),
    ("Triphala (Vibhitaki)", "Terminalia arjuna",           "Terminalia",     "Combretaceae",    "Terminalia_arjuna"),
    ("Long Pepper (Pippali)","Piper longum",                "Piper",          "Piperaceae",      "Piper_longum"),
    ("Garcinia",             "Garcinia cambogia",           "Garcinia",       "Clusiaceae",      "Garcinia_cambogia"),
    ("Coleus (Forskolin)",   "Coleus forskohlii",           "Coleus",         "Lamiaceae",       "Coleus_forskohlii"),
    ("Boswellia (Shallaki)", "Boswellia serrata",           "Boswellia",      "Burseraceae",     "Boswellia_serrata"),
    ("Triphala (Haritaki)",  "Terminalia chebula",          "Terminalia",     "Combretaceae",    "Terminalia_chebula"),
    ("Shankhapushpi",        "Convolvulus pluricaulis",     "Convolvulus",    "Convolvulaceae",  "Convolvulus_pluricaulis"),
]

ORNAMENTAL_PLANTS = [
    ("Rose",                "Rosa hybrida",                 "Rosa",           "Rosaceae",        "Rose"),
    ("Moth Orchid",         "Phalaenopsis amabilis",        "Phalaenopsis",   "Orchidaceae",     "Phalaenopsis_amabilis"),
    ("Sunflower",           "Helianthus annuus",            "Helianthus",     "Asteraceae",      "Sunflower"),
    ("African Marigold",    "Tagetes erecta",               "Tagetes",        "Asteraceae",      "Tagetes_erecta"),
    ("Jasmine (Mogra)",     "Jasminum sambac",              "Jasminum",       "Oleaceae",        "Jasminum_sambac"),
    ("Hibiscus",            "Hibiscus rosa-sinensis",       "Hibiscus",       "Malvaceae",       "Hibiscus_rosa-sinensis"),
    ("Lotus",               "Nelumbo nucifera",             "Nelumbo",        "Nelumbonaceae",   "Nelumbo_nucifera"),
    ("Bougainvillea",       "Bougainvillea spectabilis",    "Bougainvillea",  "Nyctaginaceae",   "Bougainvillea"),
    ("Chrysanthemum",       "Chrysanthemum morifolium",     "Chrysanthemum",  "Asteraceae",      "Chrysanthemum"),
    ("Dahlia",              "Dahlia pinnata",               "Dahlia",         "Asteraceae",      "Dahlia"),
    ("Peace Lily",          "Spathiphyllum wallisii",       "Spathiphyllum",  "Araceae",         "Spathiphyllum"),
    ("Bird of Paradise",    "Strelitzia reginae",           "Strelitzia",     "Strelitziaceae",  "Strelitzia_reginae"),
    ("Anthurium",           "Anthurium andraeanum",         "Anthurium",      "Araceae",         "Anthurium"),
    ("Gerbera Daisy",       "Gerbera jamesonii",            "Gerbera",        "Asteraceae",      "Gerbera"),
    ("Tiger Lily",          "Lilium lancifolium",           "Lilium",         "Liliaceae",       "Lilium_lancifolium"),
    ("Carnation",           "Dianthus caryophyllus",        "Dianthus",       "Caryophyllaceae", "Dianthus_caryophyllus"),
    ("Petunia",             "Petunia hybrida",              "Petunia",        "Solanaceae",      "Petunia"),
    ("Zinnia",              "Zinnia elegans",               "Zinnia",         "Asteraceae",      "Zinnia_elegans"),
    ("Portulaca",           "Portulaca grandiflora",        "Portulaca",      "Portulacaceae",   "Portulaca_grandiflora"),
    ("Crossandra",          "Crossandra infundibuliformis", "Crossandra",     "Acanthaceae",     "Crossandra_infundibuliformis"),
    ("Ixora",               "Ixora coccinea",               "Ixora",          "Rubiaceae",       "Ixora_coccinea"),
    ("Frangipani (Plumeria)","Plumeria rubra",              "Plumeria",       "Apocynaceae",     "Plumeria"),
    ("Adenium (Desert Rose)","Adenium obesum",              "Adenium",        "Apocynaceae",     "Adenium_obesum"),
    ("Nerium (Oleander)",   "Nerium oleander",              "Nerium",         "Apocynaceae",     "Nerium_oleander"),
    ("Night-blooming Jasmine","Cestrum nocturnum",          "Cestrum",        "Solanaceae",      "Cestrum_nocturnum"),
    ("Periwinkle (Sadabahar)","Catharanthus roseus",        "Catharanthus",   "Apocynaceae",     "Catharanthus_roseus"),
    ("Lantana",             "Lantana camara",               "Lantana",        "Verbenaceae",     "Lantana_camara"),
    ("Tulip",               "Tulipa gesneriana",            "Tulipa",         "Liliaceae",       "Tulip"),
    ("Gladiolus",           "Gladiolus communis",           "Gladiolus",      "Iridaceae",       "Gladiolus"),
    ("Heliconia",           "Heliconia psittacorum",        "Heliconia",      "Heliconiaceae",   "Heliconia"),
]

FOOD_PLANTS = [
    ("Tomato",              "Solanum lycopersicum",         "Solanum",        "Solanaceae",      "Tomato"),
    ("Spinach",             "Spinacia oleracea",            "Spinacia",       "Amaranthaceae",   "Spinach"),
    ("Mango",               "Mangifera indica",             "Mangifera",      "Anacardiaceae",   "Mango"),
    ("Banana",              "Musa acuminata",               "Musa",           "Musaceae",        "Banana"),
    ("Coconut",             "Cocos nucifera",               "Cocos",          "Arecaceae",       "Coconut"),
    ("Papaya",              "Carica papaya",                "Carica",         "Caricaceae",      "Papaya"),
    ("Guava",               "Psidium guajava",              "Psidium",        "Myrtaceae",       "Guava"),
    ("Pomegranate",         "Punica granatum",              "Punica",         "Lythraceae",      "Pomegranate"),
    ("Jackfruit",           "Artocarpus heterophyllus",     "Artocarpus",     "Moraceae",        "Jackfruit"),
    ("Bitter Gourd",        "Momordica charantia",          "Momordica",      "Cucurbitaceae",   "Bitter_melon"),
    ("Brinjal (Eggplant)",  "Solanum melongena",            "Solanum",        "Solanaceae",      "Eggplant"),
    ("Okra (Lady's Finger)","Abelmoschus esculentus",       "Abelmoschus",    "Malvaceae",       "Okra"),
    ("Coriander",           "Coriandrum sativum",           "Coriandrum",     "Apiaceae",        "Coriander"),
    ("Curry Leaf",          "Murraya koenigii",             "Murraya",        "Rutaceae",        "Murraya_koenigii"),
    ("Tamarind",            "Tamarindus indica",            "Tamarindus",     "Fabaceae",        "Tamarind"),
    ("Lemon",               "Citrus limon",                 "Citrus",         "Rutaceae",        "Lemon"),
    ("Bottle Gourd",        "Lagenaria siceraria",          "Lagenaria",      "Cucurbitaceae",   "Lagenaria_siceraria"),
    ("Drumstick (Moringa)", "Moringa oleifera",             "Moringa",        "Moringaceae",     "Moringa_oleifera"),
    ("Ridge Gourd",         "Luffa acutangula",             "Luffa",          "Cucurbitaceae",   "Luffa_acutangula"),
    ("Indian Mustard",      "Brassica juncea",              "Brassica",       "Brassicaceae",    "Brassica_juncea"),
    ("Cluster Bean (Guar)", "Cyamopsis tetragonoloba",      "Cyamopsis",      "Fabaceae",        "Cyamopsis_tetragonoloba"),
    ("Pointed Gourd (Parwal)","Trichosanthes dioica",       "Trichosanthes",  "Cucurbitaceae",   "Trichosanthes_dioica"),
    ("Ivy Gourd (Kundru)",  "Coccinia grandis",             "Coccinia",       "Cucurbitaceae",   "Coccinia_grandis"),
    ("Banana Flower",       "Musa balbisiana",              "Musa",           "Musaceae",        "Musa_balbisiana"),
    ("Sweet Potato",        "Ipomoea batatas",              "Ipomoea",        "Convolvulaceae",  "Sweet_potato"),
    ("Cassava",             "Manihot esculenta",            "Manihot",        "Euphorbiaceae",   "Cassava"),
    ("Amaranth (Rajgira)",  "Amaranthus cruentus",          "Amaranthus",     "Amaranthaceae",   "Amaranthus"),
    ("Horse Gram (Kulthi)", "Macrotyloma uniflorum",        "Macrotyloma",    "Fabaceae",        "Macrotyloma_uniflorum"),
    ("Black-eyed Pea",      "Vigna unguiculata",            "Vigna",          "Fabaceae",        "Vigna_unguiculata"),
    ("Chili Pepper",        "Capsicum annuum",              "Capsicum",       "Solanaceae",      "Chili_pepper"),
]

# ─────────────────────────────────────────────────────────────
# REAL ANIMAL TAXONOMY
# ─────────────────────────────────────────────────────────────
HOUSEHOLD_ANIMALS = [
    ("German Shepherd",         "Canis lupus familiaris",   "Canis",          "Canidae",         "German_Shepherd"),
    ("Labrador Retriever",      "Canis lupus familiaris",   "Canis",          "Canidae",         "Labrador_Retriever"),
    ("Golden Retriever",        "Canis lupus familiaris",   "Canis",          "Canidae",         "Golden_Retriever"),
    ("Indian Pariah Dog",       "Canis lupus familiaris",   "Canis",          "Canidae",         "Indian_Pariah_dog"),
    ("Beagle",                  "Canis lupus familiaris",   "Canis",          "Canidae",         "Beagle"),
    ("Pomeranian",              "Canis lupus familiaris",   "Canis",          "Canidae",         "Pomeranian_(dog)"),
    ("Poodle",                  "Canis lupus familiaris",   "Canis",          "Canidae",         "Poodle"),
    ("Dobermann",               "Canis lupus familiaris",   "Canis",          "Canidae",         "Dobermann"),
    ("Rottweiler",              "Canis lupus familiaris",   "Canis",          "Canidae",         "Rottweiler"),
    ("Dachshund",               "Canis lupus familiaris",   "Canis",          "Canidae",         "Dachshund"),
    ("Persian Cat",             "Felis catus",              "Felis",          "Felidae",         "Persian_cat"),
    ("Siamese Cat",             "Felis catus",              "Felis",          "Felidae",         "Siamese_cat"),
    ("Bengal Cat",              "Felis catus",              "Felis",          "Felidae",         "Bengal_cat"),
    ("Indian Domestic Cat",     "Felis catus",              "Felis",          "Felidae",         "Cat"),
    ("British Shorthair",       "Felis catus",              "Felis",          "Felidae",         "British_Shorthair"),
    ("European Rabbit",         "Oryctolagus cuniculus",    "Oryctolagus",    "Leporidae",       "European_rabbit"),
    ("Indian Ring-necked Parakeet","Psittacula krameri",    "Psittacula",     "Psittaculidae",   "Rose-ringed_parakeet"),
    ("Common Myna",             "Acridotheres tristis",     "Acridotheres",   "Sturnidae",       "Common_myna"),
    ("Goldfish",                "Carassius auratus",        "Carassius",      "Cyprinidae",      "Goldfish"),
    ("Betta Fish",              "Betta splendens",          "Betta",          "Osphronemidae",   "Siamese_fighting_fish"),
    ("Indian Star Tortoise",    "Geochelone elegans",       "Geochelone",     "Testudinidae",    "Indian_star_tortoise"),
    ("Guinea Pig",              "Cavia porcellus",          "Cavia",          "Caviidae",        "Guinea_pig"),
    ("Syrian Hamster",          "Mesocricetus auratus",     "Mesocricetus",   "Cricetidae",      "Golden_hamster"),
    ("Budgerigar",              "Melopsittacus undulatus",  "Melopsittacus",  "Psittaculidae",   "Budgerigar"),
    ("Cockatiel",               "Nymphicus hollandicus",    "Nymphicus",      "Cacatuidae",      "Cockatiel"),
    ("Lovebird",                "Agapornis roseicollis",    "Agapornis",      "Psittaculidae",   "Rosy-faced_lovebird"),
    ("Arowana",                 "Scleropages formosus",     "Scleropages",    "Osteoglossidae",  "Asian_arowana"),
    ("Red-eared Slider (Turtle)","Trachemys scripta elegans","Trachemys",     "Emydidae",        "Red-eared_slider"),
    ("Zebra Finch",             "Taeniopygia guttata",      "Taeniopygia",    "Estrildidae",     "Zebra_finch"),
    ("White Mouse",             "Mus musculus",             "Mus",            "Muridae",         "House_mouse"),
]

WILDLIFE_ANIMALS = [
    ("Great White Shark",       "Carcharodon carcharias",   "Carcharodon",    "Lamnidae",        "Great_white_shark"),
    ("Brown Bear",              "Ursus arctos",             "Ursus",          "Ursidae",         "Brown_bear"),
    ("Garden Snail",            "Cornu aspersum",           "Cornu",          "Helicidae",       "Cornu_aspersum"),
    ("Honey Bee",               "Apis mellifera",           "Apis",           "Apidae",          "Western_honey_bee"),
    ("Bengal Tiger",            "Panthera tigris tigris",   "Panthera",       "Felidae",         "Bengal_tiger"),
    ("Indian Leopard",          "Panthera pardus fusca",    "Panthera",       "Felidae",         "Indian_leopard"),
    ("Asiatic Lion",            "Panthera leo persica",     "Panthera",       "Felidae",         "Asiatic_lion"),
    ("Indian Elephant",         "Elephas maximus indicus",  "Elephas",        "Elephantidae",    "Asian_elephant"),
    ("Indian Rhinoceros",       "Rhinoceros unicornis",     "Rhinoceros",     "Rhinocerotidae",  "Indian_rhinoceros"),
    ("Indian Peacock",          "Pavo cristatus",           "Pavo",           "Phasianidae",     "Indian_peafowl"),
    ("Indian Cobra",            "Naja naja",                "Naja",           "Elapidae",        "Indian_cobra"),
    ("Indian Python",           "Python molurus",           "Python",         "Pythonidae",      "Indian_python"),
    ("Bengal Monitor Lizard",   "Varanus bengalensis",      "Varanus",        "Varanidae",       "Bengal_monitor"),
    ("Gharial",                 "Gavialis gangeticus",      "Gavialis",       "Gavialidae",      "Gharial"),
    ("Indian Flying Fox",       "Pteropus giganteus",       "Pteropus",       "Pteropodidae",    "Indian_flying_fox"),
    ("Sloth Bear",              "Melursus ursinus",         "Melursus",       "Ursidae",         "Sloth_bear"),
    ("Indian Pangolin",         "Manis crassicaudata",      "Manis",          "Manidae",         "Indian_pangolin"),
    ("Sea Horse (Spotted)",     "Hippocampus kuda",         "Hippocampus",    "Syngnathidae",    "Hippocampus_kuda"),
    ("Red Fox",                 "Vulpes vulpes",            "Vulpes",         "Canidae",         "Red_fox"),
    ("Golden Jackal",           "Canis aureus",             "Canis",          "Canidae",         "Golden_jackal"),
    ("Indian Wild Boar",        "Sus scrofa cristatus",     "Sus",            "Suidae",          "Wild_boar"),
    ("Nilgai",                  "Boselaphus tragocamelus",  "Boselaphus",     "Bovidae",         "Nilgai"),
    ("Sambar Deer",             "Rusa unicolor",            "Rusa",           "Cervidae",        "Sambar_deer"),
    ("Blackbuck",               "Antilope cervicapra",      "Antilope",       "Bovidae",         "Blackbuck"),
    ("Gangetic Dolphin",        "Platanista gangetica",     "Platanista",     "Platanistidae",   "South_Asian_river_dolphin"),
    ("Dugong",                  "Dugong dugon",             "Dugong",         "Dugongidae",      "Dugong"),
    ("Great Hornbill",          "Buceros bicornis",         "Buceros",        "Bucerotidae",     "Great_hornbill"),
    ("Sarus Crane",             "Antigone antigone",        "Antigone",       "Gruidae",         "Sarus_crane"),
    ("Indian Vulture",          "Gyps indicus",             "Gyps",           "Accipitridae",    "Indian_vulture"),
    ("King Cobra",              "Ophiophagus hannah",       "Ophiophagus",    "Elapidae",        "King_cobra"),
]


def build_species_df():
    rows = []
    sid = 1

    # ── PLANTS ──────────────────────────────────────────────
    # medicinal: ~540, ornamental: ~530, food: ~530 → 1600
    def expand(source, category, target_n):
        result = []
        while len(result) < target_n:
            result.extend(source)
        return result[:target_n]

    med_target, orn_target, food_target = 540, 530, 530
    med_pool  = expand(MEDICINAL_PLANTS,   "medicinal",   med_target)
    orn_pool  = expand(ORNAMENTAL_PLANTS,  "ornamental",  orn_target)
    food_pool = expand(FOOD_PLANTS,        "food",        food_target)

    for pool, fcat in [(med_pool,"medicinal"),(orn_pool,"ornamental"),(food_pool,"food")]:
        for i, (cn, sn, genus, family, wid) in enumerate(pool):
            rows.append({
                "species_id":          f"PLT-{sid:05d}",
                "biological_domain":   "plant",
                "common_name":         cn,
                "scientific_name":     sn,
                "genus":               genus,
                "family":              family,
                "kingdom":             "Plantae",
                "functional_category": fcat,
                "image_source":        f"https://en.wikipedia.org/wiki/{wid}",
                "image_url_commons":   f"https://commons.wikimedia.org/wiki/Special:FilePath/{wid}.jpg",
                "annotation_confidence": round(np.random.uniform(0.88, 0.99), 3),
                "expert_reviewed":     1 if np.random.random() < 0.05 else 0,
            })
            sid += 1

    # ── ANIMALS ─────────────────────────────────────────────
    # household: 800, wildlife: 800 → 1600
    hw_pool = expand(HOUSEHOLD_ANIMALS, "household", 800)
    wl_pool = expand(WILDLIFE_ANIMALS,  "wildlife",  800)

    for pool, fcat in [(hw_pool,"household"),(wl_pool,"wildlife")]:
        for (cn, sn, genus, family, wid) in pool:
            rows.append({
                "species_id":          f"ANM-{sid:05d}",
                "biological_domain":   "animal",
                "common_name":         cn,
                "scientific_name":     sn,
                "genus":               genus,
                "family":              family,
                "kingdom":             "Animalia",
                "functional_category": fcat,
                "image_source":        f"https://en.wikipedia.org/wiki/{wid}",
                "image_url_commons":   f"https://commons.wikimedia.org/wiki/Special:FilePath/{wid}.jpg",
                "annotation_confidence": round(np.random.uniform(0.88, 0.99), 3),
                "expert_reviewed":     1 if np.random.random() < 0.03 else 0,
            })
            sid += 1

    df = pd.DataFrame(rows)

    # Stratified 70/15/15 split within each domain×category combo
    splits = []
    for _, grp in df.groupby(["biological_domain","functional_category"]):
        idx = grp.index.tolist()
        np.random.shuffle(idx)
        n = len(idx)
        t = int(n * 0.70)
        v = int(n * 0.15)
        for i in idx[:t]:       splits.append((i, "train"))
        for i in idx[t:t+v]:    splits.append((i, "val"))
        for i in idx[t+v:]:     splits.append((i, "test"))
    split_map = {i: s for i, s in splits}
    df["split"] = df.index.map(split_map)
    return df


if __name__ == "__main__":
    df = build_species_df()
    df.to_csv("data/species/species_annotations.csv", index=False)
    df[df.split=="train"].to_csv("data/species/train.csv", index=False)
    df[df.split=="val"].to_csv("data/species/val.csv",   index=False)
    df[df.split=="test"].to_csv("data/species/test.csv", index=False)

    stats = df.groupby(["biological_domain","functional_category"]).size().to_dict()
    split_counts = df["split"].value_counts().to_dict()
    print(f"Total species rows : {len(df)}")
    print(f"Split counts       : {split_counts}")
    print(f"Domain×Category    : {stats}")
