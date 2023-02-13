import Base from "./base.js";

window.onload = async function () {
    console.log("SCRIPT RUNNING!")
    window.base = new Base();
   await window.base.run();
}