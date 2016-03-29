/**
 * Created by Arnaud on 11/02/2016.
 */

// Adresse IP du serveur hebergant le programme Python
var adresseIPServeur = "http://172.30.0.234:8080/";

//*******************************************************************//
//****************** FONCTIONS DE RESET DES CHAMPS ******************//
//*******************************************************************//

// Fonction de mise en page (réinitialisation) des champs de connexion et d'enregistrement

function resetLoginErrorEnregistrement() {
    document.getElementById("Wrong_login_enregistrement").innerHTML = "";
}

function resetPasswordErrorEnregistrement() {
    document.getElementById("Wrong_password_enregistrement").innerHTML = "";
}

function resetLoginErrorConnexion() {
    document.getElementById("Wrong_login_connexion").innerHTML = "";
}

function resetPasswordErrorConnexion() {
    document.getElementById("Wrong_password_connexion").innerHTML = "";
}

//*****************************************************//
//********************* CONNEXION *********************//
//*****************************************************//

function connexionKeyPressListener(e) {
    if (e.keyCode == 13) {
        connexion();
    }
}

// Vérifie si le naviguateur accepte les cookies
function initConnexion() {
    // Dans le cas où les cookies sont activés, on récupère le login enregistré.
    if (navigator.cookieEnabled) {
        // Cookies acceptés
        if (getCookie("nom_utilisateur") != null) {
            document.getElementById("login").innerHTML = getCookie("nom_utilisateur");
        }
        // Si les cookies ne sont pas activés, on bloque l'utilisateur.
    } else {
        alert("Veuillez activer les cookies de votre naviguateur avant de continuer.");
        basculerEtatChampsDeSaisie();
        document.getElementById("Wrong_login_connexion").innerHTML = "Veuillez activer les cookies de votre naviguateur avant de continuer.";
    }
}

// Communication (trame http) permettant à un utilisateur de se connecter
function connexion() {

    // http://www.w3schools.com/ajax/ajax_xmlhttprequest_send.asp
    var xmlhttp = new XMLHttpRequest();
    var stop = false;

    // Récupération des valeurs
    var login = document.getElementById("login").value;
    var motDePasse = document.getElementById("password").value;

    // Si les champs login ou mot de passe sont vides, on envoi aucune trame de communication
    // et on retourne un message d'erreur
    if (login == "") {
        alert("Champs login vide.");
        return 0;
    } else if (motDePasse == "") {
        alert("Champs mot de passe vide.");
        return 0;
    }

    // Chiffrage du mot de passe en md5 (clé fixe)
    var motDePasseChiffre = calcMD5(motDePasse);

    // Trame Json de communication entre le client Javascript et le serveur python
    var trame = '{"login": "' + login + '","password": "' + motDePasseChiffre + '"}';

    // Protocole d'ouverture de connexion et d'envoi de données en HTTP
    xmlhttp.open("POST", adresseIPServeur + "login");

    xmlhttp.send(trame);

    // On attend la réponse du serveur python à la requête
    xmlhttp.onreadystatechange = function () {

        // xmlhttp.status : Statut renvoyé par le serveur (cf. documentation)
        // xmlhttp.responseText : Trame Json renvoyé par le serveur (peut être vide dans certains cas)
        switch (xmlhttp.status) {
            case 200:
                // stop : Booleen permettant une execution unique du code ci dessous
                if (xmlhttp.readyState == 4 && xmlhttp.responseText != "" && stop == false) {
                    stop = true;

                    // JSON Parsing
                    var myArr = JSON.parse(xmlhttp.responseText);

                    // Gestion des cookies
                    // setCookie(NomDuCookie, ValeurASauvegarder, DuréeDeVieDuCookieEnJours)
                    setCookie("login_utilisateur", myArr.login, 7);
                    setCookie("nom_utilisateur", myArr.nom, 7);
                    setCookie("prenom_utilisateur", myArr.prenom, 7);
                    setCookie("description_utilisateur", myArr.description, 7);
                    setCookie("admin_button_view", myArr.isAdmin, 7);
                    setCookie("mail_utilisateur", myArr.mail, 7);

                    // Dans le cas où la connexion se fait suite à un oublie de mot de passe
                    // on redirige l'utilisateur vers une page permettant de modifier son mot de passe
                    if (myArr.motDePasseUnique == true) {
                        // Redirection vers le corps du site
                        window.location.href = "ecraserMotDePasse.html";
                        return 0;
                    }
                    // Redirection vers le corps du site
                    window.location.href = "menu.html";
                }
                break;
            case 1002:
                document.getElementById("Wrong_login_connexion").innerHTML = "Login incorrect";
                result = false;
                break;
            case 1003:
                document.getElementById("Wrong_password_connexion").innerHTML = "Mot de passe incorrect";
                result = false;
                break;
            case 0:
                if (xmlhttp.responseText != "" && stop == false) {
                    stop = true;
                    alert("Serveur injoignable");
                }
                break;
            default:
                if (xmlhttp.responseText != "" && stop == false) {
                    stop = true;
                    alert("Erreur inconnue : " + xmlhttp.status);
                }
        }
    };
}

//*****************************************************//
//*********************** MENU ************************//
//*****************************************************//

function initMenu() {

    if (navigator.cookieEnabled) {
        // Cookies acceptés
        var nom_utilisateur = getCookie("nom_utilisateur");
        var prenom_utilisateur = getCookie("prenom_utilisateur");
        var Description_Utilisateur = getCookie("description_utilisateur");

        document.getElementById("logo").innerHTML = prenom_utilisateur + " " + nom_utilisateur;
        document.getElementById("Description_Utilisateur").innerHTML = Description_Utilisateur;
    } else {
        alert("Veuillez activer les cookies de votre naviguateur avant de continuer.");
        basculerEtatChampsDeSaisie();
    }
}

//**********************************************************//
//*********************** GRAPHIQUE ************************//
//**********************************************************//

// Récupération des informations demandées par l'utilisateur pour créer le graphique
function GetSensorData(choix) {

    var stop = false;

    var xmlhttp = new XMLHttpRequest();

    var login = getCookie("login_utilisateur");
    var capteurId = document.getElementById("capteurId").value;

    var dateDebutValue = document.getElementById("dateDebut").value;
    var dateFinValue = document.getElementById("dateFin").value;

    var $radio = $('input[name=demo-priority]:checked');
    var mesure = $radio.attr('id');

    // Conversion Date to Timestamp
    var myDateDebut = new Date(dateDebutValue);
    var myDateFin = new Date(dateFinValue);

    var dateDebut = ((myDateDebut.getTime() / 1000).toFixed(0)) - 3600;
    var dateFin = ((myDateFin.getTime() / 1000).toFixed(0)) - 3600;

    // Trame pour récupérer les informations d'un capteur
    var trame = '{"login": "' + login + '","capteurId": "' + capteurId + '","dateDebut": "' + dateDebut + '","dateFin": "' + dateFin + '","mesure": "' + mesure + '"}';

    // Protocole d'ouverture de connexion et d'envoi de données en HTTP
    xmlhttp.open("POST", adresseIPServeur + "capteur");

    xmlhttp.send(trame);

    // Attente de la réponse du serveur
    xmlhttp.onreadystatechange = function () {

        switch (xmlhttp.status) {
            case 200:
                if (xmlhttp.readyState == 4 && xmlhttp.responseText != "" && stop == false) {
                    stop = true;

                    // Dans le cas où l'utilisateur souhaite voir un aperçu du graphique sur la page
                    if (choix == "Graphique") {

                        var donnees = [];
                        var dates = [];

                        // JSON Parsing
                        var myArr = JSON.parse(xmlhttp.responseText);

                        // Boucle de récupéartion de toutes les données renvoyées par le serveur python
                        for (var i = 0; i < myArr.releve.length; i++) {
                            var counter = myArr.releve[i];

                            donnees.push(myArr.releve[i].mesure);
                            dates.push(myArr.releve[i].dateReleve);
                        }

                        // Fonction AmCharts afin de générer le graphique à partir des données acquises
                        CreateGraphic(donnees, dates);

                        // Dans le cas où l'utilisateur souhaite télécharger un fichier CSV des données
                    } else if (choix == "CSV") {
                        // Fonction de génération de CSV
                        JSONToCSVConvertor(xmlhttp.responseText, mesure, true);

                        // Dans le cas où l'utilisateur souhaite télécharger un fichier XML des données
                    } else if (choix == "XML") {
                        var x2js = new X2JS();

                        // JSON Parsing
                        var myArr = JSON.parse(xmlhttp.responseText);

                        var xmlAsStr = x2js.json2xml_str(myArr);

                        // Formatage pour l'indentation du XML
                        var xmlIndent = vkbeautify.xml(xmlAsStr);

                        var today = new Date();
                        today = today.toISOString().substring(0, 10);

                        download(today + ".xml", xmlIndent);

                        // Dans le cas où l'utilisateur souhaite afficher le graphique dans une nouvelle page
                    } else if (choix == "FullScreen") {

                        var donnees = [];
                        var dates = [];

                        // JSON Parsing
                        var myArr = JSON.parse(xmlhttp.responseText);

                        // Boucle de récupération de toutes les valeurs renvoyées par le serveur
                        for (var i = 0; i < myArr.releve.length; i++) {
                            var counter = myArr.releve[i];
                            console.log(counter.mesure);

                            donnees.push(myArr.releve[i].mesure);
                            dates.push(myArr.releve[i].dateReleve);
                        }

                        // Fonction AmCharts de généraion de graphqiue
                        CreateGraphic(donnees, dates);
                    }
                }
                break;
            case 1006:
                alert("Balise inconnue");
                result = false;
                break;
            case 1007:
                document.getElementById("Invalid_Graph").innerHTML = "Accées interdit à " + getCookie("login_utilisateur");
                result = false;
                break;
            case 0:
                if (xmlhttp.responseText != "" && stop == false) {
                    stop = true;
                    alert("Serveur injoignable");
                }
                break;
            default:
                if (xmlhttp.responseText != "" && stop == false) {
                    stop = true;
                    alert("Erreur inconnue : " + xmlhttp.status);
                }
        }
    };
}

// Fonction de sauvegarde des données et d'ouverture d'une nouvelle page
// ATTENTION : La génération du graphique sur la nouvelle page se fait avec les fonctions
// du fichier js : /assets/js/FullScreenGraph.js
function PageFullScreenGraph() {

    var capteurId = document.getElementById("capteurId").value;

    var dateDebutValue = document.getElementById("dateDebut").value;
    var dateFinValue = document.getElementById("dateFin").value;

    var $radio = $('input[name=demo-priority]:checked');
    var mesure = $radio.attr('id');

    // Conversion Date to Timestamp
    var myDateDebut = new Date(dateDebutValue);
    var myDateFin = new Date(dateFinValue);

    var dateDebut = ((myDateDebut.getTime() / 1000).toFixed(0)) - 3600;
    var dateFin = ((myDateFin.getTime() / 1000).toFixed(0)) - 3600;

    // Sauvegarde des données à afficher dans la nouvelle page
    setCookie("capteurID", capteurId, 1);
    setCookie("dateDebut", dateDebut, 1);
    setCookie("dateFin", dateFin, 1);
    setCookie("mesureSave", mesure, 1);

    // Ouverture d'une nouvelle page dans un nouvelle onglet
    var win = window.open("graphiquePleinePage.html", '_blank');
    win.focus();
}

//****************** PROFIL UTILISATEUR ********************//

//**********************************************************//
//******************* MODIFIER PROFIL **********************//
//**********************************************************//

// Initialisation de la page de profil
function initProfile() {

    // Récupération des informations
    var nom_utilisateur = getCookie("nom_utilisateur");
    var prenom_utilisateur = getCookie("prenom_utilisateur");
    var Description_Utilisateur = getCookie("description_utilisateur");
    var mail = getCookie("mail_utilisateur");

    // Affichage des informations et modification réalisable pour un utilisateur
    document.getElementById("nomUtilisateur").innerHTML = "Nom : " + nom_utilisateur + "<br />";
    document.getElementById("prenomUtilisateur").innerHTML = "Prenom : " + prenom_utilisateur + "<br />";
    document.getElementById("descriptionUtilisateur").innerHTML = 'Description : <input id="inputDescription" style="width:50%" size="20" value="' + Description_Utilisateur + '"/>';
    document.getElementById("mailUtilisateur").innerHTML = 'Adresse mail : <input id="inputMail" style="width:50%" size="20" value="' + mail + '"/>';

    document.getElementById("logo").innerHTML = prenom_utilisateur + " " + nom_utilisateur;
    document.getElementById("Description_Utilisateur").innerHTML = Description_Utilisateur;

    // Affichage du bouton d'accès au commandes adminsistrateurs si le compte à les autorisations
    if (getCookie("admin_button_view") == "true") {
        document.getElementById("logAdmin").innerHTML = '<input id="adminPassword" type="password" style="width:30%" size="20" placeholder="admin password"/> <br /><a id="accesAdmin" onclick="initProfileAdministrateur()" class="button">Commandes administrateur</a>'
    }
}

function ModifierProfilUtilisateur() {

    var xmlhttp = new XMLHttpRequest();

    var stop = false;

    // Récupération des informations
    var desc = document.getElementById("inputDescription").value;
    var mail = document.getElementById("inputMail").value;
    var login = getCookie("login_utilisateur");

    var trame = '{"login": "' + login + '", "description" : "' + desc + '","mail":"' + mail + '"}';

    xmlhttp.open("POST", adresseIPServeur + "ModifyDescription");

    xmlhttp.send(trame);

    xmlhttp.onreadystatechange = function () {

        switch (xmlhttp.status) {
            case 200:
                if (xmlhttp.readyState == 4 && stop == false) {
                    stop = true;

                    // changement du profil et redirection vers la page de profil
                    alert("Description modifié.");
                    setCookie("description_utilisateur", desc, 7);
                    setCookie("mail_utilisateur", mail, 7);

                    // Redirection vers le corps du site
                    window.location.href = "profil.html";
                }
                break;
            default:
                if (stop == false) {
                    stop = true;
                    alert("Erreur inconnue : " + xmlhttp.status);
                }
        }
    };
}

//**********************************************************//
//**************** MODIFIER MOT DE PASSE *******************//
//**********************************************************//

function PageModifierPasswordUtilisateur() {
    document.location.href = "modifierMotDePasse.html";
}

// Affichage des informations sur la page
function initModifierMotDePasse() {
    var nom_utilisateur = getCookie("nom_utilisateur");
    var prenom_utilisateur = getCookie("prenom_utilisateur");
    var Description_Utilisateur = getCookie("description_utilisateur");

    document.getElementById("logo").innerHTML = prenom_utilisateur + " " + nom_utilisateur;
    document.getElementById("Description_Utilisateur").innerHTML = Description_Utilisateur;
}

function ModifierPasswordUtilisateur() {
    var xmlhttp = new XMLHttpRequest();
    var stop = false;

    // Récupération des informations
    var ancienpassword = document.getElementById("ancienMotDePasse").value;
    var newpassword = document.getElementById("nouveauMotDePasse").value;
    var newpassword2 = document.getElementById("nouveauMotDePasse2").value;
    var login = document.getElementById("login").value;

    if (newpassword != newpassword2) {
        alert("Vous avez entré deux nouveaux mot de passe différent");
        document.getElementById("nouveauMotDePasse").value = "";
        document.getElementById("nouveauMotDePasse2").value = "";
        return 0;
    }

    // Chiffrage des mot de passe en MD5
    ancienpassword = calcMD5(ancienpassword);
    newpassword = calcMD5(newpassword);

    // Génération de la trame de communication
    var trame = '{"login": "' + login + '","ancienPassword":"' + ancienpassword + '","newPassword":"' + newpassword + '"}';

    xmlhttp.open("POST", adresseIPServeur + "modifyPassword");

    xmlhttp.send(trame);

    xmlhttp.onreadystatechange = function () {

        switch (xmlhttp.status) {
            case 200:
                if (xmlhttp.readyState == 4 && stop == false) {
                    stop = true;
                    alert("Mot de passe modifié");
                }
                break;
            default:
                if (stop == false) {
                    stop = true;
                    alert("Erreur inconnue : " + xmlhttp.status);
                }
        }
    };
}

//***********************************************************************//
//********************** COMMANDES ADMINISTRATEUR ***********************//
//***********************************************************************//

function initProfileAdministrateur() {

    // Récupération du mot de passe admin entré
    var password = document.getElementById("adminPassword").value;

    var xmlhttp = new XMLHttpRequest();
    var login = getCookie("login_utilisateur");
    var stop = false;

    var passwordChiffre = calcMD5(password);

    // Verifier Admin ou Utilisateur
    var trame = '{"login": "' + login + '","password": "' + passwordChiffre + '"}';

    xmlhttp.open("POST", adresseIPServeur + "login");

    xmlhttp.send(trame);

    xmlhttp.onreadystatechange = function () {

        switch (xmlhttp.status) {
            case 200:

                if (xmlhttp.readyState == 4 && xmlhttp.responseText != "" && stop == false) {
                    stop = true;

                    // JSON Parsing
                    var myArr = JSON.parse(xmlhttp.responseText);

                    if (myArr.isAdmin == true) {

                        // Restructuration des commandes admin sur le profil
                        // Suppression du log admin
                        // Ajout des differentes commandes administrateur

                        document.getElementById("adminPassword").remove();
                        document.getElementById("accesAdmin").remove();

                        document.getElementById("PannelAdministrateur").innerHTML = '<h3>Commandes Administrateur</h3>';
                        document.getElementById("DivAjouterUtilisateur").innerHTML = '<a onclick="AjouterUtilisateur()" class="button">Ajouter Utilisateur</a>';
                        document.getElementById("DivSupprimerUtilisateur").innerHTML = '<a onclick="SupprimerUtilisateur()" class="button">Supprimer Utilisateur</a>';
                        document.getElementById("DivAjoutTypeCapteur").innerHTML = '<a onclick="PageAjouterTypeCapteur()" class="button">Ajouter Capteur</a>';
                        document.getElementById("DivModificationSonde").innerHTML = '<a onclick="PageAjouterSonde()" class="button">Ajouter Sonde</a>';
                        document.getElementById("DivDroitsUtilisateur").innerHTML = '<a onclick="PageModificationDroitsUtilisateur()" class="button">Modifier Utilisateur</a>';
                        document.getElementById("DivAjouterCapteurSurSonde").innerHTML = '<a onclick="pageAjouterCapteurSurSonde()" class="button">Ajouter capteur sur sonde</a>';
                        document.getElementById("DivSupprimerCapteurSurSonde").innerHTML = '<a onclick="pageSupprimerCapteurSurSonde()" class="button">Supprimer capteur sur sonde</a>';
                    }
                }
            default:
        }
    };
}

//*******************************************************//
//***************** AJOUTER UTILISATEUR *****************//
//*******************************************************//

// Redirection vers la page d'ajout d'un utilisateur
function AjouterUtilisateur() {
    document.location.href = "enregistrement.html";
}

// Réalise l'enregistrement dans la BDD d'un nouvel utilisateur
function enregistrement() {

    var xmlhttp = new XMLHttpRequest();
    var stop = false;

    // Récupération des informations
    var login = document.getElementById("login").value;
    var motDePasse = document.getElementById("password").value;
    var nom = document.getElementById("nom").value;
    var prenom = document.getElementById("prenom").value;
    var description = document.getElementById("description").value;
    var mail = document.getElementById("mail").value;

    // Test d'erreur pour les champs vides
    if (login == "") {
        alert("Champs login vide.");
        return 0;
    } else if (motDePasse == "") {
        alert("Champs mot de passe vide.");
        return 0;
    } else if (nom == "") {
        alert("Champs nom vide.");
        return 0;
    } else if (prenom == "") {
        alert("Champs prenom vide.");
        return 0;
    } else if (mail == "") {
        alert("Champs mail vide.");
        return 0;
    }

    // Chiffrage du mot de passe en MD5
    var motDePasseChiffre = calcMD5(motDePasse);

    var trame = '{"login": "' + login + '","password": "' + motDePasseChiffre + '","nom": "' + nom + '","prenom": "' + prenom + '","description": "' + description + '","mail":"' + mail + '"}'

    xmlhttp.open("POST", adresseIPServeur + "user");

    xmlhttp.send(trame);

    xmlhttp.onreadystatechange = function () {

        switch (xmlhttp.status) {
            case 200:
                if (stop == false) {
                    stop = true;
                    alert("Enregistrement effectué");
                }
                break;
            case 1000:
                if (xmlhttp.responseText != "" && stop == false) {
                    stop = true;
                    alert("Erreur inconnue");
                }
                break;
            case 1001:
                if (xmlhttp.responseText != "" && stop == false) {
                    stop = true;
                    alert("Erreur de base de données");
                }
                break;
            case 1004:
                if (xmlhttp.responseText != "" && stop == false) {
                    stop = true;
                    alert("Erreur de communication JSON");
                }
                break;
            case 1005:
                document.getElementById("Wrong_login_enregistrement").innerHTML = "Login déjà utilisé";
                break;
            case 0:
                if (xmlhttp.responseText != "" && stop == false) {
                    stop = true;
                    alert("Serveur injoignable");
                }
                break;
            default:
                if (xmlhttp.responseText != "" && stop == false) {
                    stop = true;
                    alert("Erreur inconnue : " + xmlhttp.status);
                }
        }
    };
}

//*********************************************************//
//***************** SUPPRIMER UTILISATEUR *****************//
//*********************************************************//

// Permet a un administrateur de supprimer un utilisateur de la BDD
function SupprimerUtilisateur() {
    document.location.href = "suppressionUtilisateur.html";
}

// Charge les données de la BDD pour sélectionner l'utilisateur à supprimer
function initSuppressionUtilisateurs() {

    // Récupération des informations de l'utilisateur
    var nom_utilisateur = getCookie("nom_utilisateur");
    var prenom_utilisateur = getCookie("prenom_utilisateur");
    var Description_Utilisateur = getCookie("description_utilisateur");

    document.getElementById("logo").innerHTML = prenom_utilisateur + " " + nom_utilisateur;
    document.getElementById("Description_Utilisateur").innerHTML = Description_Utilisateur;

    // HTTP UTILISATEURS
    var xmlhttp = new XMLHttpRequest();
    var url = adresseIPServeur + "userList";

    var stop = false;

    // Requête GET en HTTP pour récupérer l'ensemble des utilisateurs créés
    xmlhttp.open("GET", url, true);
    xmlhttp.send();

    xmlhttp.onreadystatechange = function () {

        switch (xmlhttp.status) {
            case 200:
                if (xmlhttp.readyState == 4 && xmlhttp.responseText != "" && stop == false) {
                    stop = true;

                    var myArr = JSON.parse(xmlhttp.responseText);

                    var nom = [];
                    var prenom = [];
                    var login = [];

                    // On vas générer un selecteur avec l'ensemble des utilisateurs
                    var chaine = '<select name="demo-category" id="UserList">';

                    // Boucle récupérant les informations du JSON pour les insérer dans le selecteur (HTML)
                    for (var i = 0; i < myArr.length; i++) {
                        nom.push(myArr[i].nom);
                        prenom.push(myArr[i].prenom);
                        login.push(myArr[i].login);

                        chaine = chaine + '<option value="">' + login[i] + ' - ' + prenom[i] + ' - ' + nom[i] + '</option>';
                    }

                    chaine = chaine + '</select>';

                    // Génération du sélecteur
                    document.getElementById("listeUtilisateurs").innerHTML = chaine;
                }
                break;
        }
    };
}

function SuppressionUtilisateur() {

    // Récupération de l'identifiant sélectionné dans le selecteur
    var index = document.getElementById("UserList");
    var all = index.options[index.selectedIndex].text;

    var login = all.split("-");

    login = login[0].trimRight();

    // Demande de confirmation pour la suppression de l'utilisateur
    var answer = confirm("Voulez-vous vraiment supprimer " + login + " ?");
    if (answer) {

        // Validation par l'administrateur
        // Envoi de la requête HTTP pour suppression de l'utilisateur
        var xmlhttp = new XMLHttpRequest();

        var stop = false;

        var trame = '{"login": "' + login + '"}';

        xmlhttp.open("POST", adresseIPServeur + "deletedUser");

        xmlhttp.send(trame);

        xmlhttp.onreadystatechange = function () {

            switch (xmlhttp.status) {
                case 200:
                    if (xmlhttp.readyState == 4 && stop == false) {
                        stop = true;

                        alert(login + " supprimé.");
                        // Suppression de l'utilisateur et redirection vers la page de suppression.
                        document.location.href = "suppressionUtilisateur.html";
                    }
                    break;
                default:
                    alert("Erreur inconnue : " + xmlhttp.status);
            }
        };
    }
}

//********************************************************//
//***************** MODIFIER UTILISATEUR *****************//
//********************************************************//

// Redirection vers la page de modification d'un utilisateur
function PageModificationDroitsUtilisateur() {
    document.location.href = "modifierUtilisateur.html";
}

function initModificationUtilisateurs() {

    // Récupération des informations utilisateur
    var nom_utilisateur = getCookie("nom_utilisateur");
    var prenom_utilisateur = getCookie("prenom_utilisateur");
    var Description_Utilisateur = getCookie("description_utilisateur");

    document.getElementById("logo").innerHTML = prenom_utilisateur + " " + nom_utilisateur;
    document.getElementById("Description_Utilisateur").innerHTML = Description_Utilisateur;

    // HTTP UTILISATEURS
    var xmlhttp = new XMLHttpRequest();
    var url = adresseIPServeur + "userList";

    var stop = false;

    // Récupération de l'ensemble des utilisateurs en BDD
    xmlhttp.open("GET", url, true);
    xmlhttp.send();

    xmlhttp.onreadystatechange = function () {

        switch (xmlhttp.status) {
            case 200:
                if (xmlhttp.readyState == 4 && xmlhttp.responseText != "" && stop == false) {
                    stop = true;

                    var myArr = JSON.parse(xmlhttp.responseText);

                    var nom = [];
                    var prenom = [];
                    var login = [];

                    // Création d'un selecteur pour l'ensemble des utilisateurs
                    // AffichageSondeModificationUtilisateurs() : Affiche les acces aux sondes de l'utilisateur selectionné
                    var chaine = '<select onchange="AffichageSondeModificationUtilisateurs()" name="demo-category" id="UserList">';

                    // Récupération de l'ensemble des utilisateur du JSON --> HTML
                    for (var i = 0; i < myArr.length; i++) {
                        nom.push(myArr[i].nom);
                        prenom.push(myArr[i].prenom);
                        login.push(myArr[i].login);

                        chaine = chaine + '<option value="">' + login[i] + ' - ' + prenom[i] + ' - ' + nom[i] + '</option>';
                    }

                    chaine = chaine + '</select>';

                    // Génération du sélecteur sur la page
                    document.getElementById("listeUtilisateur").innerHTML = chaine;
                }
                break;
        }
    };
}

// Envoi de la trame pour modification des droits d'un utilisateur au serveur python --> BDD
function ModificationUtilisateur() {

    var xmlhttp = new XMLHttpRequest();
    var stop = false;

    // Récupération du login de l'utilisateur sélectionné
    var index = document.getElementById("UserList");
    var all = index.options[index.selectedIndex].text;

    var login = all.split("-");

    login = login[0].trimRight();

    var trame = '{"login": "' + login + '","liste" : [';

    // Récupération des informations sur les nouveaux droits des stations
    var chaineCookie = getCookie("Stations");
    var chaine = chaineCookie.split("-");
    var nombreStation = getCookie("numberStation");

    for (var i = 0; i < nombreStation; i++) {
        var station = chaine[i];
        trame = trame + '{"nom":"' + station + '","access":' + document.getElementById('check' + station).checked + '},';
    }

    // Retire la derniere virgule
    trame = trame.substring(0, trame.length - 1);

    trame = trame + ']}';

    // Envoi la liste des droits modifié pour un utilisateur
    xmlhttp.open("POST", adresseIPServeur + "userRights");

    xmlhttp.send(trame);

    xmlhttp.onreadystatechange = function () {

        switch (xmlhttp.status) {
            case 200:
                if (xmlhttp.readyState == 4 && xmlhttp.responseText != "" && stop == false) {
                    stop = true;
                    alert("Droits modifiés");
                }
                break;
            default:
                if (stop == false) {
                    stop = true;
                    alert("Erreur inconnue : " + xmlhttp.status);
                }
        }
    };
}

function AffichageSondeModificationUtilisateurs() {
    var xmlhttp = new XMLHttpRequest();
    var stop = false;

    var index = document.getElementById("UserList");
    var all = index.options[index.selectedIndex].text;

    var login = all.split("-");

    login = login[0].trimRight();

    var trame = '{"login": "' + login + '"}';

    xmlhttp.open("POST", adresseIPServeur + "accessList");

    xmlhttp.send(trame);

    xmlhttp.onreadystatechange = function () {

        switch (xmlhttp.status) {
            case 200:
                if (xmlhttp.readyState == 4 && xmlhttp.responseText != "" && stop == false) {
                    stop = true;

                    var myArr = JSON.parse(xmlhttp.responseText);

                    document.getElementById("liste").innerHTML = "";

                    var chaine = "";
                    var listeStation = "";

                    setCookie("numberStation", myArr.liste.length, 1);

                    for (var i = 0; i < myArr.liste.length; i++) {
                        var id = myArr.liste[i].nom;

                        listeStation = listeStation + id + "-";

                        if (myArr.liste[i].access == true) {
                            chaine = chaine + '<span>' + id + '</span> \
                         <input type="checkbox" id="check' + id + '" name="demo-human" checked> &nbsp \
                         <label for="check' + id + '"></label><br />';
                        } else {
                            chaine = chaine + '<span>' + id + '</span> \
                         <input type="checkbox" id="check' + id + '" name="demo-human"> &nbsp \
                         <label for="check' + id + '"></label><br />';
                        }
                    }

                    setCookie("Stations", listeStation, 1);
                    document.getElementById("liste").innerHTML += chaine;
                }
                break;
            default:
                if (stop == false) {
                    stop = true;
                    alert("Erreur inconnue : " + xmlhttp.status);
                }
        }
    };
}

//************************************************************//
//******************* AJOUTER UNE SONDE **********************//
//************************************************************//

function PageAjouterSonde() {
    document.location.href = "ajouterSonde.html";
}

// Affichage des informations utilisateur
function initAjouterSonde() {

    var nom_utilisateur = getCookie("nom_utilisateur");
    var prenom_utilisateur = getCookie("prenom_utilisateur");
    var Description_Utilisateur = getCookie("description_utilisateur");

    document.getElementById("logo").innerHTML = prenom_utilisateur + " " + nom_utilisateur;
    document.getElementById("Description_Utilisateur").innerHTML = Description_Utilisateur;
}

function ajoutCapteurASonde(nombreCapteur) {
    var nombreCapteur = document.getElementById("nombreCapteur").value;
    ajoutCapteurASondeRequete(nombreCapteur);
}

// Permet d'ajouter un type de capteur à une sonde
function ajoutCapteurASondeRequete(nombreCapteur) {

    var nom_utilisateur = getCookie("nom_utilisateur");
    var prenom_utilisateur = getCookie("prenom_utilisateur");
    var Description_Utilisateur = getCookie("description_utilisateur");

    document.getElementById("logo").innerHTML = prenom_utilisateur + " " + nom_utilisateur;
    document.getElementById("Description_Utilisateur").innerHTML = Description_Utilisateur;

    // Récupération de la liste des différents types de capteurs
    var xmlhttp = new XMLHttpRequest();
    var url = adresseIPServeur + "sensorList";

    var stop = false;

    xmlhttp.open("GET", url, true);
    xmlhttp.send();

    xmlhttp.onreadystatechange = function () {

        switch (xmlhttp.status) {
            case 200:
                if (xmlhttp.readyState == 4 && xmlhttp.responseText != "" && stop == false) {

                    stop = true;

                    var myArr = JSON.parse(xmlhttp.responseText);

                    document.getElementById("listeSonde").innerHTML = "";

                    for (var j = 0; j < nombreCapteur; j++) {

                        var id = "sondeList" + j;

                        // Génération du selecteur avec les différents types de capteurs
                        var chaine = '<select name="demo-category" id="' + id + '">';

                        for (var i = 0; i < myArr.capteur.length; i++) {
                            chaine = chaine + '<option value="">' + myArr.capteur[i] + '</option>';
                        }

                        chaine = chaine + '</select>';

                        // Génératio ndans la page HTML
                        document.getElementById("listeSonde").innerHTML += chaine;
                    }
                }
                break;
        }
    };
}

function AjouterSonde() {

    var xmlhttp = new XMLHttpRequest();
    var stop = false;

    // Récupération des informations de la sonde
    var nomSonde = document.getElementById("nomSonde").value;
    var longitude = document.getElementById("longitude").value;
    var latitude = document.getElementById("latitude").value;
    var dateDeploiementBrut = document.getElementById("dateDeploiement").value;
    var nombreCapteur = document.getElementById("nombreCapteur").value;

    // Test si un des champs obligatoire est vide
    if (nomSonde == "") {
        alert("Champs nom de la sonde vide.");
        return 0;
    } else if (longitude == "") {
        alert("Champs longitude vide.");
        return 0;
    } else if (latitude == "") {
        alert("Champs latitude vide.");
        return 0;
    } else if (dateDeploiementBrut == "") {
        alert("Champs date de déploiement vide.");
        return 0;
    } else if (nombreCapteur == "") {
        alert("Champs nombre de capteur vide.");
        return 0;
    }

    // Conversion Date to Timestamp
    var dateDeploiementDATE = new Date(dateDeploiementBrut);

    var dateDeploiement = ((dateDeploiementDATE.getTime() / 1000).toFixed(0)) - 3600;

    var trame = '{"nom": "' + nomSonde + '", "longitude" : "' + longitude + '", "latitude" : "' + latitude + '",\
    "dateDeploiement": "' + dateDeploiement + '", "capteurs" : [';

    // Ajout des différents capteurs sur la sonde
    for (var i = 0; i < nombreCapteur; i++) {
        var id = "sondeList" + i;
        var index = document.getElementById(id);
        var sensorValue = index.options[index.selectedIndex].text;

        trame = trame + '"' + sensorValue + '",';
    }

    // Retire la derniere virgule
    trame = trame.substring(0, trame.length - 1);

    trame = trame + "]}";

    // Envoi de la requete
    xmlhttp.open("POST", adresseIPServeur + "addStation");

    xmlhttp.send(trame);

    xmlhttp.onreadystatechange = function () {

        switch (xmlhttp.status) {
            case 200:
                if (xmlhttp.readyState == 4 && stop == false) {
                    stop = true;
                    alert("Sonde ajouté");
                }
                break;
            default:
                if (stop == false) {
                    stop = true;
                    alert("Erreur inconnue : " + xmlhttp.status);
                }
        }
    };
}

//************************************************************//
//************* AJOUTER UN TYPE DE  CAPTEUR ******************//
//************************************************************//

// Redirection vers la page permettant l'ajout de capteur
function PageAjouterTypeCapteur() {
    document.location.href = "ajouterTypeCapteur.html";
}

// Récupération des informations de l'utilisateur
function initAjouterTypeCapteur() {
    var nom_utilisateur = getCookie("nom_utilisateur");
    var prenom_utilisateur = getCookie("prenom_utilisateur");
    var Description_Utilisateur = getCookie("description_utilisateur");

    document.getElementById("logo").innerHTML = prenom_utilisateur + " " + nom_utilisateur;
    document.getElementById("Description_Utilisateur").innerHTML = Description_Utilisateur;
}

function AjouterTypeCapteur() {

    // Récupération du nom de capteur saisie
    var TypeCateur = document.getElementById("TypeCapteur").value;

    // Test si le chamsp est vide
    if (TypeCateur == "") {
        alert("Champs Type de capteur vide.");
        return 0;
    }

    var xmlhttp = new XMLHttpRequest();
    var stop = false;

    var trame = '{"nom": "' + TypeCateur + '"}';

    // Envoi de la trame au serveur python
    xmlhttp.open("POST", adresseIPServeur + "addSensor");

    xmlhttp.send(trame);

    xmlhttp.onreadystatechange = function () {

        switch (xmlhttp.status) {
            case 200:
                if (xmlhttp.readyState == 4 && stop == false) {
                    stop = true;
                    alert("Capteur ajouté.");
                }
                break;
            default:
                alert("Erreur inconnue : " + xmlhttp.status);
        }
    };
}

//***************************************************************//
//************* AJOUTER UN CAPTEUR A UNE SONDE ******************//
//***************************************************************//

// Redirection vers la page d'ajout d'un capteur sur une sonde
function pageAjouterCapteurSurSonde() {
    document.location.href = "ajouterCapteurSurSonde.html";
}

// Initialisation de la page HTML
function initAjouterCapteurSurSonde() {

    var nom_utilisateur = getCookie("nom_utilisateur");
    var prenom_utilisateur = getCookie("prenom_utilisateur");
    var Description_Utilisateur = getCookie("description_utilisateur");

    document.getElementById("logo").innerHTML = prenom_utilisateur + " " + nom_utilisateur;
    document.getElementById("Description_Utilisateur").innerHTML = Description_Utilisateur;

    listeSonde();

}

//  Renvoie la liste des sondes
function listeSonde() {
    var xmlhttp = new XMLHttpRequest();
    var stop = false;

    // Requête GET en HTTP pour récupérer l'ensemble des utilisateurs créés
    xmlhttp.open("GET", adresseIPServeur + "stationList", true);
    xmlhttp.send();

    xmlhttp.onreadystatechange = function () {

        switch (xmlhttp.status) {
            case 200:
                if (xmlhttp.readyState == 4 && xmlhttp.responseText != "" && stop == false) {
                    stop = true;

                    var myArr = JSON.parse(xmlhttp.responseText);

                    // On va générer un sélecteur avec l'ensemble des utilisateurs
                    var chaine = '<select onchange="affichageCapteurDeSondeAjout()" name="demo-category" id="StationListAdd">';

                    // Boucle récupérant les informations du JSON pour les insérer dans le selecteur (HTML)
                    for (var i = 0; i < myArr.length; i++) {

                        chaine = chaine + '<option value="">' + myArr[i].name + '</option>';
                    }

                    chaine = chaine + '</select>';

                    // Génération HTML du sélecteur
                    document.getElementById("listeSonde").innerHTML = chaine;
                }
                break;
        }
    };
}

// Affiche l'ensemble des capteurs de la sonde
function affichageCapteurDeSondeAjout() {
    // Récupération de l'identifiant sélectionné dans le selecteur
    var index = document.getElementById("StationListAdd");
    var station = index.options[index.selectedIndex].text;

    var xmlhttp = new XMLHttpRequest();
    var stop = false;

    var trame = '{"nom": "' + station + '"}';

    // Envoi de la trame au serveur python
    xmlhttp.open("POST", adresseIPServeur + "sensorOfStation");

    xmlhttp.send(trame);

    xmlhttp.onreadystatechange = function () {

        switch (xmlhttp.status) {
            case 200:
                if (xmlhttp.readyState == 4 && xmlhttp.responseText && stop == false) {
                    stop = true;

                    var myArr = JSON.parse(xmlhttp.responseText);

                    var chaine = "";

                    for (var i = 0; i < myArr.capteur.length; i++) {
                        chaine = chaine + myArr.capteur[i] + "<br />";
                    }
                    document.getElementById("sondePresente").innerHTML = "<b>Capteurs présents :</b>";
                    document.getElementById("presentSensors").innerHTML = chaine;
                }
                break;
            default:
                if (stop == false) {
                    stop = true;
                    alert("Erreur inconnue : " + xmlhttp.status);
                }
        }
    };

    listeTypeCapteur();
}

function listeTypeCapteur() {


    // Récupération de la liste des différents types de capteurs
    var xmlhttp = new XMLHttpRequest();
    var url = adresseIPServeur + "sensorList";

    var stop = false;

    xmlhttp.open("GET", url, true);
    xmlhttp.send();

    xmlhttp.onreadystatechange = function () {

        switch (xmlhttp.status) {
            case 200:
                if (xmlhttp.readyState == 4 && xmlhttp.responseText != "" && stop == false) {

                    stop = true;

                    var myArr = JSON.parse(xmlhttp.responseText);

                    document.getElementById("listeCapteur").innerHTML = "";

                    // Génération du selecteur avec les différents types de capteurs
                    var chaine = '<select name="demo-category" id="SelecteurListeCapteur">';

                    for (var i = 0; i < myArr.capteur.length; i++) {
                        chaine = chaine + '<option value="">' + myArr.capteur[i] + '</option>';
                    }

                    chaine = chaine + '</select>';

                    // Génération dans la page HTML
                    document.getElementById("ajouterCapteur").innerHTML = "<b>Ajouter Capteur :</b>";
                    document.getElementById("listeCapteur").innerHTML += chaine;
                }
                break;
        }
    };
}

function ajouterCapteurSurSonde() {

    // Récupération des identifiants sélectionnés dans le selecteur
    var index = document.getElementById("StationListAdd");
    var station = index.options[index.selectedIndex].text;
    index = document.getElementById("SelecteurListeCapteur");
    var capteur = index.options[index.selectedIndex].text;

    var xmlhttp = new XMLHttpRequest();
    var stop = false;

    var trame = '{"station": "' + station + '","capteurType":"' + capteur + '"}';

    // Envoi de la trame au serveur python
    xmlhttp.open("POST", adresseIPServeur + "addSensorToStation");

    xmlhttp.send(trame);

    xmlhttp.onreadystatechange = function () {

        switch (xmlhttp.status) {
            case 200:
                if (stop == false) {
                    stop = true;
                    alert("Capteur " + capteur + " ajouté à la sonde " + station);

                    document.location.href = "ajouterCapteurSurSonde.html";
                }
                break;
            default:
                if (stop == false) {
                    stop = true;
                    alert("Erreur inconnue : " + xmlhttp.status);
                }
        }
    };

}

//*****************************************************************//
//************* SUPPRIMER UN CAPTEUR A UNE SONDE ******************//
//*****************************************************************//

// Redirection vers la page de suppression de capteurs sur une sonde
function pageSupprimerCapteurSurSonde() {
    document.location.href = "supprimerCapteurSurSonde.html";
}

// Mise en forme de la page HTML (données utilisateurs)
function initSupprimerCapteurSurSonde() {

    var nom_utilisateur = getCookie("nom_utilisateur");
    var prenom_utilisateur = getCookie("prenom_utilisateur");
    var Description_Utilisateur = getCookie("description_utilisateur");

    document.getElementById("logo").innerHTML = prenom_utilisateur + " " + nom_utilisateur;
    document.getElementById("Description_Utilisateur").innerHTML = Description_Utilisateur;

    listeSondeSuppression();
}

function listeSondeSuppression() {
    var xmlhttp = new XMLHttpRequest();
    var stop = false;

    // Requête GET en HTTP pour récupérer l'ensemble des stations créés
    xmlhttp.open("GET", adresseIPServeur + "stationList", true);
    xmlhttp.send();

    xmlhttp.onreadystatechange = function () {

        switch (xmlhttp.status) {
            case 200:
                if (xmlhttp.readyState == 4 && xmlhttp.responseText != "" && stop == false) {
                    stop = true;

                    var myArr = JSON.parse(xmlhttp.responseText);

                    // On vas générer un selecteur avec l'ensemble des sondes
                    var chaine = '<select onchange="affichageCapteurDeSondeSuppression()" name="demo-category" id="StationListSuppr">';

                    // Boucle récupérant les informations du JSON pour les insérer dans le selecteur (HTML)
                    for (var i = 0; i < myArr.length; i++) {
                        chaine = chaine + '<option value="">' + myArr[i].name + '</option>';
                    }

                    chaine = chaine + '</select>';

                    // Génération du sélecteur
                    document.getElementById("listeSonde").innerHTML = chaine;
                }
                break;
        }
    };
}

// Affiche les capteurs présents sur la sonde sélectionnée
function affichageCapteurDeSondeSuppression() {
    // Récupération de l'identifiant sélectionné dans le selecteur
    var index = document.getElementById("StationListSuppr");
    var station = index.options[index.selectedIndex].text;

    var xmlhttp = new XMLHttpRequest();
    var stop = false;

    var trame = '{"nom": "' + station + '"}';

    // Envoi de la trame au serveur python
    xmlhttp.open("POST", adresseIPServeur + "sensorOfStation");

    xmlhttp.send(trame);

    xmlhttp.onreadystatechange = function () {

        switch (xmlhttp.status) {
            case 200:
                if (xmlhttp.readyState == 4 && xmlhttp.responseText && stop == false) {
                    stop = true;

                    var myArr = JSON.parse(xmlhttp.responseText);

                    var chaine = "";

                    // On vas générer un selecteur avec l'ensemble des capteurs
                    var chaine = '<select name="demo-category" id="SensorListSuppr">';

                    // Boucle récupérant les informations du JSON pour les insérer dans le selecteur (HTML)
                    for (var i = 0; i < myArr.capteur.length; i++) {
                        chaine = chaine + '<option value="">' + myArr.capteur[i] + '</option>';
                    }

                    chaine = chaine + '</select>';

                    document.getElementById("listeCapteur").innerHTML = chaine;
                }
                break;
            default:
                if (stop == false) {
                    stop = true;
                    alert("Erreur inconnue : " + xmlhttp.status);
                }
        }
    };
}

// Envoi la requête de suppression au serveur puthon --> BDD
function supprimerCapteurSurSonde() {

    // Récupération de l'identifiant sélectionné dans le selecteur
    var index = document.getElementById("StationListSuppr");
    var station = index.options[index.selectedIndex].text;

    // Récupération de l'identifiant sélectionné dans le selecteur
    index = document.getElementById("SensorListSuppr");
    var capteur = index.options[index.selectedIndex].text;

    var xmlhttp = new XMLHttpRequest();
    var stop = false;

    var trame = '{"station": "' + station + '","capteurType":"' + capteur + '"}';

    // Envoi de la trame au serveur python
    xmlhttp.open("POST", adresseIPServeur + "deletedSensorToStation");

    xmlhttp.send(trame);

    xmlhttp.onreadystatechange = function () {

        switch (xmlhttp.status) {
            case 200:
                if (stop == false) {
                    stop = true;
                    alert("Capteur " + capteur + " supprimé de la sonde " + station);

                    document.location.href = "supprimerCapteurSurSonde.html";
                }
                break;
            default:
                if (stop == false) {
                    stop = true;
                    alert("Erreur inconnue : " + xmlhttp.status);
                }
        }
    };
}

//***********************************************************************//
//******************** REINITIALISER MOT DE PASSE ***********************//
//***********************************************************************//

// Redirection vers la page des mot de passe oubliés
function PageMotDePasseOublie() {
    document.location.href = "motDePasseOublie.html";
}

// Permet de recevoir par mail un mot de passe provisoire
function reinitialisationMotDePasse() {
    var xmlhttp = new XMLHttpRequest();
    var stop = false;

    // Récupération des informations saisies
    var login = document.getElementById("login").value;
    var mail = document.getElementById("mail").value;

    // Tests si les champs obligatoire sont vides
    if (login == "") {
        alert("Champs login vide.");
        return 0;
    } else if (mail == "") {
        alert("Champs mail vide.");
        return 0;
    }

    var trame = '{"login": "' + login + '","mail":"' + mail + '"}';

    // Envoi de la trame au serveur
    xmlhttp.open("POST", adresseIPServeur + "forgotPassword");

    xmlhttp.send(trame);

    xmlhttp.onreadystatechange = function () {

        switch (xmlhttp.status) {
            case 200:
                if (stop == false) {
                    stop = true;
                    alert("mail envoyé");
                    document.location.href = "index.html";
                }
                break;
            default:
                if (stop == false) {
                    stop = true;
                    alert("Erreur inconnue : " + xmlhttp.status);
                }
        }
    };
}

// Permet de remplacer son mot de passe provisoire
function ecraserPassword() {

    var xmlhttp = new XMLHttpRequest();
    var stop = false;

    // Récupération des information utilisateur + saisies
    var login = getCookie("login_utilisateur");
    var password = document.getElementById("password").value;
    var password2 = document.getElementById("password2").value;

    // Test si le nouveau password à bien été saisie
    if (password == "") {
        alert("Champs mot de passe vide.");
    }

    // test si le mot de passe de confirmation est identique au mot de passe
    if (password != password2) {
        alert("Les deux mot de passe ne sont pas identiques");
        document.getElementById("password").innerHTML = "";
        document.getElementById("password2").innerHTML = "";
        return 0;
    }

    // Chiffrage du mot de passe en MD5 avant de la transmettre au serveur python --> BDD
    password = calcMD5(password);

    var trame = '{"login": "' + login + '","password":"' + password + '"}';

    xmlhttp.open("POST", adresseIPServeur + "erasePassword");

    xmlhttp.send(trame);

    xmlhttp.onreadystatechange = function () {

        switch (xmlhttp.status) {
            case 200:
                if (xmlhttp.readyState == 4 && stop == false) {
                    stop = true;
                    alert("Mot de passe modifié");
                    document.location.href = "index.html";
                }
                break;
            default:
                if (stop == false) {
                    stop = true;
                    alert("Erreur inconnue : " + xmlhttp.status);
                }
        }
    };
}

//*****************************************************************************//
//*********************** GENERATION GRAPHIQUE AMCHARTS ***********************//
//*****************************************************************************//

// Fonction de mise en page du graphique
// https://www.amcharts.com/demos/line-chart-with-scroll-and-zoom/
function CreateGraphic(_donnees, _date) {

    var chartData = generateChartData(_donnees, _date);
    var chart = AmCharts.makeChart("chartdiv", {
        "type": "serial",
        "theme": "light",
        "marginRight": 80,
        "autoMarginOffset": 20,
        "marginTop": 7,
        "dataProvider": chartData,
        "valueAxes": [{
            "axisAlpha": 0.2,
            "dashLength": 1,
            "position": "left"
        }],
        "mouseWheelZoomEnabled": true,
        "graphs": [{
            "id": "g1",
            "balloonText": "[[value]]",
            "bullet": "round",
            "bulletBorderAlpha": 1,
            "bulletColor": "#FFFFFF",
            "hideBulletsCount": 50,
            "title": "red line",
            "valueField": "visits",
            "useLineColorForBulletBorder": true,
            "balloon": {
                "drop": true
            }
        }],
        "chartScrollbar": {
            "autoGridCount": false,
            "graph": "g1",
            "scrollbarHeight": 40
        },
        "chartCursor": {
            "limitToGraph": "g1"
        },
        "categoryField": "date",
        "categoryAxis": {
            "parseDates": false,
            "axisColor": "#DADADA",
            "dashLength": 1,
            "minorGridEnabled": true,
            "labelRotation": 90
        },
        "export": {
            "enabled": true
        }
    });

    chart.addListener("rendered", zoomChart);
    zoomChart();

    // this method is called when chart is first inited as we listen for "rendered" event
    function zoomChart() {
        // different zoom methods can be used - zoomToIndexes, zoomToDates, zoomToCategoryValues
        chart.zoomToIndexes(chartData.length - 40, chartData.length - 1);
    }

    // generate some random data, quite different range
    function generateChartData(donnees, date) {
        var chartData = [];

        // Parcours l'ensemble des données pour formatage des dates
        // TIMESTAMP --> JJ/MM/AAAA HH:MM:SS
        for (var i = 0; i < donnees.length; i++) {

            var dateFormatte = new Date(date[i] * 1000);

            var newnewdate = dateFormatte.getDate() + "/" + (dateFormatte.getMonth() + 1) + "/" + dateFormatte.getFullYear() + " \
                 " + dateFormatte.getHours() + ":" + dateFormatte.getMinutes() + ":" + dateFormatte.getSeconds();

            chartData.push({
                date: newnewdate,
                visits: donnees[i]
            });
        }
        return chartData;
    }
}

//***********************************************************//
//***************** GESTION DES COOKIES *********************//
//***********************************************************//

// Enregistrer un cookie sur le naviguateur
function setCookie(nom, Valeur, Time) {
    var today = new Date(), expires = new Date();
    // Expire au bout de "Time" jours
    expires.setTime(today.getTime() + (Time * 24 * 60 * 60 * 1000));
    document.cookie = nom + "=" + encodeURIComponent(Valeur) + ";expires=" + expires.toGMTString();
}

// Récupérer un cookie
function getCookie(nom) {
    var cookContent = document.cookie, cookEnd, i, j;
    var sName = nom + "=";

    for (i = 0, c = cookContent.length; i < c; i++) {
        j = i + sName.length;
        if (cookContent.substring(i, j) == sName) {
            cookEnd = cookContent.indexOf(";", j);
            if (cookEnd == -1) {
                cookEnd = cookContent.length;
            }
            return decodeURIComponent(cookContent.substring(j, cookEnd));
        }
    }
    return null;
}


//****************************************************************//
//************************ CHIFFRAGE MD5 *************************//
//****************************************************************//


/*
 * A JavaScript implementation of the RSA Data Security, Inc. MD5 Message
 * Digest Algorithm, as defined in RFC 1321.
 * Copyright (C) Paul Johnston 1999 - 2000.
 * Updated by Greg Holt 2000 - 2001.
 * See http://pajhome.org.uk/site/legal.html for details.
 */

/*
 * Convert a 32-bit number to a hex string with ls-byte first
 */
var hex_chr = "0123456789abcdef";
function rhex(num) {
    str = "";
    for (j = 0; j <= 3; j++)
        str += hex_chr.charAt((num >> (j * 8 + 4)) & 0x0F) +
            hex_chr.charAt((num >> (j * 8)) & 0x0F);
    return str;
}

/*
 * Convert a string to a sequence of 16-word blocks, stored as an array.
 * Append padding bits and the length, as described in the MD5 standard.
 */
function str2blks_MD5(str) {
    nblk = ((str.length + 8) >> 6) + 1;
    blks = new Array(nblk * 16);
    for (i = 0; i < nblk * 16; i++) blks[i] = 0;
    for (i = 0; i < str.length; i++)
        blks[i >> 2] |= str.charCodeAt(i) << ((i % 4) * 8);
    blks[i >> 2] |= 0x80 << ((i % 4) * 8);
    blks[nblk * 16 - 2] = str.length * 8;
    return blks;
}

/*
 * Add integers, wrapping at 2^32. This uses 16-bit operations internally
 * to work around bugs in some JS interpreters.
 */
function add(x, y) {
    var lsw = (x & 0xFFFF) + (y & 0xFFFF);
    var msw = (x >> 16) + (y >> 16) + (lsw >> 16);
    return (msw << 16) | (lsw & 0xFFFF);
}

/*
 * Bitwise rotate a 32-bit number to the left
 */
function rol(num, cnt) {
    return (num << cnt) | (num >>> (32 - cnt));
}

/*
 * These functions implement the basic operation for each round of the
 * algorithm.
 */
function cmn(q, a, b, x, s, t) {
    return add(rol(add(add(a, q), add(x, t)), s), b);
}
function ff(a, b, c, d, x, s, t) {
    return cmn((b & c) | ((~b) & d), a, b, x, s, t);
}
function gg(a, b, c, d, x, s, t) {
    return cmn((b & d) | (c & (~d)), a, b, x, s, t);
}
function hh(a, b, c, d, x, s, t) {
    return cmn(b ^ c ^ d, a, b, x, s, t);
}
function ii(a, b, c, d, x, s, t) {
    return cmn(c ^ (b | (~d)), a, b, x, s, t);
}

/*
 * Take a string and return the hex representation of its MD5.
 */
function calcMD5(str) {
    x = str2blks_MD5(str);
    a = 1732584193;
    b = -271733879;
    c = -1732584194;
    d = 271733878;

    for (i = 0; i < x.length; i += 16) {
        olda = a;
        oldb = b;
        oldc = c;
        oldd = d;

        a = ff(a, b, c, d, x[i + 0], 7, -680876936);
        d = ff(d, a, b, c, x[i + 1], 12, -389564586);
        c = ff(c, d, a, b, x[i + 2], 17, 606105819);
        b = ff(b, c, d, a, x[i + 3], 22, -1044525330);
        a = ff(a, b, c, d, x[i + 4], 7, -176418897);
        d = ff(d, a, b, c, x[i + 5], 12, 1200080426);
        c = ff(c, d, a, b, x[i + 6], 17, -1473231341);
        b = ff(b, c, d, a, x[i + 7], 22, -45705983);
        a = ff(a, b, c, d, x[i + 8], 7, 1770035416);
        d = ff(d, a, b, c, x[i + 9], 12, -1958414417);
        c = ff(c, d, a, b, x[i + 10], 17, -42063);
        b = ff(b, c, d, a, x[i + 11], 22, -1990404162);
        a = ff(a, b, c, d, x[i + 12], 7, 1804603682);
        d = ff(d, a, b, c, x[i + 13], 12, -40341101);
        c = ff(c, d, a, b, x[i + 14], 17, -1502002290);
        b = ff(b, c, d, a, x[i + 15], 22, 1236535329);

        a = gg(a, b, c, d, x[i + 1], 5, -165796510);
        d = gg(d, a, b, c, x[i + 6], 9, -1069501632);
        c = gg(c, d, a, b, x[i + 11], 14, 643717713);
        b = gg(b, c, d, a, x[i + 0], 20, -373897302);
        a = gg(a, b, c, d, x[i + 5], 5, -701558691);
        d = gg(d, a, b, c, x[i + 10], 9, 38016083);
        c = gg(c, d, a, b, x[i + 15], 14, -660478335);
        b = gg(b, c, d, a, x[i + 4], 20, -405537848);
        a = gg(a, b, c, d, x[i + 9], 5, 568446438);
        d = gg(d, a, b, c, x[i + 14], 9, -1019803690);
        c = gg(c, d, a, b, x[i + 3], 14, -187363961);
        b = gg(b, c, d, a, x[i + 8], 20, 1163531501);
        a = gg(a, b, c, d, x[i + 13], 5, -1444681467);
        d = gg(d, a, b, c, x[i + 2], 9, -51403784);
        c = gg(c, d, a, b, x[i + 7], 14, 1735328473);
        b = gg(b, c, d, a, x[i + 12], 20, -1926607734);

        a = hh(a, b, c, d, x[i + 5], 4, -378558);
        d = hh(d, a, b, c, x[i + 8], 11, -2022574463);
        c = hh(c, d, a, b, x[i + 11], 16, 1839030562);
        b = hh(b, c, d, a, x[i + 14], 23, -35309556);
        a = hh(a, b, c, d, x[i + 1], 4, -1530992060);
        d = hh(d, a, b, c, x[i + 4], 11, 1272893353);
        c = hh(c, d, a, b, x[i + 7], 16, -155497632);
        b = hh(b, c, d, a, x[i + 10], 23, -1094730640);
        a = hh(a, b, c, d, x[i + 13], 4, 681279174);
        d = hh(d, a, b, c, x[i + 0], 11, -358537222);
        c = hh(c, d, a, b, x[i + 3], 16, -722521979);
        b = hh(b, c, d, a, x[i + 6], 23, 76029189);
        a = hh(a, b, c, d, x[i + 9], 4, -640364487);
        d = hh(d, a, b, c, x[i + 12], 11, -421815835);
        c = hh(c, d, a, b, x[i + 15], 16, 530742520);
        b = hh(b, c, d, a, x[i + 2], 23, -995338651);

        a = ii(a, b, c, d, x[i + 0], 6, -198630844);
        d = ii(d, a, b, c, x[i + 7], 10, 1126891415);
        c = ii(c, d, a, b, x[i + 14], 15, -1416354905);
        b = ii(b, c, d, a, x[i + 5], 21, -57434055);
        a = ii(a, b, c, d, x[i + 12], 6, 1700485571);
        d = ii(d, a, b, c, x[i + 3], 10, -1894986606);
        c = ii(c, d, a, b, x[i + 10], 15, -1051523);
        b = ii(b, c, d, a, x[i + 1], 21, -2054922799);
        a = ii(a, b, c, d, x[i + 8], 6, 1873313359);
        d = ii(d, a, b, c, x[i + 15], 10, -30611744);
        c = ii(c, d, a, b, x[i + 6], 15, -1560198380);
        b = ii(b, c, d, a, x[i + 13], 21, 1309151649);
        a = ii(a, b, c, d, x[i + 4], 6, -145523070);
        d = ii(d, a, b, c, x[i + 11], 10, -1120210379);
        c = ii(c, d, a, b, x[i + 2], 15, 718787259);
        b = ii(b, c, d, a, x[i + 9], 21, -343485551);

        a = add(a, olda);
        b = add(b, oldb);
        c = add(c, oldc);
        d = add(d, oldd);
    }
    return rhex(a) + rhex(b) + rhex(c) + rhex(d);
}

//******************* TIME CONVERTER *********************//

// TIMESTAMP --> Date personnalisée
function timeConverter(UNIX_timestamp) {
    var a = new Date(UNIX_timestamp * 1000);
    var months = [01, 02, 03, 04, 05, 06, 07, 08, 09, 10, 11, 12];
    var year = a.getFullYear();
    var month = months[a.getMonth()];
    var date = a.getDate();
    var hour = a.getHours();
    var min = a.getMinutes();
    var sec = a.getSeconds();
    //yyyy-MM-dd HH:mm:ss
    var time = year + '-' + month + '-' + date + ' ' + hour + ':' + min + ':' + sec;
    return time;
}

//******************************************************//
//******************* IO FILES *************************//
//******************************************************//

// JSON --> CSV
// http://jsfiddle.net/hybrid13i/JXrwM/

function JSONToCSVConvertor(JSONData, ReportTitle, ShowLabel) {

    //If JSONData is not an object then JSON.parse will parse the JSON string in an Object
    var arrData = typeof JSONData != 'object' ? JSON.parse(JSONData) : JSONData;

    var CSV = '';

    //Set Report title in first row or line
    CSV += ReportTitle + '\r\n\n';

    //This condition will generate the Label/Header
    if (ShowLabel) {
        var row = "";

        //This loop will extract the label from 1st index of on array
        for (var index in arrData[0]) {

            //Now convert each value to string and comma-seprated
            row += index + ',';
        }

        row = row.slice(0, -1);

        //append Label row with line break
        CSV += row + '\r\n';
    }

    // Format Expressions
    for (var j = 0; j < arrData.releve.length; j++) {

        arrData.releve[j].dateReleve = timeConverter(arrData.releve[j].dateReleve);

        arrData.releve[j].mesure = arrData.releve[j].mesure.toString().replace('.', ',');

    }

    //1st loop is to extract each row
    for (var i = 0; i < arrData.releve.length; i++) {
        var row = "";

        //2nd loop will extract each column and convert it in string comma-seprated
        for (var index in arrData.releve[i]) {
            row += '"' + arrData.releve[i][index] + '";';
        }

        row.slice(0, row.length - 1);

        //add a line break after each row
        CSV += row + '\r\n';
    }

    if (CSV == '') {
        alert("Invalid data for CSV");
        return;
    }

    //Generate a file name
    var fileName = "MyReport_";
    //this will remove the blank-spaces from the title and replace it with an underscore
    fileName += ReportTitle.replace(/ /g, "_");

    //Initialize file format you want csv or xls
    var uri = 'data:text/csv;charset=utf-8,' + escape(CSV);

    // Now the little tricky part.
    // you can use either>> window.open(uri);
    // but this will not work in some browsers
    // or you will not get the correct file extension

    //this trick will generate a temp <a /> tag
    var link = document.createElement("a");
    link.href = uri;

    //set the visibility hidden so it will not effect on your web-layout
    link.style = "visibility:hidden";
    link.download = fileName + ".csv";

    //this part will append the anchor tag and remove it after automatic click
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// Fonction permettant d'inverser l'état de tous les champs de saisie d'une page HTML
function basculerEtatChampsDeSaisie() {
    var inputs = document.getElementsByTagName('input');
    for (var i = inputs.length, n = 0; n < i; n++) {
        inputs[n].disabled = !inputs[n].disabled;
    }
}

function download(filename, text) {
    var element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
    element.setAttribute('download', filename);

    element.style.display = 'none';
    document.body.appendChild(element);

    element.click();

    document.body.removeChild(element);
}