window.onload = function () {
    export function validateInput(element, validationFunction) {
        element.oninput = function (event) {
            let result = validationFunction(event.target.value);

            let erId = "er-" + element.id;
            let errorEle = document.getElementById(erId);

            if (result != null) {
                if (errorEle == null) {
                    errorEle = document.createElement("div")
                    errorEle.classList.add("error");
                    errorEle.id = erId;
                }
                errorEle.innerText = result;
                element.after(errorEle);
                element.parentElement.classList.add("has-error");
            } else {
                errorEle?.remove()
                element.parentElement.classList.remove("has-error");
            }
            checkFormState();
        }
        element.dispatchEvent(new Event('input'));
    }

    export function checkFormState() {
        if (document.querySelectorAll(".error").length == 0) {
            document.getElementById("submit").disabled = false;
            document.getElementById("submit-info").style.display = "none";
        } else {
            document.getElementById("submit").disabled = true;
            document.getElementById("submit-info").style.display = "block";
        }
    }

    // validateInput(document.getElementById("meno"), function (value = null) {
    //     if (value == null || value.length == 0) {
    //         return "Meno musí byť zadané";
    //     }
    // });
    // validateInput(document.getElementById("priezvisko"), function (value = null) {
    //     if (value == null || value.length == 0) {
    //         return "Priezvisko musí byť zadané";
    //     }
    // });
    // validateInput(document.getElementById("mail"), function (value = null) {
    //     if (value == null || value.length == 0) {
    //         return "Email musí byť zadaný";
    //     }
    //     let re = new RegExp('^\\S+@\\S+\\.\\S+$');
    //     if (!re.test(value)) {
    //         return "Zadaný email nemá platný formát."
    //     }
    // });
    // validateInput(document.getElementById("mobil"), function (value = null) {
    //     if (value != null && value.length > 0) {
    //         let re = new RegExp('^\\+421([0-9]{9}|(( {0,1}[0-9]{3}){3}))$');
    //         if (!re.test(value)) {
    //             return "Zadané telefónne číslo nie je v správnom tvare"
    //         }
    //     }
    // });
    // validateInput(document.getElementById("sprava"), function (value = null) {
    //     if (value == null || value.length == 0) {
    //         return "Správa musí byť zadaná.";
    //     }
    //     if (value.length < 6) {
    //         return "Správa musí byť dlšia.";
    //     }
    // });


}

