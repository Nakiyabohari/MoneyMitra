
    function cal(){
            calculator.display.value = eval(calculator.display.value);
    }
    function clearresult() {
            calculator.display.value= "";
    }
    function percentage(){
            calculator.display.value /= 100;
    }
    function delone(){
            calculator.display.value=calculator.display.value.slice(0,-1);
    }