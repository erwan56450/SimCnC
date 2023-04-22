
#
selected_language = 'fr'  # Change this to  'de' for German or 'fr' for French

translations = {
    'fr': {
        "A tool has been detected in the spindle.": "Un outil a été détecté dans la broche.",
        "There is no tool in the spindle.": "Il n'y a pas d'outil dans la broche.",
        "The clamp is closed.": "La pince est fermé",
        "The clamp is open.": "La pince est ouvert",
        "The tool remains in the spindle." :
        "There is no tool in the spindle." :
        "The clamp remained closed."
        "The clamp is open."
        "The digital output has not been well defined."
        "Tool measurement cancelled, no probe installed."
        "-------------------\n Tool {new_tool} already install \n-------------------- " : "-------------------\n Tool {new_tool} already install \n-------------------- ",
            },
    'de': {
        "A tool has been detected in the spindle.": "Ein Werkzeug wurde in der Spindel erkannt.",
        "There is no tool in the spindle.": "Es befindet sich kein Werkzeug in der Spindel.",
        "The clamp is closed": "Die Klemme ist geschlossen",
        "The clamp is open": "Die Klemme ist geöffnet",
    },
}

def _(text):
    return translations[selected_language].get(text, text)
