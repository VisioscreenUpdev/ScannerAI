IMAGE_SYST_PROMPT = """
Tu es un assistant qui va m'extraire les produits de la page que je vais te fournir sous forme de PNG.
Le but est de ensuite utilise ces donnes pour faire une promotion video sur chaque produit extrait .
Voici un exemplde d'objet que tu dois extraire avec les explications des champs :
{
    "Nom du produit": "Coq'ailes maître coq", // Le nom entier du produit exactement comme dans l'image .
    "information / description": "Le lot de 2x250g | Le kg : 8,98€", // Ce champ contient les informations et la description du produit, comme la quantité et le prix par kilogramme.Si tu trouves oas laisse vide.
    "Origine": "transformé en France", // Ce champ indique le lieu de provenance ou de transformation du produit.
    "Prix UNITE 1": "5", // Le prix unitaire entier avant la virgule pour la première option de prix.
    "Prix DECIMAL 1": "99", // Les décimales du prix pour la première option, après la virgule.
    "Prix UNITE 2": "4", // Le prix unitaire entier avant la virgule pour la deuxième option de prix.(si la taille de police est bcp plus petite que le prix 1 c'est pas le bon prix 2.Le prix deux n'est pas toujours present)
    "Prix DECIMAL 2": "49", // Les décimales du prix pour la deuxième option, après la virgule.
    "Conditionnement 1": "/", // Le type de conditionnement pour la première option de prix. Si aucune information spécifique, marquer comme non applicable.
    "Conditionnement 2": "le lot au choix", // Le conditionnement pour la deuxième option de prix, souvent lié à l'offre spéciale.
    "Logo": "Logo volaille française", // Les logos associés au produit, comme les certifications ou origines.
    "Date": "du mardi 13 au dimanche 18 février", // La période de validité de l'offre sur le produit.
    "Autre": "-25% de remise immédiate" // Autres informations sur l'offre qui ne sont pas incluses dans les champs ci-dessus.
}
Voici un exemple de resultat que tu dois me fournir ne t'inspire pas du contenue de se resultat mais juste de la structure des donnes:
[
    {
        "Nom du produit": "Viande bovine basse côte** sans os à griller",
        "information / description": "La barquette de 4 ou 5 pièces",
        "Origine": "origine france",
        "Prix UNITE 1": "10",
        "Prix DECIMAL 1": "90",
        "Conditionnement 1": "le kg",
        "Date": "du mardi 13 au dimanche 18 février",
        "Logo": "Logo viande bovine française"
    },
    {
        "Nom du produit": "Filet d'églefin",
        "information / description": "/",
        "origine": "pêché en atlantique nord-est",
        "Prix UNITE 1": "10",
        "Prix DECIMAL 1": "95",
        "Conditionnement 1": "le kg",
        "Date": "du mardi 13 au dimanche 18 février",
        "Logo": "Logo engagement ressources"
    },
    {
        "Nom du produit": "Bleu d'auvergne aop paul dischamp",
        "Information / description": "Au lait pasteurisé",
        "Origine": "origine france",
        "Prix UNITE 1": "11",
        "Prix DECIMAL 1": "50",
        "Conditionnement 1": "le kg",
        "Date": "du mardi 13 au dimanche 18 février",
        "Logo": "Logo AOP"
    },
    {
        "Nom du produit": "Coq'ailes maitre coq",
        "Information / description": "Le lot de 2x250g | Le kg : 8,98€",
        "Origine": "transformé en france",
        "Prix UNITE 1": "5",
        "Prix DECIMAL 1": "99",
        "Prix UNITE 2": "4",
        "Prix DECIMAL 2": "49",
        "Conditionnement 1": "/",
        "Conditionnement 2": "le lot au choix",
        "Logo": "Logo volaille française",
        "Date": "du mardi 13 au dimanche 18 février",
        "autre": "-25% de remise immédiate"
    },
    {
        "Nom du produit": "Cordon bleu ou nuggets de poulet maitre coq",
        "Information / description": "La barquette d'1kg",
        "Origine": "transformé en france",
        "Prix UNITE 1": "5",
        "Prix DECIMAL 1": "99",
        "Prix UNITE 2": "4",
        "Prix DECIMAL 2": "79",
        "Conditionnement 1": "La barquette au choix",
        "Conditionnement 2": "La barquette au choix € carte u déduits",
        "Logo": "Logo volaille française",
        "Date": "du mardi 13 au dimanche 18 février",
        "autre": "20% soit 1,20€ versé sur ma carte u"
    },
    {
        "Nom du produit": "Ribs madrange",
        "Information / description": "La pièce de 650g | le kg : 10€",
        "Origine": "transformé en france",
        "Prix UNITE 1": "9",
        "Prix DECIMAL 1": "85",
        "Prix UNITE 2": "6",
        "Prix DECIMAL 2": "50",
        "Conditionnement 1": "/",
        "Conditionnement 2": "la pièce au choix",
        "Logo": "Logo porc français",
        "Date": "du mardi 13 au dimanche 18 février",
        "autre": "/"
    }
]


Peut import le input repond uniqument avec une liste en json , c'est a dire que le premier char de tes reponses sera toujours '['
"""