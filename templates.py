
REMINDER_TEMPLATES = {
    'fr': {
        'before': "Objet: Rappel loyer {period}\n\nBonjour,\n\nUn rappel amical: le loyer de {amount} € est exigible le {due_date}.\nRéférence: {reference}.\nVous pouvez payer par virement via l'app en scannant le QR.\n\nMerci,\nGestion locative",
        'due': "Objet: Loyer du {period} dû aujourd'hui\n\nBonjour,\n\nVotre loyer de {amount} € est dû aujourd'hui ({due_date}). Référence: {reference}.\nMerci d'effectuer le paiement dès que possible via l'app.\n\nCordialement,\nGestion locative",
        'after': "Objet: Loyer en retard — {period}\n\nBonjour,\n\nNous n'avons pas encore reçu le loyer de {amount} € (échéance {due_date}). Référence: {reference}.\nMerci de régulariser dans les plus brefs délais.\n\nCordialement,\nGestion locative"
    },
    'nl': {
        'before': "Onderwerp: Huurherinnering {period}\n\nBeste,\n\nVriendelijke herinnering: de huur van {amount} € is verschuldigd op {due_date}.\nReferentie: {reference}.\nU kunt betalen via de app met de QR.\n\nMet vriendelijke groet,\nVerhuurbeheer",
        'due': "Onderwerp: Huur {period} vandaag verschuldigd\n\nBeste,\n\nUw huur van {amount} € is vandaag verschuldigd ({due_date}). Referentie: {reference}.\nDank om zo snel mogelijk te betalen via de app.\n\nMet vriendelijke groet,\nVerhuurbeheer",
        'after': "Onderwerp: Achterstallige huur — {period}\n\nBeste,\n\nWe hebben de huur van {amount} € (vervaldag {due_date}) nog niet ontvangen. Referentie: {reference}.\nGelieve dit spoedig te regelen.\n\nMet vriendelijke groet,\nVerhuurbeheer"
    },
    'en': {
        'before': "Subject: Rent reminder {period}\n\nHello,\n\nFriendly reminder: the rent of {amount} € is due on {due_date}.\nReference: {reference}.\nYou can pay via the app using the QR code.\n\nBest,\nProperty Management",
        'due': "Subject: Rent for {period} due today\n\nHello,\n\nYour rent of {amount} € is due today ({due_date}). Reference: {reference}.\nPlease make the payment via the app.\n\nBest,\nProperty Management",
        'after': "Subject: Overdue rent — {period}\n\nHello,\n\nWe have not yet received the rent of {amount} € (due {due_date}). Reference: {reference}.\nPlease settle as soon as possible.\n\nBest,\nProperty Management"
    }
}
