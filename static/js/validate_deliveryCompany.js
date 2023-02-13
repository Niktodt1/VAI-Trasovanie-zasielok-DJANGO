
window.onload = function () {

    function validateInput(element, validationFunction) {
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

    function checkFormState() {
        if (document.querySelectorAll(".error").length === 0) {
            document.getElementById("submit").disabled = false;
            document.getElementById("submit-info").style.display = "none";
        } else {
            document.getElementById("submit").disabled = true;
            document.getElementById("submit-info").style.display = "block";
        }
    }

    validateInput(document.getElementById("fullCompanyName"), function (value = null) {
        if (value == null || value.length === 0) {
            return "Meno spoločnosti musí byť zadané";
        }
        if (value.length < 3) {
            return "Meno musí byť dlhšie.";
        }
    });

    validateInput(document.getElementById("deliveryCompanyCode"), function (value = null) {
        if (value == null || value.length === 0) {
            return "Kód spoločnosti musí byť zadaný";
        }
        if (value.length < 3) {
            return "Kód musí byť dlhší.";
        }
    });

    validateInput(document.getElementById("city"), function (value = null) {
        if (value == null || value.length === 0) {
            return "Mesto musí byť zadané!";
        }
    });

    validateInput(document.getElementById("street"), function (value = null) {
        if (value == null || value.length === 0) {
            return "Ulica musí byť zadaná!";
        }
    });

    validateInput(document.getElementById("zipCode"), function (value = null) {
        if (value == null || value.length === 0) {
            return "PSČ musí byť zadané!";
        }
        if (value.length !== 5) {
            return "PSČ musí mať 5 čísel!"
        }
        let re = new RegExp('^\\d\\d\\d\\d\\d$');
        if (!re.test(value)) {
            return "PSČ musí mať 5 čísel!"
        }
    });

    validateInput(document.getElementById("streetNumber"), function (value = null) {
        if (value == null || value.length === 0) {
            return "Súpisné číslo musí byť zadané!";
        }
        let re = new RegExp('^[0-9]+$');
        if (!re.test(value)) {
            return "Zadaný email nemá platný formát."
        }
    });

    validateInput(document.getElementById("email"), function (value = null) {
        if (value == null || value.length === 0) {
            return "Email musí byť zadaný";
        }
        let re = new RegExp('^\\S+@\\S+\\.\\S+$');
        if (!re.test(value)) {
            return "Zadaný email nemá platný formát."
        }
    });

    validateInput(document.getElementById("phone"), function (value = null) {
        if (value == null || value.length === 0) {
            return "Telefónne číslo musí byť zadané!";
        }
        if (value != null && value.length > 0) {
            let re = new RegExp('^\\+421([0-9]{9}|(( {0,1}[0-9]{3}){3}))$');
            if (!re.test(value)) {
                return "Zadané telefónne číslo nie je v správnom tvare"
            }
        }
    });

    validateInput(document.getElementById("website"), function (value = null) {
        if (value == null || value.length === 0) {
            return "Webstránka musí byť zadaná!";
        }
        if (value != null && value.length > 0) {
            let re = new RegExp('^[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b([-a-zA-Z0-9()@:%_\\+.~#?&//=]*)');
            if (!re.test(value)) {
                return "Zadaná webstránka nie je v správnom tvare"
            }
        }
    });



}