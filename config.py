import shelve

config = shelve.open("config.shelf")

# keep these langs
config["lang"] = ["cmn", "eng", "wuu", "epo"]

# keep these users, for future usage
config["user"] = []

# block these users, for future usage
config["buser"] = []

# --is-linked-to: keep direct links only
# -t: also keep indirect links
config["trmode"] = "--is-linked-to" # "-t","--is-link-to"

# "-p": matches the translations
# "-r": matches the source sentence
config["regex"] = "-r" # "-p","-r"

# easy mode: input a word, get a sentence
# expert mode: praise the power of regex
config["rmode"] = "easy" # "expert"
