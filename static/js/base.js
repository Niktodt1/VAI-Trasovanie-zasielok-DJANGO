function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function confirmPackage(event) {
    if (event.target === null) { console.log("null")}
    let id = event.target.id.slice(-2)

    console.log("CONFIRM PACKAGE FIRED!")
    try {
        let package_to_confirm = document.getElementById("package_" + id)
        let request = fetch("http://127.0.0.1:8000/api/confirmPackage/" + id, {
            method: "PUT",
            credentials: "same-origin",
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": getCookie("csrftoken"),
            },
            body: JSON.stringify({payload: "CONFIRM package_" + id })

        })
        console.log("ERROR:" + request.status + " " + request.statusText)

        //TODO: toast o uspechu!!!
        console.log("odstranujem potvrdenu zasielku: " + "package_" + id)
        package_to_confirm.remove()
        return true;
        // return request;

    } catch (e) {
        console.log(e)
        console.log("ERROR CONFIMING PACKAGE!");
    }
    return false;
    //return null;
}

class Base {




    fillStageBarHTML(stages_count) {

        let stageProgressBar = ""
        if (stages_count === 1)  {
            stageProgressBar += `
            <div class="progress me-1 ms-1" style="height: 8px;">
                <div class="progress-bar progress-bar-animated progress-bar-striped bg-success priebeh20 priebeh-objednavky-mini" aria-label="Segment one"></div>
                <div class="progress-bar bg-secondary priebeh80 priebeh-objednavky-mini" aria-label="Segment two"></div>
            </div>`
        } else if (stages_count === 2) {
            stageProgressBar += `
            <div class="progress me-1 ms-1" style="height: 8px;">
                <div class="progress-bar progress-bar-animated progress-bar-striped bg-success priebeh40 priebeh-objednavky-mini" aria-label="Segment one"></div>
                <div class="progress-bar bg-secondary priebeh60 priebeh-objednavky-mini" aria-label="Segment two"></div>
            </div>`
        } else if (stages_count === 3) {
            stageProgressBar += `
            <div class="progress me-1 ms-1" style="height: 8px;">
                <div class="progress-bar progress-bar-animated progress-bar-striped bg-success priebeh60 priebeh-objednavky-mini" aria-label="Segment one"></div>
                <div class="progress-bar bg-secondary priebeh40 priebeh-objednavky-mini" aria-label="Segment two"></div>
            </div>`
        } else if (stages_count === 4) {
            stageProgressBar += `
            <div class="progress me-1 ms-1" style="height: 8px;">
                <div class="progress-bar progress-bar-animated progress-bar-striped bg-success priebeh80 priebeh-objednavky-mini" aria-label="Segment one"></div>
                <div class="progress-bar bg-secondary priebeh20 priebeh-objednavky-mini" aria-label="Segment two"></div>
            </div>`
        } else if (stages_count === 5) {
            stageProgressBar += `
            <div class="progress me-1 ms-1" style="height: 8px;">
                <div class="progress-bar progress-bar-animated progress-bar-striped bg-success priebeh100 priebeh-objednavky-mini" aria-label="Segment one"></div>
                <div class="progress-bar bg-secondary priebeh0 priebeh-objednavky-mini" aria-label="Segment two"></div>
            </div>`
        } else {
            stageProgressBar += `
            <div class="progress me-1 ms-1" style="height: 8px;">
                <div class="progress-bar progress-bar-animated progress-bar-striped bg-success priebeh0 priebeh-objednavky-mini" aria-label="Segment one"></div>
                <div class="progress-bar bg-secondary priebeh100 priebeh-objednavky-mini" aria-label="Segment two"></div>
            </div>`
        }
        return stageProgressBar
    }

    fillStages(stages, stages_count) {
        let stagesHTML = ""
        let count = 0;

        stages.forEach(stage => {
            let date = new Date(stage.datetime).toLocaleString()
            if (count === stages_count - 1) {
                stagesHTML += `
                <div class="carousel-item active">
                    <div class="container col-8">
                        <b> ${ date }</b><br>
                        ${ stage.stageCurrentId.stageDescription }
                        <br>
                    </div>
                </div>`;
            } else {
                stagesHTML += `
                <div class="carousel-item">
                    <div class="container col-8">
                        <b> ${ date }</b><br>
                        ${ stage.stageCurrentId.stageDescription }
                        <br>
                    </div>
                </div>`;
            }
            count++
            })

        return stagesHTML;
    }

    fillOdhad(zasielka, stages_count, lastStage) {
        let estTimeOfDelivery = new Date(lastStage.estTimeOfDelivery).toLocaleString()

        let odhadHTML = `
         <div class="container-fluid col-6 col-sm-12 odhad-objednavky-mini boldText">`;

        if (stages_count >= 5) {
            if (zasielka.typeOfDelivery.deliveryText === "Na poštu" || zasielka.typeOfDelivery.deliveryText === "Do boxu"
                || zasielka.typeOfDelivery.deliveryText === "Zásielkovňa") {
                odhadHTML += `
                Zásielka je pripravená na vyzdvihnutie:`;
            }
            else {
                odhadHTML += `
                Kuriér bol naposledy videný:`;
            }
        } else {
            odhadHTML += `
            Predpokladaný termín doručenia:`;
        }
        odhadHTML += `
        </div>
        <div class="container-fluid col-4 col-sm-12 odhad-mini boldText greenText">`;

        if (stages_count >= 5) {
            odhadHTML += `
            <div>${lastStage.lastSeen}</div>
            <div class="col-12">
                <a id="confirm_button_${zasielka.id}" class="btn btn-success btn-sm"><i class="fa-solid fa-check"></i> Prevzaté</a>
            </div>`;
        } else {
            odhadHTML += `
            ${estTimeOfDelivery}`;
        }
        odhadHTML += `
        </div>`;

        return odhadHTML

    }

    fillCollapseClasses(classes) {
        let HTML = "";
        if (classes === null) {
            HTML = "collapse karta-zasielka-maxi";
        } else {
            HTML = classes.toString();
        }
        return HTML;

    }

    fillStatus(packages_count) {
        let HTML = ``;
        if (packages_count === 0) {
            HTML = `
            <h1>Aktuálne nemáte žiadne zásielky</h1>`;
        } else if (packages_count === 1) {
            HTML = `
            <h1>Aktuálne máte 1 zásielku</h1>`;
        } else if (packages_count <= 4) {
            HTML = `
            <h1>Aktuálne máte ${packages_count} zásielky</h1>`;
        } else {
            HTML = `
            <h1>Aktuálne máte ${packages_count} zásielok</h1>`;
        }
        let statusElement = document.getElementById("status");
        // console.log("STATUS HAS: " + packages_count + " packages!")
        statusElement.innerHTML = HTML
    }



    fillHTML(zasielka, company, destinationAddress, date, stages_count, stages, lastStage, deliveryCompany, courier,
             classes, collapse_button_classes) {
        let HTML = `
        <div id="package_${zasielka.id}" class="card">
                    <div class="card-header karta-zasielka-mini p-1 ">
                        <div id="${zasielka.id}">
                            <div class="container-fluid col-12">
                                <div class="row">
                                    <div class="container-fluid col-2 ikona-obchod-mini">
                         
<!--                                                <img src="/static/${company.iconPath}" alt="${company.companyCode}" class="ikona-obchodu-mini">-->
                                            <img src="/static${company.icon}" alt="${company.companyCode}" class="ikona-obchodu-mini">
                                    </div>
                                    <div class="container-fluid col-9 objednavka-mini">
                                        <b>Objednávka:</b> ${zasielka.id}<br>
                                        <b>Na adresu:</b>
                                        ${destinationAddress.street} ${destinationAddress.streetNumber}, ${destinationAddress.zipCode} ${destinationAddress.city}
                                    </div>
                                    <div class="container-fluid col-1 btn-roztiahni-mini p-0 ">
                                        <a id="collapse_button_${zasielka.id}" class="btn text-center" data-bs-toggle="collapse" href="#collapse${zasielka.id}"><i class="${collapse_button_classes}"></i></a>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-12 col-sm-2 p-1">
                                        <div class="row">
                                            <div class="container-fluid col-6 col-sm-12 datum-objednavky-mini boldText">Dátum <br>objednávky:</div>
                                            <div class="container-fluid col-4 col-sm-12 datum-mini">${date}</div>
                                        </div>
            
                                    </div>
                                    <div class="col-12 col-sm-7 p-1">
                                        <div class="container-fluid mt-2">
                                                ${this.fillStageBarHTML(stages_count)}
                                        </div>
                                        <div class="container-fluid priebeh-mini mt-1">
                                            <!-- Carousel -->
                                            <div class="carousel" data-bs-ride="false" id="carousel${zasielka.id}" data-bs-wrap="false">
            
                                                <div class="carousel-inner">
                                                    ${this.fillStages(stages, stages_count)}
                                                </div>
            
                                                <button class="carousel-control-prev" type="button" data-bs-target="#carousel${zasielka.id}" data-bs-slide="prev">
                                                    <span class="carousel-control-prev-icon bg-dark"></span>
                                                </button>
                                                <button class="carousel-control-next " type="button" data-bs-target="#carousel${zasielka.id}" data-bs-slide="next">
                                                    <span class="carousel-control-next-icon bg-dark"></span>
                                                </button>
                                            </div>
                                        </div>
           
                                    </div>
            
                                    <div class="col-12 col-sm-3 p-1">
                                        <div class="row">
                                            ${this.fillOdhad(zasielka, stages_count, lastStage)}
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div id="collapse${zasielka.id}" class="${this.fillCollapseClasses(classes)}" data-bs-parent="#accordion">
                        <div class="card-body p-1">
                            <div class="container-fluid col-12">
                                <div class="row">
                                    <div class="container-fluid col-6 mapa">
                                        <!--<img src="public/images/senohrad.png" alt="mapa">-->
                                        MAP PREVIEW Coming Soon™
                                    </div>
                                    <div class="container-fluid col-6 kontakty-maxi" >
                                        <div class="row mt-3">
                                            <div class="container-fluid col-4 boldText">
            
                                                Posledná známa<br>
                                                poloha:
                                            </div>
                                            <div class="container col-8">
                                                ${lastStage.lastSeen}
                                            </div>
                                        </div>
                                        
                                        <div class="row mt-3">
                                            <div class="container-fluid col-4 kontakt-obchod boldText">Kontakt na<br> obchod:</div>
                                            <div class="container-fluid col-6 obchod">
                                                <div>
                                                        <img src="/static/images/envelope-fill.svg" alt="email">
                                                    <a href="mailto:${company.email}">${company.email}</a>
                                                </div>
                                                <div>
                                                    <img src="static/images/telephone-fill.svg" alt="telefon">
                                                    ${company.phone}
                                                </div>
            
                                            </div>
                                            <div class="container-fluid col-2 overflow-hidden ikona-dopravca">
                                                <img src="/static${company.icon}" alt="${company.companyCode}" class="ikona-obchodu-maxi">
                                                ${company.companyCode}
                                            </div>
                                        </div>
                                        <div class="row mt-3">
                                            <div class="container-fluid col-4 overflow-hidden kontakt-dopravca boldText">Kontakt na dopravcu:</div>
                                            <div class="container-fluid col-6 overflow-hidden dopravca">
                                                <div>
                                                    <img src="/static/images/envelope-fill.svg" alt="email">
                                                    <a href="mailto:${deliveryCompany.email}">${deliveryCompany.email}</a>
                                                </div>
                                                <div>
                                                    <img src="static/images/telephone-fill.svg" alt="telefon">
                                                    ${company.phone}
                                                </div>
                                            </div>
                                            <div class="container-fluid col-2 overflow-hidden ikona-dopravca">
                                                <img src="/static${deliveryCompany.icon}" alt="{{ deliveryCompany.deliveryCompanyCode }}" class="ikona-obchodu-maxi">
                                                {{ deliveryCompany.deliveryCompanyCode }}" ICON HERE" ?>
                                            </div>
                                        </div>
                                        <div class="row mt-3">
                                            <div class="container-fluid col-12 kontakt-kurier boldText">Zásielku Vám privezie:</div>
                                        </div>
                                        <div class="row mt-3">
                                            <div class="container-fluid col-6">
                                                <img src="/static${courier.picture}" alt="kurier" class="kurier-foto">
            
                                            </div>
                                            <div class="container-fluid col-6 kurier boldText">
                                                ${courier.name} ${courier.surname}
                                                <div>
                                                    <img src="/static/images/telephone-fill.svg" alt="telefon">
                                                    ${courier.phone}
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
            
                            </div>
                        </div>
                    </div>
                </div>
                    `;
        return HTML;
    }


    async updateHomePage() {
        //TODO: chyba ked je pouzivatel odhlaseny, hadze error 500
        try {
            let response = await fetch("http://127.0.0.1:8000/api/packages/");
            if (response.status != 200) {
                throw new Error("ERROR:" + response.status + " " + response.statusText);
            }
            let packages = await response.json()
            let packagesHTML = "";
            let packages_count = Object.keys(packages).length
            this.fillStatus(packages_count)


            for (const zasielka of packages) {
                let user = zasielka.receiverUserId;
                let date = new Date(zasielka.dateOfOrder).toLocaleString()
                let element = null
                let destinationAddress = zasielka.receiverUserId.addressId
                let company = zasielka.companyId
                let deliveryCompany = zasielka.deliveryCompanyId
                let courier = zasielka.courierId
                element = document.getElementById("package_" + zasielka.id);
                let collapse = document.getElementById("collapse" + zasielka.id);
                let collapse_button = document.getElementById("collapse_button_" + zasielka.id)

                let responseStages = null;
                responseStages = await fetch("http://127.0.0.1:8000/api/packageStages/" + zasielka.id.toString());
                if (responseStages.status != 200) {
                    console.log("ERROR:" + responseStages.status + " " + responseStages.statusText);
                    throw new Error("ERROR:" + responseStages.status + " " + responseStages.statusText);
                }
                let stages = await responseStages.json();
                let stages_count = Object.keys(stages).length;
                let lastStage = stages[stages_count - 1];

                if (element == null) {
                    // console.log("Zásielka s id:" + zasielka.id + " sa nenašla a bude pridaná!");
                    //ziskanie HTML s doterjasimi zasielkami
                    // let outdated_packagesHTML = document.getElementById("packages_django").innerHTML;
                    //pridanie novej zasielky na zaciatok
                    packagesHTML = this.fillHTML(zasielka, company, destinationAddress, date, stages_count, stages,
                        lastStage, deliveryCompany, courier, null, 'fa-up-right-and-down-left-from-center');

                    //odstranenie starych zasielok

                    //pridanie doterajsich zasielok na koniec
                    // packagesHTML += outdated_packagesHTML;
                    document.getElementById("accordion").innerHTML += packagesHTML;
                } else {
                    //zasielka sa nasla a bude aktualizovaná
                    // console.log("Zásielka s id:" + zasielka.id + " sa našla a bude aktualizovaná!");
                    let packageHTML = "";
                    let classes = collapse.classList;
                    let collapse_button_classes = collapse_button.firstElementChild.classList
                    packagesHTML = this.fillHTML(zasielka, company, destinationAddress, date, stages_count, stages,
                        lastStage, deliveryCompany, courier, classes, collapse_button_classes);

                    //aktualizacia HTML zasielky
                    element.innerHTML = packagesHTML;
                }
            }
            this.listenCollapseButtons();
            this.listenConfirmButtons();
            console.log("AJAX REFRESH")

        } catch (e) {
            console.log("ERROR WHILE UPDATING HOME PAGE!")
            console.log(e)
        }
    }

   toggleCollapseButtonIcon(event) {
        if (event.target === null) { console.log("null")}
        console.log("CLICK COLLAPSE FIRED:" + event.target.id)
        let icon = event.target;
        //zistin aku ma ikonu a reversnem ju
        console.log("icon class:" + icon.classList[1])
        if (icon.classList[1] === "fa-up-right-and-down-left-from-center") {
            console.log("expanding");
            icon.classList.remove('fa-up-right-and-down-left-from-center');
            icon.classList.add("fa-down-left-and-up-right-to-center");
        } else {
            console.log("collapsing")
            icon.classList.remove('fa-down-left-and-up-right-to-center');
            icon.classList.add("fa-up-right-and-down-left-from-center");
        }
        return true;

    }

    listenCollapseButtons() {
        let buttons = document.querySelectorAll('[id^="collapse_button_"]');
        buttons.forEach(button => {
            // console.log("listener for: " + button.id + " added")
            button.addEventListener("click", this.toggleCollapseButtonIcon)
        })
    }

    listenConfirmButtons() {
        let buttons = document.querySelectorAll('[id^="confirm_button_"]');
        buttons.forEach(button => {
            // console.log("listener for: " + button.id + " added")
            button.addEventListener("click", confirmPackage)
        })
    }

    async getPackage(id) {
        let response = await fetch("http://127.0.0.1:8000/api/packages/" + id);
        if (response.status != 200) {
            throw new Error("ERROR:" + response.status + " " + response.statusText);
        }
        let requested_package = await response.json()
        let packagesHTML = "";
    }

    async run() {
        console.log("BASE RUNNING!");
        await this.updateHomePage();
        // await this.updateHomePage();
        // await this.updateHomePage();
        setInterval(this.updateHomePage.bind(this), 5000);
    }



}
export default Base;
