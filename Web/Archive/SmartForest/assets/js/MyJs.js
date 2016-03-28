/**
 * Created by Arnaud on 11/02/2016.
 */
function popup() {
    window.alert("Test");
}

function remplissageAutomatiqueEnregistrement(){
    //alert("auto");
    document.getElementById("login").value = "abe";
    document.getElementById("password").value = "toto";
    document.getElementById("nom").value = "Bes";
    document.getElementById("prenom").value = "Arnaud";
    document.getElementById("description").value = "pouet";
}


//***********************************************************//
//***********************************************************//

function enregistrement(){

    //alert("Enregistrement");

    var login = document.getElementById("login").value;
    var motDePasse = document.getElementById("password").value;
    var nom = document.getElementById("nom").value;
    var prenom = document.getElementById("prenom").value;
    var description = document.getElementById("description").value;

    var motDePasseChiffre = calcMD5(motDePasse);

    var trame = '{"login": "' + login + '","password": "' + motDePasseChiffre + '","nom": "' + nom + '","prenom": "' + prenom + '","description": "' + description + '"}';

    HttpPost("http://172.30.0.103:8080/user",trame);

    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.status == 200) {
            alert("Enregistrement effectué");
        }else if(xmlhttp.status == 401){
            //Login existant
            document.getElementById("Wrong_Login").innerHTML = "Login déjà utilisé";
            //alert("Wrong Password");
        }
    };

}

function connexion() {

    //alert("Connexion()");

    var login = document.getElementById("login").value;
    var motDePasse = document.getElementById("password").value;
    var motDePasseChiffre = calcMD5(motDePasse);

    //alert("md5 : " + motDePasseChiffre);

    var trame = "{login: \"" + login +"\", password: \"" + motDePasseChiffre + "\"}";

    alert("login : " + login + "\npassword : " + motDePasse + "\nmd5 : " + motDePasseChiffre);

    //return 0;

    // Vérification en base de données du login et mot de passe

    HttpPost(trame);

    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.status == 200) {
            alert("OK");
        }else if(xmlhttp.status == 405){
            alert("Wrong Password");
        }else if(xmlhttp.status == 403){
            alert("Wrong Login");
        }
    };
/*
    if (login != "pouet") {
        document.getElementById("invalid_login").innerHTML = "Login incorrect";
    } else {
        if (motDePasse == "toto") {
            window.location.href = "index.html";
            setCookie("nom_utilisateur", login);
            setCookie("mot_de_passe_utilisateur", motDePasse);
        } else {
            document.getElementById("invalid_password").innerHTML = "Mot de passe incorrect";
        }
    }*/
    // Fin if login password
}

//*****************************************************//
//****************** INITIALISATIONS ******************//
//*****************************************************//

function initConnexion() {
    if (navigator.cookieEnabled) {
        // Cookies acceptés
        if (getCookie("nom_utilisateur") != null) {
            document.getElementById("login").innerHTML = getCookie("nom_utilisateur");
            document.getElementById("password").innerHTML = getCookie("mot_de_passe_utilisateur");
        }
    }
}

function initIndex() {

    if (navigator.cookieEnabled) {
        // Cookies acceptés
    } else {
        alert("Vos cookies sont désactivés.\nActivez les pour vous connecter.");
    }

    var nom_utilisateur = getCookie("nom_utilisateur");
    var Description_Utilisateur = "Default Description";

    // Récupération Description BDD
    // A coder ....
    //********

    document.getElementById("logo").innerHTML = nom_utilisateur;
    document.getElementById("Description_Utilisateur").innerHTML = Description_Utilisateur;
}

//***********************************************************//
//***************************** HTTP ************************//
//***********************************************************//

function HttpTestGet() {
    var xmlhttp = new XMLHttpRequest();
    var url = "http://172.30.0.103:8080/login";
    //var url = "toto.txt";

    // Valide le fonctionnement du protocole HTTP sur le naviguateur
    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            var myArr = JSON.parse(xmlhttp.responseText);
            GetInformations(myArr);
        } else {
            alert("Erreur HTTP\nready state : " + xmlhttp.readyState + "        status : " + xmlhttp.status);
        }
    };
    xmlhttp.open("GET", url, true);
    xmlhttp.send();

    function GetInformations(arr) {
        var out = "";
        var i;

        for (i = 0; i < arr.length; i++) {
            out += '<p>' + arr[i].Valid + '</p><br>';
        }

        document.getElementById("id01").innerHTML = out;
    }
}

function HttpTestPost() {
    alert("TEST");
    var trame = "{\"login\": \"toto\", \"password\": \"pouet\"}";
    HttpPost("http://172.30.0.103:8080/login",trame);
}

function HttpPost(_url,trame) {
    //alert("HTTP POST");
    var xmlhttp = new XMLHttpRequest();   // new HttpRequest instance
    var url = _url;
    //var url = "http://172.30.0.103:8080/login";
    //{login: "toto", password: "pouet"}

    //alert("Chaine envoyée : " + trame);

    xmlhttp.open("POST", url);

    xmlhttp.send(trame);

    return xmlhttp;

    /*
    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.status == 200) {
            alert("OK");
        }else if(xmlhttp.status == 405){
            alert("Wrong Password");
        }else if(xmlhttp.status == 403){
            alert("Wrong Login");
        }
    };*/
}

//***********************************************************//
//***************** GESTION DES COOKIES *********************//
//***********************************************************//

// Enregistrer un cookie sur le naviguateur
function setCookie(nom, Valeur) {
    var today = new Date(), expires = new Date();
    expires.setTime(today.getTime() + (7 * 24 * 60 * 60 * 1000));
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
function rhex(num)
{
    str = "";
    for(j = 0; j <= 3; j++)
        str += hex_chr.charAt((num >> (j * 8 + 4)) & 0x0F) +
            hex_chr.charAt((num >> (j * 8)) & 0x0F);
    return str;
}

/*
 * Convert a string to a sequence of 16-word blocks, stored as an array.
 * Append padding bits and the length, as described in the MD5 standard.
 */
function str2blks_MD5(str)
{
    nblk = ((str.length + 8) >> 6) + 1;
    blks = new Array(nblk * 16);
    for(i = 0; i < nblk * 16; i++) blks[i] = 0;
    for(i = 0; i < str.length; i++)
        blks[i >> 2] |= str.charCodeAt(i) << ((i % 4) * 8);
    blks[i >> 2] |= 0x80 << ((i % 4) * 8);
    blks[nblk * 16 - 2] = str.length * 8;
    return blks;
}

/*
 * Add integers, wrapping at 2^32. This uses 16-bit operations internally
 * to work around bugs in some JS interpreters.
 */
function add(x, y)
{
    var lsw = (x & 0xFFFF) + (y & 0xFFFF);
    var msw = (x >> 16) + (y >> 16) + (lsw >> 16);
    return (msw << 16) | (lsw & 0xFFFF);
}

/*
 * Bitwise rotate a 32-bit number to the left
 */
function rol(num, cnt)
{
    return (num << cnt) | (num >>> (32 - cnt));
}

/*
 * These functions implement the basic operation for each round of the
 * algorithm.
 */
function cmn(q, a, b, x, s, t)
{
    return add(rol(add(add(a, q), add(x, t)), s), b);
}
function ff(a, b, c, d, x, s, t)
{
    return cmn((b & c) | ((~b) & d), a, b, x, s, t);
}
function gg(a, b, c, d, x, s, t)
{
    return cmn((b & d) | (c & (~d)), a, b, x, s, t);
}
function hh(a, b, c, d, x, s, t)
{
    return cmn(b ^ c ^ d, a, b, x, s, t);
}
function ii(a, b, c, d, x, s, t)
{
    return cmn(c ^ (b | (~d)), a, b, x, s, t);
}

/*
 * Take a string and return the hex representation of its MD5.
 */
function calcMD5(str)
{
    x = str2blks_MD5(str);
    a =  1732584193;
    b = -271733879;
    c = -1732584194;
    d =  271733878;

    for(i = 0; i < x.length; i += 16)
    {
        olda = a;
        oldb = b;
        oldc = c;
        oldd = d;

        a = ff(a, b, c, d, x[i+ 0], 7 , -680876936);
        d = ff(d, a, b, c, x[i+ 1], 12, -389564586);
        c = ff(c, d, a, b, x[i+ 2], 17,  606105819);
        b = ff(b, c, d, a, x[i+ 3], 22, -1044525330);
        a = ff(a, b, c, d, x[i+ 4], 7 , -176418897);
        d = ff(d, a, b, c, x[i+ 5], 12,  1200080426);
        c = ff(c, d, a, b, x[i+ 6], 17, -1473231341);
        b = ff(b, c, d, a, x[i+ 7], 22, -45705983);
        a = ff(a, b, c, d, x[i+ 8], 7 ,  1770035416);
        d = ff(d, a, b, c, x[i+ 9], 12, -1958414417);
        c = ff(c, d, a, b, x[i+10], 17, -42063);
        b = ff(b, c, d, a, x[i+11], 22, -1990404162);
        a = ff(a, b, c, d, x[i+12], 7 ,  1804603682);
        d = ff(d, a, b, c, x[i+13], 12, -40341101);
        c = ff(c, d, a, b, x[i+14], 17, -1502002290);
        b = ff(b, c, d, a, x[i+15], 22,  1236535329);

        a = gg(a, b, c, d, x[i+ 1], 5 , -165796510);
        d = gg(d, a, b, c, x[i+ 6], 9 , -1069501632);
        c = gg(c, d, a, b, x[i+11], 14,  643717713);
        b = gg(b, c, d, a, x[i+ 0], 20, -373897302);
        a = gg(a, b, c, d, x[i+ 5], 5 , -701558691);
        d = gg(d, a, b, c, x[i+10], 9 ,  38016083);
        c = gg(c, d, a, b, x[i+15], 14, -660478335);
        b = gg(b, c, d, a, x[i+ 4], 20, -405537848);
        a = gg(a, b, c, d, x[i+ 9], 5 ,  568446438);
        d = gg(d, a, b, c, x[i+14], 9 , -1019803690);
        c = gg(c, d, a, b, x[i+ 3], 14, -187363961);
        b = gg(b, c, d, a, x[i+ 8], 20,  1163531501);
        a = gg(a, b, c, d, x[i+13], 5 , -1444681467);
        d = gg(d, a, b, c, x[i+ 2], 9 , -51403784);
        c = gg(c, d, a, b, x[i+ 7], 14,  1735328473);
        b = gg(b, c, d, a, x[i+12], 20, -1926607734);

        a = hh(a, b, c, d, x[i+ 5], 4 , -378558);
        d = hh(d, a, b, c, x[i+ 8], 11, -2022574463);
        c = hh(c, d, a, b, x[i+11], 16,  1839030562);
        b = hh(b, c, d, a, x[i+14], 23, -35309556);
        a = hh(a, b, c, d, x[i+ 1], 4 , -1530992060);
        d = hh(d, a, b, c, x[i+ 4], 11,  1272893353);
        c = hh(c, d, a, b, x[i+ 7], 16, -155497632);
        b = hh(b, c, d, a, x[i+10], 23, -1094730640);
        a = hh(a, b, c, d, x[i+13], 4 ,  681279174);
        d = hh(d, a, b, c, x[i+ 0], 11, -358537222);
        c = hh(c, d, a, b, x[i+ 3], 16, -722521979);
        b = hh(b, c, d, a, x[i+ 6], 23,  76029189);
        a = hh(a, b, c, d, x[i+ 9], 4 , -640364487);
        d = hh(d, a, b, c, x[i+12], 11, -421815835);
        c = hh(c, d, a, b, x[i+15], 16,  530742520);
        b = hh(b, c, d, a, x[i+ 2], 23, -995338651);

        a = ii(a, b, c, d, x[i+ 0], 6 , -198630844);
        d = ii(d, a, b, c, x[i+ 7], 10,  1126891415);
        c = ii(c, d, a, b, x[i+14], 15, -1416354905);
        b = ii(b, c, d, a, x[i+ 5], 21, -57434055);
        a = ii(a, b, c, d, x[i+12], 6 ,  1700485571);
        d = ii(d, a, b, c, x[i+ 3], 10, -1894986606);
        c = ii(c, d, a, b, x[i+10], 15, -1051523);
        b = ii(b, c, d, a, x[i+ 1], 21, -2054922799);
        a = ii(a, b, c, d, x[i+ 8], 6 ,  1873313359);
        d = ii(d, a, b, c, x[i+15], 10, -30611744);
        c = ii(c, d, a, b, x[i+ 6], 15, -1560198380);
        b = ii(b, c, d, a, x[i+13], 21,  1309151649);
        a = ii(a, b, c, d, x[i+ 4], 6 , -145523070);
        d = ii(d, a, b, c, x[i+11], 10, -1120210379);
        c = ii(c, d, a, b, x[i+ 2], 15,  718787259);
        b = ii(b, c, d, a, x[i+ 9], 21, -343485551);

        a = add(a, olda);
        b = add(b, oldb);
        c = add(c, oldc);
        d = add(d, oldd);
    }
    return rhex(a) + rhex(b) + rhex(c) + rhex(d);
}
