(function (){
    Loader = (function (){
        function a(){
            console.log("[+] Im in A");
        }
        return a
    })();
    $(function (){
        var b = new Loader();
        return ;
    })
})();

