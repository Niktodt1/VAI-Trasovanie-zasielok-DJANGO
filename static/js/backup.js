class Backup {
    async getMessages() {
        try {
            let response = await fetch("api.php?method=get-messages");
            if (response.status != 200) {
                throw new Error("ERROR:" + response.status + " " + response.statusText);
            }

            let messages = await response.json();
            let messagesHTML = "";

            messages.forEach(message => {
                let p = message.private_for != null ? "private" : "";
                let userNames = message.private_for != null ? `${message.user} > ${message.private_for}` : message.user;
                messagesHTML += `
                        <div class="message ${p}">
                            <span class="date">${message.created}</span>
                            <span class="user">${userNames} : </span>
                            <span>${message.message}</span>
                        </div>`;
            })
            document.getElementById("messages").innerHTML = messagesHTML;
        } catch (e) {
            document.getElementById("messages").innerHTML = `<h2>Nastala chyba na strane servera.</h2><p>${e.message}</p>`;
        }
    }


    async getPackages() {
        try {
            let response = await fetch("http://127.0.0.1:8000/api/packages/");
            if (response.status != 200) {
                throw new Error("ERROR:" + response.status + " " + response.statusText);
            }

            let packages = await response.json()
            let packagesHTML = "";
            console.log(response.toString())

            packages.forEach(zasielka => {
                let user = zasielka.receiverUserId;
                let date = new Date(zasielka.dateOfOrder)
                let element = null
                let obchod = zasielka.companyId

                try {
                    element = document.getElementById("package_" + zasielka.id);
                } catch (e) {
                    console.log(e.message);
                }

                if (element == null) {
                    console.log("Zásielka s id:" + zasielka.id + " sa nenašla a bude pridaná!");
                    //ziskanie HTML s doterjasimi zasielkami
                    let outdated_packagesHTML = document.getElementById("packages_django").innerHTML;
                    let
                        //pridanie novej zasielky na zaciatok
                        packagesHTML = `
                                <div id="package_${zasielka.id}" class="col-4 m-4">
                                     <hr>
                                     <h4>Zásielka ${zasielka.id} pre: ${user.name} ${user.surname}</h4><br>
                                     <p>Dátum: ${date.toLocaleString()}</p>
                                     <p>Obchod: ${obchod.companyName}</p>
                                </div>`;
                    //pridanie doterajsich zasielok na koniec
                    packagesHTML += outdated_packagesHTML;
                    document.getElementById("packages_django").innerHTML = packagesHTML;
                } else {
                    //zasielka sa nasla a bude aktualizovaná
                    console.log("Zásielka s id:" + zasielka.id + " sa našla a bude aktualizovaná!");
                    // console.log(document.getElementById(getElementById("package_" + zasielka.id)).toString());
                    let packageHTML = "";
                    packageHTML += `
                                     <hr>
                                     <h4>Zásielka ${zasielka.id} pre: ${user.name} ${user.surname}</h4><br>
                                     <p>Dátum: ${date.toLocaleString()}</p>
                                     <p>Obchod: ${obchod.companyName}</p>
                                     <p>DEBUG: UPDATED! ${Date.now().toString()}</p>`;
                    //aktualizacia HTML zasielky
                    element.innerHTML = packageHTML;
                }
                /** SKRATKA NA TIE šikmé apostrofy je LEFT_ALT+7 **/
                // <div class="col-4 m-4">
                //     <hr>
                //     <h4>Zásielka ${zasielka.id} pre: ${user.name} ${user.surname}</h4><br>
                //     <p>Dátum: ${date.toLocaleString()}</p>
                //     <p>Obchod: ${zasielka.companyId.fullCompanyName}</p>
                // </div>`;
            })
            console.log("AJAX REFRESH")
            // console.log(packages.size)


            // document.getElementById("packages_ajax").innerHTML = packagesHTML;

        } catch (e) {

        }
    }
}