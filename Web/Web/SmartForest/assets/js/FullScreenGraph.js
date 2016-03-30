/**
 * Created by Arnaud on 11/02/2016.
 */

var adresseIPServeur = "http://172.30.0.234:8080/";

function FullScreenGraph(){
    GetSensorData();
}

function GetSensorData() {

    var stop = false;

    var xmlhttp = new XMLHttpRequest();

    var login = getCookie("login_utilisateur");
    var capteurId = getCookie("capteurID");
    var dateDebut = getCookie("dateDebut");
    var dateFin = getCookie("dateFin");
    var mesure = getCookie("mesureSave");

    var trame = '{"login": "' + login + '","capteurId": "' + capteurId + '","dateDebut": "' + dateDebut + '","dateFin": "' + dateFin + '","mesure": "' + mesure + '"}';

    xmlhttp.open("POST", adresseIPServeur + "capteur");

    xmlhttp.send(trame);

    xmlhttp.onreadystatechange = function () {

        switch (xmlhttp.status) {
            case 200:
                if (xmlhttp.readyState == 4 && xmlhttp.responseText != "" && stop == false) {
                    stop = true;

                    var donnees = [];
                    var dates = [];

                    // JSON Parsing
                    var myArr = JSON.parse(xmlhttp.responseText);

                    for (var i = 0; i < myArr.releve.length; i++) {
                        var counter = myArr.releve[i];
                        console.log(counter.mesure);

                        donnees.push(myArr.releve[i].mesure);
                        dates.push(myArr.releve[i].dateReleve);
                    }
                    CreateGraphic(donnees, dates);
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
                    alert("OTHER : " + xmlhttp.status);
                }
        }
    };
}

//********************************************************************//
//*********************** GENERATION GRAPHIQUE ***********************//
//********************************************************************//

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
            "balloon":{
                "drop":true
            }
        }],
        "chartScrollbar": {
            "autoGridCount": false,
            "graph": "g1",
            "scrollbarHeight": 40
        },
        "chartCursor": {
            "limitToGraph":"g1"
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
        var toto = false;

        for (var i = 0; i < donnees.length; i++) {

            var dateFormatte = new Date(date[i]*1000);

            var newnewdate = dateFormatte.getDate() + "/" + (dateFormatte.getMonth() + 1) + "/" + dateFormatte.getFullYear() + " \
                 " + dateFormatte.getHours() + ":" + dateFormatte.getMinutes() + ":" + dateFormatte.getSeconds();


            console.log("d : " + newnewdate);
            console.log("v : " + donnees[i]);

            chartData.push({
                date: newnewdate,
                visits: donnees[i]
            });
        }
        return chartData;
    }
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

