import Base from "./base.js";

window.onload = async function () {
    console.log("HOME SCRIPT RUNNING!")
    window.base = new Base();
   await window.base.run();
}